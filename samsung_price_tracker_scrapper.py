from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from utility import getConfig, db_insert_listing_price, email_product_info
from time import sleep
import logging
from os import path
import toml

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.DEBUG, filename=path.join(path.dirname(path.realpath(__file__)),"app.log"),
                    format='%(asctime)s module:%(module)s line:%(lineno)d %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def main():
    # getting parameters from config.ini
    # config = getConfig()
    toml_path = path.join(path.dirname(path.realpath(__file__)),"config.toml")
    config = toml.load(toml_path)
    listings = config['samsung_product']
    # failed becuased misconfiged file
    for listing in listings:
        # .get("listing_name", "Galaxy Tab A8")  
        # product_url = config['samsung'].get("product_url", "https://www.samsung.com/us/mobile/tablets/buy/?modelCode=SM-X200NIDAXAR")
        # target_price = float(config['samsung'].get("target_price", "185"))
        # button_ids = config['samsung'].get("button_ids", "tradeinOptionNo")
        # emails = config['properties'].get("recipients", "test@email.com").replace(',',';')
        scraped_price = scrape_samsung_dot_com_product_price(listing["product_url"], listing["button_ids"])
        db_insert_listing_price(listing["listing_name"], listing["product_url"], scraped_price)
        if scraped_price <= listing["target_price"]:
            email_product_info(listing["listing_name"], listing["product_url"], scraped_price, listing["emails"])


def scrape_samsung_dot_com_product_price(product_url, btn_ids):
    """
        Get a Samsung.com product price given a list of button ids that need to be pressed to get correct price
        Accepts multiple button ids because for some products you need to press multiple buttons to get correct price

        product_url: String of full URL for a Samsung.com product
        btn_ids: string containing comma-separated string of button HTML ids that need to be clicked
    """
    logging.debug(f"Starting price scrapping function for URL {product_url}")
    price_path = "//div[@class='price-info']//strong"
    try:
        driver = Firefox()
        driver.get(product_url)
    except Exception as ex:
        logging.error('Failed to load product web page.')
        logging.exception(f'Exception occured: {ex}')
        exit()
    sleep(3) # Sleep for 3 seconds to let page load
    try:
        # btn_id_list = list()
        # if "," in btn_ids:
        #     btn_id_list = btn_ids.split(',')
        # else:
        #     btn_id_list.append(btn_ids)
        if btn_ids:
            for btn_id in btn_ids:
                driver.find_element(By.ID, btn_id).click()
    except Exception as ex:
        logging.error('Problem clicking specified button ids')
        logging.exception(f'Exception occured: {ex}')
        driver.close()
        exit()
    try:
        price_value = driver.find_element_by_xpath(price_path).get_attribute('innerHTML')
        print(price_value)
        if '$' == price_value[0]:
            dollar_price = price_value[1:] 
        dollar_price = float(dollar_price)
        logging.debug(f"Scrapped the following product price: {dollar_price}")
        driver.close()
        return dollar_price 
    except Exception as ex:
        logging.error('Failed to scrape price')
        logging.exception(f'Exception occured: {ex}')
        driver.close()
        exit()


if __name__ == '__main__':
    main()
