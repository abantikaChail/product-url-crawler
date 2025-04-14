import os
import json
from crawler.crawler import Crawler
from safe_runner import run_main

DOMAINS = [
    "https://www.virgio.com/",
    "https://www.tatacliq.com/",
    "https://www.nykaafashion.com/",
    "https://www.westside.com/"
]

async def main():
    results = {}
    for domain in DOMAINS:
        print(f"\nCrawling: {domain}")
        crawler = Crawler(domain)
        product_urls = await crawler.run()
        results[domain] = list(product_urls)
        print(f"Found {len(product_urls)} product URLs on {domain}")

    os.makedirs("output", exist_ok=True)

    with open("output/product_urls.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\n Results saved to output/product_urls.json")

run_main(main())
