import sqlite3
from datetime import datetime

# Sozdayom podklyuchenie
connection = sqlite3.connect('dostavka.db')

# perevodchok/ispolnitel
sql = connection.cursor()

# zapros na sozdanie tablitsi (polzovateli, sklad, korzina)
sql.execute('CREATE TABLE IF NOT EXISTS users (tg_id INTEGER, name TEXT, phone_number TEXT, address TEXT, reg_date DATETIME);')

# Sozdayom tablitsu dlya sklada
sql.execute('CREATE TABLE IF NOT EXISTS products (pr_id INTEGER PRIMARY KEY AUTOINCREMENT, pr_name TEXT, pr_price REAL, '
            'pr_quantity INTEGER, pr_des TEXT, pr_photo TEXT, reg_date DATETIME);')

# dz: tablitsa dlya korzini
###
sql.execute('CREATE TABLE IF NOT EXISTS korzina (user_id INTEGER, user_product TEXT,'
            ' prod_quantity INTEGER , total_all_product REAL);')
###

# sql.execute('alter table products add column pr_des TEXT')

# Funktsii
def register_user(tg_id, name, phone_number, adress):

    # Sozdayom podklyuchenie
    connection = sqlite3.connect('dostavka.db')
    # perevodchok/ispolnitel
    sql = connection.cursor()

    # dobavlyaem v bazu polzovatelya
    sql.execute('INSERT INTO users (tg_id, name, phone_number, adress, reg_date) VALUES (?, ?, ?,?, ?);',
                (tg_id, name, phone_number, adress, datetime.now()))

    # sohranenie obnavleniya
    connection.commit()

# proverka polzovatelya yest li on v baze
def check_user(user_id):

    # Sozdayom podklyuchenie
    connection = sqlite3.connect('dostavka.db')
    # perevodchok/ispolnitel
    sql = connection.cursor()

    checker = sql.execute('SELECT tg_id FROM users WHERE tg_id=?;', (user_id, ))

    if checker.fetchone():
        return True
    else:
        return False

# dz: (sklad)dobavlenie produkta v tablitsu products
def products_add(pr_name, pr_price, pr_count, pr_des, pr_photo):
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель .cursor()
    sql = connection.cursor()
    sql.execute('INSERT INTO products (pr_name, pr_price'
                ', pr_count, pr_des, pr_photo, reg_date) VALUES (?,?,?,?,?,?)',
                (pr_name, pr_price, pr_count, pr_des, pr_photo, datetime.now()))
    connection.commit()

############################################################### Udalenie vsego iz klassa (DZ)
def delete_products_from_sklad(products):

    # Sozdayom podklyuchenie
    connection = sqlite3.connect('dostavka.db')
    # perevodchok/ispolnitel
    sql = connection.cursor()

    sql.execute('DELETE FROM products *;')
    connection.commit()

# udalenie produkta iz sklada (product_id) iz products
def delete_exact_product_from_sklad(pr_id, pr_quantity):

    # Sozdayom podklyuchenie
    connection = sqlite3.connect('dostavka.db')
    # perevodchok/ispolnitel
    sql = connection.cursor()

    sql.execute('DELETE FROM products pr_quantity, WHERE pr_id=? AND pr_quantity=?', (pr_id, pr_quantity))
    connection.commit()

# poluchit vse produkti iz bazi(name, id)
def get_pr_name_id():
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель .cursor()
    sql = connection.cursor()

    products = sql.execute('SELECT pr_name, pr_id, pr_quantity FROM products;')

    sorted_products = [(i[0], i[1]) for i in products if i[2] > 0]

    # Chistiy spisok produktov [(name, id), (name, id)... , (name, id)]
    return sorted_products

# Poluchit informatsiyu pro opredelenniy produkt (cherez pr_id) -> (photo, des, price)
def get_exact_product(pr_id):

    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель .cursor()
    sql = connection.cursor()

    exact_product = sql.execute('SELECT pr_photo, pr_des, pr_price FROM products WHERE pr_id=?;', (pr_id, )).fetchone()

    return exact_product

# dobavlenie produktov v korzinu polzovatelya
def add_product_to_cart(user_id, user_product, prod_quantity):
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель .cursor()
    sql = connection.cursor()

    product_price = get_exact_product(user_product)[2]

    sql.execute('INSERT INTO korzina (user_id, user_product, prod_quantity, total_all_product) VALUES (?,?,?,?);', (user_id, user_product, prod_quantity, prod_quantity*product_price))

    # zapisat izmenenie
    connection.commit()

# Udalenie produktov
def delete_exact_product_from_cart(pr_id, user_id):
    # Sozdayom podklyuchenie
    connection = sqlite3.connect('dostavka.db')
    # perevodchok/ispolnitel
    sql = connection.cursor()

    # Udalenit produkt iz kozini cherez pr_id
    sql.execute('DELETE FROM korzina WHERE user_product=? AND user_id=?;', (pr_id, user_id))

    connection.commit()


def delete_product_from_cart(user_id):
    # Sozdayom podklyuchenie
    connection = sqlite3.connect('dostavka.db')
    # perevodchok/ispolnitel
    sql = connection.cursor()

    # Udalenit produkt iz kozini cherez pr_id
    sql.execute('DELETE FROM korzina WHERE user_id=?;', (user_id, ))

    connection.commit()


# Vivod korzini cherez (user_id) -> [(product, quantity, total_for_product). (...), ...]
def get_exact_user_cart(user_id):

    # Sozdayom podklyuchenie
    connection = sqlite3.connect('dostavka.db')
    # perevodchok/ispolnitel
    sql = connection.cursor()

    user_cart = sql.execute('SELECT products.pr_name, korzina.prod_quantity, korzina.total_all_product FROM korzina INNER JOIN products ON products.pr_id=korzina.user_product WHERE user_id=? ;', (user_id, )).fetchall()

    return user_cart

def get_pr_id():
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель .cursor()
    sql = connection.cursor()
    products = sql.execute('SELECT pr_name, pr_id, pr_quantity FROM products;')

    sorted_products = [i[1] for i in products if i[2] > 0]
    # Chistiy spisok produktov [id, id... , id]
    return sorted_products

# Poluchit nomer telefona i imya polzovatelya
def get_user_number_name(user_id):
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель .cursor()
    sql = connection.cursor()

    exact_user = sql.execute('SELECT name, phone_number FROM users WHERE tg_id=?;', (user_id, ))

    return exact_user.fetchone()