import logging
from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri) if uri else None
        self.db = self._client[database_name] if self._client else None
        self.users = self.db.users if self.db is not None else None
        self.chats = self.db.chats if self.db is not None else None
        self.settings = self.db.settings if self.db is not None else None

    async def add_user(self, user_id, name):
        if self.users is None: return
        user = {'_id': user_id, 'name': name, 'ban_status': False, 'is_premium': False}
        await self.users.update_one({'_id': user_id}, {'$set': user}, upsert=True)

    async def is_user_banned(self, user_id):
        if self.users is None: return False
        user = await self.users.find_one({'_id': user_id})
        return user.get('ban_status', False) if user else False

    async def ban_user(self, user_id):
        if self.users is None: return
        await self.users.update_one({'_id': user_id}, {'$set': {'ban_status': True}})

    async def unban_user(self, user_id):
        if self.users is None: return
        await self.users.update_one({'_id': user_id}, {'$set': {'ban_status': False}})

    async def make_premium(self, user_id):
        if self.users is None: return
        await self.users.update_one({'_id': user_id}, {'$set': {'is_premium': True}})

    async def remove_premium(self, user_id):
        if self.users is None: return
        await self.users.update_one({'_id': user_id}, {'$set': {'is_premium': False}})

    async def is_premium(self, user_id):
        if self.users is None: return False
        user = await self.users.find_one({'_id': user_id})
        return user.get('is_premium', False) if user else False

    async def total_users_count(self):
        if self.users is None: return 0
        return await self.users.count_documents({})

    async def get_all_users(self):
        if self.users is None: return []
        return self.users.find({})

    async def add_chat(self, chat_id, title):
        if self.chats is None: return
        chat = {'_id': chat_id, 'title': title, 'is_disabled': False}
        await self.chats.update_one({'_id': chat_id}, {'$set': chat}, upsert=True)

    async def is_chat_disabled(self, chat_id):
        if self.chats is None: return False
        chat = await self.chats.find_one({'_id': chat_id})
        return chat.get('is_disabled', False) if chat else False

    async def disable_chat(self, chat_id):
        if self.chats is None: return
        await self.chats.update_one({'_id': chat_id}, {'$set': {'is_disabled': True}})

    async def total_chats_count(self):
        if self.chats is None: return 0
        return await self.chats.count_documents({})

    async def get_all_chats(self):
        if self.chats is None: return []
        return self.chats.find({})

    async def get_settings(self, chat_id):
        if self.settings is None: return {}
        settings = await self.settings.find_one({'_id': chat_id})
        if not settings:
            default_settings = {
                '_id': chat_id,
                'button_type': 'double', # 'single' or 'double'
                'file_secure': True,
                'auto_delete': True,
                'imdb': True,
                'spell_check': True,
                'welcome': True
            }
            await self.settings.insert_one(default_settings)
            return default_settings
        return settings

    async def update_settings(self, chat_id, key, value):
        if self.settings is None: return
        await self.settings.update_one({'_id': chat_id}, {'$set': {key: value}}, upsert=True)

db = Database(Config.DATABASE_URL, Config.DATABASE_NAME)
