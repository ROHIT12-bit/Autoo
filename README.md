# Botskingdoms Auto Filter Bot

An Advanced Telegram Auto Filter Bot with multiple features, branding, and easy deployment support.

## 🚀 Features
- **Auto Filter**: Search indexed files with single/double button modes.
- **Shortener Support**: Integrated with custom shorteners for Stream and Download links.
- **IMDB Integration**: Fetch movie metadata and templates.
- **Downloader**: Download songs (YouTube) and ringtones.
- **AI & Telegraph**: Google AI (Gemini) integration and Telegraph media upload.
- **Force Subscription**: Restrict bot usage to channel members.
- **Join Request**: Automatically approve or track join requests.
- **Management**: Broadcast, Ban/Unban, Premium membership, and Settings.
- **Branding**: Fully customizable branding for @Botskingdoms.

## 📦 Deployment

### Render
Click the button below to deploy on Render:
[![Deploy to Render](https://render.com/images/deploy-to-render.svg)](https://render.com/)

### Local Setup
1. Clone the repo.
2. Install requirements: `pip install -r requirements.txt`.
3. Create a `.env` file with your variables.
4. Run: `python3 bot.py`.

## 🛠️ Config Variables
- `API_ID`: Get from my.telegram.org.
- `API_HASH`: Get from my.telegram.org.
- `BOT_TOKEN`: Get from @BotFather.
- `OWNER_ID`: Your Telegram User ID.
- `DATABASE_URL`: MongoDB URL.
- `FSUB`: Channel ID for force subscription.
- `SHORTENER_URL`: Custom shortener website URL.
- `SHORTENER_API`: Custom shortener API key.
- `GOOGLE_AI_API_KEY`: API key for Gemini.

## 📜 Bot Commands
Copy and paste this list to @BotFather:
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

## 💎 Branding
Branding **Botskingdoms**
[Updates Channel](https://t.me/BOTSKINGDOMS)
