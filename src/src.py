import customtkinter as ctk
import sqlite3
from tkinter import messagebox

# Create the SQLite database and tables
def create_database():
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            item_id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            category TEXT,
            quantity INTEGER,
            reorder_level INTEGER,
            supplier TEXT,
            location TEXT
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
        self.geometry("600x400")
        
        # Create the database
        create_database()

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Labels and Entry fields
        ctk.CTkLabel(self, text="Item ID").grid(row=0, column=0, padx=10, pady=10)
        self.entry_item_id = ctk.CTkEntry(self)
        self.entry_item_id.grid(row=0, column=1)

        ctk.CTkLabel(self, text="Name").grid(row=1, column=0, padx=10, pady=10)
        self.entry_name = ctk.CTkEntry(self)
        self.entry_name.grid(row=1, column=1)

        ctk.CTkLabel(self, text="Description").grid(row=2, column=0, padx=10, pady=10)
        self.entry_description = ctk.CTkEntry(self)
        self.entry_description.grid(row=2, column=1)

        ctk.CTkLabel(self, text="Category").grid(row=3, column=0, padx=10, pady=10)
        self.entry_category = ctk.CTkEntry(self)
        self.entry_category.grid(row=3, column=1)

        ctk.CTkLabel(self, text="Quantity").grid(row=4, column=0, padx=10, pady=10)
        self.entry_quantity = ctk.CTkEntry(self)
        self.entry_quantity.grid(row=4, column=1)

        ctk.CTkLabel(self, text="Reorder Level").grid(row=5, column=0, padx=10, pady=10)
        self.entry_reorder_level = ctk.CTkEntry(self)
        self.entry_reorder_level.grid(row=5, column=1)

        ctk.CTkLabel(self, text="Supplier").grid(row=6, column=0, padx=10, pady=10)
        self.entry_supplier = ctk.CTkEntry(self)
        self.entry_supplier.grid(row=6, column=1)

        ctk.CTkLabel(self, text="Location").grid(row=7, column=0, padx=10, pady=10)
        self.entry_location = ctk.CTkEntry(self)
        self.entry_location.grid(row=7, column=1)

        # Buttons
        ctk.CTkButton(self, text="Add Item", command=self.add_item).grid(row=8, column=0, padx=10, pady=10)
        ctk.CTkButton(self, text="Remove Item", command=self.remove_item).grid(row=8, column=1, padx=10, pady=10)
        ctk.CTkButton(self, text="Update Item", command=self.update_item).grid(row=8, column=2, padx=10, pady=10)
        ctk.CTkButton(self, text="Display Inventory", command=self.display_inventory).grid(row=9, column=0, columnspan=3, padx=10, pady=10)

    def add_item(self):
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
        try:
            cursor.execute('INSERT INTO inventory (item_id, name, description, category, quantity, reorder_level, supplier, location) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                           (item_id, name, description, category, quantity, reorder_level, supplier, location))
            conn.commit()
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
            ctk.CTkLabel(inventory_window, text=f"ID: {item[0]}, Name: {item[1]}, Quantity: {item[4]}").pack(pady=5)

if __name__ == "__main__":
    app = InventoryManagementApp()
    app.mainloop()