import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import webbrowser

class SewingInventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sewing Inventory")
        self.root.geometry("1200x900")  # Increased window width
        self.root.configure(bg="purple")

        self.current_page = 1  # Track the current page
        self.total_pages = 3  # Total pages: Inventory (1), Notes (2), Search Links (3)

        # Data storage
        self.inventory = [{"Name": f"Item {i+1}", "Quantity": 0} for i in range(30)]  # 30 items
        self.notes = "Here you can add your personal sewing notes or instructions."

        # Title
        tk.Label(root, text="Sewing Inventory", font=("Arial", 24, "bold"), bg="purple", fg="white").pack(pady=10)

        # Page Frame
        self.page_frame = tk.Frame(root, bg="purple")
        self.page_frame.pack(fill=tk.BOTH, expand=True)

        # Navigation buttons for pages
        nav_buttons_frame = tk.Frame(root, bg="purple")
        nav_buttons_frame.pack(pady=10)

        # Bigger buttons with increased font and padding
        self.inventory_btn = tk.Button(nav_buttons_frame, text="Inventory", command=self.show_inventory_page,
                                       font=("Arial", 16, "bold"), height=2, width=20, relief="solid", bd=2)
        self.inventory_btn.pack(side=tk.LEFT, padx=15)

        self.notes_btn = tk.Button(nav_buttons_frame, text="Notes", command=self.show_notes_page,
                                   font=("Arial", 16, "bold"), height=2, width=20, relief="solid", bd=2)
        self.notes_btn.pack(side=tk.LEFT, padx=15)

        self.search_links_btn = tk.Button(nav_buttons_frame, text="Search Links", command=self.show_search_links_page,
                                          font=("Arial", 16, "bold"), height=2, width=20, relief="solid", bd=2)
        self.search_links_btn.pack(side=tk.LEFT, padx=15)

        # Display the first page (Inventory)
        self.render_page()

    def render_page(self):
        # Clear previous content
        for widget in self.page_frame.winfo_children():
            widget.destroy()

        # Render the current page
        if self.current_page == 1:
            self.render_inventory_page()
        elif self.current_page == 2:
            self.render_notes_page()
        elif self.current_page == 3:
            self.render_search_links_page()

    def render_inventory_page(self):
        # Inventory Items as small horizontal boxes
        content_frame = tk.Frame(self.page_frame, bg="purple")
        content_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(content_frame, text="Search Inventory:", font=("Arial", 12), bg="purple", fg="white").pack(pady=5)

        # Search bar
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(content_frame, textvariable=self.search_var, font=("Arial", 12), width=30)
        search_entry.pack(pady=5)

        search_button = tk.Button(content_frame, text="Search", command=self.search_inventory, font=("Arial", 12), height=2, width=15)
        search_button.pack(pady=5)

        # Save/Load buttons for Excel
        save_button = tk.Button(content_frame, text="Save Inventory", command=self.save_inventory, font=("Arial", 12), height=2, width=15)
        save_button.pack(pady=5)

        load_button = tk.Button(content_frame, text="Load Inventory", command=self.load_inventory, font=("Arial", 12), height=2, width=15)
        load_button.pack(pady=5)

        items_frame = tk.Frame(content_frame, bg="purple")
        items_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a canvas to add the scrollbar to the items frame
        items_canvas = tk.Canvas(items_frame)
        items_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the canvas
        items_scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=items_canvas.yview)
        items_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        items_canvas.configure(yscrollcommand=items_scrollbar.set)

        # Create a frame inside the canvas for the inventory items
        items_scrollable_frame = tk.Frame(items_canvas, bg="purple")
        items_canvas.create_window((0, 0), window=items_scrollable_frame, anchor="nw")

        # Add inventory items as two columns (horizontally)
        self.filtered_inventory = self.inventory  # Initially show all items
        row_frame = None  # Variable to hold each row of items

        for idx, item in enumerate(self.filtered_inventory):
            if idx % 2 == 0:  # Every even index, start a new row
                row_frame = tk.Frame(items_scrollable_frame, bg="purple")
                row_frame.pack(fill=tk.X, padx=5, pady=5)

            # Create a frame for each item
            item_frame = tk.Frame(row_frame, bg="lightblue", padx=5, pady=5, relief="solid", bd=1)
            item_frame.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)

            item_name_frame = tk.Frame(item_frame, bg="lightblue")
            item_name_frame.pack(side=tk.LEFT, fill=tk.X, padx=10)

            item_name_var = tk.StringVar(value=item["Name"])  # Variable to track item name
            item_name_entry = tk.Entry(item_name_frame, textvariable=item_name_var, font=("Arial", 12), width=20)
            item_name_entry.pack(side=tk.LEFT, padx=10)

            save_button = tk.Button(item_name_frame, text="Save", command=lambda idx=idx, item_name_var=item_name_var: self.save_item_name(idx, item_name_var))
            save_button.pack(side=tk.LEFT, padx=10)

            quantity_frame = tk.Frame(item_frame, bg="lightblue")
            quantity_frame.pack(side=tk.LEFT, padx=10)

            tk.Label(quantity_frame, text="Quantity:", font=("Arial", 10), bg="lightblue").pack(side=tk.LEFT, padx=5)
            quantity_label = tk.Label(quantity_frame, text=str(item["Quantity"]), font=("Arial", 10), bg="lightblue")
            quantity_label.pack(side=tk.LEFT, padx=5)

            modify_frame = tk.Frame(item_name_frame, bg="lightblue")
            modify_frame.pack(side=tk.LEFT, padx=10)

            add_btn = tk.Button(modify_frame, text="Add", command=lambda idx=idx, quantity_label=quantity_label: self.add_quantity(idx, quantity_label))
            add_btn.pack(side=tk.LEFT, padx=5)

            subtract_btn = tk.Button(modify_frame, text="Subtract", command=lambda idx=idx, quantity_label=quantity_label: self.subtract_quantity(idx, quantity_label))
            subtract_btn.pack(side=tk.LEFT, padx=5)

        # Update the canvas scroll region
        items_scrollable_frame.update_idletasks()
        items_canvas.config(scrollregion=items_canvas.bbox("all"))

    def search_inventory(self):
        search_term = self.search_var.get().lower()
        self.filtered_inventory = [item for item in self.inventory if search_term in item["Name"].lower()]
        self.render_inventory_page()

    def save_item_name(self, idx, item_name_var):
        new_name = item_name_var.get()
        self.inventory[idx]["Name"] = new_name
        messagebox.showinfo("Item Saved", f"Item '{new_name}' has been saved.")

    def add_quantity(self, idx, quantity_label):
        self.inventory[idx]["Quantity"] += 1
        quantity_label.config(text=str(self.inventory[idx]["Quantity"]))

    def subtract_quantity(self, idx, quantity_label):
        if self.inventory[idx]["Quantity"] > 0:
            self.inventory[idx]["Quantity"] -= 1
        quantity_label.config(text=str(self.inventory[idx]["Quantity"]))

    def save_inventory(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            df = pd.DataFrame(self.inventory)
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Saved", "Inventory has been saved successfully.")

    def load_inventory(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            df = pd.read_excel(file_path)
            self.inventory = df.to_dict(orient="records")
            messagebox.showinfo("Loaded", "Inventory has been loaded successfully.")
            self.render_inventory_page()

    def render_notes_page(self):
        # Notes Page
        content_frame = tk.Frame(self.page_frame, bg="purple")
        content_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(content_frame, text="Notes", font=("Arial", 24, "bold"), bg="purple", fg="white").pack(pady=20)

        self.notes_text = tk.Text(content_frame, font=("Arial", 12), height=10, width=80)
        self.notes_text.pack(pady=10)
        self.notes_text.insert(tk.END, self.notes)  # Pre-fill with notes content

        save_notes_button = tk.Button(content_frame, text="Save Notes", command=self.save_notes, font=("Arial", 12), height=2, width=15)
        save_notes_button.pack(pady=10)

    def save_notes(self):
        self.notes = self.notes_text.get("1.0", tk.END).strip()  # Save the notes content
        messagebox.showinfo("Notes Saved", "Your notes have been saved.")

    def render_search_links_page(self):
        # Search Links Page
        content_frame = tk.Frame(self.page_frame, bg="purple")
        content_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(content_frame, text="Search Links", font=("Arial", 24, "bold"), bg="purple", fg="white").pack(pady=20)

        links_frame = tk.Frame(content_frame, bg="purple")
        links_frame.pack(pady=10)

        # Search links
        self.links = [
            {"name": "Google", "url": "https://www.google.com"},
            {"name": "YouTube", "url": "https://www.youtube.com"},
            {"name": "Pinterest", "url": "https://www.pinterest.com"}
        ]

        for link in self.links:
            link_button = tk.Button(links_frame, text=link["name"], command=lambda url=link["url"]: self.open_link(url),
                                    font=("Arial", 12), width=20, height=2)
            link_button.pack(pady=5)

    def open_link(self, url):
        webbrowser.open(url)

    def show_inventory_page(self):
        self.current_page = 1
        self.render_page()

    def show_notes_page(self):
        self.current_page = 2
        self.render_page()

    def show_search_links_page(self):
        self.current_page = 3
        self.render_page()


if __name__ == "__main__":
    root = tk.Tk()
    app = SewingInventoryApp(root)
    root.mainloop()
