from pyrogram import Client, filters
import time

@Client.on_message(filters.command("repo"))
async def repo_search(client, message):
    text = "🔍 **Repo Search:**\n\nCheck out our repos at [GitHub](https://github.com/Botskingdoms)."
    await message.reply_text(text, disable_web_page_preview=True)

@Client.on_message(filters.command("ping"))
async def ping(client, message):
    start = time.time()
    msg = await message.reply_text("Pinging...")
    end = time.time()
    await msg.edit_text(f"🏓 Pong! `{round((end - start) * 1000)}ms`")

@Client.on_message(filters.command("stickerid"))
async def sticker_id(client, message):
    if not message.reply_to_message or not message.reply_to_message.sticker:
        await message.reply_text("Reply to a sticker to get its ID.")
        return
    await message.reply_text(f"Sticker ID: `{message.reply_to_message.sticker.file_id}`")

@Client.on_message(filters.command("id"))
async def get_ids(client, message):
    text = f"Chat ID: `{message.chat.id}`\n"
    if message.from_user:
        text += f"User ID: `{message.from_user.id}`\n"
    if message.reply_to_message:
        if message.reply_to_message.from_user:
            text += f"Replied User ID: `{message.reply_to_message.from_user.id}`\n"
        if message.reply_to_message.forward_from_chat:
            text += f"Forwarded Chat ID: `{message.reply_to_message.forward_from_chat.id}`\n"
    await message.reply_text(text)

@Client.on_message(filters.command("info"))
async def user_info(client, message):
    user = message.from_user
    if message.reply_to_message:
        user = message.reply_to_message.from_user

    text = f"**User Info:**\n\nName: {user.first_name}\nID: `{user.id}`\nUsername: @{user.username if user.username else 'None'}"
    await message.reply_text(text)

@Client.on_message(filters.command("random"))
async def random_pics(client, message):
    # Placeholder for random pics
    await message.reply_photo(
        photo="https://picsum.photos/400/300",
        caption="Here is a random picture for you!"
    )
