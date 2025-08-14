import sqlite3
from datetime import datetime

def initialize_database():
    conn = sqlite3.connect('db/restaurant.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        price REAL NOT NULL,
        gst_percentage REAL DEFAULT 5.0
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_type TEXT CHECK(order_type IN ('Dine-In', 'Takeaway')),
        order_date TEXT DEFAULT CURRENT_TIMESTAMP,
        subtotal REAL,
        gst_amount REAL,
        discount REAL DEFAULT 0,
        total REAL,
        payment_method TEXT CHECK(payment_method IN ('Cash', 'Card', 'UPI')),
        table_number INTEGER
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        item_id INTEGER,
        quantity INTEGER,
        price REAL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
    )
    ''')
    
    # Insert sample menu items if empty
    cursor.execute("SELECT COUNT(*) FROM menu_items")
    if cursor.fetchone()[0] == 0:
        sample_items = [
            ('Margherita Pizza', 'Pizza', 12.99, 5.0),
            ('Pepperoni Pizza', 'Pizza', 14.99, 5.0),
            ('Caesar Salad', 'Salad', 8.99, 5.0),
            ('Garlic Bread', 'Appetizer', 4.99, 5.0),
            ('Coke', 'Beverage', 2.50, 5.0),
            ('Chocolate Cake', 'Dessert', 6.99, 5.0)
        ]
        cursor.executemany("INSERT INTO menu_items (name, category, price, gst_percentage) VALUES (?, ?, ?, ?)", sample_items)
    
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('db/restaurant.db')