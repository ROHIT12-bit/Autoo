from pyrogram import Client, filters
import requests
import os
import mimetypes
import asyncio
from telegraph import Telegraph
from config import Config
import google.generativeai as genai

# Setup Google AI
if Config.GOOGLE_AI_API_KEY:
    genai.configure(api_key=Config.GOOGLE_AI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

# Setup Telegraph
telegraph = Telegraph()
if Config.TELEGRAPH_TOKEN:
    telegraph.token = Config.TELEGRAPH_TOKEN
else:
    telegraph.create_account(short_name='Botskingdoms')

def _telegraph_upload(path):
    try:
        mime_type = mimetypes.guess_type(path)[0] or 'image/jpeg'
        with open(path, 'rb') as f:
            response = requests.post(
                'https://telegra.ph/upload',
                files={'file': ('file', f, mime_type)}
            ).json()
        return response
    except Exception as e:
        print(f"Telegraph Upload Error: {e}")
        return None

@Client.on_message(filters.command("telegraph"))
async def telegraph_upload(client, message):
    if not message.reply_to_message or not message.reply_to_message.media:
        await message.reply_text("Reply to an image/video to upload to Telegraph.")
        return

    msg = await message.reply_text("Downloading and uploading to Telegraph...")

    try:
        path = await message.reply_to_message.download()
        response = await asyncio.to_thread(_telegraph_upload, path)

        if isinstance(response, list) and response[0].get('src'):
            link = f"https://telegra.ph{response[0]['src']}"
            await msg.edit_text(f"Uploaded Successfully!\n\nLink: {link}")
        else:
            await msg.edit_text("Failed to upload to Telegraph.")

        os.remove(path)
    except Exception as e:
        await msg.edit_text(f"Error: {e}")

def _generate_ai_content(query):
    return model.generate_content(query)

@Client.on_message(filters.command("ai"))
async def google_ai(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /ai <your_question>")
        return

    if not model:
        await message.reply_text("Google AI API Key is not set in Config.")
        return

    query = " ".join(message.command[1:])
    msg = await message.reply_text("Thinking...")

    try:
        response = await asyncio.to_thread(_generate_ai_content, query)
        await msg.edit_text(f"**Google AI:**\n\n{response.text}")
    except Exception as e:
        await msg.edit_text(f"AI Error: {e}")
