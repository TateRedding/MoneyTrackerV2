import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import database.categories as cats
from popups.parent_category_popup import ParentCategoryPopup

class IdentifyTransactions:
    def __init__(self, parent, conn, cursor, transaction_data, category_data, update_categories):
        self.frame = ttk.Frame(parent)
        self.conn = conn
        self.cursor = cursor
        self.transaction_data = transaction_data
        self.category_data = category_data
        self.update_categories = update_categories

        self.parent_categories = []

        self.setup_tab()

    def setup_tab(self):
        tk.Label(self.frame, text='Unknown Transactions').pack(pady=10)

        self.tree = ttk.Treeview(self.frame, columns=('Date', 'Amount', 'Description', 'Account'), show='headings')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Description', text='Description')
        self.tree.heading('Account', text='Account')

        self.tree.column('Date', width=100, stretch=False)
        self.tree.column('Amount', width=80, stretch=False)
        self.tree.column('Description', width=800)
        self.tree.column('Account', width=170, stretch=False)

        self.tree.bind('<<TreeviewSelect>>', self.on_row_select)
        self.tree.pack(fill=tk.Y, expand=True, padx=20, pady=10, anchor='center')

        self.update_unidentified_transactions()

        tk.Label(self.frame, text='Description:').pack(pady=10)
        self.description_text = tk.Label(self.frame, text='', wraplength=600, justify='left')
        self.description_text.pack(pady=10)

        tk.Label(self.frame, text='What phrase can be used to identify this transaction?').pack(pady=10)
        self.identify_text = tk.StringVar()
        self.identify_entry = tk.Entry(self.frame, textvariable=self.identify_text)
        self.identify_entry.pack(pady=10)
        self.identify_text.trace_add('write', self.check_inputs)

        category_frame = tk.Frame(self.frame)
        category_frame.pack()

        tk.Label(category_frame, text='Select a parent category:').grid(row=0, column=0, padx=(0, 10))
        self.parent_category_var = tk.StringVar()
        self.parent_category_dropdown = ttk.Combobox(category_frame, textvariable=self.parent_category_var)
        self.parent_category_dropdown.grid(row=1, column=0, padx=(0, 10), pady=10)
        self.parent_category_dropdown.bind('<<ComboboxSelected>>', self.on_parent_category_selected)

        self.update_parent_categories()

        self.add_parent_category_button = tk.Button(category_frame, text='Add new parent category', command=self.add_parent_category)
        self.add_parent_category_button.grid(row=0, column=1, rowspan=2, padx=(10, 0), pady=10)

        tk.Label(category_frame, text='Select a child category (optional):').grid(row=2, column=0, padx=(0, 10))
        self.child_category_var = tk.StringVar()
        self.child_category_dropdown = ttk.Combobox(category_frame, textvariable=self.child_category_var)
        self.child_category_dropdown.grid(row=3, column=0, padx=(0, 10), pady=10)
        self.child_category_dropdown['values'] = []

        self.add_child_category_button = tk.Button(category_frame, text='Select parent category', command=self.add_child_category, state=tk.DISABLED)
        self.add_child_category_button.grid(row=2, column=1, rowspan=2, padx=(10, 0))

        self.submit_button = tk.Button(self.frame, text='Submit', command=self.submit, state='disabled')
        self.submit_button.pack(pady=10)

    def on_row_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            description = item['values'][2]
            self.description_text.config(text=description)

    def on_parent_category_selected(self, event=None):
        selected_parent_category = self.parent_category_var.get()
        if selected_parent_category:
            self.add_child_category_button.config(text=f'Add child category for {selected_parent_category}', state=tk.NORMAL)
            child_categories = [category[1] for category in self.category_data if category[4] == selected_parent_category]
            child_categories.sort()
            self.child_category_dropdown['values'] = child_categories
        self.check_inputs()
    
    def update_unidentified_transactions(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for row in self.transaction_data:
            if row[7] == 'Unknown':
                date = datetime.strptime(row[3], '%Y-%m-%d').strftime('%b %d, %Y')
                amount = f'${row[1]}'
                desc = row[2]
                acc = row[6]
                tree_values = [date, amount, desc, acc]
                self.tree.insert('', tk.END, values=tree_values)

    def update_parent_categories(self):
        if self.category_data:
            self.parent_categories = [category[1] for category in self.category_data if not category[3]]
            self.parent_categories.sort()
            self.parent_category_dropdown['values'] = self.parent_categories

    def check_inputs(self, *args):
        if self.identify_text.get() and self.parent_category_var.get():
            self.submit_button.config(state=tk.NORMAL)
        else:
            self.submit_button.config(state=tk.DISABLED)

    def add_parent_category(self):
        name, type = self.prompt_for_new_category()
        if name:
            if not bool(cats.get_category_by_name(self.cursor, name)):
                cats.add_category(self.conn, self.cursor, name, None, type)
                self.update_categories()
                self.parent_category_var.set(value=name)
                self.on_parent_category_selected()
            else:
                messagebox.showinfo("Info", f"The category '{name}' already exists.")
    
    def prompt_for_new_category(self):
        new_parent_category_popup = ParentCategoryPopup(self.frame, self.cursor, self.category_data)
        self.frame.wait_window(new_parent_category_popup.top)
        return new_parent_category_popup.name, new_parent_category_popup.type
    
    def add_child_category(self):
        return
    
    def submit(self):
        return
    
    def reset_form(self):
        self.description_text.config(text='')
        self.identify_text.set(value='')
        self.parent_category_var.set(value='')
        self.child_category_var.set(value='')
        self.submit_button.config(state='disabled')
