import tkinter as tk
from tkinter import ttk

class AllCategories:
    def __init__(self, parent, category_data):
        self.frame = ttk.Frame(parent)
        self.category_data = category_data

        self.setup_tab()

    def setup_tab(self):
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        tk.Label(self.frame, text="Subcategories").grid(row=0, column=0, padx=20, pady=10)
        tk.Label(self.frame, text="Main Categories").grid(row=0, column=1, padx=20, pady=10)

        self.subcategory_tree = ttk.Treeview(self.frame, columns=('ID', 'Category', 'Parent Category'), show='headings')
        self.subcategory_tree.heading('ID', text='ID')
        self.subcategory_tree.heading('Category', text='Category')
        self.subcategory_tree.heading('Parent Category', text='Parent Category')

        self.subcategory_tree.column('ID', width=80, stretch=False)
        self.subcategory_tree.column('Category', width=300, stretch=False)
        self.subcategory_tree.column('Parent Category', width=300, stretch=False)

        self.subcategory_tree.grid(row=1, column=0, sticky='ns')

        self.parent_tree = ttk.Treeview(self.frame, columns=('ID', 'Category', 'Type'), show='headings')
        self.parent_tree.heading('ID', text='ID')
        self.parent_tree.heading('Category', text='Category')
        self.parent_tree.heading('Type', text='Type')

        self.parent_tree.column('ID', width=80, stretch=False)
        self.parent_tree.column('Category', width=300, stretch=False)
        self.parent_tree.column('Type', width=200, stretch=False)

        self.parent_tree.grid(row=1, column=1, sticky='ns')

        self.subcategory_tree.bind("<<TreeviewSelect>>", self.on_subcategory_row_select)
        self.parent_tree.bind("<<TreeviewSelect>>", self.on_parent_row_select)

        self.update_categories()

        self.frame.pack(fill=tk.BOTH, expand=True)

    def on_subcategory_row_select(self, event=None):
        return
    
    def on_parent_row_select(self, event=None):
        return
    
    def update_categories(self):        
        for item in self.subcategory_tree.get_children():
            self.subcategory_tree.delete(item)

        for item in self.parent_tree.get_children():
            self.parent_tree.delete(item)
        
        for row in self.category_data:
            id = row[0]
            name = row[1]
            type = row[2]
            parent = row[4]
            
            if not type and parent:
                subcategory_tree_values = [id, name, parent]
                self.subcategory_tree.insert('', tk.END, values=subcategory_tree_values)
            else:
                parent_tree_values = [id, name, type]
                self.parent_tree.insert('', tk.END, values=parent_tree_values)
