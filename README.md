# Product URL Crawler

This project crawls e-commerce websites to extract all product URLs.

## Features
- Async crawler with `aiohttp`
- Intelligent product page detection using pattern matching
- Handles deep hierarchies with recursion
- Output in JSON format

## How to Run

```bash
git clone https://github.com/yourusername/product-url-crawler.git
cd product-url-crawler
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Output
All URLs are saved in `output/product_urls.json`

## Domains Tested
- virgio.com
- tatacliq.com
- nykaafashion.com
- westside.com

## Approach

We recursively fetch internal links and check if they match common product URL patterns like `/product/`, `/p/`, etc. The crawler uses async requests to handle large sites efficiently.
