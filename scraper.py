import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def fetch_website_links(url: str) -> list[str]:
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    links = set()

    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()

        if not href:
            continue
        if href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
            continue

        absolute_url = urljoin(url, href)
        links.add(absolute_url)

    return list(links)


def fetch_website_contents(url: str) -> str:
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    cleaned_lines = [line for line in lines if line]

    return "\n".join(cleaned_lines[:300])