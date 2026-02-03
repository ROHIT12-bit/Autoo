import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from database.ia_filterdb import get_search_results
from database.users_chats_db import db
from config import Config

@Client.on_message(filters.text & filters.group & ~filters.regex(r"^/"))
async def group_filters(client, message):
    await auto_filter(client, message)

@Client.on_message(filters.text & filters.private & ~filters.regex(r"^/"))
async def pm_filters(client, message):
    # Check if PM mode is enabled in config or settings
    await auto_filter(client, message)

async def auto_filter(client, message):
    query = message.text
    settings = await db.get_settings(message.chat.id)

    results, total = await get_search_results(query)

    if not results:
        if settings.get('spell_check', True):
            from database.ia_filterdb import get_all_file_titles
            from utils.helpers import get_spell_check
            all_titles = await get_all_file_titles()
            suggestions = get_spell_check(query, all_titles)
            if suggestions:
                btn = [[InlineKeyboardButton(s, callback_data=f"search#{s}")] for s in suggestions]
                await message.reply_text(
                    "No results found. Did you mean one of these?",
                    reply_markup=InlineKeyboardMarkup(btn)
                )
            else:
                await message.reply_text("No results found. Please check your spelling.")
        return

    btn = []
    if settings.get('button_type', 'double') == 'double':
        for i in range(0, len(results), 2):
            line = []
            line.append(InlineKeyboardButton(results[i]['file_name'], callback_data=f"file#{results[i]['file_id']}"))
            if i+1 < len(results):
                line.append(InlineKeyboardButton(results[i+1]['file_name'], callback_data=f"file#{results[i+1]['file_id']}"))
            btn.append(line)
    else:
        for res in results:
            btn.append([InlineKeyboardButton(res['file_name'], callback_data=f"file#{res['file_id']}")])

    if total > len(results):
        btn.append([InlineKeyboardButton(f"1/{total//10 + 1}", callback_data="pages"), InlineKeyboardButton("Next ➡️", callback_data=f"next#1#{query}")])

    await message.reply_text(
        f"**Found {total} results for {query}**\n\nBranding: **Botskingdoms**",
        reply_markup=InlineKeyboardMarkup(btn)
    )

@Client.on_callback_query(filters.regex(r"^search#"))
async def search_callback(client, query):
    new_query = query.data.split("#")[1]
    query.message.text = new_query # Mock message text for auto_filter
    await auto_filter(client, query.message)
    await query.answer()

@Client.on_callback_query(filters.regex(r"^next#"))
async def next_page(client, query):
    _, offset, search_query = query.data.split("#")
    offset = int(offset)

    results, total = await get_search_results(search_query, offset=offset*10)
    settings = await db.get_settings(query.message.chat.id)

    btn = []
    if settings.get('button_type', 'double') == 'double':
        for i in range(0, len(results), 2):
            line = []
            line.append(InlineKeyboardButton(results[i]['file_name'], callback_data=f"file#{results[i]['file_id']}"))
            if i+1 < len(results):
                line.append(InlineKeyboardButton(results[i+1]['file_name'], callback_data=f"file#{results[i+1]['file_id']}"))
            btn.append(line)
    else:
        for res in results:
            btn.append([InlineKeyboardButton(res['file_name'], callback_data=f"file#{res['file_id']}")])

    pages_btn = []
    if offset > 0:
        pages_btn.append(InlineKeyboardButton("⬅️ Back", callback_data=f"next#{offset-1}#{search_query}"))
    pages_btn.append(InlineKeyboardButton(f"{offset+1}/{total//10 + 1}", callback_data="pages"))
    if (offset+1)*10 < total:
        pages_btn.append(InlineKeyboardButton("Next ➡️", callback_data=f"next#{offset+1}#{search_query}"))

    btn.append(pages_btn)

    await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex(r"^file#"))
async def send_file(client, query):
    file_id = query.data.split("#")[1]
    settings = await db.get_settings(query.message.chat.id)

    # Generate Stream and Download links
    from plugins.shortener import get_shortlink
    stream_url = Config.STREAM_URL_TEMPLATE.format(username=client.username, file_id=file_id)
    download_url = Config.DOWNLOAD_URL_TEMPLATE.format(username=client.username, file_id=file_id)

    short_stream = await get_shortlink(stream_url)
    short_download = await get_shortlink(download_url)

    buttons = [
        [
            InlineKeyboardButton("Stream Online 📺", url=short_stream),
            InlineKeyboardButton("Fast Download 📥", url=short_download)
        ]
    ]

    msg = await client.send_cached_media(
        query.from_user.id,
        file_id,
        protect_content=settings.get('file_secure', True),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    if settings.get('auto_delete', True):
        from utils.helpers import auto_delete
        asyncio.create_task(auto_delete(client, msg))

    await query.answer("File sent to PM! It will be auto-deleted soon.", show_alert=True)

@Client.on_inline_query()
async def inline_search(client, query):
    search_query = query.query
    if not search_query:
        return

    results, total = await get_search_results(search_query)
    articles = []

    for res in results:
        articles.append(
            InlineQueryResultArticle(
                title=res['file_name'],
                input_message_content=InputTextMessageContent(res['file_name']),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Download", url=f"https://t.me/{client.username}?start=file_{res['file_id']}")]]),
                description=f"Size: {res.get('file_size', 'Unknown')}"
            )
        )

    await query.answer(articles, cache_time=0)
