import tkinter as tk
from tkinter import ttk
import database.identifiers as idens
from popups.change_category_popup import ChangeCategoryPopup

class AllIdentifiers:
    def __init__(self, parent, conn, cursor, identifier_data, category_data, update_identifier_data, update_transaction_data):
        self.frame = ttk.Frame(parent)
        self.conn = conn
        self.cursor = cursor
        self.identifier_data = identifier_data
        self.category_data = category_data
        self.update_identifier_data = update_identifier_data
        self.update_transaction_data = update_transaction_data

        self.setup_tab()

    def setup_tab(self):
        tk.Label(self.frame, text='All Identifiers').pack(pady=10)

        self.edit_category_button = ttk.Button(self.frame, text="Edit Category", command=self.update_category, state='disabled')
        self.edit_category_button.pack(pady=10)

        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Phrase', 'Category', 'Parent Category'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Phrase', text='Phrase')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Parent Category', text='Parent Category')

        self.tree.column('ID', width=80, stretch=False)
        self.tree.column('Phrase', width=500, stretch=False)
        self.tree.column('Category', width=300, stretch=False)
        self.tree.column('Parent Category', width=300, stretch=False)

        self.tree.bind('<<TreeviewSelect>>', self.on_row_select)
        self.update_identifiers()

        self.tree.pack(fill='y', expand=True, padx=20, pady=10, anchor='center')
    
    def on_row_select(self, event=None):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_row_data = self.tree.item(selected_item)['values']
            if not self.selected_row_data[1].startswith('This is a forced identifier for category:'):
                self.edit_category_button.config(state='normal')
            else:
                self.edit_category_button.config(state='disabled')
    
    def update_identifiers(self):   
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for row in self.identifier_data:
            id = row[0]
            phrase = row[1]
            cat = row[3]
            parent = row[4]
            tree_values = [id, phrase, cat, parent]
            self.tree.insert('', tk.END, values=tree_values)

    def update_category(self):
        new_category_id = self.prompt_to_update_category()
        if new_category_id:
            idens.update_identifier(self.conn, self.cursor, self.selected_row_data[0], new_category_id)
            self.update_identifier_data()
            self.update_transaction_data()

    def prompt_to_update_category(self):
        change_category_popup = ChangeCategoryPopup(self.frame, self.selected_row_data[2], self.category_data, self.selected_row_data[1])
        self.frame.wait_window(change_category_popup.top)
        return change_category_popup.new_category_id