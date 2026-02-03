import requests
from bs4 import BeautifulSoup
import re
import asyncio
from config import Config

def _get_imdb_info(query):
    try:
        search_url = f"https://www.imdb.com/find?q={query}&s=tt"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        result = soup.find('a', href=re.compile(r'/title/tt\d+/'))
        if not result:
            return None

        movie_url = f"https://www.imdb.com{result['href']}"
        res = requests.get(movie_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        title = soup.find('h1').text.strip()
        rating = soup.find('span', {'data-testid': 'hero-rating-bar__aggregate-rating__score'}).text.strip() if soup.find('span', {'data-testid': 'hero-rating-bar__aggregate-rating__score'}) else "N/A"

        return {
            'title': title,
            'rating': rating,
            'url': movie_url
        }
    except Exception as e:
        print(f"IMDB Error: {e}")
        return None

async def get_imdb_info(query):
    return await asyncio.to_thread(_get_imdb_info, query)

def format_imdb_template(data):
    if not data:
        return "No IMDB info found."
    return Config.IMDB_TEMPLATE.format(title=data['title'], rating=data['rating'], url=data['url'])
