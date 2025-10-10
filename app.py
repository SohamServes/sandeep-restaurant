import sqlite3
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- Public Routes ---

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
    # THIS SECTION IS THE CORRECTED LOGIC
    table_number = request.form['tableNumber']
    
    # Validation
    if not name or not phone or not table_number:
        return "Error: All fields are required.", 400
    if not phone.isdigit() or len(phone) != 10:
        return "Error: A 10-digit phone number is required.", 400

    cart_data_string = request.form.get('cartData')
    if cart_data_string:
        cart_items = json.loads(cart_data_string)
    else:
        cart_items = []

    conn = get_db_connection()
    cur = conn.cursor()
    # THIS IS THE CORRECTED DATABASE INSERT
    cur.execute('INSERT INTO orders (customer_name, customer_phone, table_number) VALUES (?, ?, ?)',
                (name, phone, table_number))
    order_id = cur.lastrowid
    
    for item in cart_items:
        cur.execute('INSERT INTO order_items (order_id, item_name, quantity, price) VALUES (?, ?, ?, ?)',
                    (order_id, item['name'], item['quantity'], item['price']))

    conn.commit()
    conn.close()
    
    return render_template('order_success.html', name=name, order_id=order_id)

# --- Admin Security Routes ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('admin_orders'))
        else:
            flash('Invalid password!')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

# --- Protected Admin Routes ---

@app.route('/admin/orders')
def admin_orders():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    all_orders = conn.execute('SELECT * FROM orders ORDER BY order_date DESC').fetchall()
    conn.close()
    return render_template('admin_orders.html', all_orders=all_orders)

@app.route('/bill/<int:order_id>')
def view_bill(order_id):
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    items = conn.execute('SELECT * FROM order_items WHERE order_id = ?', (order_id,)).fetchall()
    conn.close()
    grand_total = 0
    for item in items:
        grand_total += item['price'] * item['quantity']
    return render_template('bill.html', order=order, items=items, grand_total=grand_total)

@app.route('/admin/menu')
def admin_menu():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    menu_items = conn.execute('SELECT * FROM menu ORDER BY id').fetchall()
    conn.close()
    return render_template('admin_menu.html', menu_items=menu_items)

# (The rest of the admin/menu routes for add, edit, delete are the same)

@app.route('/admin/menu/delete/<int:id>', methods=['POST'])
def delete_menu_item(id):
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM menu WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Item deleted successfully.', 'success')
    return redirect(url_for('admin_menu'))

@app.route('/admin/menu/add', methods=['GET', 'POST'])
def add_menu_item():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']
        conn = get_db_connection()
        conn.execute('INSERT INTO menu (name, description, price, category) VALUES (?, ?, ?, ?)',
                     (name, description, price, category))
        conn.commit()
        conn.close()
        flash('Item added successfully.', 'success')
        return redirect(url_for('admin_menu'))
    return render_template('add_item.html')

@app.route('/admin/menu/edit/<int:id>', methods=['GET', 'POST'])
def edit_menu_item(id):
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM menu WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']
        conn.execute('UPDATE menu SET name = ?, description = ?, price = ?, category = ? WHERE id = ?',
                     (name, description, price, category, id))
        conn.commit()
        conn.close()
        flash('Item updated successfully.', 'success')
        return redirect(url_for('admin_menu'))
    conn.close()
    return render_template('edit_item.html', item=item)


if __name__ == '__main__':
    app.run(debug=True)