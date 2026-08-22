from urllib.parse import urlparse

import validators

MAX_URL_LENGTH = 255


def normalize_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}".lower()


def is_valid_url(url):
    if not url or len(url) > MAX_URL_LENGTH:
        return False
    if not validators.url(url):
        return False
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
