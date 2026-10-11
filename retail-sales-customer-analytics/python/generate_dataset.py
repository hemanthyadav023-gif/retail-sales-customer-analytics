"""Regenerate the synthetic retail dataset if needed. Run: python python/generate_dataset.py"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "retail_sales.csv"
OUT.parent.mkdir(exist_ok=True)
np.random.seed(42)
products = [
    ("Laptop", "Electronics", 65000, 52000), ("Smartphone", "Electronics", 28000, 22000),
    ("Headphones", "Electronics", 2500, 1500), ("Monitor", "Electronics", 14000, 10500),
    ("Office Chair", "Furniture", 9000, 6500), ("Desk", "Furniture", 12000, 8500),
    ("Backpack", "Accessories", 2200, 1200), ("Keyboard", "Accessories", 1800, 1000),
    ("Mouse", "Accessories", 900, 450), ("Printer", "Electronics", 15000, 11500),
]
cities = ["Hyderabad", "Warangal", "Bengaluru", "Chennai", "Pune", "Mumbai", "Delhi"]
segments = ["Consumer", "Corporate", "Small Business"]
payments = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash"]
dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
rows = []
for i in range(1, 2501):
    name, cat, price, cost = products[np.random.randint(len(products))]
    qty = int(np.random.choice([1, 1, 1, 2, 2, 3, 4]))
    unit_price = round(price * np.random.uniform(.92, 1.08), 2)
    unit_cost = round(cost * np.random.uniform(.96, 1.04), 2)
    discount = float(np.random.choice([0, .05, .10, .15], p=[.45, .3, .2, .05]))
    revenue = round(qty * unit_price * (1-discount), 2)
    total_cost = round(qty * unit_cost, 2)
    rows.append({
        "order_id": f"ORD{i:05d}", "order_date": pd.Timestamp(np.random.choice(dates)).strftime("%Y-%m-%d"),
        "customer_id": f"CUST{np.random.randint(1,701):04d}", "product": name, "category": cat,
        "city": np.random.choice(cities), "customer_segment": np.random.choice(segments, p=[.55,.25,.20]),
        "quantity": qty, "unit_price": unit_price, "unit_cost": unit_cost, "discount_pct": discount,
        "revenue": revenue, "total_cost": total_cost, "payment_method": np.random.choice(payments)
    })
df = pd.DataFrame(rows)
df["profit"] = (df["revenue"] - df["total_cost"]).round(2)
missing = np.random.choice(df.index, 18, replace=False)
df.loc[missing[:6], "city"] = np.nan
df.loc[missing[6:12], "payment_method"] = np.nan
df.loc[missing[12:], "customer_segment"] = np.nan
df.to_csv(OUT, index=False)
print(f"Saved {len(df):,} rows to {OUT}")
