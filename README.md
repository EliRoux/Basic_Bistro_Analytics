
# Basic Bistro Analytics

### End-to-End Restaurant Sales Analytics | Python • PostgreSQL • SQL • Power BI

## Project Overview

Basic Bistro Analytics is an end-to-end data analytics portfolio project demonstrating how restaurant transaction data can be transformed into meaningful business intelligence.

The project uses **Python, PostgreSQL, SQL, and Power BI** to develop a reproducible analytics workflow, from synthetic data generation and database loading to SQL analysis and interactive reporting.

The public version operates entirely on fictional synthetic datasets, allowing the technical implementation to be demonstrated without publishing confidential business records.

## Project Objectives

- Build a reproducible data pipeline using Python and PostgreSQL.
- Organise restaurant transaction data into structured relational database tables.
- Develop SQL views for business performance analysis.
- Analyse revenue, product performance, transaction activity, and payment methods.
- Support interactive business intelligence reporting through Power BI.
- Demonstrate responsible handling of confidential business information.

---

## Technology Stack

| Technology | Application |
|------------|-------------|
| Python | Synthetic data generation, data processing, and pipeline automation |
| PostgreSQL | Relational database management and analytical data storage |
| SQL | Data aggregation, analytical views, and business queries |
| Power BI | Interactive dashboards and KPI reporting |
| Git & GitHub | Version control and portfolio documentation |
| CSV | Synthetic transactional data exchange |

---

## Data Pipeline Architecture

The public analytics workflow follows this structure:

```text
Bundled Synthetic Reference CSVs
              |
              v
      Python Data Generator
              |
              v
     Generated Synthetic CSVs
              |
              v
       Python Data Loader
              |
              v
      PostgreSQL Database
     basic_bistro_synthetic
              |
              v
        SQL Analytics Views
              |
              v
       Power BI Dashboard
```

The pipeline regenerates synthetic transactions and loads them into a separate PostgreSQL database.

It does not require access to the original restaurant database or private processed exports.

---

## Business Analytics

The project supports the analysis of several key restaurant performance indicators.

### Sales Performance

- Total sales revenue
- Average daily turnover
- Average invoice value
- Best and worst performing sales days
- Total transaction volume
- Revenue trends over time

### Product and Department Performance

- Sales performance by product
- Revenue contribution by department
- Product quantities sold
- Product sales trends
- Product mix analysis

### Payment Analysis

- Transaction activity by payment method
- Payment method distribution
- Payment-related sales trends

---

## PostgreSQL Analytical Views

The Python data loader creates the following PostgreSQL analytical views:

| SQL View | Purpose |
|----------|---------|
| `vw_sales_summary` | Overall sales performance |
| `vw_daily_sales` | Daily revenue and sales activity |
| `vw_department_performance` | Department-level performance |
| `vw_product_performance` | Individual product performance |
| `vw_payment_methods` | Payment method analysis |
| `vw_product_sales_analysis` | Detailed product sales analysis |

Additional SQL analysis scripts are available in `System/sql/`.

---

## Power BI Dashboard

The project supports an interactive Power BI dashboard connected to the PostgreSQL synthetic database.

### Dashboard KPIs

The dashboard includes the following performance indicators:

- Total Turnover
- Total Invoices
- Average Daily Turnover
- Average Invoice Value
- Best Day Turnover
- Worst Day Turnover

Date slicers allow users to explore performance across different reporting periods.

### Dashboard Screenshots

Screenshots of the dashboard will be added to demonstrate the analytical results and visualisations.

The local `.pbix` dashboard file is excluded from the public repository.

Users can connect Power BI Desktop to the `basic_bistro_synthetic` PostgreSQL database and import the analytical views.

---

## Installation and Setup

### Prerequisites

Before running the project, install:

- Python 3.11+
- PostgreSQL
- Power BI Desktop (optional)
- Git (optional)

### Step 1: Install Dependencies

Create and activate a Python virtual environment.

Install the required Python packages:

```bash
pip install -r requirements-public.txt
```

### Step 2: Configure Environment Variables

Create a local `.env` file using `.env.example` as a template.

Enter your PostgreSQL connection credentials.

**Important:** Never commit `.env` or expose database passwords.

### Step 3: Create the PostgreSQL Database

Run the following command:

```bash
psql -U postgres -c "CREATE DATABASE basic_bistro_synthetic;"
```

Skip this step if the database already exists.

### Step 4: Execute the Public Pipeline

Run:

```bash
python System/python/run_public_pipeline.py
```

Alternatively, on Windows:

```bat
RUN_PUBLIC_PIPELINE.bat
```

The pipeline regenerates fictional synthetic transactions before loading them into PostgreSQL.

To load existing synthetic CSVs without regenerating them:

```bash
python System/python/run_public_pipeline.py --skip-generate
```

### Step 5: Connect Power BI

Open Power BI Desktop and connect to PostgreSQL.

Use the database:

```text
basic_bistro_synthetic
```

Import the relevant analytical views and build the required visualisations.

Ensure that all Power BI queries reference the synthetic database.

---

## Verification

### Verify Python Scripts

Run:

```bash
python -m compileall -q System/python
```

### Verify the Public Pipeline

Run:

```bash
python System/python/run_public_pipeline.py --skip-generate
```

### Verify PostgreSQL Data

Execute the following SQL queries:

```sql
SELECT current_database();

SELECT COUNT(*)
FROM public.sales_invoices;

SELECT *
FROM public.vw_sales_summary;
```

These database checks require a running PostgreSQL server and valid local credentials.

---

## Data Privacy and Security

This repository is intended for public portfolio demonstration.

The published workflow uses synthetic transactional datasets and does not require access to original restaurant business records.

### Security Measures

- Separation of public synthetic datasets from private source exports.
- A dedicated PostgreSQL database for synthetic data.
- Local database credentials stored in an excluded `.env` file.
- Exclusion of private exports, local executables, build output, and Power BI project files.
- Restriction of CSV tracking to `System/data/synthetic/*.csv`.

### Git Repository Security

Before publishing, review tracked files and Git history using:

```bash
git ls-files
git log --all --name-only
git status
```

A `.gitignore` file does not remove files that have already been committed.

If confidential information or credentials were previously committed, clean the Git history and rotate exposed credentials before publication.

**Privacy Note:** Although the public datasets are fictional, no formal privacy guarantee is made regarding synthetic data derived from private distributions without an independent disclosure review.

---

## Skills Demonstrated

This project demonstrates practical experience in:

- Python-based data pipeline development
- Relational database management
- SQL analytics and reporting
- Data processing and validation
- Business intelligence and KPI development
- Workflow automation
- Synthetic data generation
- Data security awareness
- Technical documentation and reproducibility

---

## Future Improvements

Potential extensions to the project include:

- Automated data quality testing
- Pipeline execution logging and monitoring
- Additional SQL-based business analyses
- Advanced sales trend visualisations
- Automated reporting workflows
- Sales forecasting using time-series models

---

## Project Purpose

This project was developed as a portfolio demonstration of practical data analytics and data engineering skills.

It illustrates how transactional business data can be organised into a structured, reproducible analytical workflow that supports operational reporting and business decision-making.

All publicly distributed transaction data is synthetic and should not be interpreted as actual restaurant performance.
