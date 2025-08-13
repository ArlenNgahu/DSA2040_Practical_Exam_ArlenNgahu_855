# DSA2040 Practical Exam — Retail Data Warehouse
## Author
- **Name:** Arlen Ngahu  
- **ID:** 855  
- **Course:** DSA2040  
- **Date:** 13 August 2025


## Overview
This project builds a small **Retail Data Warehouse** using the UCI *Online Retail* dataset and demonstrates OLAP-style analysis.  
It includes:
- **Task 1:** Star schema (SQL DDL)
- **Task 2:** ETL pipeline (Python → SQLite)
- **Task 3:** OLAP queries + visualizations + analysis report

---

## Repository Structure
```
.
├── sql/
│   └── create_tables_retail_dw.sql        # DDL for star schema
├── charts/
│   ├── chart_sales_by_country.png
│   ├── chart_monthly_sales_uk.png
│   └── chart_top10_products.png
├── etl_retail.py                          # ETL (UCI dataset → SQLite)
├── visualize_queries.py                   # Runs SQL and outputs charts
├── retail_dw.db                           # SQLite database (generated)
└── README.md
```

---

## Dataset
- **Source:** UCI Machine Learning Repository — *Online Retail* (2010–2011)
- **Fields used:** InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country

---

## Star Schema (Task 1)
**Fact:** `SalesFact`  
**Dimensions:** `CustomerDim`, `ProductDim`, `TimeDim`

**Keys & Measures**
- `SalesFact(SalesFactID PK, InvoiceNo, StockCode FK, CustomerID FK, TimeID FK, Quantity, UnitPrice, TotalSales, Country)`
- `CustomerDim(CustomerID PK, Country, CustomerName)`
- `ProductDim(StockCode PK, Description, Category)`
- `TimeDim(TimeID PK, InvoiceDate, Day, Month, Quarter, Year, WeekOfYear)`

               +----------------+
               |  ProductDim    |
               | PK StockCode   |
               | Description    |
               | Category       |
               +--------+-------+
                        |
                        |
+----------------+      |     +----------------+
| CustomerDim    |      |     | TimeDim        |
| PK CustomerID  |      |     | PK TimeID      |
| Country        |      |     | InvoiceDate    |
| CustomerName   |      |     | Day, Month,... |
+--------+-------+      |     +--------+-------+
         |               |              |
         +---------------+--------------+
                         |
                 +-------+--------+
                 |   SalesFact    |
                 | PK SalesFactID |
                 | InvoiceNo      |
                 | FK StockCode   |
                 | FK CustomerID  |
                 | FK TimeID      |
                 | Quantity       |
                 | UnitPrice      |
                 | TotalSales     |
                 | Country        |
                 +----------------+


---

## ETL (Task 2)
`etl_retail.py`:
- Loads raw data, cleans it, calculates `TotalSales`
- Builds and loads `CustomerDim`, `ProductDim`, `TimeDim`, and `SalesFact` into `retail_dw.db`

**Run:**
```bash
pip install pandas openpyxl
python etl_retail.py
```

---

## OLAP Queries & Visualizations (Task 3)
`visualize_queries.py` connects to `retail_dw.db`, runs SQL queries, and creates PNGs.

### Queries:
1. **Total Sales by Country**
2. **Monthly Sales — United Kingdom**
3. **Top 10 Products by Sales**

**Run:**
```bash
pip install pandas matplotlib
python visualize_queries.py
```

---

## OLAP Analysis Report
The data warehouse created for this task contains transaction data from the **UCI Online Retail** dataset, covering sales between **December 2010 and December 2011**. Using OLAP queries, we analyzed:  
**(1)** total sales by country, **(2)** monthly sales trends for the United Kingdom, and **(3)** the top 10 products by sales.

From the total sales by country visualization, the **United Kingdom** dominates overall revenue, far exceeding other countries — indicating the retailer’s core market is domestic while international sales form a smaller share. The **monthly sales trend** for the UK shows a clear seasonal pattern with a strong **Q4 (Oct–Dec)** uplift, likely due to holiday shopping; smaller spikes likely align with promotions. The **top products** are largely gift and household items, suggesting consistent customer interest in these categories.

**Recommendations:**  
- Increase marketing and inventory ahead of Q4  
- Maintain sufficient stock of top-selling products  
- Evaluate targeted international growth

**Limitations:** Dataset is historical (2010–2011) and some categories/products may be obsolete. Integrating more recent data would improve relevance.

---

## License

[text](LICENSE)

## .gitignore

[text](.gitignore)