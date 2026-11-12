
# SQL Analysis – Basic Bistro Analytics

## Overview

This folder contains SQL scripts documenting the database queries, analytical views, and business analysis developed for the Basic Bistro Analytics project.

The SQL code demonstrates how PostgreSQL is used to analyse restaurant sales data and prepare information for business intelligence reporting in Power BI.

**Important:** The SQL files in this folder are included for portfolio documentation, transparency, and code review purposes. They are not directly executed by the public Python pipeline.

---

## SQL Development Environment

The project uses the following technologies:

- **PostgreSQL:** Stores synthetic restaurant transaction data and supports analytical queries.
- **pgAdmin:** Provides the development environment used to write, execute, test, and manage SQL queries.
- **SQL:** Performs data aggregation, analysis, and preparation of reporting datasets.
- **Power BI:** Connects to PostgreSQL to retrieve analytical results and visualise business performance.

The SQL scripts in this folder provide a readable reference to the SQL logic developed and tested using pgAdmin.

---

## SQL Workflow

The SQL analysis and reporting workflow follows this structure:

    Synthetic Restaurant Sales Data
                  |
                  v
          PostgreSQL Database
                  |
                  v
         SQL Development in pgAdmin
                  |
                  v
         Analytical SQL Queries
                  |
                  v
          PostgreSQL Views
                  |
                  v
           Power BI Dashboard

PostgreSQL executes the SQL queries and stores the analytical views.

Power BI connects directly to PostgreSQL to retrieve the relevant datasets.

pgAdmin is used to develop and manage the SQL logic but is not required for Power BI to access the database.

---

## Purpose of the SQL Scripts

The SQL code demonstrates techniques used to:

- Query relational database tables.
- Aggregate restaurant sales transactions.
- Analyse revenue and transaction activity.
- Evaluate product and department performance.
- Identify sales patterns and trends.
- Calculate key business performance indicators.
- Prepare structured analytical datasets for Power BI.
- Support business intelligence reporting.

---

## SQL Analysis Categories

### Sales Analysis

SQL queries are used to examine:

- Total revenue
- Daily turnover
- Transaction volumes
- Average invoice values
- Sales performance over time

### Product and Department Analysis

SQL queries support the analysis of:

- Product sales performance
- Product quantities sold
- Revenue contribution by product
- Department-level performance
- Product sales distribution

### Payment Analysis

SQL queries support the examination of:

- Payment methods
- Transaction distribution by payment method
- Sales totals associated with payment methods

### Business Intelligence Reporting

SQL analytical views provide structured datasets that can be imported into Power BI.

These datasets support the development of interactive dashboards, business KPIs, and performance reports.

---

## PostgreSQL Analytical Views

The Basic Bistro Analytics project uses the following analytical views:

| SQL View | Purpose |
|----------|---------|
| `vw_sales_summary` | Overall restaurant sales performance |
| `vw_daily_sales` | Daily revenue and transaction activity |
| `vw_department_performance` | Department-level sales analysis |
| `vw_product_performance` | Individual product performance |
| `vw_payment_methods` | Payment method analysis |
| `vw_product_sales_analysis` | Detailed product sales analysis |

The SQL files in this folder may document the queries and view definitions used during development.

The public Python pipeline separately creates the required analytical views through its database-loading process.

---

## Relationship to the Python Pipeline

The Basic Bistro Analytics project includes a public Python pipeline responsible for generating and loading synthetic data into PostgreSQL.

The SQL files in this folder are **not direct dependencies of that pipeline**.

The pipeline does not read or execute these SQL files.

However, the pipeline may independently implement equivalent SQL logic to create the required analytical views.

### Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| Python Pipeline | Generates and loads synthetic transactional data |
| PostgreSQL | Stores data and executes SQL queries |
| pgAdmin | Used to develop, test, and manage SQL |
| SQL Files | Document analytical SQL logic for portfolio review |
| Power BI | Retrieves PostgreSQL data for dashboard reporting |

### Important Distinction

The SQL files are provided as examples of the analytical work performed during project development.

They are not automatically executed when running the public Python pipeline.

Editing these files does not automatically update the PostgreSQL database, its analytical views, or the Power BI dashboard.

To apply SQL changes, the relevant queries must be executed against the intended PostgreSQL database.

Any affected Power BI datasets or visualisations may also need to be refreshed.

---

## Data Privacy and Security

This public repository is intended to demonstrate SQL development and analytical capabilities using synthetic restaurant sales data.

The SQL scripts should reference only publicly documented database structures.

They must not contain:

- Confidential restaurant transaction records
- Private business information
- Database passwords or credentials
- Sensitive connection details
- References requiring access to private source databases

The public demonstration database is named:

`basic_bistro_synthetic`

All SQL examples included in this repository should be suitable for use with the public synthetic database.

---

## Portfolio Purpose

The SQL files are included to demonstrate practical experience in:

- PostgreSQL database querying
- SQL query development
- Data aggregation and transformation
- Analytical view design
- Business performance analysis
- Preparing datasets for Power BI
- Database-driven business intelligence

These files serve as **readable examples of SQL development work**, allowing recruiters and other developers to review the analytical logic without requiring direct access to the PostgreSQL database or Power BI dashboard.

All publicly distributed transaction data is synthetic and should not be interpreted as actual restaurant performance.
