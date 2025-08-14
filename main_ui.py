import tkinter as tk
from tkinter import ttk, messagebox
from db_utils import get_db_connection
from calculator import BillCalculator
import datetime

class RestaurantBillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Billing System")
        self.root.geometry("1000x700")
        
        self.current_order = []
        self.order_type = "Dine-In"
        self.payment_method = "Cash"
        self.discount_percentage = 0
        
        self.setup_ui()
        self.load_menu_items()
    
    def setup_ui(self):
        # Menu Frame
        menu_frame = ttk.LabelFrame(self.root, text="Menu", padding=10)
        menu_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.menu_tree = ttk.Treeview(menu_frame, columns=('name', 'category', 'price'), show='headings')
        self.menu_tree.heading('name', text='Item Name')
        self.menu_tree.heading('category', text='Category')
        self.menu_tree.heading('price', text='Price ($)')
        self.menu_tree.column('name', width=200)
        self.menu_tree.column('category', width=150)
        self.menu_tree.column('price', width=100)
        self.menu_tree.pack(fill=tk.BOTH, expand=True)
        
        # Order Frame
        order_frame = ttk.LabelFrame(self.root, text="Current Order", padding=10)
        order_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.order_tree = ttk.Treeview(order_frame, columns=('name', 'price', 'quantity', 'total'), show='headings')
        self.order_tree.heading('name', text='Item Name')
        self.order_tree.heading('price', text='Price ($)')
        self.order_tree.heading('quantity', text='Qty')
        self.order_tree.heading('total', text='Total ($)')
        self.order_tree.column('name', width=200)
        self.order_tree.column('price', width=100)
        self.order_tree.column('quantity', width=50)
        self.order_tree.column('total', width=100)
        self.order_tree.pack(fill=tk.BOTH, expand=True)
        
        # Controls Frame
        controls_frame = ttk.Frame(self.root)
        controls_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        # Order Type
        ttk.Label(controls_frame, text="Order Type:").grid(row=0, column=0, padx=5)
        self.order_type_var = tk.StringVar(value="Dine-In")
        ttk.Radiobutton(controls_frame, text="Dine-In", variable=self.order_type_var, value="Dine-In").grid(row=0, column=1, padx=5)
        ttk.Radiobutton(controls_frame, text="Takeaway", variable=self.order_type_var, value="Takeaway").grid(row=0, column=2, padx=5)
        
        # Table Number (for Dine-In)
        ttk.Label(controls_frame, text="Table Number:").grid(row=0, column=3, padx=5)
        self.table_number_entry = ttk.Entry(controls_frame, width=5)
        self.table_number_entry.grid(row=0, column=4, padx=5)
        
        # Quantity Controls
        ttk.Label(controls_frame, text="Quantity:").grid(row=1, column=0, padx=5)
        self.quantity_spinbox = ttk.Spinbox(controls_frame, from_=1, to=10, width=5)
        self.quantity_spinbox.grid(row=1, column=1, padx=5)
        
        # Add to Order Button
        ttk.Button(controls_frame, text="Add to Order", command=self.add_to_order).grid(row=1, column=2, padx=5)
        
        # Remove from Order Button
        ttk.Button(controls_frame, text="Remove Selected", command=self.remove_from_order).grid(row=1, column=3, padx=5)
        
        # Discount
        ttk.Label(controls_frame, text="Discount (%):").grid(row=1, column=4, padx=5)
        self.discount_entry = ttk.Entry(controls_frame, width=5)
        self.discount_entry.insert(0, "0")
        self.discount_entry.grid(row=1, column=5, padx=5)
        
        # Payment Method
        ttk.Label(controls_frame, text="Payment Method:").grid(row=2, column=0, padx=5)
        self.payment_method_var = tk.StringVar(value="Cash")
        ttk.Radiobutton(controls_frame, text="Cash", variable=self.payment_method_var, value="Cash").grid(row=2, column=1, padx=5)
        ttk.Radiobutton(controls_frame, text="Card", variable=self.payment_method_var, value="Card").grid(row=2, column=2, padx=5)
        ttk.Radiobutton(controls_frame, text="UPI", variable=self.payment_method_var, value="UPI").grid(row=2, column=3, padx=5)
        
        # Bill Summary
        summary_frame = ttk.LabelFrame(controls_frame, text="Bill Summary", padding=5)
        summary_frame.grid(row=3, column=0, columnspan=6, pady=10, sticky="ew")
        
        ttk.Label(summary_frame, text="Subtotal:").grid(row=0, column=0, sticky="e")
        self.subtotal_label = ttk.Label(summary_frame, text="$0.00")
        self.subtotal_label.grid(row=0, column=1, sticky="w")
        
        ttk.Label(summary_frame, text="GST (5%):").grid(row=1, column=0, sticky="e")
        self.gst_label = ttk.Label(summary_frame, text="$0.00")
        self.gst_label.grid(row=1, column=1, sticky="w")
        
        ttk.Label(summary_frame, text="Discount:").grid(row=2, column=0, sticky="e")
        self.discount_label = ttk.Label(summary_frame, text="$0.00")
        self.discount_label.grid(row=2, column=1, sticky="w")
        
        ttk.Label(summary_frame, text="Total:").grid(row=3, column=0, sticky="e")
        self.total_label = ttk.Label(summary_frame, text="$0.00", font=('Arial', 10, 'bold'))
        self.total_label.grid(row=3, column=1, sticky="w")
        
        # Process Order Button
        ttk.Button(controls_frame, text="Process Order", command=self.process_order).grid(row=4, column=0, columnspan=6, pady=10)
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
    
    def load_menu_items(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT item_id, name, category, price FROM menu_items")
        items = cursor.fetchall()
        conn.close()
        
        for item in items:
            self.menu_tree.insert('', tk.END, values=(item[1], item[2], f"{item[3]:.2f}"), iid=item[0])
    
    def add_to_order(self):
        selected_item = self.menu_tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item from the menu")
            return
        
        quantity = int(self.quantity_spinbox.get())
        if quantity < 1:
            messagebox.showwarning("Warning", "Quantity must be at least 1")
            return
        
        item_id = int(selected_item)
        item_values = self.menu_tree.item(selected_item, 'values')
        item_name = item_values[0]
        item_price = float(item_values[2])
        
        # Check if item already in order
        for item in self.current_order:
            if item['item_id'] == item_id:
                item['quantity'] += quantity
                self.update_order_display()
                return
        
        # Add new item to order
        self.current_order.append({
            'item_id': item_id,
            'name': item_name,
            'price': item_price,
            'quantity': quantity
        })
        
        self.update_order_display()
    
    def remove_from_order(self):
        selected_item = self.order_tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item from the order")
            return
        
        item_id = int(selected_item)
        for i, item in enumerate(self.current_order):
            if item['item_id'] == item_id:
                del self.current_order[i]
                break
        
        self.update_order_display()
    
    def update_order_display(self):
        # Clear current display
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        
        # Add current order items
        for item in self.current_order:
            total_price = item['price'] * item['quantity']
            self.order_tree.insert('', tk.END, iid=item['item_id'],
                                 values=(item['name'], f"{item['price']:.2f}", 
                                         item['quantity'], f"{total_price:.2f}"))
        
        # Update bill summary
        self.update_bill_summary()
    
    def update_bill_summary(self):
        try:
            discount_percentage = float(self.discount_entry.get())
        except ValueError:
            discount_percentage = 0
        
        bill = BillCalculator.process_order(self.current_order, discount_percentage)
        
        self.subtotal_label.config(text=f"${bill['subtotal']:.2f}")
        self.gst_label.config(text=f"${bill['gst_amount']:.2f}")
        self.discount_label.config(text=f"${bill['discount_amount']:.2f}")
        self.total_label.config(text=f"${bill['total']:.2f}")
    
    def process_order(self):
        if not self.current_order:
            messagebox.showwarning("Warning", "Cannot process empty order")
            return
        
        try:
            discount_percentage = float(self.discount_entry.get())
        except ValueError:
            discount_percentage = 0
        
        # Get order details
        order_type = self.order_type_var.get()
        payment_method = self.payment_method_var.get()
        table_number = None
        
        if order_type == "Dine-In":
            try:
                table_number = int(self.table_number_entry.get())
            except ValueError:
                messagebox.showwarning("Warning", "Please enter a valid table number")
                return
        
        # Calculate bill
        bill = BillCalculator.process_order(self.current_order, discount_percentage)
        
        # Save to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert order
        cursor.execute('''
        INSERT INTO orders (order_type, subtotal, gst_amount, discount, total, payment_method, table_number)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_type,
            bill['subtotal'],
            bill['gst_amount'],
            bill['discount_amount'],
            bill['total'],
            payment_method,
            table_number
        ))
        
        order_id = cursor.lastrowid
        
        # Insert order items
        for item in self.current_order:
            cursor.execute('''
            INSERT INTO order_items (order_id, item_id, quantity, price)
            VALUES (?, ?, ?, ?)
            ''', (
                order_id,
                item['item_id'],
                item['quantity'],
                item['price']
            ))
        
        conn.commit()
        conn.close()
        
        # Generate receipt
        self.generate_receipt(order_id, bill, order_type, payment_method, table_number)
        
        # Reset for new order
        self.current_order = []
        self.update_order_display()
        messagebox.showinfo("Success", "Order processed successfully!")
    
    def generate_receipt(self, order_id, bill, order_type, payment_method, table_number):
        receipt = f"""
        RESTAURANT BILLING SYSTEM
        -------------------------
        Order ID: {order_id}
        Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Order Type: {order_type}
        {f"Table: {table_number}" if table_number else ""}
        -------------------------
        ITEMS:
        """
        
        for item in bill['items']:
            receipt += f"\n{item['name']} x{item['quantity']} @ ${item['price']:.2f} = ${item['price'] * item['quantity']:.2f}"
        
        receipt += f"""
        -------------------------
        Subtotal: ${bill['subtotal']:.2f}
        GST (5%): ${bill['gst_amount']:.2f}
        Discount: ${bill['discount_amount']:.2f}
        -------------------------
        TOTAL: ${bill['total']:.2f}
        -------------------------
        Payment Method: {payment_method}
        """
        
        # Save receipt to file
        with open(f"data/receipt_{order_id}.txt", "w") as f:
            f.write(receipt)
        
        print(receipt)  # For demo purposes, would be printing in real system

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantBillingApp(root)
    root.mainloop()