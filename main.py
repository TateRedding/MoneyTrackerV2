import tkinter as tk
from tkinter import ttk
import sqlite3
import database.accounts as accs
import database.categories as cats
import database.identifiers as idens
import database.transactions as trans
from tabs.all_categories import AllCategories
from tabs.all_identifiers import AllIdentifiers
from tabs.all_transactions import AllTransactions
from tabs.identify_transactions import IdentifyTransactions
from tabs.monthly_data import MonthlyData
from tabs.sql import SQL
from tabs.upload import Upload
# from updates.v1 import update_v1

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Money Tracker')

        self.conn = sqlite3.connect('money-tracker-prod.db')
        self.cursor = self.conn.cursor()

        self.update_database(self.conn, self.cursor)

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
        self.all_categories = AllCategories(self.notebook, self.conn, self.cursor, self.category_data, self.update_category_data, self.update_identifier_data, self.update_transaction_data)
        self.all_identifiers = AllIdentifiers(self.notebook, self.conn, self.cursor, self.identifier_data, self.category_data, self.update_identifier_data, self.update_transaction_data)
        self.all_transactions = AllTransactions(self.notebook, self.conn, self.cursor, self.transaction_data, self.category_data, self.update_transaction_data, self.update_identifier_data)
        self.identify_transactions = IdentifyTransactions(self.notebook, self.conn, self.cursor, self.transaction_data, self.category_data, self.update_category_data, self.update_identifier_data, self.update_transaction_data)
        self.monthly_data = MonthlyData(self.notebook, self.cursor, self.category_data)
        self.sql = SQL(self.notebook, self.conn, self.cursor)
        self.upload = Upload(self.notebook, self.conn, self.cursor, self.account_data, self.update_transaction_data)

        self.notebook.add(self.all_transactions.frame, text='Transactions')
        self.notebook.add(self.upload.frame, text='Upload')
        self.notebook.add(self.identify_transactions.frame, text='Identify Transactions')
        self.notebook.add(self.monthly_data.frame, text='Monthly Data')
        self.notebook.add(self.all_categories.frame, text='Categories')
        self.notebook.add(self.all_identifiers.frame, text='Identifiers')
        self.notebook.add(self.sql.frame, text='SQL')
        return

    def update_category_data(self):
        self.category_data = cats.get_all_categories(self.cursor)
        self.all_categories.category_data = self.category_data
        self.all_identifiers.category_data = self.category_data
        self.all_transactions.category_data = self.category_data
        self.identify_transactions.category_data = self.category_data
        self.monthly_data.category_data = self.category_data

        self.all_categories.update_categories()
        self.all_transactions.load_categories()
        self.identify_transactions.update_parent_categories()
        self.monthly_data.update_category_data()
    
    def update_identifier_data(self):
        self.identifier_data = idens.get_all_identifiers(self.cursor)
        self.all_identifiers.identifier_data = self.identifier_data

        self.all_identifiers.update_identifiers()

    def update_transaction_data(self):
        self.transaction_data = trans.get_all_transactions(self.cursor)
        self.all_transactions.transaction_data = self.transaction_data
        self.identify_transactions.transaction_data = self.transaction_data

        self.all_transactions.update_transactions()
        self.all_transactions.update_month_data()
        self.identify_transactions.update_unidentified_transactions()
        self.monthly_data.totals.update_month_data()
        self.monthly_data.averages.update_month_data()

    def update_database(self, conn, cursor):
        # update_v1(conn, cursor)
        return

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
