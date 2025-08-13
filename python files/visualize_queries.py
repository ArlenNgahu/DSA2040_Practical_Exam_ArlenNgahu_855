import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("retail_dw.db")

# -----------------------
# 1. Sales by Country
# -----------------------
query1 = """
SELECT Country, SUM(TotalSales) AS TotalSales
FROM SalesFact
GROUP BY Country
ORDER BY TotalSales DESC;
"""
df_country = pd.read_sql_query(query1, conn)
print("\n--- Sales by Country ---")
print(df_country.head())

plt.figure(figsize=(10,6))
plt.bar(df_country['Country'], df_country['TotalSales'], color='skyblue')
plt.xticks(rotation=90)
plt.xlabel("Country")
plt.ylabel("Total Sales")
plt.title("Total Sales by Country")
plt.tight_layout()
plt.savefig("chart_sales_by_country.png")
plt.close()

# -----------------------
# 2. Monthly Sales for UK
# -----------------------
query2 = """
SELECT td.Year AS Year, td.Month AS Month, SUM(sf.TotalSales) AS MonthlySales
FROM SalesFact sf
JOIN TimeDim td ON sf.TimeID = td.TimeID
WHERE sf.Country = 'United Kingdom'
GROUP BY td.Year, td.Month
ORDER BY td.Year, td.Month;
"""
df_uk = pd.read_sql_query(query2, conn)
print("\n--- Monthly Sales UK ---")
print(df_uk.head())

df_uk['YearMonth'] = df_uk['Year'].astype(str) + "-" + df_uk['Month'].astype(str).str.zfill(2)
plt.figure(figsize=(12,6))
plt.plot(df_uk['YearMonth'], df_uk['MonthlySales'], marker='o', color='orange')
plt.xticks(rotation=45)
plt.xlabel("Month")
plt.ylabel("Monthly Sales")
plt.title("Monthly Sales - United Kingdom")
plt.tight_layout()
plt.savefig("chart_monthly_sales_uk.png")
plt.close()

# -----------------------
# 3. Top 10 Products by Sales
# -----------------------
query3 = """
SELECT pd.Description AS Description, SUM(sf.TotalSales) AS TotalSales
FROM SalesFact sf
JOIN ProductDim pd ON sf.StockCode = pd.StockCode
GROUP BY pd.Description
ORDER BY TotalSales DESC
LIMIT 10;
"""
df_products = pd.read_sql_query(query3, conn)
print("\n--- Top 10 Products ---")
print(df_products.head())

plt.figure(figsize=(10,6))
plt.barh(df_products['Description'], df_products['TotalSales'], color='green')
plt.xlabel("Total Sales")
plt.ylabel("Product Description")
plt.title("Top 10 Products by Sales")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("chart_top10_products.png")
plt.close()

conn.close()
print("\nCharts saved as: chart_sales_by_country.png, chart_monthly_sales_uk.png, chart_top10_products.png")
