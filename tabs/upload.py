import tkinter as tk
from tkinter import ttk, filedialog
from utils.file_parsers import parse_file
import database.transactions as trans

class Upload:
    def __init__(self, parent, conn, cursor, account_data, update_transactions):
        self.frame = ttk.Frame(parent)
        self.cursor = cursor
        self.conn = conn
        self.account_data = account_data
        self.update_transactions = update_transactions
        self.file_path = tk.StringVar()
        self.new_record_count = tk.IntVar(value=0)
        self.setup_tab()

    def setup_tab(self):
        tk.Label(self.frame, text='Upload Statements').pack(pady=10)
        tk.Label(self.frame, text='Select Account').pack(pady=10)
        
        self.account_var = tk.StringVar()
        self.account_map = {name: id for id, name, type in self.account_data}
        self.account_dropdown = ttk.Combobox(self.frame, textvariable=self.account_var)
        self.account_dropdown['values'] = [account[1] for account in self.account_data]
        self.account_dropdown.bind('<<ComboBoxSelection>>', self.check_inputs)
        self.account_dropdown.pack(pady=10)

        tk.Label(self.frame, text='Choose a file').pack(pady=10)
        tk.Button(self.frame, text='Select File', command=self.select_file).pack(pady=10)
        self.file_name_label = tk.Label(self.frame, text = 'Selected File: None')
        self.file_name_label.pack(pady=10)

        self.upload_button = tk.Button(self.frame, text='Upload', command=self.process_file, state=tk.DISABLED)
        self.upload_button.pack(pady=10)

        self.new_record_label = tk.Label(self.frame, text='Upload a file to add new records')
        self.new_record_label.pack(pady=10)

        self.file_path.trace_add('write', self.check_inputs)

    def check_inputs(self, *args):
        if self.file_path.get() and self.account_var.get():
            self.upload_button.config(state=tk.NORMAL)
        else:
            self.upload_button.config(state=tk.DISABLED)

    def select_file(self):
        file = filedialog.askopenfilename(
            initialdir='~/Documents',
            title='Select CSV File',
            filetypes=(('CSV files', '*.csv'), ('CSV files', '*.CSV'), ('All files', '*.*'))
        )
        if file:
            self.file_path.set(value=file)
            self.file_name_label.config(text=f'Selected file: {file}')
    
    def process_file(self):
        selected_file = self.file_path.get()
        account_name = self.account_var.get()
        account_id = self.account_map[account_name]
        if selected_file and account_id:
            data = parse_file(self.cursor, selected_file, account_id, account_name)
            new_record_count = trans.add_transactions(self.conn, self.cursor, data)
            self.new_record_label.config(text=f'New records added: {new_record_count}')
            self.account_var.set(value='')
            self.file_path.set(value='')
            self.file_name_label.configure(text='Selected file: None')
            self.update_transactions()
        else:
            print('Please select a file and an account.')