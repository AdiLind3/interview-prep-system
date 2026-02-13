-- Solution: Human Traffic of Stadium
WITH high_traffic AS (
    SELECT
        id,
        visit_date,
        people,
        id - ROW_NUMBER() OVER (ORDER BY id) AS grp
    FROM stadium
    WHERE people >= 100
),
consecutive_groups AS (
    SELECT grp
    FROM high_traffic
    GROUP BY grp
    HAVING COUNT(*) >= 3
)
SELECT
    h.id,
    h.visit_date,
    h.people
FROM high_traffic h
INNER JOIN consecutive_groups c ON h.grp = c.grp
ORDER BY h.visit_date;
