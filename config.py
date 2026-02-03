import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.environ.get("API_ID", "12345"))
    API_HASH = os.environ.get("API_HASH", "abcdef")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    OWNER_ID = int(os.environ.get("OWNER_ID", "12345678"))
    DATABASE_URL = os.environ.get("DATABASE_URL", "")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "Botskingdoms")
    COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "Telegram_files")

    CHANNELS = [int(ch) for ch in os.environ.get("CHANNELS", "").split() if ch]
    FSUB = os.environ.get("FSUB", "")
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "Botskingdoms")
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "BOTSKINGDOMS")

    START_PIC = os.environ.get("START_PIC", "https://graph.org/file/e322409581a95e2697e88.jpg")

    # Shortener
    SHORTENER_URL = os.environ.get("SHORTENER_URL", "")
    SHORTENER_API = os.environ.get("SHORTENER_API", "")

    # Features
    AUTO_DELETE = bool(os.environ.get("AUTO_DELETE", True))
    AUTO_DELETE_TIME = int(os.environ.get("AUTO_DELETE_TIME", 600))

    # AI and Telegraph
    TELEGRAPH_TOKEN = os.environ.get("TELEGRAPH_TOKEN", "")
    GOOGLE_AI_API_KEY = os.environ.get("GOOGLE_AI_API_KEY", "")

    # Extra settings
    TIMEZONE = os.environ.get("TIMEZONE", "Asia/Kolkata")
    STREAM_SITES = os.environ.get("STREAM_SITES", "1. [Netflix](https://netflix.com)\n2. [Prime Video](https://amazon.com)\n3. [Disney+](https://disneyplus.com)")
    IMDB_TEMPLATE = os.environ.get("IMDB_TEMPLATE", "**{title}**\n⭐ Rating: {rating}\n🔗 [IMDB Link]({url})")
    WELCOME_MSG = os.environ.get("WELCOME_MSG", "Welcome {mention} to {title}!")
    START_MSG = os.environ.get("START_MSG", "Hello {mention}, {wish}!\n\nI am an Advanced Auto Filter Bot with many features.\n\nBranding: **Botskingdoms**")
    ABOUT_MSG = os.environ.get("ABOUT_MSG", "**About This Bot**\n\nName: Botskingdoms Filter Bot\nOwner: [Admin](tg://user?id={owner_id})\nLanguage: Python\nFramework: Pyrogram\n\n© @{updates_channel}")
    STREAM_URL_TEMPLATE = os.environ.get("STREAM_URL_TEMPLATE", "https://t.me/{username}?start=stream_{file_id}")
    DOWNLOAD_URL_TEMPLATE = os.environ.get("DOWNLOAD_URL_TEMPLATE", "https://t.me/{username}?start=dl_{file_id}")
