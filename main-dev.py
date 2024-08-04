import tkinter as tk
from tkinter import ttk
import sqlite3
import database.db_setup as setup
import database.accounts as accs
import database.categories as cats
import database.identifiers as idens
import database.transactions as trans
from tabs.all_categories import AllCategories
from tabs.all_identifiers import AllIdentifiers
from tabs.all_transactions import AllTransactions
from tabs.sql import SQL
from tabs.upload import Upload

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Money Tracker v2')

        self.conn = sqlite3.connect('money-tracker-dev.db')
        self.cursor = self.conn.cursor()

        setup.init_db(self.conn, self.cursor)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.account_data = accs.get_all_accounts(self.cursor)
        self.category_data = cats.get_all_categories(self.cursor)
        self.identifier_data = idens.get_all_identifiers(self.cursor)
        self.transaction_data = trans.get_all_transactions(self.cursor)

        self.create_tabs()

        def on_closing():
            self.conn.close()
            root.destroy()

        self.root.protocol('WM_DELETE_WINDOW', on_closing)

    def create_tabs(self):
        self.all_categories = AllCategories(self.notebook, self.category_data)
        self.all_identidfiers = AllIdentifiers(self.notebook, self.identifier_data)
        self.all_transactions = AllTransactions(self.notebook, self.transaction_data)
        self.sql = SQL(self.notebook, self.conn, self.cursor)
        self.upload = Upload(self.notebook, self.conn, self.cursor, self.account_data, self.update_transactions)

        self.notebook.add(self.all_transactions.frame, text='Transactions')
        self.notebook.add(self.upload.frame, text='Upload')
        self.notebook.add(self.all_categories.frame, text='Categories')
        self.notebook.add(self.all_identidfiers.frame, text='Identifiers')
        self.notebook.add(self.sql.frame, text='SQL')
        return

    def update_catagories(self):
        self.category_data = cats.get_all_categories(self.cursor)
    
    def update_identifiers(self):
        self.identifier_data = idens.get_all_identifiers(self.cursor)

    def update_transactions(self):
        self.transaction_data = trans.get_all_transactions(self.cursor)
        self.all_transactions.transaction_data = self.transaction_data
        self.all_transactions.update_transactions()

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
