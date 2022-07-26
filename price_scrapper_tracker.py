from utility import db_insert_listing_price, scrape_product_price, price_alert_email
import logging
from os import path, environ
import toml
from dotenv import load_dotenv
_ = load_dotenv()


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.DEBUG, filename=path.join(path.dirname(path.realpath(__file__)),"app.log"),
                    format='%(asctime)s module:%(module)s line:%(lineno)d %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def main():
    email_address = environ.get("EMAIL_ADDRESS")
    email_password = environ.get("EMAIL_APP_PASSWORD")
    # Getting program parameters from config.toml
    toml_path = path.join(path.dirname(path.realpath(__file__)),"config.toml")
    config = toml.load(toml_path)
    listings = config['product_info']
    alert_info = config['alert_info']
    for listing in listings:
        scraped_price = scrape_product_price(listing["product_url"], listing["button_ids"], listing["price_xpath"])
        db_insert_listing_price(listing["listing_name"], listing["product_url"], scraped_price)
        # Send email alert only if these parameters are filled
        if all([listing["target_price"], email_address, email_password]):
            if scraped_price <= listing["target_price"]:
                price_alert_email(listing["listing_name"], listing["product_url"], scraped_price, alert_info["recipients"])


if __name__ == '__main__':
    main()
