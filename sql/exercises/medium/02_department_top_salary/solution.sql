-- Solution: Department Highest Salary
SELECT
    d.name AS department,
    e.name AS employee,
    e.salary
FROM employee e
INNER JOIN department d ON e.departmentId = d.id
WHERE (e.departmentId, e.salary) IN (
    SELECT departmentId, MAX(salary)
    FROM employee
    GROUP BY departmentId
)
ORDER BY d.name;
