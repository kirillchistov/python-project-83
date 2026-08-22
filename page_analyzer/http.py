import requests
from bs4 import BeautifulSoup

REQUEST_TIMEOUT = 10
SEO_DISPLAY_LIMIT = 200


def truncate_seo(value, limit=SEO_DISPLAY_LIMIT):
    if not value:
        return ""
    if len(value) <= limit:
        return value
    return f"{value[:limit]}..."


def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.h1.get_text(strip=True) if soup.h1 else None
    title = soup.title.get_text(strip=True) if soup.title else None
    meta = soup.find("meta", attrs={"name": "description"})
    description = None
    if meta is not None and meta.get("content"):
        description = meta.get("content").strip()
    return {
        "h1": h1,
        "title": title,
        "description": description,
    }


def check_url(url):
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    seo = parse_page(response.text)
    seo["status_code"] = response.status_code
    return seo
