import tkinter as tk
from tkinter import ttk

class AllIdentifiers:
    def __init__(self, parent, identifier_data):
        self.frame = ttk.Frame(parent)
        self.identifier_data = identifier_data

        self.setup_tab()

    def setup_tab(self):
        tk.Label(self.frame, text="All Identifiers", padx=20, pady=10).pack()

        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Phrase', 'Category', 'Parent Category'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Phrase', text='Phrase')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Parent Category', text='Parent Category')

        self.tree.column('ID', width=80, stretch=False)
        self.tree.column('Phrase', width=500, stretch=False)
        self.tree.column('Category', width=300, stretch=False)
        self.tree.column('Parent Category', width=300, stretch=False)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)
        self.update_identifiers()

        self.tree.pack(fill=tk.Y, expand=True, padx=20, anchor='center')
    
    def on_row_select(self, event=None):
        return
    
    def update_identifiers(self):        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for row in self.identifier_data:
            id = row[0]
            phrase = row[1]
            cat = row[4]
            parent = row[3]
            tree_values = [id, phrase, cat, parent]
            self.tree.insert('', tk.END, values=tree_values)