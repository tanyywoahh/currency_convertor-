from flask import Flask, render_template, request
import requests
import matplotlib.pyplot as plt
import os
from functools import lru_cache
from datetime import datetime

app = Flask(__name__)
API_KEY = "19c111866d374beb922b35e5"  # Fixed: proper quotes

# Ensure static folder exists
os.makedirs("static", exist_ok=True)

@lru_cache(maxsize=100)
def fetch_currency_codes(date_key):
    """Fetch all available currency codes from API"""
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/codes"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("supported_codes", [])
    except:
        # Fallback currencies
        return [
            ("USD", "United States Dollar"),
            ("EUR", "Euro"), 
            ("INR", "Indian Rupee"),
            ("GBP", "British Pound Sterling"),
            ("JPY", "Japanese Yen"),
            ("AUD", "Australian Dollar"),
            ("CAD", "Canadian Dollar"),
            ("CHF", "Swiss Franc"),
            ("CNY", "Chinese Yuan"),
            ("BRL", "Brazilian Real")
        ]

@app.route("/", methods=["GET", "POST"])
def home():
    date_key = datetime.now().strftime("%Y-%m-%d-%H")
    currencies = fetch_currency_codes(date_key)
    
    result = None
    rate = None
    from_cur = "USD"
    to_cur = "INR"
    amount = ""
    
    if request.method == "POST":
        try:
            from_cur = request.form.get("from", "USD")
            to_cur = request.form.get("to", "INR")
            amount = request.form.get("amount", "")
            
            if amount:
                amount_val = float(amount)
                url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_cur}/{to_cur}/{amount_val}"
                response = requests.get(url, timeout=5)
                data = response.json()
                
                if data.get("result") == "success":
                    result = round(data["conversion_result"], 2)
                    rate = round(data["conversion_rate"], 4)
                else:
                    result = "API Error - Try again"
        except:
            result = "Invalid input"
    
    # Pass variables safely to template
    return render_template("index.html", 
                         result=result, 
                         rate=rate,
                         currencies=currencies, 
                         from_cur=from_cur, 
                         to_cur=to_cur,
                         amount=amount)

@app.route("/chart")
def chart():
    base_currency = request.args.get("base", "USD")
    
    try:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data.get("result") == "success":
            rates = data["conversion_rates"]
            currencies = ["INR", "EUR", "GBP", "JPY", "AUD"]
            values = [rates.get(c, 0) for c in currencies]
            
            plt.figure(figsize=(10, 6))
            plt.bar(currencies, values, color='steelblue')
            plt.title(f"{base_currency} Exchange Rates")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig("static/chart.png")
            plt.close()
    except:
        pass
    
    date_key = datetime.now().strftime("%Y-%m-%d-%H")
    currencies = fetch_currency_codes(date_key)
    
    return render_template("chart.html", base=base_currency, currencies=currencies)

if __name__ == "__main__":
    app.run(debug=True)
