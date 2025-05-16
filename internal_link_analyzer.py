import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys

visited = set()

def is_internal_link(base_url, link):
    return urlparse(link).netloc == urlparse(base_url).netloc or urlparse(link).netloc == ''

def crawl(url, base_url, depth=1, max_depth=2):
    if url in visited or depth > max_depth:
        return
    visited.add(url)
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"\n📄 Page: {url}")
        links = set()
        for a in soup.find_all('a', href=True):
            full_link = urljoin(base_url, a['href'])
            if is_internal_link(base_url, full_link):
                links.add(full_link)
        if not links:
            print("❌ No internal links found.")
        else:
            for link in links:
                print(f"  ↳ {link}")
        for link in links:
            crawl(link, base_url, depth + 1, max_depth)
    except Exception as e:
        print(f"❌ Failed to fetch {url} — {e}")

if __name__ == "__main__":
    start_url = input("Enter the full website URL (e.g., https://example.com): ").strip()
    crawl(start_url, start_url)
