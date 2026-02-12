-- Solution: Sales Ranking by Department with Window Functions
WITH employee_totals AS (
    SELECT
        e.id as employee_id,
        e.name,
        e.department,
        SUM(s.amount) as total_sales
    FROM employees e
    INNER JOIN sales s ON e.id = s.employee_id
    GROUP BY e.id, e.name, e.department
    HAVING total_sales > 0
)
SELECT
    employee_id,
    name,
    department,
    total_sales,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY total_sales DESC) as rank_in_dept
FROM employee_totals
ORDER BY department, rank_in_dept;
