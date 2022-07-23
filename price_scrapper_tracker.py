from utility import db_insert_listing_price, scrape_product_price, email_product_info
import logging
from os import path
import toml


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.DEBUG, filename=path.join(path.dirname(path.realpath(__file__)),"app.log"),
                    format='%(asctime)s module:%(module)s line:%(lineno)d %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def main():
    # Getting program parameters from config.toml
    toml_path = path.join(path.dirname(path.realpath(__file__)),"config.toml")
    config = toml.load(toml_path)
    listings = config['product_info']
    for listing in listings:
        scraped_price = scrape_product_price(listing["product_url"], listing["button_ids"], listing["price_xpath"])
        db_insert_listing_price(listing["listing_name"], listing["product_url"], scraped_price)
        if scraped_price <= listing["target_price"]:
            email_product_info(listing["listing_name"], listing["product_url"], scraped_price, listing["emails"])


if __name__ == '__main__':
    main()
