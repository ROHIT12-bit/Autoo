import aiohttp
from config import Config

async def get_shortlink(url):
    if not Config.SHORTENER_URL or not Config.SHORTENER_API:
        return url

    endpoint = f"https://{Config.SHORTENER_URL}/api?api={Config.SHORTENER_API}&url={url}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                data = await response.json()
                if data.get('status') == "success":
                    return data.get('shortenedUrl')
                return url
    except Exception as e:
        print(f"Shortener Error: {e}")
        return url

# Example command to test shortener
from pyrogram import Client, filters

@Client.on_message(filters.command("shorten") & filters.user(Config.OWNER_ID))
async def shorten_command(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /shorten <url>")
        return
    url = message.command[1]
    short_url = await get_shortlink(url)
    await message.reply_text(f"Shortened URL: {short_url}")
