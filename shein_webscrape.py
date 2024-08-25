import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def is_zero(elt):
    return elt.text == '0'

def element_text_not_equal(locator, text):
    def condition(driver):
        element = driver.find_element(*locator)
        return element.text != text
    return condition

# Replace 'https://example.com/reviews' with the actual URL
def scrape_product_reviews(url):
    service = Service('/Users/hollandamazonia/Downloads/chromedriver-mac-arm64/chromedriver')
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    driver.refresh()
    
    wait = WebDriverWait(driver, 300)  # Adjust the timeout as needed
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rate-num")))
    print(element)
    # average_rating_element = wait.until_not(EC.text_to_be_present_in_element((By.CLASS_NAME, "rate-num"), '0'))
    average_rating_element = wait.until(element_text_not_equal((By.CLASS_NAME, "rate-num"), '0'))
    average_rating_element = wait.until(element_text_not_equal((By.CLASS_NAME, "rate-num"), ''))
    print(element.text != 0)
    print(element.text)
    print(average_rating_element)
    

    # Get the page source after JavaScript execution
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    html_tag = soup.find('html', lang='en', mir='ltr', brd='sh')
    body_tag = html_tag.find('body', lang='us')
    outer_product_menu = body_tag.find('div', class_='c-outermost-ctn j-outermost-ctn')
    product_menu = outer_product_menu.find('div', id='goods-detail-v3')
    product_menu = product_menu.find('div', class_='goods-detailv2')
    product_menu = product_menu.find('div', class_='goods-detailv2__media')
    product_menu = product_menu.find('div', class_='goods-detailv2__media-inner')
    product_menu = product_menu.find('div', class_=['product-intro'])
    product_menu = product_menu.find('div', class_='product-intro__galleryWrap')
    get_top_level_tags(product_menu)
    print("----------------------------------")
    product_menu = product_menu.find('div')
    get_top_level_tags(product_menu)
    print("----------------------------------")
    review_menu = product_menu.find('div', class_=['common-reviews', 'j-expose__common-review-container', 'sticky-under-gallery'])
    get_top_level_tags(review_menu)
    print("----------------------------------")
    review_menu = review_menu.find('div', class_=['customer-reviews'])
    get_top_level_tags(review_menu)
    review_menu = review_menu.find('div', class_=['common-reviews__averate'])
    print("----------------------------------")
    print("reviews:")
    get_top_level_tags(review_menu)
    average_rating = review_menu.find('div', class_=['ave-rate'])
    print("----------------------------------")
    get_top_level_tags(average_rating)
    rate_num = average_rating.find('div', class_=['rate-num'])
    print(rate_num.text)

    #get_top_level_tags(average_rating)
        
    # Find all review elements
    # review_elements = soup.find_all('div', class_='review')


    # Extract review text from each element
    # for review_element in review_elements:
        # review_text = review_element.text
        # print(review_text)

def get_top_level_tags(current_tag):
    top_level_tags = current_tag.find_all(recursive=False)
    for tag in top_level_tags:
        print(tag.name)
        print(tag.attrs)
    return top_level_tags

def get_products_by_category(category_url):

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
    product_urls = []
    try:
        for i in range(3):
            product_menu = outer_product_menu.find('div', id='product-list-v2')
            product_menu = product_menu.find('div', class_='product-list-v2')
            product_menu = product_menu.find('div', class_=['product-list-v2__main_side', 'product-list-v2__main_top', 'product-list-v2__main_view-new', 'product-list-v2__main'])
            product_menu = product_menu.find('div', class_=['product-list-v2__container'])
            product_menu = product_menu.find('section')
            product_menu = product_menu.find('div')
            #get_top_level_tags(product_menu)
            section_tags = product_menu.find_all('section', class_='product-card')  # Adjust the class selector as needed
            for tag in section_tags:
                bottom_tag = tag.find('div', class_='product-card__bottom-wrapper')
                title_tag = bottom_tag.find('div', class_=['product-card__goods-title-container'])
                link_tag = title_tag.find('a')
                link = link_tag['href']
                product_url = link[:link.find('html')+4]
                product_url = "https://us.shein.com" + product_url
                #print(product_url)
                product_urls.append(product_url)
            if no_errors:
                break
    except AttributeError as e:
        print(e)
        no_errors = False
    return product_urls
        

def web_scrape_shein(category_url='https://us.shein.com/RecommendSelection/Women-Clothing-sc-017172961.html?adp=&categoryJump=true&ici=us_tab03navbar03&src_identifier=fc%3DWomen%20Clothing%60sc%3DWomen%20Clothing%60tc%3D0%60oc%3D0%60ps%3Dtab03navbar03%60jc%3DitemPicking_017172961&src_module=topcat&src_tab_page_id=page_select_class1724526469016'):
    product_urls = get_products_by_category(category_url)
    # print(product_urls)
    for product_url in product_urls:
        scrape_product_reviews(product_url)
        break # limits to 1 product for testing

    # all_reviews = []
    #for url in product_urls:
    #     reviews = scrape_product_reviews(url)
    #     all_reviews.extend(reviews)

    # Randomly sample 1000 reviews
    # random.shuffle(all_reviews)
    # sampled_reviews = all_reviews[:1000]

#web_scrape_shein()
scrape_product_reviews('https://us.shein.com/SHEIN-Rosie-Hollow-Out-Button-Front-Crop-Blouse-p-22785930.html')

    