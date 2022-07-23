import sqlite3
# import win32com.client as win32
import logging
from os import path
from time import sleep
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.DEBUG, filename=path.join(path.dirname(path.realpath(__file__)),"app.log"),
                    format='%(asctime)s module:%(module)s line:%(lineno)d %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def scrape_product_price(product_url, btn_ids, price_xpath):
    """
        Get a product price given a list of button ids that need to be pressed to get correct price
        Accepts multiple button ids because for some products you need to press multiple buttons to get correct price

        product_url: String of full URL for an online product listing
        btn_ids: string containing comma-separated string of button HTML ids that need to be clicked
    """
    logging.debug(f"Starting price scrapping function for URL {product_url}")
    # price_path = "//div[@class='price-info']//strong"
    try:
        driver = Firefox()
        driver.get(product_url)
    except Exception as ex:
        logging.error('Failed to load product web page.')
        logging.exception(f'Exception occured: {ex}')
        exit()
    sleep(3) # Sleep for 3 seconds to let page load
    try:
        if btn_ids:
            for btn_id in btn_ids:
                driver.find_element(By.ID, btn_id).click()
    except Exception as ex:
        logging.error('Problem clicking specified button ids')
        logging.exception(f'Exception occured: {ex}')
        driver.close()
        exit()
    try:
        # price_value = driver.find_element_by_xpath(price_xpath).get_attribute('innerHTML')
        price_value = driver.find_element("xpath",price_xpath).get_attribute('innerHTML')
        print(price_value)
        if '$' == price_value[0]:
            price_value = price_value[1:]
        price_value = float(price_value)
        logging.debug(f"Scrapped the following product price: {price_value}")
        driver.close()
        return price_value 
    except Exception as ex:
        logging.error('Failed to scrape price')
        # likely because Xpath wrong, add that in log?
        logging.exception(f'Exception occured: {ex}')
        driver.close()
        exit()



def db_insert_listing_price(listing_name, listing_url, dollar_price):
    """
        Upload score info to price_tracker.db
    """
    try:
        logging.debug(f"Starting DB insert of newly scrapped price")
        connection = sqlite3.connect("price_tracker.db")
        cursor = connection.cursor()
        cursor.execute(f"INSERT OR IGNORE INTO listing(\
                                name,\
                                url\
                            ) VALUES(\
                                '{listing_name}',\
                                '{listing_url}'\
                            )")
        connection.commit()
        cursor.execute(f"SELECT id FROM listing WHERE name='{listing_name}'")
        listing_id = cursor.fetchone()[0]
        # TODO: Add to log if listing _id is not found
        insert_price = f"INSERT INTO price(listing_id,price_in_cents) VALUES ('{listing_id}','{dollar_price*100}')"
        cursor.execute(insert_price)
        connection.commit()
        logging.debug(f"Successfully inserted new {listing_name} price of {dollar_price} into SQLite DB.")
    except Exception as ex:
        logging.error('Failed to scrape price')
        logging.exception(f'Exception occured: {ex}')
    finally:
        if connection:
            connection.close()
            logging.debug("The SQLite connection is closed")
    

# def email_product_info(product_name, product_url, price, emails):
#     logging.debug("Attempting to send price alert email")
#     try:
#         outlook = win32.Dispatch('outlook.application')
#     except Exception as ex:
#         logging.error('Failed to connect to Outlook Application')
#         logging.exception(f'Exception occured: {ex}')
#         exit()
#     mail = outlook.CreateItem(0)
#     if len(emails) > 0:
#         mail.To = ';'.join(emails)
#     else:
#         logging.error('No recipient emails specified')
#         exit()
#     mail.Subject = f'{product_name} is now ${price}'
#     mail.Body = f'The set target price for the product {product_name} has been reached.\n\
#                 The current price is ${price}.\n\
#                 Product URL: {product_url}'
#     mail.Send()
#     logging.debug(f"Sent price alert email for product {product_name}")