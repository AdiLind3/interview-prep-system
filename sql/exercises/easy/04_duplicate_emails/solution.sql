-- Solution: Duplicate Emails
SELECT
    email
FROM person
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY email;
