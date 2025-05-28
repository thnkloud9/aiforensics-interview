import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    return BeautifulSoup(response.text, "html.parser")

def extract_titles(soup):
    print(f"{soup}")
    return [book.h3.a["title"] for book in soup.select(".product_pod")]

def get_next_page(soup, current_url):
    next_button = soup.select_one("li.next > a")
    if next_button:
        relative_url = next_button["href"]
        return urljoin(current_url, relative_url)
    return None

def get_all_titles():
    titles = []
    url = urljoin(BASE_URL, "index.html")

    while url:
        soup = get_soup(url)
        titles.extend(extract_titles(soup))
        url = get_next_page(soup, url)  # Move to next page

    return titles

if __name__ == "__main__":
    all_titles = get_all_titles()
    for i, title in enumerate(all_titles, 1):
        print(f"{i}. {title}")