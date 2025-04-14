# config.py
PRODUCT_PATTERNS = [
    r"/product[s]?/[a-zA-Z0-9\-_]+",
    r"/p/[a-zA-Z0-9\-_]+",
    r"/item/[a-zA-Z0-9\-_]+",
    r"/prod/[a-zA-Z0-9\-_]+",
    r"/shop/[a-zA-Z0-9\-_]+",
    r"/[a-zA-Z0-9\-_]+/p$"
]


MAX_CONCURRENCY = 10
MAX_DEPTH = 6
