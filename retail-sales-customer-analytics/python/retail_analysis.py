"""
Retail Sales & Customer Analytics
Run from the project root:
    python python/retail_analysis.py
Outputs are saved under visuals/ and reports/.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "retail_sales.csv"
VISUALS_DIR = ROOT / "visuals"
REPORTS_DIR = ROOT / "reports"
VISUALS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. Keep data/retail_sales.csv in the project."
        )

    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    print("=" * 65)
    print("RETAIL SALES & CUSTOMER ANALYTICS")
    print("=" * 65)
    print(f"Raw rows: {len(df):,} | Columns: {len(df.columns)}")
    print("\nMissing values before cleaning:")
    print(df.isna().sum()[df.isna().sum() > 0].to_string())

    # Data quality checks and cleaning
    df = df.drop_duplicates(subset=["order_id"]).copy()
    for col in ["city", "payment_method", "customer_segment"]:
        df[col] = df[col].fillna("Unknown")
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df["total_cost"] = pd.to_numeric(df["total_cost"], errors="coerce")
    df["profit"] = df["revenue"] - df["total_cost"]
    df = df.dropna(subset=["order_date", "revenue", "total_cost"])

    # KPIs
    total_revenue = df["revenue"].sum()
    total_profit = df["profit"].sum()
    total_orders = df["order_id"].nunique()
    total_customers = df["customer_id"].nunique()
    units_sold = df["quantity"].sum()
    avg_order_value = total_revenue / total_orders if total_orders else 0
    profit_margin = (total_profit / total_revenue * 100) if total_revenue else 0

    print("\nKEY PERFORMANCE INDICATORS")
    print(f"Total revenue       : ₹{total_revenue:,.2f}")
    print(f"Total profit        : ₹{total_profit:,.2f}")
    print(f"Total orders        : {total_orders:,}")
    print(f"Unique customers    : {total_customers:,}")
    print(f"Units sold          : {units_sold:,}")
    print(f"Average order value : ₹{avg_order_value:,.2f}")
    print(f"Profit margin       : {profit_margin:.2f}%")

    # Grouped analysis
    monthly = (df.assign(month=df["order_date"].dt.to_period("M").astype(str))
                 .groupby("month", as_index=False)
                 .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique")))
    category = (df.groupby("category", as_index=False)
                  .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), units=("quantity", "sum"))
                  .sort_values("revenue", ascending=False))
    product = (df.groupby("product", as_index=False)
                 .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), units=("quantity", "sum"))
                 .sort_values("revenue", ascending=False))
    city = (df.groupby("city", as_index=False)
              .agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
              .sort_values("revenue", ascending=False))
    segment = (df.groupby("customer_segment", as_index=False)
                 .agg(customers=("customer_id", "nunique"), revenue=("revenue", "sum"), profit=("profit", "sum"))
                 .sort_values("revenue", ascending=False))
    payment = (df.groupby("payment_method", as_index=False)
                 .agg(orders=("order_id", "nunique"), revenue=("revenue", "sum"))
                 .sort_values("orders", ascending=False))

    # Save outputs for reproducibility and for the portfolio
    monthly.to_csv(REPORTS_DIR / "monthly_trend.csv", index=False)
    category.to_csv(REPORTS_DIR / "category_performance.csv", index=False)
    product.to_csv(REPORTS_DIR / "product_performance.csv", index=False)
    city.to_csv(REPORTS_DIR / "city_performance.csv", index=False)
    segment.to_csv(REPORTS_DIR / "customer_segment_performance.csv", index=False)
    payment.to_csv(REPORTS_DIR / "payment_method_analysis.csv", index=False)
    df.to_csv(REPORTS_DIR / "retail_sales_cleaned.csv", index=False)

    # Charts
    plt.figure(figsize=(11, 5))
    plt.plot(monthly["month"], monthly["revenue"], marker="o")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue (INR)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / "monthly_revenue_trend.png", dpi=160)
    plt.close()

    plt.figure(figsize=(9, 5))
    plt.bar(category["category"], category["revenue"])
    plt.title("Revenue by Category")
    plt.xlabel("Category")
    plt.ylabel("Revenue (INR)")
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / "revenue_by_category.png", dpi=160)
    plt.close()

    top_products = product.head(10).sort_values("revenue")
    plt.figure(figsize=(9, 5))
    plt.barh(top_products["product"], top_products["revenue"])
    plt.title("Product Revenue Ranking")
    plt.xlabel("Revenue (INR)")
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / "product_revenue_ranking.png", dpi=160)
    plt.close()

    # Evidence-based summary (computed from this dataset)
    best_category = category.iloc[0]
    best_product = product.iloc[0]
    best_city = city.iloc[0]
    summary = f"""# Analysis Summary

- Total revenue: ₹{total_revenue:,.2f}
- Total profit: ₹{total_profit:,.2f}
- Orders: {total_orders:,}
- Unique customers: {total_customers:,}
- Units sold: {units_sold:,}
- Average order value: ₹{avg_order_value:,.2f}
- Profit margin: {profit_margin:.2f}%
- Highest-revenue category: {best_category['category']} (₹{best_category['revenue']:,.2f})
- Highest-revenue product: {best_product['product']} (₹{best_product['revenue']:,.2f})
- Highest-revenue city: {best_city['city']} (₹{best_city['revenue']:,.2f})

Note: This project uses a synthetic practice dataset; results are illustrative and are not real company data.
"""
    (REPORTS_DIR / "analysis_summary.md").write_text(summary, encoding="utf-8")
    print("\nTOP CATEGORIES")
    print(category.to_string(index=False, formatters={"revenue": "₹{:,.2f}".format, "profit": "₹{:,.2f}".format}))
    print("\nTOP PRODUCTS")
    print(product.head(5).to_string(index=False, formatters={"revenue": "₹{:,.2f}".format, "profit": "₹{:,.2f}".format}))
    print("\nSaved charts to visuals/ and analysis tables + summary to reports/")
    print("Done. Review reports/analysis_summary.md before writing resume claims.")

if __name__ == "__main__":
    main()
