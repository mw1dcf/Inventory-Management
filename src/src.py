import customtkinter as ctk
import sqlite3
from tkinter import messagebox

# Create the SQLite database and tables
def create_database():
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            category TEXT,
            quantity INTEGER,
            reorder_level INTEGER,
            supplier TEXT,
            location TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            action TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Log actions in the database
def log_action(item_id, action):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO logs (item_id, action) VALUES (?, ?)', (item_id, action))
    conn.commit()
    conn.close()

# Inventory Management Class
class InventoryManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Management System")
        self.geometry("800x600")  # Updated window size
        
        # Centering the window
        self.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())

        # Create the database
        create_database()

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Labels and Entry fields with increased font size
        # Removed Item ID entry field
        ctk.CTkLabel(self, text="Name", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        self.entry_name = ctk.CTkEntry(self, font=("Arial", 14))
        self.entry_name.grid(row=0, column=1)

        ctk.CTkLabel(self, text="Description", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10)
        self.entry_description = ctk.CTkEntry(self, font=("Arial", 14))
        self.entry_description.grid(row=1, column=1)

        ctk.CTkLabel(self, text="Category", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10)
        self.entry_category = ctk.CTkEntry(self, font=("Arial", 14))
        self.entry_category.grid(row=2, column=1)

        ctk.CTkLabel(self, text="Quantity", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=10)
        self.entry_quantity = ctk.CTkEntry(self, font=("Arial", 14))
        self.entry_quantity.grid(row=3, column=1)

        ctk.CTkLabel(self, text="Reorder Level", font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=10)
        self.entry_reorder_level = ctk.CTkEntry(self, font=("Arial", 14))
        self.entry_reorder_level.grid(row=4, column=1)

        ctk.CTkLabel(self, text="Supplier", font=("Arial", 14)).grid(row=5, column=0, padx=10, pady=10)
        self.entry_supplier = ctk.CTkEntry(self, font=("Arial", 14))
        self.entry_supplier.grid(row=5, column=1)

        ctk.CTkLabel(self, text="Location", font=("Arial", 14)).grid(row=6, column=0, padx=10, pady=10)
        self.entry_location = ctk.CTkEntry(self, font=("Arial", 14))
        self.entry_location.grid(row=6, column=1)

        # Buttons with increased font size
        ctk.CTkButton(self, text="Add Item", command=self.add_item, font=("Arial", 14)).grid(row=7, column=0, padx=10, pady=10)
        ctk.CTkButton(self, text="Remove Item", command=self.remove_item, font=("Arial", 14)).grid(row=7, column=1, padx=10, pady=10)
        ctk.CTkButton(self, text="Update Item", command=self.update_item, font=("Arial", 14)).grid(row=7, column=2, padx=10, pady=10)
        ctk.CTkButton(self, text="Display Inventory", command=self.display_inventory, font=("Arial", 14)).grid(row=8, column=0, columnspan=3, padx=10, pady=10)
        ctk.CTkButton(self, text="Display Logs", command=self.display_logs, font=("Arial", 14)).grid(row=9, column=0, columnspan=3, padx=10, pady=10)

    def add_item(self):
        name = self.entry_name.get()
        description = self.entry_description.get()
        category = self.entry_category.get()
        quantity = int(self.entry_quantity.get())
        reorder_level = int(self.entry_reorder_level.get())
        supplier = self.entry_supplier.get()
        location = self.entry_location.get()

        conn = sqlite3.connect('inventory_management.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO inventory (name, description, category, quantity, reorder_level, supplier, location) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                           (name, description, category, quantity, reorder_level, supplier, location))
            conn.commit()
            item_id = cursor.lastrowid  # Get the auto-incremented item_id
            log_action(item_id, "Added")
            messagebox.showinfo("Success", "Item added successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Item ID already exists.")
        finally:
            conn.close()

    def remove_item(self):
        item_id = self.entry_item_id.get()
        conn = sqlite3.connect('inventory_management.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM inventory WHERE item_id = ?', (item_id,))
        conn.commit()
        log_action(item_id, "Removed")
        messagebox.showinfo("Success", "Item removed successfully!")
        conn.close()

    def update_item(self):
        item_id = self.entry_item_id.get()
        name = self.entry_name.get()
        description = self.entry_description.get()
        category = self.entry_category.get()
        quantity = int(self.entry_quantity.get())
        reorder_level = int(self.entry_reorder_level.get())
        supplier = self.entry_supplier.get()
        location = self.entry_location.get()

        conn = sqlite3.connect('inventory_management.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE inventory SET name = ?, description = ?, category = ?, quantity = ?, reorder_level = ?, supplier = ?, location = ? WHERE item_id = ?
        ''', (name, description, category, quantity, reorder_level, supplier, location, item_id))
        conn.commit()
        log_action(item_id, "Updated")
        messagebox.showinfo("Success", "Item updated successfully!")
        conn.close()

    def display_inventory(self):
        conn = sqlite3.connect('inventory_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM inventory')
        items = cursor.fetchall()
        conn.close()

        inventory_window = ctk.CTkToplevel(self)
        inventory_window.title("Inventory List")
        inventory_window.geometry("400x300")

        for index, item in enumerate(items):
            ctk.CTkLabel(inventory_window, text=f"ID: {item[0]}, Name: {item[1]}, Quantity: {item[4]}", font=("Arial", 12)).pack(pady=5)

    def display_logs(self):
        conn = sqlite3.connect('inventory_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM logs')
        logs = cursor.fetchall()
        conn.close()

        logs_window = ctk.CTkToplevel(self)
        logs_window.title("Logs")
        logs_window.geometry("400x300")

        for index, log in enumerate(logs):
            ctk.CTkLabel(logs_window, text=f"Log ID: {log[0]}, Item ID: {log[1]}, Action: {log[2]}, Timestamp: {log[3]}", font=("Arial", 12)).pack(pady=5)

if __name__ == "__main__":
    app = InventoryManagementApp()
    app.mainloop()
