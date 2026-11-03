-- ============================================================
-- Basic Bistro Analytics
-- Database Schema
-- ============================================================

-- ------------------------------------------------------------
-- Product Sales
-- ------------------------------------------------------------

DROP TABLE IF EXISTS product_sales;

CREATE TABLE product_sales (
    sale_id SERIAL PRIMARY KEY,
    sale_datetime TIMESTAMP NOT NULL,
    department VARCHAR(100) NOT NULL,
    product_code VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    sold_qty INTEGER NOT NULL,
    total_sales NUMERIC(12,2) NOT NULL
);


-- ------------------------------------------------------------
-- Daily Turnover
-- ------------------------------------------------------------

DROP TABLE IF EXISTS daily_turnover;

CREATE TABLE daily_turnover (
    turnover_id SERIAL PRIMARY KEY,
    sale_date DATE NOT NULL UNIQUE,
    cash NUMERIC(12,2) NOT NULL,
    credit_card NUMERIC(12,2) NOT NULL,
    accounts NUMERIC(12,2) NOT NULL,
    cheque NUMERIC(12,2) NOT NULL,
    non_turnover NUMERIC(12,2) NOT NULL,
    tips NUMERIC(12,2) NOT NULL,
    total_sales NUMERIC(12,2) NOT NULL,
    sales_rounding NUMERIC(12,2) NOT NULL,
    turnover_incl NUMERIC(12,2) NOT NULL,
    tax NUMERIC(12,2) NOT NULL,
    turnover_excl NUMERIC(12,2) NOT NULL,
    invoice_count INTEGER NOT NULL
);


-- ------------------------------------------------------------
-- Sales Invoices
-- ------------------------------------------------------------

DROP TABLE IF EXISTS sales_invoices;

CREATE TABLE sales_invoices (
    invoice_id SERIAL PRIMARY KEY,
    sale_datetime TIMESTAMP NOT NULL,
    invoice_number VARCHAR(50) NOT NULL UNIQUE,
    exclusive NUMERIC(12,2) NOT NULL,
    inclusive NUMERIC(12,2) NOT NULL,
    employee VARCHAR(100) NOT NULL,
    tax NUMERIC(12,2) NOT NULL,
    recorded_datetime TIMESTAMP NOT NULL,
    cash NUMERIC(12,2) NOT NULL,
    credit_card NUMERIC(12,2) NOT NULL,
    accounts NUMERIC(12,2) NOT NULL,
    cheque NUMERIC(12,2) NOT NULL,
    non_turnover NUMERIC(12,2) NOT NULL
);


-- ------------------------------------------------------------
-- Sales Exceptions
-- ------------------------------------------------------------

DROP TABLE IF EXISTS sales_exceptions;

CREATE TABLE sales_exceptions (
    exception_id SERIAL PRIMARY KEY,
    exception_type VARCHAR(100) NOT NULL,
    qty NUMERIC(12,2),
    table_number NUMERIC(12,2),
    invoice_number VARCHAR(50) NOT NULL,
    exception_datetime TIMESTAMP NOT NULL,
    date DATE NOT NULL,
    value NUMERIC(12,2) NOT NULL,
    invoice_value_before NUMERIC(12,2),
    invoice_value_after NUMERIC(12,2),
    employee VARCHAR(100) NOT NULL,
    authorized_by VARCHAR(100) NOT NULL
);