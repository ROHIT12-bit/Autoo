<h1 align="center">
  <b>Botskingdoms Auto Filter Bot</b>
</h1>

<p align="center">
  <img src="https://graph.org/file/e322409581a95e2697e88.jpg" alt="Botskingdoms Logo" width="200">
</p>

<p align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Python"></a>
  <a href="https://docs.pyrogram.org"><img src="https://img.shields.io/badge/Framework-Pyrogram-orange?style=for-the-badge" alt="Pyrogram"></a>
  <a href="https://www.mongodb.com"><img src="https://img.shields.io/badge/Database-MongoDB-green?style=for-the-badge&logo=mongodb" alt="MongoDB"></a>
</p>

<p align="center">
  <b>An Advanced Auto Filter Bot with Shortener Support, AI, and Media Tools.</b>
</p>

---

## 🚀 Features

- 📂 **Auto Filter**: Advanced file search with Single/Double button modes.
- 🔗 **Shortener Support**: Supports all shortener websites for Stream/Download links.
- 🎬 **IMDB Integration**: Get movie details with professional templates.
- 🎵 **Media Downloader**: Fast YouTube song and ringtone downloads.
- 🤖 **Google AI**: Powered by Gemini for smart conversations.
- 💎 **Premium System**: Manage premium memberships and user permissions.
- 📢 **Force Sub**: Request to join and mandatory channel subscription.
- 🛠️ **Admin Tools**: Bulk broadcast, indexing, and user management.
- 🎨 **Branding**: Fully customizable for **@Botskingdoms**.

---

## 🛠️ Configuration

Configure the following environment variables in your `.env` file or deployment dashboard:

| Variable | Description |
|----------|-------------|
| `API_ID` | Your Telegram API ID from my.telegram.org |
| `API_HASH` | Your Telegram API Hash from my.telegram.org |
| `BOT_TOKEN` | Your Bot Token from @BotFather |
| `OWNER_ID` | Your Telegram User ID |
| `DATABASE_URL` | Your MongoDB Connection String |
| `FSUB` | Channel ID for Force Subscription |
| `SHORTENER_URL` | Your Shortener Website URL (e.g., gplinks.in) |
| `SHORTENER_API` | Your Shortener API Key |
| `GOOGLE_AI_API_KEY` | Your Google Gemini API Key |

---

## 📦 Deployment

### 🚀 Deploy to Render
1. Create a Blueprint on [Render](https://render.com).
2. Use the provided `render.yaml`.

[![Deploy to Render](https://render.com/images/deploy-to-render.svg)](https://render.com/)

### 💻 Local Deployment
```bash
# Clone the repository
git clone https://github.com/Botskingdoms/Auto-Filter-Bot.git
cd Auto-Filter-Bot

# Install dependencies
pip install -r requirements.txt

# Run the bot
python3 bot.py
```

---

## 📜 Bot Commands
| Command | Description |
|---------|-------------|
| `/start` | Initialize the bot |
| `/help` | View help menu |
| `/settings` | Open settings dashboard |
| `/imdb` | Search movies on IMDB |
| `/song` | Download YouTube songs |
| `/ai` | Chat with Google AI |
| `/index` | Index channel files (Admin) |
| `/stats` | View bot statistics |

*Full command list available in the help menu.*

### 📋 Full Command List (for @BotFather)
```text
start - Start the bot
help - Get help menu
stats - Bot statistics (Owner)
settings - Configure bot settings
imdb - Search movie info from IMDB
song - Download song from YouTube
ringtone - Download ringtones
ai - Ask anything to Google AI
telegraph - Upload media to Telegraph
ping - Check bot speed
id - Get Telegram IDs
info - Get user info
index - Index channel files (Owner)
broadcast - Broadcast to users (Owner)
grp_broadcast - Broadcast to groups (Owner)
ban - Ban a user (Owner)
unban - Unban a user (Owner)
leave - Leave a chat (Owner)
disable - Disable a chat (Owner)
add_premium - Add premium user (Owner)
remove_premium - Remove premium user (Owner)
delete - Delete files by query (Owner)
filestore - Store a file (Owner)
shorten - Shorten a URL (Owner)
streaming - Best streaming sites
spotify - Spotify info
stickerid - Get sticker ID
random - Random picture
```

---

## 🤝 Support & Branding
<p align="center">
  <b>Branding: Botskingdoms</b><br>
  <a href="https://t.me/BOTSKINGDOMS">
    <img src="https://img.shields.io/badge/Telegram-Updates-blue?style=for-the-badge&logo=telegram" alt="Updates">
  </a>
</p>
