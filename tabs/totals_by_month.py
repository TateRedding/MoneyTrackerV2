import tkinter as tk
from tkinter import ttk
import database.transactions as trans
import tabs.monthly_data as monthly

class TotalsByMonth:
    def __init__(self, parent, cursor):
        self.parent = parent
        self.cursor = cursor
        self.month_map = monthly.get_month_map(self.cursor)
        self.selected_month = list(self.month_map.values())[0] if self.month_map else None
        self.parent_category_font = ('TkDefaultFont', 10, 'bold')
        self.setup_tab()

    def setup_tab(self):
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.frame, text='Select Month:').pack(padx=10, pady=5)
        
        self.month_var = tk.StringVar()
        self.month_dropdown = monthly.setup_month_dropdown(self.frame, self.month_var, self.month_map, self.on_month_selected)
        self.month_dropdown.pack(padx=10, pady=5)

        self.treeview_frame = tk.Frame(self.frame)
        self.treeview_frame.pack(fill=tk.BOTH, expand=True)

        self.treeviews = {}

        self.update_monthly_data()

    def update_treeviews(self):
        for widget in self.treeview_frame.winfo_children():
            widget.destroy()

        data = self.get_data()
        types = data.keys()

        for i, type_name in enumerate(types):
            type_label = tk.Label(self.treeview_frame, text=type_name.capitalize(), font=('TkDefaultFont', 16, 'bold'))
            type_label.grid(row=0, column=i, padx=10, pady=5, sticky='ew')

            total_label = tk.Label(self.treeview_frame, text=f"${data[type_name]['total']:,.2f}", font=('TkDefaultFont', 14, 'bold'))
            total_label.grid(row=1, column=i, padx=10, pady=5)

            treeview = ttk.Treeview(self.treeview_frame, columns=('Category', 'Amount'), show='headings')
            treeview.heading('Category', text='Category')
            treeview.heading('Amount', text='Amount')
            treeview.column('Category', width=300, stretch=False)
            treeview.column('Amount', width=150, stretch=False)
            treeview.grid(row=2, column=i, padx=5, pady=5, sticky='ns')
            self.treeview_frame.grid_rowconfigure(2, weight=1)

            self.treeviews[type_name] = treeview

        for col in range(len(types)):
            self.treeview_frame.grid_columnconfigure(col, weight=1)

        for type in types:
            treeview = self.treeviews[type]
            for category in data[type]['categories']:
                category_total = data[type]['categories'][category]['total']
                child_categories = data[type]['categories'][category]['child_categories']
                category_row = treeview.insert('', 'end', values=(category, f'${category_total:,.2f}'))
                treeview.item(category_row, tags=("bold",))
                treeview.tag_configure("bold", font=self.parent_category_font)
                for child_category in child_categories:
                    if len(child_categories) == 1 and child_category == 'Other':
                        continue
                    child_category_total = data[type]['categories'][category]['child_categories'][child_category]
                    treeview.insert('', 'end', values=(f'    {child_category}', f'    ${child_category_total:,.2f}'))

    def get_data(self):
        category_totals = trans.get_totals_by_month(self.cursor, self.selected_month)
        data = {}

        for row in category_totals:
            category, parent_category, type, total_amount = row
            if type not in data:
                data[type] = {'total': 0, 'categories': {}}
            if not parent_category:
                parent_category = category
                category = 'Other'
            if parent_category not in data[type]['categories']:
                data[type]['categories'][parent_category] = {'total': 0, 'child_categories': {}}
            if category not in data[type]['categories'][parent_category]['child_categories']:
                data[type]['categories'][parent_category]['child_categories'][category] = 0
            data[type]['total'] += total_amount
            data[type]['categories'][parent_category]['total'] += total_amount
            data[type]['categories'][parent_category]['child_categories'][category] += total_amount
        return data

    def on_month_selected(self, event):
        display_month = self.month_var.get()
        if display_month in self.month_map:
            self.selected_month = self.month_map[display_month]
            self.update_treeviews()

    def update_monthly_data(self):
        self.month_map = monthly.get_month_map(self.cursor)
        monthly.update_month_dropdown(self.month_dropdown, self.month_map)
        if self.selected_month in self.month_map.values():
            self.update_treeviews()
        else:
            label = tk.Label(self.treeview_frame, text='No transactions available for the selected month.', font=('TkDefaultFont', 16, 'bold'))
            label.grid(row=0, column=0, sticky='ew')
            self.treeview_frame.grid_columnconfigure(0, weight=1)
