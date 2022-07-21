import sqlite3
import win32com.client as win32
import logging
from os import path


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.DEBUG, filename=path.join(path.dirname(path.realpath(__file__)),"app.log"),
                    format='%(asctime)s module:%(module)s line:%(lineno)d %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


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
    

def email_product_info(product_name, product_url, price, *args):
    logging.debug("Attempting to send price alert email")
    try:
        outlook = win32.Dispatch('outlook.application')
    except Exception as ex:
        logging.error('Failed to connect to Outlook Application')
        logging.exception(f'Exception occured: {ex}')
        exit()
    mail = outlook.CreateItem(0)
    if len(args) > 0:
        mail.To = ';'.join(args)
    else:
        logging.error('No recipient emails specified')
        exit()
    mail.Subject = f'{product_name} is now ${price}'
    mail.Body = f'The set target price for the product {product_name} has been reached.\n\
                The current price is ${price}.\n\
                Product URL: {product_url}'
    mail.Send()
    logging.debug(f"Sent price alert email for product {product_name}")

if __name__ == '__main__':
    print(path.join(path.dirname(path.dirname(path.realpath(__file__))),"app.log"))
    product_name = "Galaxy Tab A8"
    product_url = "https://www.samsung.com/us/mobile/tablets/buy/?modelCode=SM-X200NIDAXAR"
    price = 250
    email_product_info(product_name, product_url, price, 'test1@gmail.com', 'test2@gmail.com')