import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import webbrowser


class SewingInventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sewing Inventory")
        self.root.geometry("1200x900")
        self.root.configure(bg="purple")

        self.current_page = 1
        self.items_per_page = 24
        self.inventory = [{"Name": f"Item {i + 1}", "Quantity": 0} for i in range(60)]  # 60 items
        self.notes = ""
        self.links = [
            {"name": "Google", "url": "https://www.google.com"},
            {"name": "YouTube", "url": "https://www.youtube.com"},
            {"name": "Pinterest", "url": "https://www.pinterest.com"}
        ]

        # Title
        tk.Label(root, text="Sewing Inventory", font=("Arial", 24, "bold"), bg="purple", fg="white").pack(pady=10)

        # Page Frame
        self.page_frame = tk.Frame(root, bg="purple")
        self.page_frame.pack(fill=tk.BOTH, expand=True)

        # Navigation Buttons
        nav_buttons_frame = tk.Frame(root, bg="purple")
        nav_buttons_frame.pack(pady=10)

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
        for widget in self.page_frame.winfo_children():
            widget.destroy()

        if self.current_page == 1:
            self.render_inventory_page()
        elif self.current_page == 2:
            self.render_notes_page()
        elif self.current_page == 3:
            self.render_search_links_page()

    def render_inventory_page(self):
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        items_to_display = self.inventory[start_idx:end_idx]
        self.total_pages = -(-len(self.inventory) // self.items_per_page)

        tk.Label(self.page_frame, text="Search Inventory:", font=("Arial", 12), bg="purple", fg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self.page_frame, textvariable=self.search_var, font=("Arial", 12), width=30)
        search_entry.grid(row=0, column=1, padx=10, pady=5)

        search_button = tk.Button(self.page_frame, text="Search", command=self.search_inventory, font=("Arial", 12))
        search_button.grid(row=0, column=2, padx=10, pady=5)

        save_button = tk.Button(self.page_frame, text="Save Inventory", command=self.save_inventory, font=("Arial", 12))
        save_button.grid(row=1, column=1, padx=10, pady=5)

        load_button = tk.Button(self.page_frame, text="Load Inventory", command=self.load_inventory, font=("Arial", 12))
        load_button.grid(row=1, column=2, padx=10, pady=5)

        items_frame = tk.Frame(self.page_frame, bg="purple")
        items_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        for idx, item in enumerate(items_to_display):
            row = idx // 6
            col = idx % 6

            item_frame = tk.Frame(items_frame, bg="lightblue", padx=5, pady=5, relief="solid", bd=1)
            item_frame.grid(row=row, column=col, padx=5, pady=5)

            name_var = tk.StringVar(value=item["Name"])
            name_entry = tk.Entry(item_frame, font=("Arial", 12), width=15, textvariable=name_var)
            name_entry.pack(pady=5)
            name_entry.bind("<FocusOut>", lambda e, idx=idx + start_idx: self.update_name(idx, name_var))

            tk.Label(item_frame, text=f"Quantity: {item['Quantity']}", font=("Arial", 10), bg="lightblue").pack()

            tk.Button(item_frame, text="Add", command=lambda idx=idx + start_idx: self.add_quantity(idx)).pack(side=tk.LEFT, padx=5)
            tk.Button(item_frame, text="Subtract", command=lambda idx=idx + start_idx: self.subtract_quantity(idx)).pack(side=tk.RIGHT, padx=5)

        nav_frame = tk.Frame(self.page_frame, bg="purple")
        nav_frame.grid(row=3, column=0, columnspan=3, pady=10)

        prev_btn = tk.Button(nav_frame, text="<< Previous", command=self.previous_page, font=("Arial", 12))
        prev_btn.pack(side=tk.LEFT, padx=5)
        if self.current_page == 1:
            prev_btn["state"] = "disabled"

        page_label = tk.Label(nav_frame, text=f"Page {self.current_page} of {self.total_pages}", font=("Arial", 12), bg="purple", fg="white")
        page_label.pack(side=tk.LEFT, padx=5)

        next_btn = tk.Button(nav_frame, text="Next >>", command=self.next_page, font=("Arial", 12))
        next_btn.pack(side=tk.RIGHT, padx=5)
        if self.current_page == self.total_pages:
            next_btn["state"] = "disabled"

    def render_notes_page(self):
        notes_text = tk.Text(self.page_frame, font=("Arial", 12), height=20, width=80)
        notes_text.insert("1.0", self.notes)
        notes_text.pack(pady=10)

        def save_notes():
            self.notes = notes_text.get("1.0", "end").strip()
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(self.notes)
                messagebox.showinfo("Saved", "Notes saved successfully.")

        tk.Button(self.page_frame, text="Save Notes", command=save_notes, font=("Arial", 12)).pack(pady=5)

    def render_search_links_page(self):
        links_frame = tk.Frame(self.page_frame, bg="purple")
        links_frame.pack(pady=10)

        for idx, link in enumerate(self.links):
            link_frame = tk.Frame(links_frame, bg="purple")
            link_frame.pack(pady=5)

            link_button = tk.Button(link_frame, text=link["name"], font=("Arial", 12),
                                    command=lambda url=link["url"]: webbrowser.open(url))
            link_button.pack(side=tk.LEFT, padx=5)

            delete_button = tk.Button(link_frame, text="Delete", font=("Arial", 12),
                                      command=lambda idx=idx: self.delete_link(idx))
            delete_button.pack(side=tk.LEFT, padx=5)

        add_link_frame = tk.Frame(self.page_frame, bg="purple")
        add_link_frame.pack(pady=10)

        tk.Label(add_link_frame, text="Add New Link:", font=("Arial", 12), bg="purple", fg="white").grid(row=0, column=0, padx=5)
        name_var = tk.StringVar()
        url_var = tk.StringVar()
        tk.Entry(add_link_frame, textvariable=name_var, font=("Arial", 12), width=20).grid(row=0, column=1, padx=5)
        tk.Entry(add_link_frame, textvariable=url_var, font=("Arial", 12), width=40).grid(row=0, column=2, padx=5)

        def add_link():
            name = name_var.get().strip()
            url = url_var.get().strip()
            if name and url:
                self.links.append({"name": name, "url": url})
                self.render_search_links_page()
                messagebox.showinfo("Added", "Link added successfully.")

        tk.Button(add_link_frame, text="Add Link", command=add_link, font=("Arial", 12)).grid(row=0, column=3, padx=5)

    def delete_link(self, idx):
        del self.links[idx]
        self.render_search_links_page()

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.render_inventory_page()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.render_inventory_page()

    def add_quantity(self, idx):
        self.inventory[idx]["Quantity"] += 1
        self.render_inventory_page()

    def subtract_quantity(self, idx):
        if self.inventory[idx]["Quantity"] > 0:
            self.inventory[idx]["Quantity"] -= 1
        self.render_inventory_page()

    def update_name(self, idx, name_var):
        self.inventory[idx]["Name"] = name_var.get()

    def save_inventory(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            pd.DataFrame(self.inventory).to_excel(file_path, index=False)
            messagebox.showinfo("Saved", "Inventory saved successfully.")

    def load_inventory(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            self.inventory = pd.read_excel(file_path).to_dict(orient="records")
            messagebox.showinfo("Loaded", "Inventory loaded successfully.")
            self.render_inventory_page()

    def search_inventory(self):
        search_term = self.search_var.get().lower()
        self.inventory = [item for item in self.inventory if search_term in item["Name"].lower()]
        self.current_page = 1
        self.render_inventory_page()

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
