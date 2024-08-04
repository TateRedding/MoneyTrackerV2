import tkinter as tk
from tkinter import ttk
from datetime import datetime

class AllTransactions:
    def __init__(self, parent, transaction_data):
        self.frame = ttk.Frame(parent)
        self.transaction_data = transaction_data

        self.setup_tab()

    def setup_tab(self):
        tk.Label(self.frame, text='All Transactions').pack(pady=10)

        self.tree = ttk.Treeview(self.frame, columns=('Date', 'Amount', 'Category', 'Parent Category', 'Description', 'Account'), show='headings')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Parent Category', text='Parent Category')
        self.tree.heading('Description', text='Description')
        self.tree.heading('Account', text='Account')

        self.tree.column('Date', width=100, stretch=False)
        self.tree.column('Amount', width=80, stretch=False)
        self.tree.column('Category', width=250, stretch=False)
        self.tree.column('Parent Category', width=250, stretch=False)
        self.tree.column('Description', width=800)
        self.tree.column('Account', width=170, stretch=False)

        self.tree.bind('<<TreeviewSelect>>', self.on_row_select)
        self.update_transactions()

        self.tree.pack(fill=tk.Y, expand=True, padx=20, pady=10, anchor='center')

    def on_row_select(self, event=None):
        return
    
    def update_transactions(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for row in self.transaction_data:
            date = datetime.strptime(row[3], '%Y-%m-%d').strftime('%b %d, %Y')
            amount = f'${row[1]}'
            cat = row[7]
            parent = row[8]
            desc = row[2]
            acc = row[6]
            tree_values = [date, amount, cat, parent, desc, acc]
            self.tree.insert('', tk.END, values=tree_values)