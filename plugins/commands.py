from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database.users_chats_db import db
from database.ia_filterdb import get_total_files
from utils.helpers import get_wish

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await db.add_user(message.from_user.id, message.from_user.first_name)

    if len(message.command) > 1:
        data = message.command[1]
        if data.startswith("stream_") or data.startswith("dl_") or data.startswith("file_"):
            file_id = data.split("_", 1)[1]
            if "file" not in data:
                await message.reply_text(f"Preparing your {'stream' if 'stream' in data else 'download'} link...")
            await client.send_cached_media(message.chat.id, file_id)
            return

    wish = get_wish()
    text = Config.START_MSG.format(mention=message.from_user.mention, wish=wish)

    buttons = [
        [
            InlineKeyboardButton("Updates Channel", url=f"https://t.me/{Config.UPDATES_CHANNEL}"),
            InlineKeyboardButton("Support Group", url=f"https://t.me/{Config.SUPPORT_CHAT}")
        ],
        [
            InlineKeyboardButton("About", callback_data="about"),
            InlineKeyboardButton("Help", callback_data="help")
        ]
    ]

    if Config.START_PIC:
        await message.reply_photo(
            photo=Config.START_PIC,
            caption=text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await message.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

@Client.on_message(filters.command("help"))
async def help_command(client, message):
    text = "Help Menu:\n\n- Send movie name to search.\n- /stats to see bot statistics.\n- /index to index files (Admin only)."
    await message.reply_text(text)

@Client.on_message(filters.command("stats") & filters.user(Config.OWNER_ID))
async def stats(client, message):
    users = await db.total_users_count()
    chats = await db.total_chats_count()
    files = await get_total_files()
    text = f"**Statistics:**\n\nTotal Users: {users}\nTotal Chats: {chats}\nTotal Files: {files}"
    await message.reply_text(text)

@Client.on_callback_query(filters.regex("about"))
async def about_cb(client, query):
    text = Config.ABOUT_MSG.format(owner_id=Config.OWNER_ID, updates_channel=Config.UPDATES_CHANNEL)
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start_back")]]))

@Client.on_callback_query(filters.regex("start_back"))
async def start_back(client, query):
    wish = get_wish()
    text = Config.START_MSG.format(mention=query.from_user.mention, wish=wish)
    buttons = [
        [
            InlineKeyboardButton("Updates Channel", url=f"https://t.me/{Config.UPDATES_CHANNEL}"),
            InlineKeyboardButton("Support Group", url=f"https://t.me/{Config.SUPPORT_CHAT}")
        ],
        [
            InlineKeyboardButton("About", callback_data="about"),
            InlineKeyboardButton("Help", callback_data="help")
        ]
    ]
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.new_chat_members)
async def welcome(client, message):
    for member in message.new_chat_members:
        if member.id == (await client.get_me()).id:
            await db.add_chat(message.chat.id, message.chat.title)
            await message.reply_text(f"Thanks for adding me to {message.chat.title}!\n\nUse /settings to configure me.")
        else:
            settings = await db.get_settings(message.chat.id)
            if settings.get('welcome', True):
                await message.reply_text(Config.WELCOME_MSG.format(mention=member.mention, title=message.chat.title))
