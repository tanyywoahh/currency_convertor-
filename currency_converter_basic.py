# Basic Currency Converter (Static Rates)

rates = {
    "USD": 1,
    "INR": 83.2,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 148.5
}

print("Available Currencies:", ", ".join(rates.keys()))

from_currency = input("From Currency: ").upper()
to_currency = input("To Currency: ").upper()
amount = float(input("Amount: "))

if from_currency in rates and to_currency in rates:
    usd_amount = amount / rates[from_currency]
    converted = usd_amount * rates[to_currency]
    print(f"\n{amount} {from_currency} = {converted:.2f} {to_currency}")
else:
    print("Invalid currency code ❌")
