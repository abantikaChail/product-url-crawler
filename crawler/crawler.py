import aiohttp
import asyncio
from bs4 import BeautifulSoup
from crawler.config import MAX_CONCURRENCY, MAX_DEPTH
from crawler.url_filter import is_product_url, is_valid_url
from crawler.utils import normalize_url
from tqdm import tqdm

class Crawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.seen = set()
        self.product_urls = set()
        self.sem = asyncio.Semaphore(MAX_CONCURRENCY)

    async def fetch(self, session, url):
        try:
            async with self.sem:
                async with session.get(url, timeout=10) as resp:
                    if 'text/html' in resp.headers.get('Content-Type', ''):
                        return await resp.text()
        except:
            return None

    async def parse(self, session, url, depth=0):
        if url in self.seen or depth > MAX_DEPTH:
            return
        self.seen.add(url)
        html = await self.fetch(session, url)
        if not html:
            return
        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup.find_all("a", href=True):
            href = tag['href']
            full_url = normalize_url(url, href)
            if not is_valid_url(full_url):
                continue
            if is_product_url(full_url):
                self.product_urls.add(full_url)
            elif self.base_url in full_url:
                await self.parse(session, full_url, depth + 1)

    async def run(self):
        async with aiohttp.ClientSession() as session:
            await self.parse(session, self.base_url)
        return self.product_urls
