import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import requests

# Constants
API_KEY = "fe94a9d8d9f92496f0660552d937a670"
API_URL = "http://data.fixer.io/api/latest"
SUPPORTED_CURRENCIES = ["EGP", "EUR", "KWD", "USD"]
CATEGORIES = ["Life Expenses", "Electricity", "Gas", "Rental", "Grocery", "Savings", "Education", "Charity"]
PAY_METHODS = ["Cash", "Credit Card", "Paypal"]

class ExpenseTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("600x500")
        self.user_data = []
        self.total_expenses = []
        self.total_row_id = None

        self.amo_var = tk.StringVar()
        self.curr_var = tk.StringVar(value="EGP")
        self.cat_var = tk.StringVar(value="Life Expenses")
        self.pay_var = tk.StringVar(value="Cash")

        self.setup_ui()

    def setup_ui(self):
        # Entry Frame
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, columnspan=6, pady=10, padx=10)

        self.add_label_entry(frame, "Amount:", self.amo_var, 0)
        self.add_label_combobox(frame, "Currency:", self.curr_var, SUPPORTED_CURRENCIES, 1)
        self.add_label_combobox(frame, "Category:", self.cat_var, CATEGORIES, 2)
        self.add_label_combobox(frame, "Pay Method:", self.pay_var, PAY_METHODS, 3)

        # Date
        ttk.Label(frame, text="Date:").grid(row=4, column=0, sticky="w", pady=5)
        date_label = ttk.Label(frame, text=datetime.datetime.now().strftime("%d/%m/%Y"))
        date_label.grid(row=4, column=1, pady=5)

        # Submit Button
        submit_btn = ttk.Button(frame, text="Add Expense", command=self.submit_expense)
        submit_btn.grid(row=5, column=1, pady=10)

        # Treeview
        self.tree = ttk.Treeview(self, columns=("Amount", "Currency", "Category", "Payment"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor='center')

        self.tree.grid(row=6, column=0, columnspan=6, pady=10, padx=10)
        self.tree.tag_configure("total", background="#f0f0f0", foreground="blue", font=('Arial', 10, 'bold'))

    def add_label_entry(self, frame, text, var, row):
        ttk.Label(frame, text=text).grid(row=row, column=0, sticky="w", pady=5)
        ttk.Entry(frame, textvariable=var).grid(row=row, column=1, pady=5)

    def add_label_combobox(self, frame, text, var, values, row):
        ttk.Label(frame, text=text).grid(row=row, column=0, sticky="w", pady=5)
        ttk.Combobox(frame, textvariable=var, values=values, state="readonly").grid(row=row, column=1, pady=5)

    def currency_exchange(self):
        user_curr = self.curr_var.get()
        try:
            amount = float(self.amo_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")
            return None

        params = {"access_key": API_KEY, "symbols": f"{user_curr},USD"}
        response = requests.get(API_URL, params=params)
        data = response.json()

        if "rates" not in data or user_curr not in data["rates"]:
            messagebox.showerror("API Error", "Failed to fetch exchange rates.")
            return None

        amount_eur = amount * (1 / data["rates"][user_curr])
        amount_usd = amount_eur * data["rates"]["USD"]
        return round(amount_usd, 2)

    def submit_expense(self):
        converted = self.currency_exchange()
        if converted is None:
            return

        self.total_expenses.append(converted)
        entry = (self.amo_var.get(), self.curr_var.get(), self.cat_var.get(), self.pay_var.get())
        self.user_data.append(entry)
        self.tree.insert("", "end", values=entry)
        self.update_total()

        self.amo_var.set("")

    def update_total(self):
        if self.total_row_id:
            self.tree.delete(self.total_row_id)

        total = round(sum(self.total_expenses), 2)
        self.total_row_id = self.tree.insert("", "end", values=(f"{total} USD", "", "", ""), tags=("total",))

if __name__ == "__main__":
    app = ExpenseTracker()
    app.mainloop()
