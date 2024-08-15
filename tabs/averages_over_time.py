import tkinter as tk
from tkinter import ttk
import database.categories as cats
import database.transactions as trans
import tabs.monthly_data as monthly
from utils.utility_functions import sort_tree

class AveragesOverTime:
    def __init__(self, parent, cursor, category_data):
        self.frame = tk.Frame(parent)
        self.cursor = cursor
        self.category_data = category_data
        self.month_map = monthly.get_month_map(self.cursor)
        self.selected_start_month = None
        self.selected_end_month = None
        self.parent_categories = []
        
        self.setup_tab()

        self.update_category_data()

    def setup_tab(self):
        selection_frame = tk.Frame(self.frame)
        selection_frame.pack(pady=10)

        tk.Label(selection_frame, text='Select Start Month').grid(row=0, column=0, padx=(0, 10))
        self.start_month_var = tk.StringVar()
        self.start_month_dropdown = monthly.setup_month_dropdown(selection_frame, self.start_month_var, self.month_map, self.on_month_selected)
        self.start_month_dropdown.set(value = '')
        self.start_month_dropdown.grid(row=1, column=0, padx=(0, 10))

        tk.Label(selection_frame, text='Select End Month').grid(row=0, column=1, padx=(10, 0))
        self.end_month_var = tk.StringVar()
        self.end_month_dropdown = monthly.setup_month_dropdown(selection_frame, self.end_month_var, self.month_map, self.on_month_selected)
        self.end_month_dropdown.set(value = '')
        self.end_month_dropdown.grid(row=1, column=1, padx=(10, 0))

        self.tree = ttk.Treeview(self.frame, columns=[], show='headings')
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)
    
    def on_month_selected(self, event=None):
        start_display_month = self.start_month_var.get()
        end_display_month = self.end_month_var.get()
        if start_display_month in self.month_map:
            self.selected_start_month = self.month_map[start_display_month]
        if end_display_month in self.month_map:
            self.selected_end_month = self.month_map[end_display_month]
        if self.selected_start_month and self.selected_end_month:
            data = trans.get_monthly_totals_with_range(self.cursor, self.selected_start_month, self.selected_end_month)
            months = []
            totals = {}
            for month, category, amount in data:
                if month not in totals:
                    totals[month] = {}
                    months.append(month)
                if category not in totals[month]:
                    totals[month][category] = amount
            if months and totals:
                self.update_treeview(months, totals)

    def update_treeview(self, months, totals):
        self.tree.delete(*self.tree.get_children())

        month_strings = [key for key, value in self.month_map.items() if value in months]
        columns = ['Category'] + month_strings + ['Average']
        self.tree['columns'] = columns

        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: sort_tree(self.tree, c, False))
            self.tree.column(col, width=100, anchor=tk.W)

        for category in self.parent_categories:
            category_name = category.title()
            month_values = [f'${totals.get(month, {}).get(category, 0):,.2f}' for month in months]
            grand_total = sum(totals.get(month, {}).get(category, 0) for month in months)
            average = grand_total / len(months) if months else 0
            values = (category_name,) + tuple(month_values) + (f'${average:,.2f}',)
            
            self.tree.insert('', tk.END, text='1', values=values)

    def update_category_data(self):
        self.parent_categories = sorted(['Unknown'] + [row[1] for row in self.category_data if not row[3]])
        self.on_month_selected()

    def update_month_data(self):
        self.month_map = monthly.get_month_map(self.cursor)
        monthly.update_month_dropdown(self.start_month_dropdown, self.month_map)
        monthly.update_month_dropdown(self.end_month_dropdown, self.month_map)
