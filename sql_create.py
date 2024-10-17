import sqlite3 as sql
from contextlib import closing


with sql.connect("inventory.db") as con:
    with closing(con.cursor()) as cursor:
        cursor.execute("PRAGMA foreign_keys = ON;")
        #cursor.execute("DROP TABLE item;")
        #cursor.execute("CREATE TABLE brand(brand_id INTEGER PRIMARY KEY, brand TEXT NON NULL, email_address TEXT, website TEXT);")
        #cursor.execute("CREATE TABLE item_info(item_info_id INTEGER, item TEXT NON NULL, ip_rating TEXT, weight FLOAT(16), amperage FLOAT(16), type TEXT NON NULL, replacement_cost FLOAT(24), brand_id INTEGER, PRIMARY KEY (item_info_id), FOREIGN KEY (brand_id) REFERENCES brand(brand_id) ON DELETE CASCADE);")
        #cursor.execute("CREATE TABLE item(item_id INTEGER, store_location TEXT NON NULL, condition TEXT, item_info_id INTEGER NON NULL, PRIMARY KEY (item_id), FOREIGN KEY (item_info_id) REFERENCES item_info(item_info_id) ON DELETE CASCADE);")
        #print(cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';").fetchall())
        #print(cursor.execute("SELECT * FROM brand;").fetchall())
        cursor.execute("UPDATE item_info SET website = '' WHERE item_info_id = ?;")
