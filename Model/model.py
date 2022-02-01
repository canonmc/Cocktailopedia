import sqlite3
from Model.Cocktail import Cocktail
from random import randint

def dbaccess(func):
    '''handles connection opening and closing'''
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        response = func(*args, cursor = cursor, conn = conn, **kwargs)
        conn.close()
        return response
    return wrapper

@dbaccess
def init_db(cursor = None, conn = None):
    '''creates the database if it is not already made'''

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drinks (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
)""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
    drinkid INTEGER,
    ingredient TEXT,
    quantity DOUBLE,
    unit TEXT,
    FOREIGN KEY (drinkid) REFERENCES drinks(id) ON DELETE CASCADE
)""")
    conn.commit()

@dbaccess
def query(string, conn = None, cursor = None):
    '''allows quick querying (only works for select statements)'''

    cursor.execute(string)
    print(cursor.fetchall())

@dbaccess
def insert(cocktail : Cocktail, cursor = None, conn = None):
    '''inserts a cocktail into the database'''

    id = 0
    while True:
        id = randint(0,1000)
        cursor.execute(f'SELECT * FROM drinks WHERE id = {id}')
        if not cursor.fetchone():
            break
    try:
        cursor.execute(f'INSERT INTO drinks VALUES (:id, :name)', {'id':id, 'name':cocktail.name})
        conn.commit()
        for item, (amount, unit) in cocktail.ingredients.items():
            print(item,amount,unit)
            cursor.execute(f'INSERT INTO ingredients VALUES (:drinkid, :ingredient, :quantity, :unit)', {'drinkid':id, 'ingredient': item, 'quantity':amount, 'unit':unit})
            conn.commit()
    except sqlite3.IntegrityError as IE:
        print("Duplicate Drink Name:", cocktail.name)
    print("Successfully Added")

@dbaccess
def get_ingredients(cursor = None, conn = None):
    '''Returns all ingredients known to the database'''

    cursor.execute("SELECT DISTINCT ingredient FROM ingredients")
    return list(map(lambda x: x[0], cursor.fetchall()))

@dbaccess
def get_possible(*args, cursor = None, conn = None):
    '''Returns the ID of any drink that can be made, given a list of available ingredients passed into the function'''

    if not args:
        return []
    ingredients = "("
    for i in args[:-1]:
        ingredients += "'" + i + "'"
        ingredients += ', '
    ingredients += "'" + args[-1] + "'"
    ingredients += ')'

    cursor.execute(f''' 
    SELECT id FROM drinks INNER JOIN
    (SELECT drinkid, COUNT(*) FROM ingredients GROUP BY drinkid
    INTERSECT
    SELECT drinkid, COUNT(*) FROM ingredients WHERE ingredient IN {ingredients} GROUP BY drinkid)
    ON id = drinkid
''')
    ans = cursor.fetchall()
    return list(map(lambda i : i[0], ans))

@dbaccess
def get_table(table, cursor = None, conn = None):
    '''displays all tables'''

    cursor.execute(f"SELECT * FROM {table}")
    return cursor.fetchall()

@dbaccess
def get_recipe(id, conn = None, cursor = None):
    cursor.execute(f'SELECT name FROM drinks WHERE id = {id}')
    name = cursor.fetchone()[0]
    cursor.execute(f'SELECT ingredient,quantity,unit FROM ingredients WHERE drinkid = {id}')
    ingredients = cursor.fetchall()
    return Cocktail(name, *ingredients)

@dbaccess
def delete(name, conn = None, cursor = None):
    cursor.execute(f'SELECT id FROM drinks WHERE name = "{name}"')
    id = cursor.fetchone()[0]
    cursor.execute(f'''DELETE FROM ingredients WHERE drinkid = {id}''')
    cursor.execute(f'DELETE FROM drinks WHERE id = {id}')
    conn.commit()

def organize_ingredients():
    from config import liquors
    ingredients = get_ingredients()
    boundary = len(liquors.intersection(ingredients))
    ingredients.sort()
    ingredients.sort(key = lambda x : x not in liquors)
    l,other = ingredients[:boundary], ingredients[boundary:]
    return l,other