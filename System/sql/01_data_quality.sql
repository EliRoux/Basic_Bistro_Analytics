-- ============================================================
-- BASIC BISTRO ANALYTICS
-- 01 - DATA QUALITY CHECKS
-- ============================================================

-- ------------------------------------------------------------
-- 1. TABLE ROW COUNTS
-- ------------------------------------------------------------

SELECT 'product_sales' AS table_name, COUNT(*) AS row_count
FROM product_sales

UNION ALL

SELECT 'daily_turnover', COUNT(*)
FROM daily_turnover

UNION ALL

SELECT 'sales_invoices', COUNT(*)
FROM sales_invoices

UNION ALL

SELECT 'sales_exceptions', COUNT(*)
FROM sales_exceptions;


-- ------------------------------------------------------------
-- 2. PRODUCT SALES - MISSING VALUES
-- ------------------------------------------------------------

SELECT
    COUNT(*) FILTER (WHERE sale_datetime IS NULL) AS missing_sale_datetime,
    COUNT(*) FILTER (WHERE department IS NULL) AS missing_department,
    COUNT(*) FILTER (WHERE product_code IS NULL) AS missing_product_code,
    COUNT(*) FILTER (WHERE product_name IS NULL) AS missing_product_name,
    COUNT(*) FILTER (WHERE sold_qty IS NULL) AS missing_quantity,
    COUNT(*) FILTER (WHERE total_sales IS NULL) AS missing_sales
FROM product_sales;


-- ------------------------------------------------------------
-- 3. PRODUCT SALES - DATE RANGE
-- ------------------------------------------------------------

SELECT
    MIN(sale_datetime) AS first_sale,
    MAX(sale_datetime) AS last_sale
FROM product_sales;


-- ------------------------------------------------------------
-- 4. PRODUCT SALES - NEGATIVE QUANTITIES
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS negative_quantity_records,
    COALESCE(SUM(ABS(sold_qty)), 0) AS negative_quantity
FROM product_sales
WHERE sold_qty < 0;


-- ------------------------------------------------------------
-- 5. PRODUCT SALES - NEGATIVE SALES
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS negative_sales_records,
    COALESCE(SUM(ABS(total_sales)), 0) AS negative_sales_value
FROM product_sales
WHERE total_sales < 0;


-- ------------------------------------------------------------
-- 6. PRODUCT SALES - ZERO VALUE RECORDS
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS zero_value_records,
    COALESCE(SUM(sold_qty), 0) AS zero_value_quantity
FROM product_sales
WHERE total_sales = 0;


-- ------------------------------------------------------------
-- 7. PRODUCT SALES - DEPARTMENT CHECK
-- ------------------------------------------------------------

SELECT
    department,
    COUNT(*) AS records,
    SUM(sold_qty) AS quantity_sold,
    SUM(total_sales) AS total_sales
FROM product_sales
GROUP BY department
ORDER BY total_sales DESC;


-- ------------------------------------------------------------
-- 8. PRODUCT SALES - REVENUE RECONCILIATION
-- ------------------------------------------------------------

SELECT
    SUM(total_sales) AS product_sales_total
FROM product_sales;


-- ------------------------------------------------------------
-- 9. DAILY TURNOVER - TOTALS
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS days,
    SUM(total_sales) AS total_sales,
    SUM(turnover_incl) AS turnover_incl,
    SUM(turnover_excl) AS turnover_excl,
    SUM(tax) AS total_tax,
    SUM(invoice_count) AS invoice_count
FROM daily_turnover;


-- ------------------------------------------------------------
-- 10. SALES INVOICES - DUPLICATE INVOICES
-- ------------------------------------------------------------

SELECT
    invoice_number,
    COUNT(*) AS occurrences
FROM sales_invoices
GROUP BY invoice_number
HAVING COUNT(*) > 1
ORDER BY occurrences DESC;


-- ------------------------------------------------------------
-- 11. SALES INVOICES - DATE RANGE
-- ------------------------------------------------------------

SELECT
    MIN(sale_datetime) AS first_invoice,
    MAX(sale_datetime) AS last_invoice
FROM sales_invoices;


-- ------------------------------------------------------------
-- 12. SALES INVOICES - TOTALS
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS invoice_count,
    SUM(exclusive) AS total_exclusive,
    SUM(inclusive) AS total_inclusive,
    SUM(tax) AS total_tax,
    AVG(inclusive) AS average_invoice_value
FROM sales_invoices;


-- ------------------------------------------------------------
-- 13. SALES EXCEPTIONS - TYPE BREAKDOWN
-- ------------------------------------------------------------

SELECT
    exception_type,
    COUNT(*) AS exception_count,
    SUM(value) AS total_value
FROM sales_exceptions
GROUP BY exception_type
ORDER BY total_value DESC;


-- ------------------------------------------------------------
-- 14. SALES EXCEPTIONS - DATE RANGE
-- ------------------------------------------------------------

SELECT
    MIN(exception_datetime) AS first_exception,
    MAX(exception_datetime) AS last_exception
FROM sales_exceptions;


-- ------------------------------------------------------------
-- 15. SALES EXCEPTIONS - TOTAL VALUE
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS exception_records,
    SUM(value) AS total_exception_value
FROM sales_exceptions;