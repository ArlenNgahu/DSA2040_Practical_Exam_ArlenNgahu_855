-- 3. Top 10 Products by Sales
-- Purpose: Identify the best-selling products overall.
-- Helps in inventory planning and marketing.
SELECT pd.Description, SUM(sf.TotalSales) AS TotalSales
FROM SalesFact sf
JOIN ProductDim pd ON sf.StockCode = pd.StockCode
GROUP BY pd.Description
ORDER BY TotalSales DESC
LIMIT 10;