import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

def _download_song(query, is_ringtone=False):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'default_search': 'ytsearch',
        'max_downloads': 1,
    }

    if is_ringtone:
        # Ringtone logic: maybe limit duration or search for ringtones
        query += " ringtone"

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            if 'entries' in info:
                info = info['entries'][0]

            file_path = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"
            return file_path, info['title'], info.get('duration', 0)
    except Exception as e:
        print(f"Download Error: {e}")
        return None, None, 0

async def download_song(query, is_ringtone=False):
    return await asyncio.to_thread(_download_song, query, is_ringtone)

@Client.on_message(filters.command("song"))
async def song_downloader(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /song <song_name>")
        return

    query = " ".join(message.command[1:])
    msg = await message.reply_text(f"Searching for '{query}'...")

    file_path, title, duration = await download_song(query)

    if file_path and os.path.exists(file_path):
        await msg.edit_text(f"Uploading '{title}'...")
        await message.reply_audio(
            audio=file_path,
            title=title,
            duration=duration,
            caption=f"**{title}**\n\nBranding: **Botskingdoms**"
        )
        os.remove(file_path)
        await msg.delete()
    else:
        await msg.edit_text("Failed to download the song. Please try again.")

@Client.on_message(filters.command("ringtone"))
async def ringtone_downloader(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /ringtone <name>")
        return

    query = " ".join(message.command[1:])
    msg = await message.reply_text(f"Searching for ringtone '{query}'...")

    file_path, title, duration = await download_song(query, is_ringtone=True)

    if file_path and os.path.exists(file_path):
        await msg.edit_text(f"Uploading ringtone '{title}'...")
        await message.reply_audio(
            audio=file_path,
            title=title,
            duration=duration,
            caption=f"**{title}**\n\nBranding: **Botskingdoms**"
        )
        os.remove(file_path)
        await msg.delete()
    else:
        await msg.edit_text("Failed to download the ringtone. Please try again.")

@Client.on_message(filters.command("spotify"))
async def spotify_info(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /spotify <song_link/name>")
        return
    query = " ".join(message.command[1:])
    # Spotify usually requires an API key for details, but we can search it on YT as a fallback
    await message.reply_text(f"Spotify details for '{query}':\n\nUse /song to download this track.")
