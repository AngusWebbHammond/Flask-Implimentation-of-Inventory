from flask import Flask, render_template, request, redirect, jsonify
import sqlite3 as sql
from contextlib import closing

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inventory")
def inventory():
    with sql.connect("inventory.db") as con:
        con.row_factory=sql.Row
        with closing(con.cursor()) as cursor:
            items_o = cursor.execute("SELECT item_info.item, brand.brand, item_info.ip_rating, item_info.weight, item_info.amperage, COUNT(*) AS Count_of FROM item_info JOIN brand ON brand.brand_id = item_info.brand_id JOIN item ON item_info.item_info_id = item.item_info_id GROUP BY item_info.item ORDER BY item;")
            items = []
            for i in items_o:
                items.append(dict(i))
    return render_template("inventory.html", items=items)

@app.route("/inventory/add", methods=["GET", "POST"])
def inventory_add():
    with sql.connect("inventory.db") as con:
        con.row_factory=sql.Row
        with closing(con.cursor()) as cursor:
            items_o = cursor.execute("SELECT item_info.item_info_id, item_info.item, brand.brand FROM item_info LEFT JOIN brand ON brand.brand_id = item_info.brand_id ORDER BY item;")
            items = []
            for i in items_o:
                items.append(dict(i))
            items_i = cursor.execute("SELECT item_info.item, brand.brand, item_info.ip_rating, item_info.weight, item_info.amperage, COUNT(*) AS Count_of FROM item_info JOIN brand ON brand.brand_id = item_info.brand_id JOIN item ON item_info.item_info_id = item.item_info_id GROUP BY item_info.item ORDER BY item;")
            items_2 = []
            for i in items_i:
                items_2.append(dict(i))

    if request.method == "POST":
        item_info_id = request.form.get("item_info_id")
        store_location = request.form.get("store_location")
        condition = request.form.get("condition")

        if not item_info_id:
            return render_template("inventory_add.html", items=items, out="Please do not leave the item field blank")
        
        with sql.connect("inventory.db") as con:
            con.row_factory=sql.Row
            with closing(con.cursor()) as cursor:
                cursor.execute("INSERT INTO item (item_info_id, store_location, condition) VALUES(?, ?, ?);", (item_info_id, store_location, condition))
                items_i = cursor.execute("SELECT item_info.item, brand.brand, item_info.ip_rating, item_info.weight, item_info.amperage, COUNT(*) AS Count_of FROM item_info JOIN brand ON brand.brand_id = item_info.brand_id JOIN item ON item_info.item_info_id = item.item_info_id GROUP BY item_info.item;")
                items_2 = []
                for i in items_i:
                    items_2.append(dict(i))
                con.commit()

    return render_template("inventory_add.html", items=items, items_2=items_2)

@app.route("/item_info", methods=["GET", "POST"])
def item_info():
    with sql.connect("inventory.db") as con:
        con.row_factory=sql.Row
        with closing(con.cursor()) as cursor:
            cursor.execute("PRAGMA foreign_keys = ON;")
            items_o=cursor.execute("SELECT item_info.item_info_id, item_info.item, item_info.ip_rating, item_info.weight, item_info.amperage, item_info.type, item_info.replacement_cost, brand.brand, item_info.website FROM item_info LEFT JOIN brand ON item_info.brand_id = brand.brand_id ORDER BY item_info.item;").fetchall()
            items=[]
            for i in items_o:
                items.append(dict(i))
            brands_o=cursor.execute("SELECT * FROM brand ORDER BY brand;").fetchall()
            brands = []
            for i in brands_o:
                brands.append(dict(i))
                
    if request.method == "POST":
        item = request.form.get("item")
        ip_rating = request.form.get("ip_rating")
        weight = request.form.get("weight")
        amperage = request.form.get("amperage")
        type = request.form.get("type")
        replacement_cost = request.form.get("replacement_cost")
        brand = request.form.get("brand")
        if not item:
            return render_template("item_info.html", items=items, brands=brands, out="Please do not leave the field blank")
        try:
            with closing(sql.connect("inventory.db")) as con:
                con.row_factory=sql.Row
                with closing(con.cursor()) as cursor:
                    cursor.execute("PRAGMA foreign_keys = ON;")
                    cursor.execute("INSERT INTO item_info (item, ip_rating, weight, amperage, type, replacement_cost, brand_id) VALUES(?, ?, ?, ?, ?, ?, ?);", (item, ip_rating, weight, amperage, type, replacement_cost, brand))
                    items_o=cursor.execute("SELECT item_info.item_info_id, item_info.item, item_info.ip_rating, item_info.weight, item_info.amperage, item_info.type, item_info.replacement_cost, brand.brand, item_info.website FROM item_info LEFT JOIN brand ON item_info.brand_id = brand.brand_id ORDER BY item_info.item;").fetchall()
                    items=[]
                    for i in items_o:
                        items.append(dict(i))
                    con.commit()
        except:
            pass
        
    return render_template("item_info.html", items=items, brands=brands)

@app.route("/delete_item_info", methods=["POST"])
def delete_item_info():
    id = request.form.get("id")
    if id:
        try:
            with sql.connect("inventory.db") as con:
                with closing(con.cursor()) as cursor:
                    cursor.execute("PRAGMA foreign_keys = ON;")
                    cursor.execute("DELETE FROM item_info WHERE item_info_id = ?;", (id,))
        except:
            pass
    return redirect("/item_info")

@app.route("/manufacturer", methods=["GET", "POST"])
def manufacturer():
    with sql.connect("inventory.db") as con:
        with closing(con.cursor()) as cursor:
            cursor.execute("PRAGMA foreign_keys = ON;")
            manufacturers = cursor.execute("SELECT * FROM brand ORDER BY brand;").fetchall()
    if request.method == "POST":
        brand = request.form.get("brand")
        email = request.form.get("email")
        website = request.form.get("website")
        if not brand:
            return render_template("manufacturer.html", manufacturers=manufacturers, out="Please do not leave the field blank")
        try:
            with closing(sql.connect("inventory.db")) as con:
                with closing(con.cursor()) as cursor:
                    cursor.execute("PRAGMA foreign_keys = ON;")
                    cursor.execute("INSERT INTO brand (brand, website, email_address) VALUES(?, ?, ?);", (brand, website, email))
                    manufacturers = cursor.execute("SELECT * FROM brand ORDER BY brand;").fetchall()
                    con.commit()
        except:
            pass
    return render_template("manufacturer.html", manufacturers=manufacturers)

@app.route("/delete_brand", methods=["POST"])
def delete_brand():
    id = request.form.get("id")
    if id:
        try:
            with sql.connect("inventory.db") as con:
                with closing(con.cursor()) as cursor:
                    cursor.execute("PRAGMA foreign_keys = ON;")
                    cursor.execute("DELETE FROM brand WHERE brand_id = ?;", (id,))
        except:
            pass
    return redirect("/manufacturer")

@app.route("/update_item_info", methods=["POST"])
def update_item_info():
    item_info_id = request.form.get("item_info_id")
    website = request.form.get("website")
    print(item_info_id, website)
    try:
        with sql.connect("inventory.db") as con:
            with closing(con.cursor()) as cursor:
                cursor.execute("PRAGMA foreign_keys = ON;")
                print("Test1")
                cursor.execute("UPDATE item_info SET website = ? WHERE item_info_id = ?;", (website, item_info_id))
                print("Test2")
                con.commit()
    except:
        pass
    return redirect("/item_info")
