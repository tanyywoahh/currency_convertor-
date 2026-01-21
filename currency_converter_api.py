import requests

API_KEY = "YOUR_API_KEY_HERE"   # get from exchangerate-api.com
url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

response = requests.get(url)
data = response.json()

rates = data["conversion_rates"]

print("Available Currencies:", ", ".join(list(rates.keys())[:15]), "...")

from_currency = input("From Currency: ").upper()
to_currency = input("To Currency: ").upper()
amount = float(input("Amount: "))

if from_currency in rates and to_currency in rates:
    converted = amount / rates[from_currency] * rates[to_currency]
    print(f"\n{amount} {from_currency} = {converted:.2f} {to_currency}")
else:
    print("Invalid currency code ❌")
