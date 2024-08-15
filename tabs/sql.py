import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from utils.utility_functions import sort_tree

class SQL:
    def __init__(self, parent, conn, cursor):
        self.frame = ttk.Frame(parent)
        self.cursor = cursor
        self.conn = conn
        self.setup_tab()

    def setup_tab(self):
        tk.Label(self.frame, text='SQL').pack(pady=10)
        
        self.textbox = tk.Text(self.frame, wrap='word', height=5, width=70)
        self.textbox.pack(padx=10, pady=10)

        self.execute_button = ttk.Button(self.frame, text='Execute Query', command=self.execute_query)
        self.execute_button.pack(pady=10)
        
        self.tree = ttk.Treeview(self.frame, columns=[], show='headings')
        self.tree.pack(padx=20, pady=10, fill='both', expand=True)

    def execute_query(self):
        query = self.textbox.get('1.0', tk.END).strip()
        if not query:
            messagebox.showwarning('Input Error', 'Please enter an SQL query.')
            return
        try:
            self.cursor.execute(query)
            self.conn.commit()

            if query.lower().startswith('select'):
                rows = self.cursor.fetchall()
                self.display_results(rows)
            else:
                messagebox.showinfo('Success', 'Query executed successfully.')
                self.tree.delete(*self.tree.get_children())
                self.tree['columns'] = []
        
        except sqlite3.Error as e:
            messagebox.showerror('SQL Error', f'An error occurred: {e}')
            self.tree.delete(*self.tree.get_children())
            self.tree['columns'] = []

    def display_results(self, rows):
        self.tree.delete(*self.tree.get_children())

        self.tree['columns'] = [desc[0] for desc in self.cursor.description]
        for col in self.tree['columns']:
            self.tree.heading(col, text=col.upper(), command=lambda c=col: sort_tree(self.tree, c, False))
            self.tree.column(col, width=100, anchor='center')

        for row in rows:
            self.tree.insert('', tk.END, values=row)
