import asyncio
from pyrogram import Client, filters
from database.users_chats_db import db
from config import Config
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

@Client.on_message(filters.command("broadcast") & filters.user(Config.OWNER_ID))
async def broadcast(client, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a message to broadcast it.")
        return

    msg = await message.reply_text("Broadcast started...")
    users = await db.get_all_users()
    count = 0
    total = await db.total_users_count()

    async for user in users:
        try:
            await message.reply_to_message.copy(user['_id'])
            count += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_to_message.copy(user['_id'])
            count += 1
        except (UserIsBlocked, InputUserDeactivated):
            pass
        except Exception as e:
            print(f"Broadcast error for {user['_id']}: {e}")

    await msg.edit_text(f"Broadcast completed. Sent to {count} users.")

@Client.on_message(filters.command("grp_broadcast") & filters.user(Config.OWNER_ID))
async def grp_broadcast(client, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a message to broadcast it to groups.")
        return

    msg = await message.reply_text("Group Broadcast started...")
    chats = await db.get_all_chats()
    count = 0

    async for chat in chats:
        try:
            await message.reply_to_message.copy(chat['_id'])
            count += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_to_message.copy(chat['_id'])
            count += 1
        except Exception as e:
            print(f"Group Broadcast error for {chat['_id']}: {e}")

    await msg.edit_text(f"Group Broadcast completed. Sent to {count} groups.")
