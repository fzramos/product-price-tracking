from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from helpers import db_insert_listing_price, email_product_info
from time import sleep

def main():
    # parameters
    listing_name = "Galaxy Tab A8"
    product_url = "https://www.samsung.com/us/mobile/tablets/buy/?modelCode=SM-X200NIDAXAR"
    target_price = 185
    no_trade_btn_id = 'tradeinOptionNo'
    scraped_price = scrape_samsung_dot_com_product_price(product_url, no_trade_btn_id)
    db_insert_listing_price(listing_name, product_url, scraped_price)
    if scraped_price <= target_price:
        email_product_info(listing_name, product_url, scraped_price, 'fzrocco@gmail.com')

def scrape_samsung_dot_com_product_price(product_url, *args):
    """
        Get a Samsung.com product price given a list of button ids that need to be pressed to get correct price
        Accepts multiple button ids because for some products you need to press multiple buttons to get correct price

        product_url: String of full URL for a Samsung.com product
        *args: optional variable number of button HTML ids that need to be clicked
    """
    price_path = "//div[@class='price-info']//strong"
    try:
        driver = Firefox()
        driver.get(product_url)
    except:
        print('Failed to load product web page.')
        exit()
    sleep(3) # Sleep for 3 seconds to let page load
    try:
        if len(args)>0:
            for btn_id in args:
                driver.find_element(By.ID, btn_id).click()
    except:
        print('Problem clicking specified button ids')
        exit()
    try:
        price_value = driver.find_element_by_xpath(price_path).get_attribute('innerHTML')
        print(price_value)
        if '$' == price_value[0]:
            dollar_price = price_value[1:] 
        dollar_price = float(dollar_price)
        return dollar_price 
    except:
        print('Failed to scrape price')
        exit()

if __name__ == '__main__':
    main()
