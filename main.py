from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urljoin
from fastapi.middleware.cors import CORSMiddleware
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str
    website: str

def search_item_bestbuy(item_name):
    # Initialize the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Construct the Best Buy search page URL with the item name and intl=nosplash
        search_url = f"https://www.bestbuy.com/site/searchpage.jsp?st={item_name}&intl=nosplash"
        driver.get(search_url)

        # Wait for the search results to load
        wait = WebDriverWait(driver, 10)
        first_result = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-item.lv")))

        # Get the URL of the first search result
        first_result_link = first_result.find_element(By.CSS_SELECTOR, "a.image-link")
        first_result_url = first_result_link.get_attribute("href")

        # Get the name of the first search result item
        first_result_name = first_result.find_element(By.CSS_SELECTOR, "h4.sku-title > a").text

        return first_result_url, first_result_name

    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        # Close the browser
        driver.quit()

    return None, None

def get_item_price_bestbuy(url):
    # Initialize the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        
        product_url = f"{url}&intl=nosplash"

        # Navigate to the product page
        driver.get(product_url)

        # Wait for the price element to be present
        wait = WebDriverWait(driver, 10)
        price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.priceView-hero-price.priceView-customer-price > span[aria-hidden="true"]')))

        # Get the page source HTML
        html = driver.page_source

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract the price text
        price = price_element.text.strip('$')
        price = price + "$"
        return price

    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        # Close the browser
        driver.quit()

    return None

def search_item_walmart(item_name):
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

    first_result = soup.find('a', class_='absolute w-100 h-100 z-1 hide-sibling-opacity z-2')
    if first_result:
        relative_url = first_result['href']
        base_url = 'https://www.walmart.com'
        item_url = urljoin(base_url, relative_url)
        item_title = first_result.find('span', class_='w_iUH7').text.strip()
        return item_url, item_title
    else:
        print("No search results found.")
        return None, None

def get_item_price_walmart(url):
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
        price_text = price_element.text.strip()
        price_match = re.search(r'\$?(\d+(?:,\d+)*(?:\.\d+)?)', price_text) 
        if price_match:
            price = price_match.group(1).replace(',', '')
            price = price + "$"
            return price
        else:
            print("Price not found in the extracted text.")
            return None
    else:
        print("Price element not found on the page.")
        return None

def search_item_newegg(item_name):
    search_url = 'https://www.newegg.com/p/pl?' + urlencode({'d': item_name})
    
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
        item_title = first_result.text.strip()
        return item_url, item_title
    else:
        print("No search results found.")
        return None, None

def get_item_price_newegg(url):
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
        price = f"{price_dollar}{price_cents}$"
        return price
    else:
        print("Price not found on the page.")
        return None

@app.post("/search")
def search_item(item: Item):
    if item.website == "walmart":
        item_url, item_title = search_item_walmart(item.name)
        if item_url:
            price = get_item_price_walmart(item_url)
            if price:
                return {"website": "Walmart", "url": item_url, "title": item_title, "price": price}
            else:
                return {"website": "Walmart", "url": "", "title": item_title, "price": "Price not found"}
        else:
            return {"website": "Walmart", "url": "", "title": item.name, "price": "No search results found"}
    elif item.website == "newegg":
        item_url, item_title = search_item_newegg(item.name)
        if item_url:
            price = get_item_price_newegg(item_url)
            if price:
                return {"website": "Newegg", "url": item_url, "title": item_title, "price": price}
            else:
                return {"website": "Newegg", "url": "", "title": item_title, "price": "Price not found"}
        else:
            return {"website": "Newegg", "url": "", "title": item.name, "price": "No search results found"}
    elif item.website == "bestbuy":
        item_url, item_title = search_item_bestbuy(item.name)
        if item_url:
            price = get_item_price_bestbuy(item_url)
            if price:
                return {"website": "BestBuy", "url": item_url, "title": item_title, "price": price}
            else:
                return {"website": "BestBuy", "url": "", "title": item_title, "price": "Price not found"}
        else:
            return {"website": "BestBuy", "url": "", "title": item.name, "price": "No search results found"}
    else:
        return {"website": item.website, "url": "", "title": item.name, "price": "Unsupported website"}