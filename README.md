# -Currency-Converter

🚀 Features

✅ Real-time currency conversion using ExchangeRate-API

✅ Supports multiple major currencies 🌍

✅ Clean and responsive GUI with Tkinter 🖥️

✅ Save and view past conversions in an embedded SQLite database 🗃️

✅ Input validation and user-friendly error messages 🚫

✅ Conversion history view in tabular format 📋

✅ One-click clear button and Enter key functionality for quick use ⌨️

🛠️ Project Structure


currency_converter/

├── currency_converter.py     # Main GUI app

├── db_manager.py             # Database handler

├── currency_converter.db     # SQLite database file

└── output.png                # Screenshot of the app

🧠 How It Works


Enter the amount and select source and target currencies.


Click Convert to fetch the latest rate and see the converted value.


Click Show History to view a detailed table of all past conversions.


🧰 Requirements

Python 3.7+requests+tkinter (comes built-in with Python)

Internet connection 🌐 (for fetching live exchange rates)


Install missing dependencies using:


pip install requests

🔑 Setup Instructions

Clone the repo or download the ZIP.


Get your free API key from ExchangeRate API.


Replace the placeholder in currency_converter.py:


python

API_KEY = 'YOUR_API_KEY'  # 🔁 Replace this!

Run the app:

python currency_converter.py

🗃️ Database

SQLite is used to store past conversions.

Each record includes:


Amount


From currency


To currency

Converted amount

Timestamp

📦 Future Enhancements

🔍 Search/filter conversion history


📤 Export history to CSV


🌐 Multi-language support


💬 Dark mode support
