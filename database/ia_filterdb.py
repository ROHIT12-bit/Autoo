import logging
import re
from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

logger = logging.getLogger(__name__)

client = AsyncIOMotorClient(Config.DATABASE_URL) if Config.DATABASE_URL else None
db = client[Config.DATABASE_NAME] if client else None
col = db[Config.COLLECTION_NAME] if db else None

async def save_file(file_data):
    """Save file data to database"""
    if col is None:
        return False
    try:
        await col.update_one(
            {'file_id': file_data['file_id']},
            {'$set': file_data},
            upsert=True
        )
        return True
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        return False

async def get_search_results(query, offset=0, limit=10):
    """Search files in database"""
    if col is None:
        return [], 0

    query = query.strip()
    if not query:
        return [], 0

    # Process query to be more flexible (replace spaces with .*)
    query_pattern = query.replace(" ", ".*")
    try:
        regex = re.compile(query_pattern, re.IGNORECASE)
    except:
        regex = re.compile(re.escape(query), re.IGNORECASE)

    filter_query = {'file_name': regex}

    cursor = col.find(filter_query).sort('_id', -1).skip(offset).limit(limit)
    results = await cursor.to_list(length=limit)
    total_results = await col.count_documents(filter_query)

    return results, total_results

async def delete_files(query):
    """Delete multiple files from database"""
    if col is None:
        return 0
    query_pattern = query.replace(" ", ".*")
    try:
        regex = re.compile(query_pattern, re.IGNORECASE)
    except:
        regex = re.compile(re.escape(query), re.IGNORECASE)
    res = await col.delete_many({'file_name': regex})
    return res.deleted_count

async def get_total_files():
    if col is None:
        return 0
    return await col.count_documents({})

async def is_file_exists(file_id):
    if col is None:
        return False
    return await col.count_documents({'file_id': file_id}) > 0

async def get_all_file_titles():
    if col is None:
        return []
    cursor = col.find({}, {'file_name': 1})
    titles = await cursor.to_list(length=1000) # Limit to 1000 for performance
    return [t['file_name'] for t in titles]
