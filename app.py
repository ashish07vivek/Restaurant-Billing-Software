from db_utils import initialize_database
from main_ui import RestaurantBillingApp
import tkinter as tk

def main():
    # Initialize database
    initialize_database()
    
    # Start GUI
    root = tk.Tk()
    app = RestaurantBillingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()