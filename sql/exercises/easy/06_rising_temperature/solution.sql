-- Solution: Rising Temperature
SELECT
    w1.id
FROM weather w1
INNER JOIN weather w2
    ON DATE(w1.recordDate) = DATE(w2.recordDate, '+1 day')
WHERE w1.temperature > w2.temperature
ORDER BY w1.id;
