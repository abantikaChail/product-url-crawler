from crawler.config import PRODUCT_PATTERNS

def is_product_url(url):
    return any(pat in url for pat in PRODUCT_PATTERNS)

def is_valid_url(url):
    return url.startswith("http")
