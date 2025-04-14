from crawler.config import PRODUCT_PATTERNS

import re

def is_product_url(url):
    return any(re.search(pat, url) for pat in PRODUCT_PATTERNS)


def is_valid_url(url):
    return url.startswith("http")
