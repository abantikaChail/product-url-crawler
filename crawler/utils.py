from urllib.parse import urljoin, urldefrag

def normalize_url(base, link):
    link = urljoin(base, link)
    link = urldefrag(link).url  # remove fragments
    return link
