-- Solution: Median Employee Salary
WITH ranked AS (
    SELECT
        id,
        company,
        salary,
        ROW_NUMBER() OVER (PARTITION BY company ORDER BY salary, id) AS rn,
        COUNT(*) OVER (PARTITION BY company) AS cnt
    FROM employee
)
SELECT
    id,
    company,
    salary
FROM ranked
WHERE rn BETWEEN (cnt + 1) / 2 AND (cnt + 2) / 2
ORDER BY company, salary;
