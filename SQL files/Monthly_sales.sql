-- 2. Monthly Sales for the United Kingdom
-- Purpose: Show how sales vary month-by-month for the UK.
-- Useful for identifying seasonal trends or sales patterns.
SELECT td.Year, td.Month, SUM(sf.TotalSales) AS MonthlySales
FROM SalesFact sf
JOIN TimeDim td ON sf.TimeID = td.TimeID
WHERE sf.Country = 'United Kingdom'
GROUP BY td.Year, td.Month
ORDER BY td.Year, td.Month;

