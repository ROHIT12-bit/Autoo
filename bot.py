import logging
import logging.config
from pyrogram import Client, __version__
from config import Config

# Get logging configurations
logging.getLogger("pyrogram").setLevel(logging.WARNING)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Botskingdoms",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="plugins"),
            workers=200,
            max_concurrent_transmissions=10
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.username = me.username
        print(f"{me.first_name} for Pyrogram v{__version__} (Layer {self.layer}) started on {me.username}.")

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")

if __name__ == "__main__":
    app = Bot()
    app.run()
