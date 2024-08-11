import tkinter as tk
from tkinter import ttk
import database.categories as cats

class ChangeCategoryPopup:
    def __init__(self, parent, current_category, category_data, phrase=None):
        self.top = tk.Toplevel(parent)
        self.top.title("Change Category")
        self.current_category = current_category
        self.category_data = category_data
        self.phrase = phrase
        self.new_category_id = 0
        self.category_map = {row[1]:row[0] for row in self.category_data}
        
        self.frame = ttk.Frame(self.top, padding="10")
        self.frame.pack(fill="both", expand=True)

        if phrase:
            ttk.Label(self.frame, text="Phrase:").pack(anchor="w")
            ttk.Label(self.frame, text=phrase).pack(anchor="w", pady=5)
        
        ttk.Label(self.frame, text="Parent Category:").pack(anchor="w")
        self.parent_category_dropdown = ttk.Combobox(self.frame)
        self.parent_category_dropdown.bind("<<ComboboxSelected>>", self.on_parent_category_select)
        self.parent_category_dropdown.pack(fill="x", pady=5)

        ttk.Label(self.frame, text="Child Category").pack(anchor="w")
        self.child_category_dropdown = ttk.Combobox(self.frame)
        self.child_category_dropdown.bind("<<ComboboxSelected>>", self.set_new_category)
        self.child_category_dropdown.pack(fill="x", pady=5)

        self.load_categories()
        
        ttk.Button(self.frame, text="OK", command=self.ok).pack(side="left", padx=5)
        ttk.Button(self.frame, text="Cancel", command=self.cancel).pack(side="left", padx=5)

    def load_categories(self):
        parent_categories = sorted([row[1] for row in self.category_data if not row[3]])
        self.parent_category_dropdown['values'] = parent_categories
        parent_category = None

        if self.current_category in parent_categories:
            parent_category = self.current_category
        else:
            parent_category = [row[4] for row in self.category_data if row[1] == self.current_category][0]

        self.parent_category_dropdown.set(parent_category)
        child_categories = sorted([row[1] for row in self.category_data if row[4] == parent_category])
        self.child_category_dropdown['values'] = ['None'] + child_categories

        if self.current_category in child_categories:
            self.child_category_dropdown.set(self.current_category)
        else:
            self.child_category_dropdown.set(value='None')

    def on_parent_category_select(self, event=None):
        child_categories = sorted([row[1] for row in self.category_data if row[4] == self.parent_category_dropdown.get()])
        self.child_category_dropdown['values'] = ['None'] + child_categories
        self.child_category_dropdown.set(value='None')
        self.set_new_category()


    def set_new_category(self, event=None):
        if self.child_category_dropdown.get() == 'None':
            self.new_category_id = self.category_map[self.parent_category_dropdown.get()]
        else:
            self.new_category_id = self.category_map[self.child_category_dropdown.get()]


    def ok(self):
        self.top.destroy()

    def cancel(self):
        self.new_category_id = 0
        self.top.destroy()
