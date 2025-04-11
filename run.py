import asyncio
import json
from crawler.crawler import Crawler

DOMAINS = [
    "https://www.virgio.com/",
    "https://www.tatacliq.com/",
    "https://www.nykaafashion.com/",
    "https://www.westside.com/"
]

async def main():
    output = {}
    for domain in DOMAINS:
        print(f"Crawling: {domain}")
        crawler = Crawler(domain)
        product_urls = await crawler.run()
        output[domain] = list(product_urls)
    
    with open("output/product_urls.json", "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
