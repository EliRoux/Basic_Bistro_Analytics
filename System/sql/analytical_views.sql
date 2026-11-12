DROP VIEW IF EXISTS vw_sales_summary;
CREATE VIEW vw_sales_summary AS
SELECT
    COUNT(*) AS trading_days,
    ROUND(SUM(turnover_incl)::numeric, 2) AS total_turnover,
    ROUND(AVG(turnover_incl)::numeric, 2) AS average_daily_turnover,
    ROUND(MAX(turnover_incl)::numeric, 2) AS best_day_turnover,
    ROUND(MIN(turnover_incl)::numeric, 2) AS worst_day_turnover,
    SUM(invoice_count) AS total_invoices,
    ROUND(
        (SUM(turnover_incl) / NULLIF(SUM(invoice_count), 0))::numeric,
        2
    ) AS average_invoice_value
FROM daily_turnover;
SELECT *
FROM vw_daily_sales;
-----------------------------
#-'daily sales view'-#
-----------------------------
CREATE OR REPLACE VIEW vw_daily_sales AS
SELECT
    sale_date,
    ROUND(total_sales::numeric, 2) AS total_sales,
    invoice_count,
    ROUND(
        (total_sales / NULLIF(invoice_count, 0))::numeric,
        2
    ) AS average_invoice_value,
    TRIM(TO_CHAR(sale_date, 'Day')) AS day_of_week,
    EXTRACT(ISODOW FROM sale_date) AS day_number
FROM daily_turnover
ORDER BY sale_date;
-----------------------------------
SELECT *
FROM vw_daily_sales;

------------------------------------
#-'product performance view'-#
------------------------------------
CREATE OR REPLACE VIEW vw_product_performance AS
SELECT
    product_name,
    department,
    SUM(sold_qty) AS units_sold,
    ROUND(SUM(total_sales)::numeric, 2) AS total_sales,
    ROUND(
        (SUM(total_sales) / NULLIF(SUM(sold_qty), 0))::numeric,
        2
    ) AS average_revenue_per_unit,
    ROUND(
        (
            SUM(total_sales)
            / NULLIF(
                SUM(SUM(total_sales)) OVER (),
                0
            ) * 100
        )::numeric,
        2
    ) AS revenue_percentage
FROM product_sales
WHERE department <> 'PREPSCREENS'
GROUP BY
    product_name,
    department
HAVING SUM(total_sales) > 0
ORDER BY total_sales DESC;
--------------------------------
SELECT *
FROM vw_product_performance;


---------------------------------
-#'deparement performance view'-#
---------------------------------
CREATE OR REPLACE VIEW vw_department_performance AS
SELECT
    department,
    SUM(sold_qty) AS units_sold,
    ROUND(SUM(total_sales)::numeric, 2) AS total_sales,
    COUNT(DISTINCT product_name) AS unique_products,
    ROUND(
        (
            SUM(total_sales)
            / NULLIF(SUM(sold_qty), 0)
        )::numeric,
        2
    ) AS average_revenue_per_unit,
    ROUND(
        (
            SUM(total_sales)
            / NULLIF(
                SUM(SUM(total_sales)) OVER (),
                0
            ) * 100
        )::numeric,
        2
    ) AS revenue_percentage
FROM product_sales
WHERE department <> 'PREPSCREENS'
GROUP BY department
HAVING SUM(total_sales) > 0
ORDER BY total_sales DESC;
---------------------------------
SELECT *
FROM vw_department_performance;

--------------------------------
#-'payment method performance'-#
----------------------------------
CREATE OR REPLACE VIEW vw_payment_methods AS
SELECT
    ROUND(SUM(cash)::numeric, 2) AS total_cash,
    ROUND(SUM(credit_card)::numeric, 2) AS total_credit_card,
    ROUND(SUM(accounts)::numeric, 2) AS total_accounts,
    ROUND(SUM(cheque)::numeric, 2) AS total_cheque,
    ROUND(SUM(non_turnover)::numeric, 2) AS total_non_turnover,

    ROUND(
        (
            SUM(cash)
            / NULLIF(SUM(inclusive), 0)
            * 100
        )::numeric,
        2
    ) AS cash_percentage,

    ROUND(
        (
            SUM(credit_card)
            / NULLIF(SUM(inclusive), 0)
            * 100
        )::numeric,
        2
    ) AS credit_card_percentage,

    ROUND(
        (
            SUM(accounts)
            / NULLIF(SUM(inclusive), 0)
            * 100
        )::numeric,
        2
    ) AS accounts_percentage,

    ROUND(
        (
            SUM(cheque)
            / NULLIF(SUM(inclusive), 0)
            * 100
        )::numeric,
        2
    ) AS cheque_percentage,

    ROUND(
        (
            SUM(non_turnover)
            / NULLIF(SUM(inclusive), 0)
            * 100
        )::numeric,
        2
    ) AS non_turnover_percentage

FROM sales_invoices;
--------------------------------------
SELECT *
FROM vw_payment_methods;
--------------------------------------

#- "product sales analysis"-#

--------------------------------------
CREATE OR REPLACE VIEW vw_product_sales_analysis AS

SELECT
    sale_datetime,

    -- Date and time
    sale_datetime::DATE AS sale_date,
    sale_datetime::TIME AS sale_time,
    EXTRACT(HOUR FROM sale_datetime)::INTEGER AS sale_hour,

    -- Calendar information
    EXTRACT(DOW FROM sale_datetime)::INTEGER AS day_of_week_number,
    TRIM(TO_CHAR(sale_datetime, 'Day')) AS day_of_week,

    EXTRACT(MONTH FROM sale_datetime)::INTEGER AS month_number,
    TRIM(TO_CHAR(sale_datetime, 'Month')) AS month_name,

    EXTRACT(YEAR FROM sale_datetime)::INTEGER AS year,

    -- South African seasons
    CASE
        WHEN EXTRACT(MONTH FROM sale_datetime) IN (12, 1, 2)
            THEN 'Summer'

        WHEN EXTRACT(MONTH FROM sale_datetime) IN (3, 4, 5)
            THEN 'Autumn'

        WHEN EXTRACT(MONTH FROM sale_datetime) IN (6, 7, 8)
            THEN 'Winter'

        WHEN EXTRACT(MONTH FROM sale_datetime) IN (9, 10, 11)
            THEN 'Spring'
    END AS season,

    -- Product information
    department,
    product_code,
    product_name,

    -- Sales
    sold_qty,
    total_sales,

    -- Revenue percentage
    ROUND(
        (
            SUM(total_sales) OVER (
                PARTITION BY product_code
            )
            /
            NULLIF(
                SUM(total_sales) OVER (),
                0
            )
        ) * 100,
        2
    ) AS revenue_percentage

FROM product_sales

WHERE department NOT IN (
    'INGREDIENTS / EXTRAS',
    'PREP SCREEN'
);
--------------------------------------
SELECT *
FROM vw_product_sales_analysis;
--------------------------------------
SELECT
    MIN(sale_datetime::date) AS first_date,
    MAX(sale_datetime::date) AS last_date,
    COUNT(DISTINCT sale_datetime::date) AS trading_days
FROM product_sales;