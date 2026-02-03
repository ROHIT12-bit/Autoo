from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_chats_db import db
from config import Config

@Client.on_message(filters.command("ban") & filters.user(Config.OWNER_ID))
async def ban_user(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /ban <user_id>")
        return
    user_id = int(message.command[1])
    await db.ban_user(user_id)
    await message.reply_text(f"User {user_id} banned.")

@Client.on_message(filters.command("unban") & filters.user(Config.OWNER_ID))
async def unban_user(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /unban <user_id>")
        return
    user_id = int(message.command[1])
    await db.unban_user(user_id)
    await message.reply_text(f"User {user_id} unbanned.")

@Client.on_message(filters.command("add_premium") & filters.user(Config.OWNER_ID))
async def add_premium(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /add_premium <user_id>")
        return
    user_id = int(message.command[1])
    await db.make_premium(user_id)
    await message.reply_text(f"User {user_id} added to premium.")

@Client.on_message(filters.command("remove_premium") & filters.user(Config.OWNER_ID))
async def remove_premium(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /remove_premium <user_id>")
        return
    user_id = int(message.command[1])
    await db.remove_premium(user_id)
    await message.reply_text(f"User {user_id} removed from premium.")

@Client.on_message(filters.command("leave") & filters.user(Config.OWNER_ID))
async def leave_chat(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /leave <chat_id>")
        return
    chat_id = int(message.command[1])
    await client.leave_chat(chat_id)
    await message.reply_text(f"Left chat {chat_id}.")

@Client.on_message(filters.command("disable") & filters.user(Config.OWNER_ID))
async def disable_chat(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /disable <chat_id>")
        return
    chat_id = int(message.command[1])
    await db.disable_chat(chat_id)
    await message.reply_text(f"Chat {chat_id} disabled.")

@Client.on_message(filters.command("settings") & (filters.group | filters.private))
async def settings_command(client, message):
    # Only allow owner or group admins
    if message.chat.type != "private":
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in ["administrator", "creator"] and message.from_user.id != Config.OWNER_ID:
            return

    settings = await db.get_settings(message.chat.id)
    text = f"**Settings for {message.chat.title or 'Private Chat'}**"

    btn = [
        [
            InlineKeyboardButton(f"Button: {settings['button_type'].capitalize()}", callback_data=f"set#button_type#{settings['button_type']}"),
            InlineKeyboardButton(f"Auto Delete: {'✅' if settings['auto_delete'] else '❌'}", callback_data=f"set#auto_delete#{settings['auto_delete']}")
        ],
        [
            InlineKeyboardButton(f"IMDB: {'✅' if settings['imdb'] else '❌'}", callback_data=f"set#imdb#{settings['imdb']}"),
            InlineKeyboardButton(f"Spell Check: {'✅' if settings['spell_check'] else '❌'}", callback_data=f"set#spell_check#{settings['spell_check']}")
        ],
        [
            InlineKeyboardButton(f"Welcome: {'✅' if settings['welcome'] else '❌'}", callback_data=f"set#welcome#{settings['welcome']}")
        ]
    ]

    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex(r"^set#"))
async def update_settings(client, query):
    _, key, value = query.data.split("#")

    if key == "button_type":
        new_value = "single" if value == "double" else "double"
    else:
        new_value = False if value == "True" else True

    await db.update_settings(query.message.chat.id, key, new_value)

    settings = await db.get_settings(query.message.chat.id)
    btn = [
        [
            InlineKeyboardButton(f"Button: {settings['button_type'].capitalize()}", callback_data=f"set#button_type#{settings['button_type']}"),
            InlineKeyboardButton(f"Auto Delete: {'✅' if settings['auto_delete'] else '❌'}", callback_data=f"set#auto_delete#{settings['auto_delete']}")
        ],
        [
            InlineKeyboardButton(f"IMDB: {'✅' if settings['imdb'] else '❌'}", callback_data=f"set#imdb#{settings['imdb']}"),
            InlineKeyboardButton(f"Spell Check: {'✅' if settings['spell_check'] else '❌'}", callback_data=f"set#spell_check#{settings['spell_check']}")
        ],
        [
            InlineKeyboardButton(f"Welcome: {'✅' if settings['welcome'] else '❌'}", callback_data=f"set#welcome#{settings['welcome']}")
        ]
    ]

    await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(btn))
    await query.answer("Settings updated!")
