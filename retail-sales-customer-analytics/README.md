# Retail Sales & Customer Analytics

An end-to-end portfolio project exploring retail transaction data with Python and MySQL. The dataset is **synthetic and created for practice**; it is not from a real company.

## Business questions
- What are total revenue, profit, units sold, orders, and average order value?
- How do revenue and profit change month by month?
- Which categories, products, and cities contribute the most revenue?
- How do customer segments and payment methods compare?
- How do observed metrics differ by discount level?

## Tech stack
Python, pandas, NumPy, Matplotlib, MySQL 8+, MySQL Workbench.

## Repository structure
```text
retail-sales-customer-analytics/
├── data/
│   └── retail_sales.csv
├── python/
│   ├── generate_dataset.py
│   └── retail_analysis.py
├── sql/
│   └── analysis_queries.sql
├── visuals/                 # generated charts are saved here
├── reports/                 # generated CSV tables and summary are saved here
├── requirements.txt
└── README.md
```

## Run locally (Windows / VS Code)
1. Install Python 3.10+ and the VS Code Python extension.
2. Open this folder in VS Code (`File → Open Folder`).
3. In VS Code Terminal, run:
   ```bash
   python -m pip install -r requirements.txt
   python python/retail_analysis.py
   ```
4. Check `visuals/` for charts and `reports/` for the cleaned data, analysis tables, and generated summary.

To regenerate the dataset:
```bash
python python/generate_dataset.py
```
This overwrites `data/retail_sales.csv` with a reproducible synthetic dataset.

## MySQL setup
1. Open `sql/analysis_queries.sql` in MySQL Workbench and execute the database/table creation statements.
2. Use **Table Data Import Wizard** on `retail_sales`, selecting `data/retail_sales.csv`.
3. Confirm the imported row count and date/decimal column types.
4. Run the analysis queries in the SQL file. If import maps columns incorrectly, stop and correct the mapping before running queries.

## Notes
- Revenue = quantity × unit price × (1 − discount).
- Profit = revenue − total cost.
- Average order value is total revenue divided by distinct order count.
- The dataset contains a small number of missing categorical values so the cleaning workflow can demonstrate handling missing data.
- Review generated output before writing quantitative claims on a resume. Do not describe synthetic data as real business data.

## Possible improvements
- Add repeat-customer / RFM analysis.
- Add automated data-quality tests.
- Build a Power BI dashboard from the cleaned data and SQL outputs.
