import tkinter as tk
from tkinter import ttk
import database.categories as cats

class ChildCategoryPopup:
    def __init__(self, parent, cursor, category_data, current_category_id):
        self.top = tk.Toplevel(parent)
        self.top.title("Edit Child Category")
        self.cursor = cursor
        self.category_data = category_data
        self.parent_category_map = {row[1]:row[0] for row in self.category_data if not row[3]}

        current_category = cats.get_category_by_id(self.cursor, current_category_id)
        self.name = current_category[1]
        self.parent_id = current_category[3]
        self.parent_category = current_category[4]
        
        self.frame = ttk.Frame(self.top, padding="10")
        self.frame.pack(fill="both", expand=True)
        
        ttk.Label(self.frame, text="Category Name:").pack(anchor="w")
        self.name_entry = ttk.Entry(self.frame)
        self.name_entry.insert(0, self.name)
        self.name_entry.pack(fill="x", pady=5)

        ttk.Label(self.frame, text="Parent Category:").pack(anchor="w")
        self.parent_category_dropdown = ttk.Combobox(self.frame)
        self.parent_category_dropdown.bind("<<ComboboxSelected>>", self.on_parent_category_select)
        self.parent_category_dropdown.pack(fill="x", pady=5)

        self.load_parent_categories()
        
        ttk.Button(self.frame, text="OK", command=self.ok).pack(side="left", padx=5)
        ttk.Button(self.frame, text="Cancel", command=self.cancel).pack(side="left", padx=5)

    def load_parent_categories(self):
        parent_categories = sorted(list(self.parent_category_map.keys()))
        self.parent_category_dropdown['values'] = parent_categories
        if (self.parent_category in parent_categories):
            self.parent_category_dropdown.set(self.parent_category)

    def on_parent_category_select(self, event=None):
        selected_parent_category = self.parent_category_dropdown.get()
        self.parent_id = self.parent_category_map[selected_parent_category]

    def ok(self):
        self.name = self.name_entry.get()
        self.parent_id = self.parent_id
        self.top.destroy()

    def cancel(self):
        self.top.destroy()
