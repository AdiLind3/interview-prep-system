-- Solution: Department Top Three Salaries
WITH ranked AS (
    SELECT
        e.id,
        e.name AS employee,
        e.salary,
        e.departmentId,
        d.name AS department,
        DENSE_RANK() OVER (PARTITION BY e.departmentId ORDER BY e.salary DESC) AS salary_rank
    FROM employee e
    INNER JOIN department d ON e.departmentId = d.id
)
SELECT
    department,
    employee,
    salary
FROM ranked
WHERE salary_rank <= 3
ORDER BY department, salary DESC, employee;
