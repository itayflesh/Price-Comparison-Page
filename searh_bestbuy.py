from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def search_item(item_name):
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


def get_product_price(url):
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
        return price

    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        # Close the browser
        driver.quit()

    return None

item_name = input("Enter the item name: ")
first_result_url, first_result_name = search_item(item_name)
if first_result_url:
    price = get_product_price(first_result_url)
    if price:
        print(f'Price of {first_result_name}: {price}$')