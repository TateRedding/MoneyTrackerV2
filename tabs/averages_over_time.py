import tkinter as tk
from tkinter import ttk

class AveragesOverTime:
    def __init__(self, parent, cursor):
        self.frame = tk.Frame(parent)
        self.cursor = cursor
        self.setup_tab()

    def setup_tab(self):
        self.notebook = ttk.Notebook(self.frame)