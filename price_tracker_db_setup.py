import sqlite3

connection = sqlite3.connect("price_tracker.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS listing (\
                    id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    name TEXT, \
                    url TEXT, \
                    UNIQUE(name, url) \
                )")
cursor.execute("CREATE TABLE IF NOT EXISTS price (\
                    id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    listing_id INTEGER, \
                    price_in_cents INTEGER, \
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, \
                    FOREIGN KEY(listing_id) REFERENCES listing(id) \
                )")