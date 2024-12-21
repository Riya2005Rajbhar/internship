import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Amazon Login Details
AMAZON_EMAIL = "your_email@example.com"  # Replace with your email
AMAZON_PASSWORD = "your_password"       # Replace with your password

# Categories to Scrape
CATEGORIES = [
    "https://www.amazon.in/gp/bestsellers/kitchen/ref=zg_bs_nav_kitchen_0",
    "https://www.amazon.in/gp/bestsellers/shoes/ref=zg_bs_nav_shoes_0",
    "https://www.amazon.in/gp/bestsellers/computers/ref=zg_bs_nav_computers_0",
    "https://www.amazon.in/gp/bestsellers/electronics/ref=zg_bs_nav_electronics_0",
    # Add more categories if needed
]

# Selenium WebDriver setup
driver = webdriver.Chrome()  # Replace with the path to your WebDriver
wait = WebDriverWait(driver, 10)

def amazon_login():
    """Log in to Amazon."""
    driver.get("https://www.amazon.in/")
    driver.find_element(By.ID, "nav-link-accountList").click()
    wait.until(EC.presence_of_element_located((By.ID, "ap_email"))).send_keys(AMAZON_EMAIL, Keys.ENTER)
    wait.until(EC.presence_of_element_located((By.ID, "ap_password"))).send_keys(AMAZON_PASSWORD, Keys.ENTER)
    time.sleep(5)

def extract_product_details(product):
    """Extract product details."""
    try:
        name = product.find_element(By.CLASS_NAME, "p13n-sc-truncate").text
        price = product.find_element(By.CLASS_NAME, "p13n-sc-price").text
        discount = product.find_element(By.CLASS_NAME, "a-color-price").text
        rating = product.find_element(By.CLASS_NAME, "a-icon-alt").text
        sold_by = "N/A"  # Placeholder, implement specific logic if available
        ship_from = "N/A"  # Placeholder, implement specific logic if available
        description = "N/A"  # Placeholder, implement specific logic if available
        images = [img.get_attribute("src") for img in product.find_elements(By.TAG_NAME, "img")]
        return {
            "Product Name": name,
            "Product Price": price,
            "Sale Discount": discount,
            "Rating": rating,
            "Ship From": ship_from,
            "Sold By": sold_by,
            "Product Description": description,
            "All Available Images": images,
        }
    except NoSuchElementException:
        return None

def scrape_category(category_url):
    """Scrape data from a category page."""
    driver.get(category_url)
    time.sleep(5)
    products_data = []

    for rank in range(1, 1501):  # Iterate through top 1500 products
        try:
            product = driver.find_element(By.CSS_SELECTOR, f"#zg-ordered-list > li:nth-child({rank})")
            product_details = extract_product_details(product)
            if product_details:
                products_data.append(product_details)
        except NoSuchElementException:
            break
    return products_data

def save_data(data, file_name):
    """Save data to a CSV file."""
    keys = data[0].keys()
    with open(file_name, "w", newline="", encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def main():
    """Main function to execute the script."""
    try:
        amazon_login()
        all_data = []
        for category_url in CATEGORIES:
            category_data = scrape_category(category_url)
            all_data.extend(category_data)
        save_data(all_data, "amazon_bestsellers.csv")
        print("Scraping complete! Data saved to 'amazon_bestsellers.csv'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
