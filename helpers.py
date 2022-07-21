import sqlite3

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
        print(listing_id)
        insert_price = f"INSERT INTO price(listing_id,price_in_cents) VALUES ('{listing_id}','{dollar_price*100}')"
        print(insert_price)
        cursor.execute(insert_price)
        connection.commit()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table, ", error)
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")