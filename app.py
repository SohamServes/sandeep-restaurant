import sqlite3
import json
from flask import Flask, render_template, request

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu():
    conn = get_db_connection()
    appetizers = conn.execute('SELECT * FROM menu WHERE category = ?', ('Appetizer',)).fetchall()
    main_courses = conn.execute('SELECT * FROM menu WHERE category = ?', ('Main Course',)).fetchall()
    breads = conn.execute('SELECT * FROM menu WHERE category = ?', ('Breads',)).fetchall()
    conn.close()
    return render_template('menu.html', appetizers=appetizers, main_courses=main_courses, breads=breads)

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/submit_order', methods=['POST'])
def submit_order():
    name = request.form['fullName']
    phone = request.form['phone']
    address = request.form['address']
    cart_data_string = request.form.get('cartData', '[]')
    cart_items = json.loads(cart_data_string)
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO orders (customer_name, customer_phone, customer_address) VALUES (?, ?, ?)',
                (name, phone, address))
    order_id = cur.lastrowid
    
    for item in cart_items:
        cur.execute('INSERT INTO order_items (order_id, item_name, quantity, price) VALUES (?, ?, ?, ?)',
                    (order_id, item['name'], item['quantity'], item['price']))

    conn.commit()
    conn.close()
    
    return render_template('order_success.html')

# NEW: Route for the admin page to view orders
@app.route('/admin/orders')
def admin_orders():
    conn = get_db_connection()
    # Fetch all orders, with the newest ones first
    all_orders = conn.execute('SELECT * FROM orders ORDER BY order_date DESC').fetchall()
    # Fetch all the individual items from all orders
    all_items = conn.execute('SELECT * FROM order_items').fetchall()
    conn.close()
    # Send both lists to the template
    return render_template('admin_orders.html', all_orders=all_orders, all_items=all_items)


if __name__ == '__main__':
    app.run(debug=True)