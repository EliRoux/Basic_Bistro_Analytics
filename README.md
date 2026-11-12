Basic Bistro Analytics

End-to-End Restaurant Sales Analytics | Python • PostgreSQL • SQL • Power BI

Project Overview

Basic Bistro Analytics is an end-to-end data analytics portfolio project demonstrating how restaurant transaction data can be transformed into actionable business intelligence.

The project uses Python, PostgreSQL, SQL, and Power BI to build a reproducible analytics workflow, from data generation and database loading to business performance reporting.

The public version operates exclusively on fictional synthetic datasets, allowing the technical implementation to be demonstrated without publishing confidential business records.

Project Objectives

Build a reproducible data pipeline using Python and PostgreSQL.

Organise transactional restaurant data into structured database tables.

Develop SQL views for business performance analysis.

Analyse revenue, product performance, transaction activity, and payment methods.

Support interactive business intelligence reporting through Power BI.

Demonstrate responsible handling of confidential business information.

Technology Stack

Technology

Application

Python

Synthetic data generation, data processing, and pipeline automation

PostgreSQL

Relational database and analytical data storage

SQL

Data aggregation, analytical views, and business queries

Power BI

Interactive dashboards and KPI reporting

Git & GitHub

Version control and portfolio documentation

CSV

Synthetic transactional data exchange

Data Pipeline Architecture

The public analytics workflow follows this structure:

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

The pipeline is designed to regenerate synthetic transactions and load them into a separate PostgreSQL database.

It does not require access to the original restaurant database or private processed exports.

Business Analytics

The project supports analysis of several key restaurant performance indicators.

Sales Performance

Total sales revenue

Average daily turnover

Average invoice value

Best and worst performing sales days

Total transaction volume

Revenue trends over time

Product and Department Performance

Sales performance by product

Revenue contribution by department

Product quantities sold

Product sales trends

Product mix analysis

Payment Analysis

Transaction activity by payment method

Payment method distribution

Payment-related sales trends

PostgreSQL Analytical Views

The data loader creates the following analytical views:

SQL View

Purpose

vw_sales_summary

Overall sales performance

vw_daily_sales

Daily revenue and sales activity

vw_department_performance

Department-level performance

vw_product_performance

Individual product performance

vw_payment_methods

Payment method analysis

vw_product_sales_analysis

Detailed product sales analysis

Additional SQL analysis scripts are available in System/sql/.

Power BI Dashboard

The project supports an interactive Power BI dashboard connected to the PostgreSQL synthetic database.

Dashboard KPIs include:

Total Turnover

Total Invoices

Average Daily Turnover

Average Invoice Value

Best Day Turnover

Worst Day Turnover

Date slicers allow users to explore performance across different reporting periods.

Dashboard screenshots: To be added.

The local .pbix dashboard file is excluded from the public repository. Users can connect their own Power BI Desktop installation to the basic_bistro_synthetic database and import the analytical views.

Installation and Setup

Prerequisites

Python 3.11+

PostgreSQL

Power BI Desktop (optional)

Git (optional)

1. Install Dependencies

Create and activate a Python virtual environment, then install the required packages:

pip install -r requirements-public.txt

2. Configure Environment Variables

Create a local .env file using .env.example as a template.

Enter your PostgreSQL connection credentials.

Never commit .env or expose database passwords.

3. Create the Database

Run the following command:

psql -U postgres -c "CREATE DATABASE basic_bistro_synthetic;"

Skip this step if the database already exists.

4. Execute the Public Pipeline

Run:

python System/python/run_public_pipeline.py

Alternatively, on Windows:

RUN_PUBLIC_PIPELINE.bat

The pipeline regenerates fictional synthetic transactions before loading them into PostgreSQL.

To load existing synthetic CSVs without regeneration:

python System/python/run_public_pipeline.py --skip-generate

5. Connect Power BI

Open Power BI Desktop and connect to the PostgreSQL database:

Database: basic_bistro_synthetic

Import the relevant analytical views and build the required visualisations.

Ensure all Power BI queries reference the synthetic database.

Verification

Verify that the Python scripts compile:

python -m compileall -q System/python

Run the public pipeline using existing synthetic data:

python System/python/run_public_pipeline.py --skip-generate

Verify the database connection and loaded data:

SELECT current_database();

SELECT COUNT(*)
FROM public.sales_invoices;

SELECT *
FROM public.vw_sales_summary;

These database checks require a running PostgreSQL server and valid local credentials.

Data Privacy and Security

This repository is intended for public portfolio demonstration.

The published workflow uses synthetic transactional datasets and does not require original restaurant business records.

Security measures include:

Separation of public synthetic datasets from private source exports.

A dedicated PostgreSQL database for synthetic data.

Local database credentials stored in an excluded .env file.

Exclusion of private exports, local executables, build output, and Power BI project files.

Restriction of CSV tracking to System/data/synthetic/*.csv.

Before publication, repository files and Git history should be reviewed using:

git ls-files
git log --all --name-only
git status

If confidential information or credentials were previously committed, Git history must be cleaned and exposed credentials rotated before publishing.

Privacy note: Although the public datasets are fictional, no formal privacy guarantee is made regarding synthetic data derived from private distributions without an independent disclosure review.

Skills Demonstrated

This project demonstrates practical experience in:

Python-based data pipeline development

Relational database management

SQL analytics and reporting

Data processing and validation

Business intelligence and KPI development

Workflow automation

Synthetic data generation

Data security awareness

Technical documentation and reproducibility

Future Improvements

Potential extensions include:

Automated data quality testing

Pipeline execution logging and monitoring

Additional SQL-based business analyses

Advanced sales trend visualisations

Automated reporting workflows

Sales forecasting using time-series models

Project Purpose

This project was developed as a portfolio demonstration of practical data analytics and data engineering skills.

It illustrates how transactional business data can be organised into a structured, reproducible analytical workflow that supports operational reporting and business decision-making.

All publicly distributed transaction data is synthetic and should not be interpreted as actual restaurant performance.
