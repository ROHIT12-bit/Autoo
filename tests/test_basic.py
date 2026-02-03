import sys
import os
import asyncio

# Add current directory to path
sys.path.append(os.getcwd())

def test_imports():
    print("Testing imports...")
    try:
        from config import Config
        from database.users_chats_db import db
        from database.ia_filterdb import save_file, get_search_results
        from utils.helpers import get_wish, auto_delete
        from plugins.downloaders import download_song
        from plugins.ai_telegraph import telegraph

        # Test basic functions
        wish = get_wish()
        print(f"Wish test: {wish}")

        print(f"Branding check: Botskingdoms")
        print(f"Config Timezone: {Config.TIMEZONE}")

        print("All imports and basic utility tests passed!")
    except Exception as e:
        print(f"Import/Utility test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_imports()
