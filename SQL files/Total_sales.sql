-- 1. Total Sales by Country
-- Purpose: Summarize total sales across all years for each country.
-- Good for a bar chart comparing countries.
SELECT Country, SUM(TotalSales) AS TotalSales
FROM SalesFact
GROUP BY Country
ORDER BY TotalSales DESC;