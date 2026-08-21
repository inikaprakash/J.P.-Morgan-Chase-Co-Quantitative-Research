import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score


data = pd.read_csv("Nat_Gas.csv")

data["Dates"] = pd.to_datetime(data["Dates"])
data = data.sort_values("Dates").reset_index(drop=True)

print(data.head())

plt.figure(figsize=(10, 5))
plt.plot(data["Dates"], data["Prices"], marker="o")
plt.xlabel("Date")
plt.ylabel("Price")
plt.title("Historical Natural Gas Prices")
plt.grid(True)
plt.show()


x = np.arange(len(data))
y = data["Prices"]


def price_model(x, a, b, c, d):
    return (
        a
        + b * x
        + c * np.sin(2 * np.pi * x / 12)
        + d * np.cos(2 * np.pi * x / 12)
    )


params, covariance = curve_fit(price_model, x, y)

data["Estimated"] = price_model(x, *params)


r2 = r2_score(y, data["Estimated"])
rmse = np.sqrt(np.mean((y - data["Estimated"]) ** 2))

print(f"R² Score: {r2:.4f}")
print(f"RMSE: {rmse:.4f}")

future_x = np.arange(len(data) + 12)

future_dates = pd.date_range(
    start=data["Dates"].iloc[0],
    periods=len(future_x),
    freq="ME"  
)

future_prices = price_model(future_x, *params)

forecast_df = pd.DataFrame({
    "Date": future_dates,
    "Forecast_Price": future_prices
})

print("\nForecasted Prices:")
print(forecast_df.tail(12))


plt.figure(figsize=(12, 6))

plt.plot(
    data["Dates"],
    data["Prices"],
    marker="o",
    label="Actual Prices"
)

plt.plot(
    future_dates,
    future_prices,
    linestyle="--",
    label="Forecast"
)

plt.xlabel("Date")
plt.ylabel("Price")
plt.title("Natural Gas Prices with One-Year Forecast")
plt.legend()
plt.grid(True)
plt.show()


start_date = data["Dates"].iloc[0]


def months_since_start(date):
    """
    Computes fractional months elapsed since the
    beginning of the dataset.
    """
    months = (
        (date.year - start_date.year) * 12
        + (date.month - start_date.month)
    )

    
    months += (date.day - 1) / 30.44

    return months


def estimate_price(date):
    """
    Estimates the natural gas price for any date.

    Parameters:
        date (str or datetime): Date to estimate.

    Returns:
        float: Estimated price.
    """
    date = pd.to_datetime(date)

    if date < data["Dates"].min():
        print("Warning: Date is before the available dataset.")
    elif date > future_dates.max():
        print("Warning: Date exceeds one-year forecast horizon.")

    months = months_since_start(date)

    return round(float(price_model(months, *params)), 2)



print("\nPrice Estimates:")
print("2022-08-15 :", estimate_price("2022-08-15"))
print("2023-12-25 :", estimate_price("2023-12-25"))
print("2025-06-30 :", estimate_price("2025-06-30"))