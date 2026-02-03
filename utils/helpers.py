import datetime
import pytz
import asyncio
import difflib
from config import Config

def get_wish():
    time = datetime.datetime.now(pytz.timezone(Config.TIMEZONE))
    hour = time.hour
    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 17:
        return "Good Afternoon"
    elif 17 <= hour < 21:
        return "Good Evening"
    else:
        return "Good Night"

async def auto_delete(client, message, delay=Config.AUTO_DELETE_TIME):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except:
        pass

def get_spell_check(query, all_titles):
    suggestions = difflib.get_close_matches(query, all_titles, n=5, cutoff=0.6)
    if suggestions:
        return suggestions
    return None
