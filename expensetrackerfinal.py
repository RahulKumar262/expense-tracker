import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import sqlite3
import matplotlib.pyplot as plt # type: ignore

def save_record():
    """Saves the current record to the table and the SQLite database."""
    item_name = item_name_var.get()
    item_price = item_price_entry.get()
    if not item_price:
        messagebox.showwarning("Error", "Please fill all fields.")
        return
    try:
        item_price = float(item_price)
    except ValueError:
        messagebox.showwarning("Error", "Invalid item price.")
        return
    
    # Get the current date
    current_date = datetime.date.today().strftime("%d %B %Y")
    # Insert the new record into the table
    cursor.execute("INSERT INTO expenses (item_name, item_price, purchase_date) VALUES (?, ?, ?)",
                   (item_name, item_price, current_date))
    conn.commit()  # Commit changes to the database
    # Clear the entry fields
    load_data()  # Reload data after saving record

def load_data():
    """Loads data from the SQLite database and inserts it into the table."""
    for row in table.get_children():
        table.delete(row)
    cursor.execute("SELECT * FROM expenses")
    for row in cursor.fetchall():   
        table.insert("", tk.END, values=row)
    # Load budget from the database
    cursor.execute("SELECT budget FROM budget")
    row = cursor.fetchone()
    if row:
        global total_budget
        total_budget = row[0]

def delete_record():
    """Deletes the selected record from the table."""
    selected_item = table.selection()[0]
    serial_no = table.item(selected_item, "values")[0]
    # Delete the record from the SQLite database
    cursor.execute("DELETE FROM expenses WHERE serial_no=?", (serial_no,))
    conn.commit()  # Commit changes to the database
    load_data()  # Reload data after deleting record

def update_record():
    """Updates the selected record in the table."""
    selected_item = table.selection()[0]
    serial_no = table.item(selected_item, "values")[0]
    item_name = item_name_var.get()
    item_price = item_price_entry.get()
    if not item_price:
        messagebox.showwarning("Error", "Please fill all fields.")
        return
    try:
        item_price = float(item_price)
    except ValueError:
        messagebox.showwarning("Error", "Invalid item price.")
        return
    current_date = datetime.date.today().strftime("%d %B %Y")
    # Update the record in the SQLite database
    cursor.execute("UPDATE expenses SET item_name=?, item_price=?, purchase_date=? WHERE serial_no=?",
                   (item_name, item_price, current_date, serial_no))
    conn.commit()  # Commit changes to the database
    load_data()  # Reload data after updating record

def show_visualization():
    """Opens a new window to display a pie chart showing total expenses and budget left."""
    global total_budget
    # Retrieve data from the SQLite database
    cursor.execute("SELECT item_name, item_price FROM expenses")
    rows = cursor.fetchall()
    
    # Calculate total expenses for each category
    category_expenses = {}
    total_expenses = 0
    for row in rows:
        item_name = row[0]
        item_price = row[1]
        total_expenses += item_price
        if item_name in category_expenses:
            category_expenses[item_name] += item_price
        else:
            category_expenses[item_name] = item_price
    
    # Calculate budget left
    budget_left = total_budget - total_expenses
    
    # Prepare data for plotting
    labels = list(category_expenses.keys()) + ["Remaining Budget"]
    values = list(category_expenses.values()) + [budget_left]
    
    # Prepare labels with actual amounts
    labels_with_amounts = [f"{label} (₹{value:.2f})" for label, value in zip(labels, values)]
    
    # Plot pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(values, labels=labels_with_amounts, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Total Expenses and Budget Left by Category')
    plt.tight_layout()
    plt.show()

def set_budget():
    """Sets the total budget."""
    global total_budget
    total_budget = float(budget_entry.get())
    # Update or insert budget into the database
    cursor.execute("SELECT * FROM budget")
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE budget SET budget=?", (total_budget,))
    else:
        cursor.execute("INSERT INTO budget (budget) VALUES (?)", (total_budget,))
    conn.commit()  # Commit changes to the database
    messagebox.showinfo("Budget Set", f"Total Budget set to ₹{total_budget}")

# Connect to SQLite database
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create expenses table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses(serial_no INTEGER PRIMARY KEY,item_name TEXT,item_price REAL,purchase_date TEXT)''')

# Create budget table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS budget(budget REAL)''')

# Create the main window
root = tk.Tk()
root.title("Daily Expenses")

# Create the table
table = ttk.Treeview(root, columns=("Serial no", "Item Name", "Item Price", "Purchase Date"), show="headings")
table.heading("Serial no", text="Serial no")
table.heading("Item Name", text="Item Name")
table.heading("Item Price", text="Item Price")
table.heading("Purchase Date", text="Date")
table.pack(side=tk.LEFT)

# Load data from SQLite database
load_data()

# Create a frame for the buttons and entry fields
button_frame = tk.Frame(root)
button_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Create the radio buttons for the item name
item_name_var = tk.StringVar()
food_button = tk.Radiobutton(button_frame, text="Food", variable=item_name_var, value="Food")
travel_button = tk.Radiobutton(button_frame, text="Travel", variable=item_name_var, value="Travel")
books_button = tk.Radiobutton(button_frame, text="Books", variable=item_name_var, value="Books")
entertainment_button = tk.Radiobutton(button_frame, text="Entertainment", variable=item_name_var, value="Entertainment")
misc_button = tk.Radiobutton(button_frame, text="Miscellaneous", variable=item_name_var, value="Miscellaneous")
save = tk.Button(button_frame, text="Save Record", command=save_record)

food_button.grid(row=0, column=0, padx=5, pady=5)
travel_button.grid(row=1, column=0, padx=5, pady=5)
books_button.grid(row=2, column=0, padx=5, pady=5)
entertainment_button.grid(row=3, column=0, padx=5, pady=5)
misc_button.grid(row=4, column=0, padx=5, pady=5)

# Create the entry fields
item_price_label = tk.Label(button_frame, text="Item Price")
item_price_label.grid(row=5, column=0, padx=5, pady=5)
item_price_entry = tk.Entry(button_frame)
item_price_entry.grid(row=6, column=0, padx=5, pady=5)
save.grid(row=7, column=0, padx=5, pady=5)

# Create the buttons

exit = tk.Button(button_frame, text="Exit", command=root.quit)
update = tk.Button(button_frame, text="Update", command=update_record)
delete = tk.Button(button_frame, text="Delete", command=delete_record)
show= tk.Button(button_frame, text="Show Expenditure", command=show_visualization)
budget_label = tk.Label(button_frame, text="Set Total Budget:")
budget_button = tk.Button(button_frame, text="Set Budget", command=set_budget)

budget_label.grid(row=0, column=1, padx=5, pady=5)
budget_entry = tk.Entry(button_frame)
budget_entry.grid(row=1, column=1, padx=5, pady=5)
exit.grid(row=7, column=1, padx=5, pady=5)
update.grid(row=3, column=1, padx=5, pady=5)
delete.grid(row=4, column=1, padx=5, pady=5)
show.grid(row=5, column=1, padx=5, pady=5)
budget_button.grid(row=2, column=1, padx=5, pady=5)

root.mainloop()
