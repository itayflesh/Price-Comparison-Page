import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode

def search_item(item_name):
    search_url = 'https://www.newegg.com/p/pl?' + urlencode({'d': item_name, 'N': 4131})
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.newegg.com/',
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

    first_result = soup.select_one('div.item-cell a.item-title')
    if first_result:
        item_url = first_result['href']
        print(first_result.text.strip())
        return item_url
    else:
        print("No search results found.")
        return None

def get_item_price(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.newegg.com/',
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

    price_element = soup.select_one('li.price-current')
    if price_element:
        price_dollar = price_element.strong.text.strip()
        price_cents = price_element.sup.text.strip()
        price = f"{price_dollar}.{price_cents}"
        return price
    else:
        print("Price not found on the page.")
        return None

# Get user input for the item name
item_name = input("Enter the item name: ")

item_url = search_item(item_name)
if item_url:
    print(f"URL of the first search result: {item_url}")
    price = get_item_price(item_url)
    if price:
        print(f"The price of the item is: ${price}")