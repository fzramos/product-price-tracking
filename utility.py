import sqlite3
import logging
from time import sleep
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
import os
import smtplib
from email.message import EmailMessage
from bs4 import BeautifulSoup
from dotenv import load_dotenv
_ = load_dotenv()


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.DEBUG, filename=os.path.join(os.path.dirname(os.path.realpath(__file__)),"app.log"),
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
        if price_value is None:
            logging.error(f'Failed to scrape price using the given xpath: {price_xpath}\n from URL: {product_url}')
            exit()
        # parsing HTML so we only get the price value, ie 19.99<strike>50.00</strike>
        price_value = BeautifulSoup(price_value,features="html.parser").find(text=True, recursive=False)
        if '$' == price_value[0]:
            price_value = price_value[1:]
        print(price_value)
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


def send_email(to, subject, message):
    email_address = os.environ.get("EMAIL_ADDRESS")
    email_password = os.environ.get("EMAIL_APP_PASSWORD")

    # create email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = ', '.join(to)
    msg.set_content(message)

    #send email
    # for outlook: smtplib.SMTP(host="smtp-mail.outlook.com", port=587)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
    except Exception as ex:
        logging.error("Failed to send email. Please confirm values in .env are correct.")
        logging.exception(ex)
        exit()


def price_alert_email(product_name, product_url, price, emails):
    subject = f'{product_name} is now ${price}'
    body = f'The set target price for the product {product_name} has been reached.\n\
                The current price is ${price}.\n\
                Product URL: {product_url}'
    send_email(emails, subject, body)
    logging.debug(f"Sent price alert email for product {product_name}")