from pyrogram import Client, filters
from utils.imdb_helpers import get_imdb_info, format_imdb_template
from config import Config

@Client.on_message(filters.command("imdb"))
async def imdb_search(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /imdb <movie_name>")
        return

    query = " ".join(message.command[1:])
    data = await get_imdb_info(query)
    text = format_imdb_template(data)
    await message.reply_text(text)

@Client.on_message(filters.command("streaming"))
async def best_streaming(client, message):
    # Best Streaming Website feature
    text = f"🚀 **Best Streaming Websites:**\n\n{Config.STREAM_SITES}\n\nBranding: **Botskingdoms**"
    await message.reply_text(text, disable_web_page_preview=True)
