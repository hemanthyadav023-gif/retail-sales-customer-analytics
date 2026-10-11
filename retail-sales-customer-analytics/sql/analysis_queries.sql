-- Retail Sales & Customer Analytics (MySQL 8+)
CREATE DATABASE IF NOT EXISTS retail_analytics;
USE retail_analytics;

-- Create this table before importing data/retail_sales.csv using MySQL Workbench's
-- Table Data Import Wizard. Keep column order consistent with the CSV.
CREATE TABLE IF NOT EXISTS retail_sales (
    order_id VARCHAR(20) PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id VARCHAR(20),
    product VARCHAR(50),
    category VARCHAR(50),
    city VARCHAR(50),
    customer_segment VARCHAR(50),
    quantity INT,
    unit_price DECIMAL(12,2),
    unit_cost DECIMAL(12,2),
    discount_pct DECIMAL(5,2),
    revenue DECIMAL(14,2),
    total_cost DECIMAL(14,2),
    payment_method VARCHAR(30),
    profit DECIMAL(14,2)
);

-- 1. Overall KPIs
SELECT ROUND(SUM(revenue),2) AS total_revenue,
       ROUND(SUM(profit),2) AS total_profit,
       SUM(quantity) AS units_sold,
       COUNT(DISTINCT order_id) AS total_orders,
       COUNT(DISTINCT customer_id) AS unique_customers,
       ROUND(AVG(revenue),2) AS average_order_value
FROM retail_sales;

-- 2. Monthly revenue and profit
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
       ROUND(SUM(revenue),2) AS revenue,
       ROUND(SUM(profit),2) AS profit,
       COUNT(DISTINCT order_id) AS orders
FROM retail_sales
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;

-- 3. Category performance
SELECT category, ROUND(SUM(revenue),2) AS revenue,
       ROUND(SUM(profit),2) AS profit, SUM(quantity) AS units_sold
FROM retail_sales
GROUP BY category
ORDER BY revenue DESC;

-- 4. Top 5 products
SELECT product, ROUND(SUM(revenue),2) AS revenue,
       ROUND(SUM(profit),2) AS profit, SUM(quantity) AS units_sold
FROM retail_sales
GROUP BY product
ORDER BY revenue DESC
LIMIT 5;

-- 5. City performance
SELECT city, ROUND(SUM(revenue),2) AS revenue,
       ROUND(SUM(profit),2) AS profit
FROM retail_sales
GROUP BY city
ORDER BY revenue DESC;

-- 6. Customer segment performance
SELECT customer_segment, COUNT(DISTINCT customer_id) AS customers,
       ROUND(SUM(revenue),2) AS revenue, ROUND(SUM(profit),2) AS profit
FROM retail_sales
GROUP BY customer_segment
ORDER BY revenue DESC;

-- 7. Payment method mix
SELECT payment_method, COUNT(DISTINCT order_id) AS orders,
       ROUND(SUM(revenue),2) AS revenue
FROM retail_sales
GROUP BY payment_method
ORDER BY orders DESC;

-- 8. Monthly category trends
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, category,
       ROUND(SUM(revenue),2) AS revenue
FROM retail_sales
GROUP BY DATE_FORMAT(order_date, '%Y-%m'), category
ORDER BY month, revenue DESC;

-- 9. Discount impact (descriptive, not causal)
SELECT discount_pct, COUNT(*) AS order_lines,
       ROUND(AVG(revenue),2) AS avg_revenue,
       ROUND(AVG(profit),2) AS avg_profit,
       ROUND(SUM(revenue),2) AS total_revenue
FROM retail_sales
GROUP BY discount_pct
ORDER BY discount_pct;

-- 10. Data quality check
SELECT
    SUM(city IS NULL) AS missing_city,
    SUM(customer_segment IS NULL) AS missing_segment,
    SUM(payment_method IS NULL) AS missing_payment_method,
    COUNT(*) AS total_rows
FROM retail_sales;

USE retail_analytics;

SELECT COUNT(*) AS total_records
FROM retail_sales;

SELECT *
FROM retail_sales
LIMIT 10;

---- updated queries----

USE retail_analytics;

SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders
FROM retail_sales
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;


SELECT
    category,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(quantity) AS units_sold,
    ROUND(
        SUM(profit) / NULLIF(SUM(revenue), 0) * 100,
        2
    ) AS profit_margin_pct
FROM retail_sales
GROUP BY category
ORDER BY total_revenue DESC;


SELECT
    product,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(quantity) AS units_sold
FROM retail_sales
GROUP BY product
ORDER BY total_revenue DESC
LIMIT 5;


SELECT
    city,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders
FROM retail_sales
GROUP BY city
ORDER BY total_revenue DESC;


USE retail_analytics;

SELECT
    customer_segment,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM retail_sales
GROUP BY customer_segment
ORDER BY total_revenue DESC;


SELECT
    payment_method,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(revenue), 2) AS average_order_value
FROM retail_sales
GROUP BY payment_method
ORDER BY total_orders DESC;


SELECT
    discount_pct,
    COUNT(*) AS total_orders,
    ROUND(AVG(revenue), 2) AS average_revenue,
    ROUND(AVG(profit), 2) AS average_profit,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM retail_sales
GROUP BY discount_pct
ORDER BY discount_pct;


SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT order_id) AS unique_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(city IS NULL) AS missing_city,
    SUM(customer_segment IS NULL) AS missing_segment,
    SUM(payment_method IS NULL) AS missing_payment_method
FROM retail_sales;




