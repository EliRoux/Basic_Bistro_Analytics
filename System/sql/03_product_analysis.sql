-- ============================================================
-- BASIC BISTRO ANALYTICS
-- 02 - Product Analysis
-- ============================================================


-- ------------------------------------------------------------
-- 1. Sales by department
-- ------------------------------------------------------------

SELECT
    department,
    COUNT(*) AS records,
    SUM(sold_qty) AS quantity_sold,
    ROUND(SUM(total_sales)::numeric, 2) AS total_sales
FROM product_sales
GROUP BY department
ORDER BY total_sales DESC;


-- ------------------------------------------------------------
-- 2. Top 20 products by revenue
-- ------------------------------------------------------------

SELECT
    product_code,
    product_name,
    department,
    SUM(sold_qty) AS quantity_sold,
    ROUND(SUM(total_sales)::numeric, 2) AS total_sales
FROM product_sales
GROUP BY
    product_code,
    product_name,
    department
ORDER BY total_sales DESC
LIMIT 20;


-- ------------------------------------------------------------
-- 3. Top 20 products by quantity sold
-- ------------------------------------------------------------

SELECT
    product_code,
    product_name,
    department,
    SUM(sold_qty) AS quantity_sold,
    ROUND(SUM(total_sales)::numeric, 2) AS total_sales
FROM product_sales
GROUP BY
    product_code,
    product_name,
    department
ORDER BY quantity_sold DESC
LIMIT 20;


-- ------------------------------------------------------------
-- 4. Department contribution to total sales
-- ------------------------------------------------------------

SELECT
    department,
    ROUND(SUM(total_sales)::numeric, 2) AS total_sales,
    ROUND(
        (
            SUM(total_sales)
            / NULLIF((SELECT SUM(total_sales) FROM product_sales), 0)
            * 100
        )::numeric,
        2
    ) AS sales_percentage
FROM product_sales
GROUP BY department
ORDER BY total_sales DESC;


-- ------------------------------------------------------------
-- 5. Product sales by month
-- ------------------------------------------------------------

SELECT
    DATE_TRUNC('month', sale_datetime)::date AS month,
    ROUND(SUM(total_sales)::numeric, 2) AS total_sales,
    SUM(sold_qty) AS quantity_sold
FROM product_sales
GROUP BY DATE_TRUNC('month', sale_datetime)
ORDER BY month;


-- ------------------------------------------------------------
-- 6. Average selling price by product
-- ------------------------------------------------------------

SELECT
    product_code,
    product_name,
    department,
    SUM(sold_qty) AS quantity_sold,
    ROUND(
        (SUM(total_sales) / NULLIF(SUM(sold_qty), 0))::numeric,
        2
    ) AS average_selling_price,
    ROUND(SUM(total_sales)::numeric, 2) AS total_sales
FROM product_sales
GROUP BY
    product_code,
    product_name,
    department
HAVING SUM(sold_qty) > 0
ORDER BY total_sales DESC;