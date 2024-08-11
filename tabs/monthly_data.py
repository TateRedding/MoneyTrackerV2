import tkinter as tk
from tkinter import ttk
from datetime import datetime
import database.transactions as trans
from tabs.averages_over_time import AveragesOverTime
from tabs.totals_by_month import TotalsByMonth

class MonthlyData:
    def __init__(self, parent, cursor):
        self.frame = tk.Frame(parent)
        self.cursor = cursor
        self.setup_tab()

    def setup_tab(self):
        self.notebook = ttk.Notebook(self.frame)
        self.totals = TotalsByMonth(self.notebook, self.cursor)
        self.averages = AveragesOverTime(self.notebook, self.cursor)
        
        self.notebook.add(self.totals.frame, text="Totals by Month")
        self.notebook.add(self.averages.frame, text="Averages Over Time")
        self.notebook.pack(expand=1, fill='both')

def get_month_map(cursor):
    month_map = {}
    months = trans.get_month_range(cursor)
    for month_str in months:
        month_name = datetime.strptime(month_str, '%Y-%m').strftime('%B %Y')
        month_map[month_name] = month_str
    return month_map

def setup_month_dropdown(frame, month_var, month_map, on_month_selected):
    month_dropdown = ttk.Combobox(frame, textvariable=month_var)
    update_month_dropdown(month_dropdown, month_map)
    month_dropdown.bind("<<ComboboxSelected>>", on_month_selected)
    month_dropdown.pack(padx=10, pady=5)
    return month_dropdown

def update_month_dropdown(menu, month_map):
    month_names = list(month_map.keys())
    menu['values'] = month_names
    if month_names:
        menu.set(month_names[0])
