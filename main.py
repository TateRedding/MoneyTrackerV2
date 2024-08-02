import tkinter as tk
from tkinter import ttk
import sqlite3

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Money Tracker v2")

        self.conn = sqlite3.connect('money-tracker-prod.db')
        self.cursor = self.conn.cursor()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        self.create_tabs()

        def on_closing():
            self.conn.close()
            root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_closing)

    def create_tabs(self):
        return

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
