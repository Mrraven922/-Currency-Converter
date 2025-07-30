import tkinter as tk
from tkinter import ttk, messagebox
import requests
from db_manager import DBManager

API_KEY = '63599010b98ca1197d03b67a'
  # Replace this with your actual API key!
if API_KEY == 'YOUR_API_KEY':
    messagebox.showwarning("API Key Missing", "Please replace 'YOUR_API_KEY' with your real API key in currency_converter.py")

API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"
CODES_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/codes"

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter with History")
        self.root.geometry("480x350")
        self.root.resizable(False, False)

        self.db = DBManager()

        self.currencies = self.get_supported_currencies()

        self.setup_ui()

    def get_supported_currencies(self):
        try:
            response = requests.get(CODES_URL)
            response.raise_for_status()
            data = response.json()
            if data['result'] == 'success':
                return [code for code, name in data['supported_codes']]
            else:
                raise Exception("Failed to get codes")
        except Exception:
            # fallback static list
            return ["USD", "EUR", "GBP", "INR", "AUD", "CAD", "JPY", "CNY"]

    def setup_ui(self):
        self.from_currency_var = tk.StringVar(value="USD")
        self.to_currency_var = tk.StringVar(value="INR")
        self.result_var = tk.StringVar()

        ttk.Label(self.root, text="Amount:").grid(row=0, column=0, padx=15, pady=8, sticky="w")
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1, padx=15, pady=8)

        ttk.Label(self.root, text="From Currency:").grid(row=1, column=0, padx=15, pady=8, sticky="w")
        self.from_dropdown = ttk.Combobox(self.root, textvariable=self.from_currency_var, values=self.currencies, state="readonly")
        self.from_dropdown.grid(row=1, column=1, padx=15, pady=8)

        ttk.Label(self.root, text="To Currency:").grid(row=2, column=0, padx=15, pady=8, sticky="w")
        self.to_dropdown = ttk.Combobox(self.root, textvariable=self.to_currency_var, values=self.currencies, state="readonly")
        self.to_dropdown.grid(row=2, column=1, padx=15, pady=8)

        convert_btn = ttk.Button(self.root, text="Convert", command=self.convert_currency)
        convert_btn.grid(row=3, column=0, padx=15, pady=15, sticky="ew")

        clear_btn = ttk.Button(self.root, text="Clear", command=self.clear_fields)
        clear_btn.grid(row=3, column=1, padx=15, pady=15, sticky="ew")

        history_btn = ttk.Button(self.root, text="Show History", command=self.show_history)
        history_btn.grid(row=4, column=0, columnspan=2, padx=15, pady=5, sticky="ew")

        self.result_label = ttk.Label(self.root, textvariable=self.result_var, font=("Arial", 14), foreground="blue", anchor="center", justify="center")
        self.result_label.grid(row=5, column=0, columnspan=2, padx=15, pady=10)

        self.root.bind('<Return>', lambda event: self.convert_currency())

    def convert_currency(self):
        try:
            from_curr = self.from_currency_var.get()
            to_curr = self.to_currency_var.get()
            amount_str = self.amount_entry.get().strip()

            if not amount_str:
                messagebox.showwarning("Input Error", "Please enter the amount.")
                return

            amount = float(amount_str)
            if amount <= 0:
                messagebox.showwarning("Input Error", "Please enter a positive amount.")
                return

            response = requests.get(API_URL + from_curr)
            response.raise_for_status()
            data = response.json()

            if data['result'] == 'success':
                rate = data['conversion_rates'].get(to_curr)
                if rate is None:
                    messagebox.showerror("Error", f"Currency {to_curr} not found.")
                    return

                converted_amount = amount * rate
                last_update = data.get('time_last_update_utc', '')

                result_text = f"{amount:.2f} {from_curr} = {converted_amount:.2f} {to_curr}"
                if last_update:
                    result_text += f"\nRates last updated: {last_update}"

                self.result_var.set(result_text)

                self.db.save_conversion(amount, from_curr, to_curr, converted_amount)
            else:
                messagebox.showerror("API Error", "Failed to fetch exchange rates.")
        except ValueError:
            messagebox.showerror("Input Error", "Invalid amount. Please enter a number.")
        except requests.exceptions.RequestException:
            messagebox.showerror("Network Error", "Could not connect to exchange rate service.")

    def clear_fields(self):
        self.amount_entry.delete(0, tk.END)
        self.result_var.set("")

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Conversion History")
        history_window.geometry("650x350")

        columns = ("Amount", "From", "To", "Converted", "Timestamp")
        tree = ttk.Treeview(history_window, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        tree.pack(fill=tk.BOTH, expand=True)

        records = self.db.fetch_all_conversions()
        for rec in records:
            tree.insert('', tk.END, values=rec[1:])

    def on_close(self):
        self.db.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
