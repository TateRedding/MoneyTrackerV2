import tkinter as tk
from tkinter import ttk
from datetime import datetime
import database.transactions as trans
from popups.change_category_popup import ChangeCategoryPopup

class AllTransactions:
    def __init__(self, parent, conn, cursor, transaction_data, category_data, update_transaction_data, update_identifier_data):
        self.frame = tk.Frame(parent)
        self.conn = conn
        self.cursor = cursor
        self.transaction_data = transaction_data
        self.category_data = category_data
        self.update_transaction_data = update_transaction_data
        self.update_identifier_data = update_identifier_data

        self.setup_tab()

    def setup_tab(self):
        tk.Label(self.frame, text='All Transactions').pack(pady=10)

        self.edit_category_button = ttk.Button(self.frame, text='Edit Category', command=self.update_category, state='disabled')
        self.edit_category_button.pack(pady=10)

        self.setup_filters()
        self.setup_tree()


    def setup_filters(self):
        filter_frame = tk.Frame(self.frame)
        dropdown_frame = tk.Frame(filter_frame)

        tk.Label(dropdown_frame, text='Parent Category').grid(row=0, column=0, pady=5, padx=5)
        self.parent_category_dropdown = ttk.Combobox(dropdown_frame)
        self.parent_category_dropdown.bind('<<ComboboxSelected>>', self.on_parent_category_select)
        self.parent_category_dropdown.grid(row=1, column=0, pady=5, padx=5)

        ttk.Label(dropdown_frame, text='Child Category').grid(row=0, column=1, pady=5, padx=5)
        self.child_category_dropdown = ttk.Combobox(dropdown_frame)
        self.child_category_dropdown.bind('<<ComboboxSelected>>', self.on_child_category_select)
        self.child_category_dropdown.grid(row=1, column=1, pady=5, padx=5)

        self.filter_button = ttk.Button(dropdown_frame, text='Set Filters', command=self.filter_transactions)
        self.filter_button.grid(row=2, column=0, columnspan=2, pady=5, padx=5)

        self.load_categories()

        dropdown_frame.grid(row=0, column=0)
        filter_frame.columnconfigure(0, weight=1)
        filter_frame.pack(fill='x', pady=10)

    def load_categories(self):
        parent_categories = sorted([row[1] for row in self.category_data if not row[3]])
        self.parent_category_dropdown['values'] = ['All'] + parent_categories

    def on_parent_category_select(self, event=None):
        child_categories = sorted([row[1] for row in self.category_data if row[4] == self.parent_category_dropdown.get()])
        self.child_category_dropdown['values'] = ['All', 'None'] + child_categories
        self.child_category_dropdown.set(value='All')
    
    def on_child_category_select(self, event=None):
        return
    
    def filter_transactions(self, event=None):
        data = self.transaction_data
        parent_category = self.parent_category_dropdown.get()
        if parent_category and not parent_category == 'All':
            data = [transaction for transaction in data if transaction[7] == parent_category or transaction[8] == parent_category]

        child_category = self.child_category_dropdown.get()
        if child_category and not child_category == 'All':
            if child_category == 'None':
                data = [transaction for transaction in data if transaction[8] == 'N/A']
            else:
                data = [transaction for transaction in data if transaction[7] == child_category]

        self.update_transactions(data)
    
    def setup_tree(self):
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Date', 'Amount', 'Category', 'Parent Category', 'Description', 'Account'), show='headings')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Parent Category', text='Parent Category')
        self.tree.heading('Description', text='Description')
        self.tree.heading('Account', text='Account')

        self.tree.column('ID', width=0, stretch=False)
        self.tree.column('Date', width=100, stretch=False)
        self.tree.column('Amount', width=80, stretch=False)
        self.tree.column('Category', width=250, stretch=False)
        self.tree.column('Parent Category', width=250, stretch=False)
        self.tree.column('Description', width=800)
        self.tree.column('Account', width=170, stretch=False)

        self.tree.bind('<<TreeviewSelect>>', self.on_row_select)
        self.update_transactions()

        self.tree.pack(fill='y', expand=True, padx=20, pady=10, anchor='center')

    def on_row_select(self, event=None):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_row_data = self.tree.item(selected_item)['values']
            if not self.selected_row_data[3] == 'Unknown':
                self.edit_category_button.config(state='normal')
            else:
                self.edit_category_button.config(state='disabled')
    
    def update_transactions(self, data=None):
        if not data:
            data = self.transaction_data

        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for row in data:
            id = row[0]
            date = datetime.strptime(row[3], '%Y-%m-%d').strftime('%b %d, %Y')
            amount = f'${row[1]}'
            cat = row[7]
            parent = row[8]
            desc = row[2]
            acc = row[6]
            tree_values = [id, date, amount, cat, parent, desc, acc]
            self.tree.insert('', tk.END, values=tree_values)
    
    def update_category(self):
        new_category_id = self.prompt_to_update_category()
        if new_category_id:
            trans.force_update_category(self.conn, self.cursor, self.selected_row_data[0], new_category_id)
            self.update_transaction_data()
            self.update_identifier_data()

    def prompt_to_update_category(self):
        change_category_popup = ChangeCategoryPopup(self.frame, self.selected_row_data[3], self.category_data)
        self.frame.wait_window(change_category_popup.top)
        return change_category_popup.new_category_id
    
    

