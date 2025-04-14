import aiohttp
import asyncio
import async_timeout
from bs4 import BeautifulSoup
from crawler.config import MAX_CONCURRENCY, MAX_DEPTH
from crawler.url_filter import is_product_url, is_valid_url
from crawler.utils import normalize_url
from tqdm import tqdm
from urllib.parse import urlparse
from robotexclusionrulesparser import RobotExclusionRulesParser

class Crawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.seen = set()
        self.product_urls = set()
        self.sem = asyncio.Semaphore(MAX_CONCURRENCY)
        self.robots = None

    async def setup_robots(self, session):
        parsed = urlparse(self.base_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        try:
            async with session.get(robots_url, timeout=10) as resp:
                if resp.status == 200:
                    content = await resp.text()
                    self.robots = RobotExclusionRulesParser()
                    self.robots.parse(content)
                    print(f"Loaded robots.txt from {robots_url}")
                else:
                    print(f"robots.txt not found at {robots_url}")
                    self.robots = None
        except Exception as e:
            print(f"Failed to load robots.txt: {e}")
            self.robots = None

    def is_allowed(self, url):
        if self.robots:
            return self.robots.is_allowed("*", url)
        return True

    async def fetch(self, session, url):
        try:
            async with self.sem:
                async with async_timeout.timeout(10):
                    async with session.get(url) as resp:
                        if 'text/html' in resp.headers.get('Content-Type', ''):
                            print(f"Fetched: {url}")
                            return await resp.text()
                        else:
                            print(f"Skipped non-HTML content: {url}")
        except asyncio.TimeoutError:
            print(f"Timeout fetching: {url}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return None

    async def parse(self, session, url, depth=0):
        if url in self.seen or depth > MAX_DEPTH:
            return
        self.seen.add(url)

        if not self.is_allowed(url):
            print(f"Blocked by robots.txt: {url}")
            return

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
                print(f"Found product: {full_url}")
                self.product_urls.add(full_url)
            elif self.base_url in full_url:
                await self.parse(session, full_url, depth + 1)

        print(f"Finished: {url}")

    async def run(self):
        try:
            async with aiohttp.ClientSession() as session:
                await self.setup_robots(session)
                await self.parse(session, self.base_url)
            return self.product_urls
        except asyncio.CancelledError:
            print("Crawler was cancelled.")
            return self.product_urls

