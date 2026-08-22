import requests

REQUEST_TIMEOUT = 10


def get_url_status_code(url):
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.status_code
