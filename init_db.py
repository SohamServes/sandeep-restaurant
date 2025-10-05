import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# --- Appetizers ---
cur.execute("INSERT INTO menu (name, description, price, category) VALUES (?, ?, ?, ?)",
            ('Paneer Tikka', 'Cubes of cottage cheese marinated in spices and grilled in a tandoor.', 250, 'Appetizer')
            )
cur.execute("INSERT INTO menu (name, description, price, category) VALUES (?, ?, ?, ?)",
            ('Samosa', 'Crispy pastry filled with spiced potatoes and peas (2 pieces).', 120, 'Appetizer')
            )
cur.execute("INSERT INTO menu (name, description, price, category) VALUES (?, ?, ?, ?)",
            ('Hara Bhara Kabab', 'Pan-fried spiced patties made with spinach, peas, and potatoes.', 210, 'Appetizer')
            )
cur.execute("INSERT INTO menu (name, description, price, category) VALUES (?, ?, ?, ?)",
            ('Tandoori Chicken', 'Chicken marinated in yogurt and spices, roasted in a tandoor.', 350, 'Appetizer')
            )

# --- Main Course ---
cur.execute("INSERT INTO menu (name, description, price, category) VALUES (?, ?, ?, ?)",
            ('Butter Chicken', 'Tender chicken pieces cooked in a rich, creamy tomato gravy.', 450, 'Main Course')
            )
cur.execute("INSERT INTO menu (name, description, price, category) VALUES (?, ?, ?, ?)",
            ('Shahi Paneer', 'Cottage cheese cooked in a rich, creamy Mughlai gravy.', 320, 'Main Course')
            )
cur.execute("INSERT INTO menu (name, description, price, category) VALUES (?, ?, ?, ?)",
            ('Dal Makhani', 'Black lentils simmered with spices, butter and cream.', 240, 'Main Course')
            )
cur.execute("INSERT INTO menu (name, description, price, category) VALUES (?, ?, ?, ?)",
            ('Mutton Rogan Josh', 'Aromatic curried meat dish of Persian origin.', 550, 'Main Course')
            )

# --- Breads & Rice ---
cur.execute("INSERT INTO menu (name, description, price, category) VALUES (?, ?, ?, ?)",
            ('Garlic Naan', 'Soft flatbread topped with minced garlic and coriander.', 75, 'Breads')
            )
cur.execute("INSERT INTO menu (name, description, price, category) VALUES (?, ?, ?, ?)",
            ('Tandoori Roti', 'Whole wheat unleavened bread cooked in a tandoor.', 40, 'Breads')
            )
cur.execute("INSERT INTO menu (name, description, price, category) VALUES (?, ?, ?, ?)",
            ('Jeera Rice', 'Basmati rice flavored with cumin seeds.', 180, 'Breads')
            )

connection.commit()
connection.close()

print("Database initialized with more items!") 