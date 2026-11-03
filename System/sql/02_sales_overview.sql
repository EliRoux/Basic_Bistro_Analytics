-- ============================================================
-- BASIC BISTRO ANALYTICS
-- 01 - Sales Overview
-- ============================================================


-- ------------------------------------------------------------
-- 1. Overall sales summary
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS invoice_records,
    ROUND(SUM(exclusive)::numeric, 2) AS total_exclusive,
    ROUND(SUM(inclusive)::numeric, 2) AS total_inclusive,
    ROUND(SUM(tax)::numeric, 2) AS total_tax,
    ROUND(AVG(inclusive)::numeric, 2) AS average_invoice_value
FROM sales_invoices;


-- ------------------------------------------------------------
-- 2. Daily sales performance
-- ------------------------------------------------------------

SELECT
    DATE(sale_datetime) AS sale_date,
    COUNT(*) AS invoice_count,
    ROUND(SUM(inclusive)::numeric, 2) AS total_sales,
    ROUND(AVG(inclusive)::numeric, 2) AS average_invoice_value
FROM sales_invoices
GROUP BY DATE(sale_datetime)
ORDER BY sale_date;


-- ------------------------------------------------------------
-- 3. Sales by payment method
-- ------------------------------------------------------------

SELECT
    ROUND(SUM(cash)::numeric, 2) AS cash,
    ROUND(SUM(credit_card)::numeric, 2) AS credit_card,
    ROUND(SUM(accounts)::numeric, 2) AS accounts,
    ROUND(SUM(cheque)::numeric, 2) AS cheque,
    ROUND(SUM(non_turnover)::numeric, 2) AS non_turnover
FROM sales_invoices;


-- ------------------------------------------------------------
-- 4. Payment method percentages
-- ------------------------------------------------------------

SELECT
    ROUND(SUM(cash)::numeric, 2) AS cash,
    ROUND(SUM(credit_card)::numeric, 2) AS credit_card,
    ROUND(SUM(accounts)::numeric, 2) AS accounts,
    ROUND(SUM(cheque)::numeric, 2) AS cheque,
    ROUND(SUM(non_turnover)::numeric, 2) AS non_turnover,

    ROUND(
        (SUM(cash) / NULLIF(SUM(inclusive), 0) * 100)::numeric,
        2
    ) AS cash_percentage,

    ROUND(
        (SUM(credit_card) / NULLIF(SUM(inclusive), 0) * 100)::numeric,
        2
    ) AS credit_card_percentage,

    ROUND(
        (SUM(accounts) / NULLIF(SUM(inclusive), 0) * 100)::numeric,
        2
    ) AS accounts_percentage,

    ROUND(
        (SUM(cheque) / NULLIF(SUM(inclusive), 0) * 100)::numeric,
        2
    ) AS cheque_percentage
FROM sales_invoices;


-- ------------------------------------------------------------
-- 5. Daily turnover comparison
-- ------------------------------------------------------------

SELECT
    sale_date,
    total_sales,
    turnover_incl,
    turnover_excl,
    invoice_count,
    ROUND(
        (total_sales / NULLIF(invoice_count, 0))::numeric,
        2
    ) AS average_invoice_value
FROM daily_turnover
ORDER BY sale_date;