import os
import sys
import csv
import json
import sqlite3
from datetime import datetime

try:
    import streamlit as st
except Exception:
    st = None

APP_DIRS = ["db", "data"]
DB_PATH = os.path.join("db", "restaurant.db")
MENU_CSV = os.path.join("data", "menu.csv")
BILLS_JSON = os.path.join("data", "sample_bills.json")
SALES_CSV = os.path.join("data", "sales_report.csv")

def ensure_dirs():
    for d in APP_DIRS:
        os.makedirs(d, exist_ok=True)

def init_db():
    ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY AUTOINCREMENT, item_name TEXT NOT NULL, category TEXT, price REAL NOT NULL, gst REAL DEFAULT 0.05)")
    cur.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, total REAL, gst REAL, discount REAL, payment_method TEXT, mode TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cur.execute("CREATE TABLE IF NOT EXISTS order_items (id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER, item_name TEXT, quantity INTEGER, price REAL, FOREIGN KEY(order_id) REFERENCES orders(id))")
    conn.commit()
    conn.close()

DEFAULT_MENU = [
    {"item_name": "Masala Dosa", "category": "South Indian", "price": 80, "gst": 0.05},
    {"item_name": "Idli", "category": "South Indian", "price": 40, "gst": 0.05},
    {"item_name": "Veg Thali", "category": "Meals", "price": 150, "gst": 0.05},
    {"item_name": "Paneer Butter Masala", "category": "North Indian", "price": 180, "gst": 0.05},
    {"item_name": "Butter Naan", "category": "North Indian", "price": 30, "gst": 0.05}
]

def ensure_menu_file():
    ensure_dirs()
    if not os.path.exists(MENU_CSV):
        with open(MENU_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["item_name", "category", "price", "gst"])
            w.writeheader()
            for row in DEFAULT_MENU:
                w.writerow(row)


def load_menu():
    ensure_menu_file()
    with open(MENU_CSV, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        out = []
        for row in r:
            try:
                out.append({"item_name": row["item_name"], "category": row.get("category", ""), "price": float(row["price"]), "gst": float(row.get("gst", 0.05))})
            except Exception:
                pass
        return out


def save_menu(menu):
    with open(MENU_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["item_name", "category", "price", "gst"])
        w.writeheader()
        for row in menu:
            w.writerow(row)

def calculate_total(items, gst=0.05, discount=0.0):
    subtotal = sum(i["price"] * i["quantity"] for i in items)
    tax = subtotal * gst
    discount_amount = subtotal * discount
    total = round(subtotal + tax - discount_amount, 2)
    return {"subtotal": round(subtotal, 2), "tax": round(tax, 2), "discount": round(discount_amount, 2), "total": total}


def save_order(items, payment_method, mode, gst=0.05, discount=0.0):
    init_db()
    totals = calculate_total(items, gst=gst, discount=discount)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO orders(total, gst, discount, payment_method, mode, created_at) VALUES(?,?,?,?,?,?)", (totals["total"], gst, discount, payment_method, mode, datetime.now()))
    order_id = cur.lastrowid
    for it in items:
        cur.execute("INSERT INTO order_items(order_id, item_name, quantity, price) VALUES(?,?,?,?)", (order_id, it["item_name"], it["quantity"], it["price"]))
    conn.commit()
    conn.close()
    ensure_dirs()
    bill = {"order_id": order_id, "items": items, "payment_method": payment_method, "mode": mode, "totals": totals, "created_at": datetime.now().isoformat()}
    try:
        if os.path.exists(BILLS_JSON):
            with open(BILLS_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
    except Exception:
        data = []
    data.append(bill)
    with open(BILLS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    write_sales_row(totals["total"], payment_method)
    return bill


def write_sales_row(amount, payment_method):
    ensure_dirs()
    header = ["datetime", "amount", "payment_method"]
    new_file = not os.path.exists(SALES_CSV)
    with open(SALES_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(header)
        w.writerow([datetime.now().isoformat(timespec="seconds"), amount, payment_method])


def console_app():
    init_db()
    while True:
        print("\n1. Show Menu\n2. Place Order\n3. Exit")
        ch = input("Enter choice: ")
        if ch == "1":
            for m in load_menu():
                print(m["item_name"], "-", m["price"])
        elif ch == "2":
            menu = load_menu()
            items = []
            while True:
                name = input("Item name (blank to finish): ")
                if not name:
                    break
                qty = int(input("Quantity: "))
                m = next((x for x in menu if x["item_name"] == name), None)
                if not m:
                    print("Not found")
                    continue
                items.append({"item_name": name, "quantity": qty, "price": m["price"]})
            if not items:
                continue
            pm = input("Payment method (Cash/Card/UPI): ") or "Cash"
            mode = input("Mode (Dine-in/Takeaway): ") or "Dine-in"
            bill = save_order(items, pm, mode)
            print("Saved order", bill["order_id"], "Total:", bill["totals"]["total"])
        elif ch == "3":
            break


def streamlit_app():
    st.title("Restaurant Billing System")
    init_db()
    menu = load_menu()
    st.subheader("Manage Menu")
    with st.expander("View / Edit Menu"):
        st.table(menu)
        with st.form("add_item"):
            st.write("Add or Update Item")
            item = st.text_input("Item Name")
            cat = st.text_input("Category")
            price = st.number_input("Price", min_value=1.0)
            gst = st.number_input("GST", min_value=0.0, max_value=1.0, value=0.05)
            submitted = st.form_submit_button("Save Item")
            if submitted and item:
                exists = [m for m in menu if m["item_name"] == item]
                if exists:
                    for m in menu:
                        if m["item_name"] == item:
                            m["category"] = cat
                            m["price"] = price
                            m["gst"] = gst
                else:
                    menu.append({"item_name": item, "category": cat, "price": price, "gst": gst})
                save_menu(menu)
                st.success("Item saved")
    st.subheader("Place Order")
    items = []
    for m in menu:
        qty = st.number_input(f"{m['item_name']} ({m['price']})", min_value=0, step=1, key=m['item_name'])
        if qty > 0:
            items.append({"item_name": m["item_name"], "quantity": qty, "price": m["price"]})
    pm = st.selectbox("Payment Method", ["Cash", "Card", "UPI"])
    mode = st.selectbox("Mode", ["Dine-in", "Takeaway"])
    if st.button("Save Order"):
        if not items:
            st.error("No items selected")
        else:
            bill = save_order(items, pm, mode)
            st.success(f"Order {bill['order_id']} saved. Total {bill['totals']['total']}")


import unittest

class Tests(unittest.TestCase):
    def test_calculate_total_basic(self):
        items = [{"price": 100, "quantity": 2}, {"price": 50, "quantity": 1}]
        r = calculate_total(items, gst=0.05, discount=0.1)
        self.assertEqual(r["subtotal"], 250.0)
        self.assertAlmostEqual(r["tax"], 12.5, places=2)
        self.assertAlmostEqual(r["discount"], 25.0, places=2)
        self.assertAlmostEqual(r["total"], 237.5, places=2)

    def test_calculate_total_zero(self):
        items = []
        r = calculate_total(items)
        self.assertEqual(r["subtotal"], 0.0)
        self.assertEqual(r["tax"], 0.0)
        self.assertEqual(r["discount"], 0.0)
        self.assertEqual(r["total"], 0.0)

    def test_db_schema(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db()
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        names = {r[0] for r in cur.fetchall()}
        conn.close()
        self.assertTrue({"menu", "orders", "order_items"}.issubset(names))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=[sys.argv[0]])
    elif st is not None and st._is_running_with_streamlit if hasattr(st, '_is_running_with_streamlit') else False:
        streamlit_app()
    else:
        console_app()

