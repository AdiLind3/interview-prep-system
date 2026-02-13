-- Solution: Managers with at Least Five Direct Reports
SELECT
    e.name
FROM employee e
INNER JOIN (
    SELECT managerId
    FROM employee
    WHERE managerId IS NOT NULL
    GROUP BY managerId
    HAVING COUNT(*) >= 5
) m ON e.id = m.managerId
ORDER BY e.name;
