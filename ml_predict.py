import pandas as pd
from sklearn.linear_model import LinearRegression

data = pd.read_csv("usd_inr.csv")

X = data[["Day"]]
y = data["Rate"]

model = LinearRegression()
model.fit(X, y)

future_day = [[11]]
prediction = model.predict(future_day)

print("Predicted USD → INR for Day 11:", round(prediction[0], 2))
