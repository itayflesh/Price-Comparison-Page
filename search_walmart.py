import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode

from urllib.parse import urljoin

def search_item(item_name):
    search_url = 'https://www.walmart.com/search?' + urlencode({'q': item_name})
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.walmart.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making the search request: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    first_result = soup.find('a', class_='absolute w-100 h-100 z-1 hide-sibling-opacity')
    if first_result:
        relative_url = first_result['href']
        base_url = 'https://www.walmart.com'
        item_url = urljoin(base_url, relative_url)
        return item_url
    else:
        print("No search results found.")
        return None

def get_item_price(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.walmart.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making the request: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    price_element = soup.find('span', {'itemprop': 'price'})
    if price_element:
        price = price_element.text.strip()
        return price
    else:
        print("Price not found on the page.")
        return None

# Example usage
item_name = 'ipad air'
item_url = search_item(item_name)
if item_url:
    print(f"URL of the first search result: {item_url}")
    price = get_item_price(item_url)
    if price:
        print(f"The price of the item is: {price}")