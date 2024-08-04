import tkinter as tk
import database.categories as cats

class ParentCategoryPopup:
    def __init__(self, parent, cursor, category_data, current_category_id=None):
        self.top = tk.Toplevel(parent)
        self.top.title('Add or Edit Parent Category')

        all_types = sorted(set([category[2] for category in category_data if category[2]]))
        self.name = None
        self.type = None

        tk.Label(self.top, text='Name:').pack(padx=10, pady=10)
        
        self.name_var = tk.StringVar()
        self.type_var = tk.StringVar()

        if current_category_id:
            category = cats.get_category_by_id(cursor, current_category_id)
            if category:
                self.name_var.set(value=category[1])
                self.type_var.set(value=category[2])

        self.name_var.trace_add('write', self.validate)
        self.type_var.trace_add('write', self.validate)
        
        tk.Entry(self.top, textvariable=self.name_var).pack(padx=10, pady=10)

        self.type_frame = tk.Frame(self.top)
        self.type_frame.pack(padx=10, pady=10)
        
        tk.Label(self.type_frame, text='Select category type:').pack(anchor='w')
        for type in all_types:
            tk.Radiobutton(self.type_frame, text=type.capitalize(), variable=self.type_var, value=type).pack(anchor='w')

        self.ok_button = tk.Button(self.top, text='OK', command=self.on_ok)
        self.ok_button.pack(pady=10)

        self.validate()

    def validate(self, *args):
        name = self.name_var.get()
        type = self.type_var.get()
        if name and type:
            self.ok_button.config(state=tk.NORMAL)
        else:
            self.ok_button.config(state=tk.DISABLED)

    def on_ok(self):
        self.name = self.name_var.get()
        self.type = self.type_var.get()
        self.top.destroy()
