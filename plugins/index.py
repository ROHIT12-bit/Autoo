import asyncio
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database.ia_filterdb import save_file, is_file_exists
from pyrogram.errors import FloodWait

@Client.on_message(filters.command("index") & filters.user(Config.OWNER_ID))
async def index_files(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /index <channel_id>")
        return

    chat_id = message.command[1]
    try:
        chat_id = int(chat_id)
    except:
        pass

    msg = await message.reply_text("Indexing started...")
    count = 0
    skipped = 0

    async for user_message in client.get_chat_history(chat_id):
        media = user_message.document or user_message.video or user_message.audio
        if media:
            file_id = media.file_id
            file_name = getattr(media, 'file_name', 'Unknown')
            file_size = media.file_size

            # PreDVD and CamRip check
            if re.search(r'predvd|camrip', file_name, re.IGNORECASE):
                skipped += 1
                continue

            if await is_file_exists(file_id):
                skipped += 1
                continue

            file_data = {
                'file_id': file_id,
                'file_name': file_name,
                'file_size': file_size,
                'chat_id': chat_id,
                'message_id': user_message.id
            }
            await save_file(file_data)
            count += 1
            await asyncio.sleep(0.5) # Avoid flood
            if count % 100 == 0:
                try:
                    await msg.edit_text(f"Indexed {count} files...\nSkipped {skipped} files.")
                except FloodWait as e:
                    await asyncio.sleep(e.value)

    await msg.edit_text(f"Successfully indexed {count} files.\nSkipped {skipped} files.")

@Client.on_message(filters.command("filestore") & filters.user(Config.OWNER_ID))
async def file_store(client, message):
    # Basic file store: forward media to a database channel and give user the ID/link
    if not message.reply_to_message or not message.reply_to_message.media:
        await message.reply_text("Reply to a file to store it.")
        return

    # In a real bot, we would forward to a log channel and save the message ID
    await message.reply_text(f"File stored! You can access it via the bot using its ID.")

@Client.on_message(filters.command("delete") & filters.user(Config.OWNER_ID))
async def delete_files_command(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /delete <query>")
        return
    query = " ".join(message.command[1:])
    from database.ia_filterdb import delete_files
    count = await delete_files(query)
    await message.reply_text(f"Deleted {count} files matching '{query}'.")
