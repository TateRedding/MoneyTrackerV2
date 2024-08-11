import tkinter as tk
from tkinter import ttk
import database.categories as cats
from popups.parent_category_popup import ParentCategoryPopup

class AllCategories:
    def __init__(self, parent, conn, cursor, category_data, update_category_data, update_identifier_data, update_transaction_data):
        self.frame = ttk.Frame(parent)
        self.conn = conn
        self.cursor = cursor
        self.category_data = category_data
        self.update_category_data = update_category_data
        self.update_identifier_data = update_identifier_data
        self.update_transaction_data = update_transaction_data

        self.setup_tab()

    def setup_tab(self):
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        tk.Label(self.frame, text='Child Categories').grid(row=0, column=0, pady=10)
        self.edit_child_category_button = ttk.Button(self.frame, text="Edit Child Category", command=self.update_child_category, state='disabled')
        self.edit_child_category_button.grid(row=1, column=0, pady=10)

        self.child_tree = ttk.Treeview(self.frame, columns=('ID', 'Category', 'Parent Category'), show='headings')
        self.child_tree.heading('ID', text='ID')
        self.child_tree.heading('Category', text='Category')
        self.child_tree.heading('Parent Category', text='Parent Category')

        self.child_tree.column('ID', width=80, stretch=False)
        self.child_tree.column('Category', width=300, stretch=False)
        self.child_tree.column('Parent Category', width=300, stretch=False)

        self.child_tree.grid(row=2, column=0, sticky='ns')

        self.child_tree.bind('<<TreeviewSelect>>', self.on_child_category_row_select)

        tk.Label(self.frame, text='Parent Categories').grid(row=0, column=1, pady=10)

        self.edit_parent_category_button = ttk.Button(self.frame, text="Edit Parent Category", command=self.update_parent_category, state='disabled')
        self.edit_parent_category_button.grid(row=1, column=1, pady=10)

        self.parent_tree = ttk.Treeview(self.frame, columns=('ID', 'Category', 'Type'), show='headings')
        self.parent_tree.heading('ID', text='ID')
        self.parent_tree.heading('Category', text='Category')
        self.parent_tree.heading('Type', text='Type')

        self.parent_tree.column('ID', width=80, stretch=False)
        self.parent_tree.column('Category', width=300, stretch=False)
        self.parent_tree.column('Type', width=200, stretch=False)

        self.parent_tree.grid(row=2, column=1, sticky='ns')

        self.parent_tree.bind('<<TreeviewSelect>>', self.on_parent_row_select)

        self.update_categories()

        self.frame.pack(fill=tk.BOTH, expand=True)

    def on_child_category_row_select(self, event=None):
        selected_item = self.child_tree.selection()
        if selected_item:
            self.selected_child_row_data = self.child_tree.item(selected_item)['values']
            self.edit_child_category_button.config(state='normal')
    
    def update_child_category(self, event=None):
        return
    
    def on_parent_row_select(self, event=None):
        selected_item = self.parent_tree.selection()
        if selected_item:
            self.selected_parent_row_data = self.parent_tree.item(selected_item)['values']
            self.edit_parent_category_button.config(state='normal')
    
    def update_parent_category(self, event=None):
        name, type = self.prompt_to_change_parent_category()
        if not (name == self.selected_parent_row_data[1] and type == self.selected_parent_row_data[2]):
            cats.update_category(self.conn, self.cursor, self.selected_parent_row_data[0], name, None, type)
            self.update_data()

    def prompt_to_change_parent_category(self):
        edit_parent_category_popup = ParentCategoryPopup(self.frame, self.cursor, self.category_data, self.selected_parent_row_data[0])
        self.frame.wait_window(edit_parent_category_popup.top)
        return edit_parent_category_popup.name, edit_parent_category_popup.type

    def update_data(self):
        self.update_category_data()
        self.update_identifier_data()
        self.update_transaction_data()
    
    def update_categories(self):        
        for item in self.child_tree.get_children():
            self.child_tree.delete(item)

        for item in self.parent_tree.get_children():
            self.parent_tree.delete(item)
        
        for row in self.category_data:
            id = row[0]
            name = row[1]
            type = row[2]
            parent = row[4]
            
            if not type and parent:
                child_tree_values = [id, name, parent]
                self.child_tree.insert('', tk.END, values=child_tree_values)
            else:
                parent_tree_values = [id, name, type]
                self.parent_tree.insert('', tk.END, values=parent_tree_values)
