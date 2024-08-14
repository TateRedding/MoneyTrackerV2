import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from popups.parent_category_popup import ParentCategoryPopup
import database.categories as cats
import database.identifiers as idens

class IdentifyTransactions:
    def __init__(self, parent, conn, cursor, transaction_data, category_data, update_category_data, update_identifier_data, update_transaction_data):
        self.frame = ttk.Frame(parent)
        self.conn = conn
        self.cursor = cursor
        self.transaction_data = transaction_data
        self.category_data = category_data
        self.update_category_data = update_category_data
        self.update_identifier_data = update_identifier_data
        self.update_transaction_data = update_transaction_data

        self.parent_categories = []
        self.parent_category_map = {}
        self.child_category_map = {}

        self.setup_tab()

    def setup_tab(self):
        tk.Label(self.frame, text='Unknown Transactions').pack(pady=10)

        self.remaining_label = tk.Label(self.frame, text='Remaining: N/A')
        self.remaining_label.pack(pady=10)

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
        self.tree.pack(fill='y', expand=True, padx=20, pady=10, anchor='center')

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
            self.child_category_map = {category[1]: category[0] for category in self.category_data if category[4] == selected_parent_category}
            child_categories = sorted(list(self.child_category_map.keys()))
            self.child_category_dropdown['values'] = ['None'] + child_categories
            self.child_category_var.set(value='None')
        self.check_inputs()
    
    def update_unidentified_transactions(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        count = 0
        for row in self.transaction_data:
            if row[7] == 'Unknown':
                count += 1
                date = datetime.strptime(row[3], '%Y-%m-%d').strftime('%b %d, %Y')
                amount = f'${row[1]}'
                desc = row[2]
                acc = row[6]
                tree_values = [date, amount, desc, acc]
                self.tree.insert('', tk.END, values=tree_values)

        self.remaining_label.config(text=f'Remaining: {count}')

    def update_parent_categories(self):
        if self.category_data:
            self.parent_category_map = {category[1]: category[0] for category in self.category_data if not category[3]}
            self.parent_categories = sorted(list(self.parent_category_map.keys()))
            self.parent_category_dropdown['values'] = self.parent_categories

    def check_inputs(self, *args):
        if self.identify_text.get() and self.parent_category_var.get():
            self.submit_button.config(state=tk.NORMAL)
        else:
            self.submit_button.config(state=tk.DISABLED)

    def add_parent_category(self):
        name, type = self.prompt_for_new_parent_category()
        if name:
            if not bool(cats.get_category_by_name(self.cursor, name)):
                cats.add_category(self.conn, self.cursor, name, None, type)
                self.update_category_data()
                self.parent_category_var.set(value=name)
                self.on_parent_category_selected()
            else:
                messagebox.showinfo('Info', f"The category '{name}' already exists.")
    
    def prompt_for_new_parent_category(self):
        new_parent_category_popup = ParentCategoryPopup(self.frame, self.cursor, self.category_data)
        self.frame.wait_window(new_parent_category_popup.top)
        return new_parent_category_popup.name, new_parent_category_popup.type
    
    def add_child_category(self):
        name = self.prompt_for_new_child_category()
        if name:
            parent_category_name = self.parent_category_var.get()
            if parent_category_name:
                parent_id = self.parent_category_map[parent_category_name]
                if parent_id:
                    if not bool(cats.get_category_by_name(self.cursor, name)):
                        cats.add_category(self.conn, self.cursor, name, parent_id, None)
                        self.update_category_data()
                        self.on_parent_category_selected()
                        self.child_category_var.set(name)
                    else:
                        messagebox.showinfo('Info', f"The category '{name}' already exists.")
                else:
                    messagebox.showinfo('Info', 'The selected parent category was not found. This may be a bug.')
            else:
                messagebox.showinfo('Info', 'No parent category is selected.')
    
    def prompt_for_new_child_category(self):
        new_child_category = simpledialog.askstring('New Child Category', 'Enter the new child category name:')
        return new_child_category
    
    def submit(self):        
        description = self.description_text.cget('text')
        phrase = self.identify_text.get()
        parent_category_name = self.parent_category_var.get()
        child_category_name = self.child_category_var.get()

        if phrase not in description:
            messagebox.showerror('Error', 'The entered text does not appear in the description. This is case sensitive.')
            return
        
        category_id = 0
        if child_category_name and not child_category_name == 'None':
            category_id = self.child_category_map[child_category_name]
        elif parent_category_name:
            category_id = self.parent_category_map[parent_category_name]
        else:
            messagebox.showinfo('Info', 'No category was found. This may be a bug.')

        if phrase and category_id:
            if not bool(idens.get_identifier_by_phrase(self.cursor, phrase)):
                idens.add_identifier(self.conn, self.cursor, phrase, category_id)
                self.update_transaction_data()
                messagebox.showinfo('Success', f"Identifier '{phrase}' added for the category {child_category_name if child_category_name and not child_category_name == 'None' else parent_category_name}.")
                self.reset_form()
                self.update_identifier_data()
                self.update_transaction_data()
            else:
                messagebox.showinfo('Info', f"Identifier '{phrase}' already exists.")
        else:
            messagebox.showinfo('Info', 'Please provide an identifier phrase and a category.')
    
    def reset_form(self):
        self.description_text.config(text='')
        self.identify_text.set(value='')
        self.parent_category_var.set(value='')
        self.child_category_var.set(value='')
        self.submit_button.config(state='disabled')
