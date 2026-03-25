# E-commerce ETL Pipeline (Pandas)


##  Overview
- This project implements a **production-style ETL (Extract, Transform, Load) pipeline** using Python and Pandas.
- The pipeline processes transactional data from multiple sources, performs data cleaning, joins datasets, computes aggregated metrics, and generates data quality reports.


## Problem Statement
Given customer and order datasets, identify key business insights such as:

* Daily sales performance
* Customer spending patterns
* Data quality issues in the dataset


## Features
* ✅ Multi-source data ingestion (JSON + CSV)
* ✅ Data cleaning and validation
* ✅ Dataset joining using `customer_id`
* ✅ Aggregations using Pandas (`groupby + agg`)
* ✅ Data quality tracking (valid vs invalid records)
* ✅ Logging (console + file)
* ✅ CLI-based execution
* ✅ Class-based pipeline design


## Architecture
Extract → Transform → Load

### Flow:
* **Extract** → Read JSON (orders) and CSV (customers)
* **Transform** → Clean data → Join → Aggregate
* **Load** → Save outputs (CSV + JSON)


## 🔄 Transformation Logic

### SQL Equivalent

```sql
WITH final_data AS (
    SELECT 
        o.order_id,
        o.customer_id,
        o.amount,
        o.date,
        c.name
    FROM orders o
    LEFT JOIN customers c
        ON o.customer_id = c.customer_id
    WHERE 
        o.amount IS NOT NULL
        AND TRIM(c.name) <> ''
)

--Daily Sales
SELECT 
    date,
    SUM(amount) AS total_sales,
    COUNT(order_id) AS order_count
FROM final_data
GROUP BY date;

--Customer Metrics
SELECT 
    customer_id,
    name,
    SUM(amount) AS total_spend
FROM final_data
GROUP BY customer_id, name;
```


## Data Validation
The pipeline ensures data quality by:
* Removing orders with null `amount`
* Removing customers with empty or missing names
* Dropping unmatched records after join
* Logging invalid records


## Project Structure
ecommerce-etl/
│
├── main.py              # CLI entry point
├── pipeline.py          # ETL pipeline logic
├── logger.py            # Logging configuration
├── generate_data.py     # Script to generate sample data
│
├── data/
│   ├── orders.json
│   └── customers.csv
│
├── output/
│   ├── sales.csv
│   ├── customer_metrics.csv
│   └── data_quality.json
│
├── requirements.txt
├── README.md


## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the pipeline
```bash
python main.py --orders data/orders.json --customers data/customers.csv --output output/
```


##  Outputs

### 🔹 Daily Sales (`sales.csv`)
```csv
date,total_sales,order_count
2024-01-01,29058.0,62
2024-01-02,33340.0,65
```

### 🔹 Customer Metrics (`customer_metrics.csv`)
```csv
customer_id,name,total_spend
1,Customer_1,2443.0
2,Customer_2,4845.0
```

### 🔹 Data Quality Report (`data_quality.json`)
```json
{
    "total_rows": 800,
    "transformed rows": 692,
    "dropped rows": 108
}
```


## Logging
* Logs pipeline execution steps
* Tracks dropped/invalid records
* Outputs to:
  * Console
  * `pipeline.log` file


## Tech Stack
* Python
* Pandas
* Logging
* argparse (CLI)


## Key Learnings
* Building end-to-end ETL pipelines
* Translating SQL logic into Pandas
* Handling real-world data quality issues
* Designing modular and scalable pipelines


## Future Improvements
* Add config-driven pipeline (JSON/YAML)
* Implement unit tests (pytest)
* Add Airflow orchestration
* Handle large-scale datasets (chunking/streaming)


## Author

Arul Joe Kevin V
Aspiring Data Engineer
