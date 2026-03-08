import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def fetch_page(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch: {url} (Status code: {response.status_code})")
            return None
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for tag in soup.find_all("a", href=True):
        absolute_url = urljoin(base_url, tag["href"])
        parsed = urlparse(absolute_url)

        
        if parsed.scheme in ["http", "https"]:
            links.add(absolute_url)

    return links



def web_crawler(seed_url, max_pages=5):
    queue = []
    visited = set()
    page_count = 0

    
    os.makedirs("pages", exist_ok=True)

    queue.append(seed_url)

    while queue and page_count < max_pages:
        current_url = queue.pop(0)

        if current_url in visited:
            continue

        print(f"\nFetching: {current_url}")

        html = fetch_page(current_url)
        if html is None:
            continue

        page_count += 1
        filename = f"pages/page_{page_count}.html"

        
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html)

        print(f"Saved: {filename}")

        
        links = extract_links(html, current_url)
        print(f"Extracted {len(links)} links")

        for link in links:
            if link not in visited and link not in queue:
                queue.append(link)

        visited.add(current_url)

        
        time.sleep(1)

    
    print("\n--- CRAWL SUMMARY ---")
    print(f"Total pages crawled: {page_count}")
    print(f"Total unique URLs visited: {len(visited)}")



if __name__ == "__main__":
    seed = "https://en.wikipedia.org/wiki/Main_page"
    web_crawler("https://en.wikipedia.org/wiki/Main_page",max_pages=5)


