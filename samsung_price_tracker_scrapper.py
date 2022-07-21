from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
import sqlite3
from time import sleep

listing_name = "Galaxy Tab A8"
price_page_url = "https://www.samsung.com/us/mobile/tablets/buy/?modelCode=SM-X200NIDAXAR"
no_trade_btn = 'tradeinOptionNo'
price_path = "//div[@class='price-info']//strong"
 
driver = Firefox()
driver.get(price_page_url)
sleep(3) # Sleep for 3 seconds to let page load
driver.find_element(By.ID, no_trade_btn).click()
price_value = driver.find_element_by_xpath(price_path).get_attribute('innerHTML')
print(price_value)
if '$' == price_value[0]:
    price = price_value[1:] 
price = float(price)
print(price)

# adding info to SQLite DB
print(f"INSERT OR IGNORE INTO listing(name,url) VALUES('{listing_name}','{price_page_url}')")
try:
    connection = sqlite3.connect("price_tracker.db")
    cursor = connection.cursor()
    cursor.execute(f"INSERT OR IGNORE INTO listing(\
                            name,\
                            url\
                        ) VALUES(\
                            '{listing_name}',\
                            '{price_page_url}'\
                        )")
    cursor.execute(f"SELECT id FROM listing WHERE name='{listing_name}'")
    listing_id = cursor.fetchone()[0]
    # TODO: Add to log if listing _id is not found
    print(listing_id)
    insert_price = f"INSERT INTO price(listing_id,price_in_cents) VALUES ('{listing_id}','{price*100}')"
    print(insert_price)
    cursor.execute(insert_price)
    # TODO: This insert is failing for some reason, must debug

except sqlite3.Error as error:
    print("Failed to read data from sqlite table", error)
finally:
    if connection:
        connection.close()
        print("The SQLite connection is closed")