# :truck: BLMO-Logistics-Engine

### :book: Master's Thesis Project by Pavan Kumar Yella
**Institution:** Hochschule Fresenius University of Applied Sciences, Berlin  
**Date:** June 2026

### :book: Project Overview
This repository contains the implementation of my Master's thesis project:  
**"AI-based Decision Support for Last-Mile Carrier Selection in E-Commerce Logistics"**.  
The project demonstrates an end-to-end data engineering pipeline that optimizes Berlin last-mile logistics using data-driven carrier selection models.

### :brain: System Architecture
The system follows a modular data engineering architecture:
Data Sources (CSV/API) > Extraction Layer (Python, SQL) > Transformation (Pandas, DuckDB) > Loading/Storage (PostgreSQL) > Visualization (Power BI / Dashboards).

### :gear: Technology Stack
* **Programming Language:** Python 3.x
* **Database:** SQL / PostgreSQL / DuckDB
* **Business Intelligence:** Power BI
* **Development Environment:** Jupyter / Google Colab
* **Libraries:** pandas, numpy, sqlalchemy, matplotlib, duckdb, scikit-learn

### :rocket: Key Features
* **Automated ETL Pipeline:** End-to-end workflow from data ingestion to reporting.
* **Carrier Selection Model:** AI-driven decision support for optimal last-mile carrier choice.
* **BI Dashboards:** Interactive dashboards for logistics KPIs and performance tracking.
* **Quality Management:** Built-in handling of missing values, duplicates, and data validation.

### :checkered_flag: Getting Started
1. **Clone:** `git clone https://github.com/PavanKumarYella16/BLMO-Logistics-Engine.git`
2. **Install:** `pip install -r requirements.txt`
3. **Run:** `python scripts/run_pipeline.py`
4. **Dashboard:** Import processed data into Power BI.

### :jigsaw: Project Structure
Key directories include:
* `/Data`: Source data and processed outputs.
* `/scripts`: ETL pipeline logic.
* `/notebooks`: Development and analysis notebooks.
* `/docs`: Project documentation.

### :test_tube: Testing and Quality Assurance
Includes data validation assertions, unit tests for transformation logic, and performance benchmarking.

### :balance_scale: License
* **Code:** MIT License
