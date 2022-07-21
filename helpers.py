import sqlite3
import win32com.client as win32

def db_insert_listing_price(listing_name, listing_url, dollar_price):
    """
        Upload score info to price_tracker.db
    """
    try:
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

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table, ", error)
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")

def email_product_info(product_name, product_url, price, *args):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    if len(args) > 0:
        mail.To = ';'.join(args)
    else:
        print('No recipient emails specified')
        exit()
    mail.Subject = f'{product_name} is now ${price}'
    mail.Body = f'The set target price for the product {product_name} has been reached.\n\
                The current price is ${price}.\n\
                Product URL: {product_url}'
    mail.Send()
    print(f"Email sent for product {product_name}")

if __name__ == '__main__':
    product_name = "Galaxy Tab A8"
    product_url = "https://www.samsung.com/us/mobile/tablets/buy/?modelCode=SM-X200NIDAXAR"
    price = 250
    email_product_info(product_name, product_url, price, 'fzrocco@gmail.com', 'aboutallthat@gmail.com')