import pandas as pd
import numpy as np

np.random.seed(42)

n = 500

data = {
    "date": pd.date_range(start="2023-01-01", periods=n, freq="D"),
    "region": np.random.choice(["Europe", "Asia", "North America"], n),
    "product": np.random.choice(["Laptop", "Phone", "Tablet"], n),
    "units_sold": np.random.randint(1, 10, n),
    "price_per_unit": np.random.randint(200, 1500, n)
}

df = pd.DataFrame(data)
df["revenue"] = df["units_sold"] * df["price_per_unit"]

df.to_csv("sales_data.csv", index=False)

print("Dataset created successfully!")