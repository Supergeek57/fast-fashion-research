import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

def is_zero(elt):
    return elt.text == '0'

def element_text_not_equal(locator, text):
    def condition(driver):
        element = driver.find_element(*locator)
        return element.text != text
    return condition

# Replace 'https://example.com/reviews' with the actual URL
def scrape_product_reviews(url, product_name, data_dict):
    service = Service('/Users/hollandamazonia/Downloads/chromedriver-mac-arm64/chromedriver')
    driver = webdriver.Chrome(service=service)
    driver.get(url)
 
    wait = WebDriverWait(driver, 35)  # Adjust the timeout as needed
    no_errors = False
    for i in range(5):
        try:
            driver.refresh()
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rate-num")))
            average_rating_element = wait.until(element_text_not_equal((By.CLASS_NAME, "rate-num"), '0'))
            average_rating_element = wait.until(element_text_not_equal((By.CLASS_NAME, "rate-num"), ''))
            average_rating_element = wait.until(element_text_not_equal((By.CLASS_NAME, "rate-num"), ' '))
            no_errors = True
            break
        except selenium.common.exceptions.TimeoutException as e:
            continue
    if not no_errors:
        print("timeout, skipping rating for this product")
        return data_dict

    print(element.text != 0)
    rating = element.text
    print(rating)
    data_dict[product_name]['avg_rating'] = rating
    return data_dict

def get_top_level_tags(current_tag):
    top_level_tags = current_tag.find_all(recursive=False)
    for tag in top_level_tags:
        print(tag.name)
        print(tag.attrs)
    return top_level_tags

def get_products_by_category(category_url, data_dict):

    service = Service('/Users/hollandamazonia/Downloads/chromedriver-mac-arm64/chromedriver')
    driver = webdriver.Chrome(service=service)
    driver.get(category_url)

    # Wait for the page to load completely (adjust the time as needed)
    driver.implicitly_wait(200)

    # Get the page source after JavaScript execution
    page_source = driver.page_source
    soup_category = BeautifulSoup(page_source, 'html.parser')
    html_tag = soup_category.find('html', lang='en', mir='ltr', brd='sh')
    body_tag = html_tag.find('body', lang='us')
    outer_product_menu = body_tag.find('div', class_='c-outermost-ctn j-outermost-ctn')
    no_errors = True
    try:
        for i in range(3):
            product_menu = outer_product_menu.find('div', id='product-list-v2')
            product_menu = product_menu.find('div', class_='product-list-v2')
            product_menu = product_menu.find('div', class_=['product-list-v2__main_side', 'product-list-v2__main_top', 'product-list-v2__main_view-new', 'product-list-v2__main'])
            product_menu = product_menu.find('div', class_=['product-list-v2__container'])
            product_menu = product_menu.find('section')
            product_menu = product_menu.find('div')
            get_top_level_tags(product_menu)
            section_tags = product_menu.find_all('section', class_='product-card')  # Adjust the class selector as needed
            for tag in section_tags:
                bottom_tag = tag.find('div', class_='product-card__bottom-wrapper')
                title_tag = bottom_tag.find('div', class_=['product-card__goods-title-container'])
                link_tag = title_tag.find('a')
                product_name = link_tag['data-title']
                origin_price = link_tag['data-us-origin-price']
                data_us_price = link_tag['data-us-price']
                print(product_name)
                print(origin_price)
                print(data_us_price)
                link = link_tag['href']
                product_url = link[:link.find('html')+4]
                product_url = "https://us.shein.com" + product_url
                data_dict[product_name] = {'old_price': origin_price, 'new_price': data_us_price, 'url': product_url}
            if no_errors:
                break
    except AttributeError as e:
        print(e)
        no_errors = False
    return data_dict
        

def web_scrape_shein(category_url='https://us.shein.com/RecommendSelection/Women-Clothing-sc-017172961.html?adp=&categoryJump=true&ici=us_tab03navbar03&src_identifier=fc%3DWomen%20Clothing%60sc%3DWomen%20Clothing%60tc%3D0%60oc%3D0%60ps%3Dtab03navbar03%60jc%3DitemPicking_017172961&src_module=topcat&src_tab_page_id=page_select_class1724526469016'):
    test_data_dict = {'test': 'testing data dict :)'}
    json.dump(test_data_dict, open('test_data.json', 'w'))
    data_dict = {}
    data_dict = get_products_by_category(category_url, data_dict)
    # print(product_urls)
    for product_name in data_dict:
        product_url = data_dict[product_name]['url']
        data_dict = scrape_product_reviews(product_url, product_name, data_dict)
        time.sleep(2)
    print(data_dict)

    json.dump(data_dict, open('data.json', 'w'))

web_scrape_shein()
#scrape_product_reviews('https://us.shein.com/SHEIN-Rosie-Hollow-Out-Button-Front-Crop-Blouse-p-22785930.html')

    