# SQL Cheat Sheet for Interview Prep

## Table of Contents
- [JOIN Types](#join-types)
- [Window Functions](#window-functions)
- [Common Table Expressions (CTEs)](#common-table-expressions-ctes)
- [Aggregation Functions](#aggregation-functions)
- [Date/Time Functions](#datetime-functions)
- [String Functions](#string-functions)
- [Subqueries](#subqueries)
- [Performance Tips](#performance-tips)

---

## JOIN Types

### INNER JOIN
Returns only matching rows from both tables.
```sql
SELECT a.*, b.*
FROM table_a a
INNER JOIN table_b b ON a.id = b.a_id;
```

### LEFT JOIN
Returns all rows from left table, matched rows from right (NULL if no match).
```sql
SELECT a.*, b.*
FROM table_a a
LEFT JOIN table_b b ON a.id = b.a_id;
```

### RIGHT JOIN
Returns all rows from right table, matched rows from left (NULL if no match).
```sql
SELECT a.*, b.*
FROM table_a a
RIGHT JOIN table_b b ON a.id = b.a_id;
```

### FULL OUTER JOIN
Returns all rows from both tables (NULL where no match).
```sql
SELECT a.*, b.*
FROM table_a a
FULL OUTER JOIN table_b b ON a.id = b.a_id;
```

### CROSS JOIN
Cartesian product of both tables.
```sql
SELECT a.*, b.*
FROM table_a a
CROSS JOIN table_b b;
```

### SELF JOIN
Join table to itself.
```sql
SELECT e1.name AS employee, e2.name AS manager
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.id;
```

### Finding Non-Matching Rows
```sql
-- Rows in A but not in B
SELECT a.*
FROM table_a a
LEFT JOIN table_b b ON a.id = b.a_id
WHERE b.a_id IS NULL;
```

---

## Window Functions

### Basic Syntax
```sql
<function> OVER (
    [PARTITION BY column]
    [ORDER BY column]
    [ROWS or RANGE frame]
)
```

### ROW_NUMBER()
Assigns unique sequential integer to rows.
```sql
SELECT
    name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as row_num
FROM employees;
```

### RANK() vs DENSE_RANK()
- `RANK()`: Skips numbers after ties (1, 2, 2, 4)
- `DENSE_RANK()`: No gaps (1, 2, 2, 3)

```sql
SELECT
    name,
    score,
    RANK() OVER (ORDER BY score DESC) as rank,
    DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank
FROM students;
```

### LAG() and LEAD()
Access previous/next row values.
```sql
SELECT
    date,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY date) as prev_revenue,
    LEAD(revenue, 1) OVER (ORDER BY date) as next_revenue,
    revenue - LAG(revenue, 1) OVER (ORDER BY date) as growth
FROM daily_sales;
```

### NTILE()
Distribute rows into N buckets.
```sql
SELECT
    name,
    salary,
    NTILE(4) OVER (ORDER BY salary) as quartile
FROM employees;
```

### Running Totals
```sql
SELECT
    date,
    amount,
    SUM(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total
FROM transactions;
```

### Moving Averages
```sql
SELECT
    date,
    value,
    AVG(value) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7day
FROM metrics;
```

---

## Common Table Expressions (CTEs)

### Basic CTE
```sql
WITH high_earners AS (
    SELECT * FROM employees WHERE salary > 100000
)
SELECT department, COUNT(*) as count
FROM high_earners
GROUP BY department;
```

### Multiple CTEs
```sql
WITH
sales_summary AS (
    SELECT customer_id, SUM(amount) as total_sales
    FROM orders
    GROUP BY customer_id
),
top_customers AS (
    SELECT customer_id, total_sales
    FROM sales_summary
    WHERE total_sales > 10000
)
SELECT c.name, tc.total_sales
FROM top_customers tc
JOIN customers c ON tc.customer_id = c.id;
```

### Recursive CTE
```sql
-- Find all subordinates of a manager
WITH RECURSIVE employee_hierarchy AS (
    -- Base case: Start with manager
    SELECT id, name, manager_id, 0 as level
    FROM employees
    WHERE id = 1

    UNION ALL

    -- Recursive case: Find direct reports
    SELECT e.id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT * FROM employee_hierarchy;
```

---

## Aggregation Functions

### Basic Aggregations
```sql
SELECT
    department,
    COUNT(*) as employee_count,
    COUNT(DISTINCT role) as unique_roles,
    AVG(salary) as avg_salary,
    MIN(salary) as min_salary,
    MAX(salary) as max_salary,
    SUM(salary) as total_salary
FROM employees
GROUP BY department;
```

### GROUP BY with HAVING
```sql
SELECT
    department,
    AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 75000;
```

### GROUP BY Multiple Columns
```sql
SELECT
    department,
    job_title,
    COUNT(*) as count
FROM employees
GROUP BY department, job_title;
```

### Conditional Aggregation
```sql
SELECT
    department,
    COUNT(CASE WHEN gender = 'F' THEN 1 END) as female_count,
    COUNT(CASE WHEN gender = 'M' THEN 1 END) as male_count,
    AVG(CASE WHEN seniority = 'Senior' THEN salary END) as avg_senior_salary
FROM employees
GROUP BY department;
```

---

## Date/Time Functions

### Current Date/Time
```sql
SELECT
    CURRENT_DATE as today,
    CURRENT_TIMESTAMP as now,
    DATE('2024-01-15') as specific_date;
```

### Date Arithmetic
```sql
SELECT
    date_column,
    DATE(date_column, '+7 days') as next_week,
    DATE(date_column, '-1 month') as last_month,
    DATE(date_column, 'start of month') as month_start;
```

### Date Parts
```sql
SELECT
    date_column,
    strftime('%Y', date_column) as year,
    strftime('%m', date_column) as month,
    strftime('%d', date_column) as day,
    strftime('%w', date_column) as day_of_week,
    strftime('%W', date_column) as week_of_year;
```

### Date Differences
```sql
SELECT
    JULIANDAY(end_date) - JULIANDAY(start_date) as days_between;
```

---

## String Functions

### Case Conversion
```sql
SELECT
    UPPER(name) as uppercase,
    LOWER(name) as lowercase;
```

### Concatenation
```sql
SELECT
    first_name || ' ' || last_name as full_name,
    CONCAT(first_name, ' ', last_name) as full_name_v2;
```

### Substring
```sql
SELECT
    SUBSTR(text, 1, 10) as first_10_chars,
    SUBSTR(text, -5) as last_5_chars;
```

### Pattern Matching
```sql
-- LIKE patterns
SELECT * FROM users WHERE email LIKE '%@gmail.com';
SELECT * FROM products WHERE name LIKE 'Phone%';
SELECT * FROM codes WHERE code LIKE '___-___';  -- Exactly 7 chars with dash

-- GLOB patterns (case-sensitive)
SELECT * FROM files WHERE name GLOB '*.txt';
```

### String Functions
```sql
SELECT
    LENGTH(text) as char_count,
    TRIM(text) as trimmed,
    LTRIM(text) as left_trimmed,
    RTRIM(text) as right_trimmed,
    REPLACE(text, 'old', 'new') as replaced;
```

---

## Subqueries

### Subquery in SELECT
```sql
SELECT
    name,
    salary,
    (SELECT AVG(salary) FROM employees) as company_avg,
    salary - (SELECT AVG(salary) FROM employees) as diff_from_avg
FROM employees;
```

### Subquery in WHERE
```sql
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

### Subquery in FROM
```sql
SELECT dept, avg_salary
FROM (
    SELECT department as dept, AVG(salary) as avg_salary
    FROM employees
    GROUP BY department
) subquery
WHERE avg_salary > 80000;
```

### Correlated Subquery
```sql
SELECT name, salary, department
FROM employees e1
WHERE salary = (
    SELECT MAX(salary)
    FROM employees e2
    WHERE e2.department = e1.department
);
```

### EXISTS
```sql
SELECT c.name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);
```

### IN with Subquery
```sql
SELECT name
FROM employees
WHERE department_id IN (
    SELECT id FROM departments WHERE location = 'New York'
);
```

---

## Performance Tips

### 1. Use Indexes
```sql
CREATE INDEX idx_employee_department ON employees(department);
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
```

### 2. Avoid SELECT *
```sql
-- Bad
SELECT * FROM large_table;

-- Good
SELECT id, name, email FROM users;
```

### 3. Use LIMIT for Testing
```sql
SELECT * FROM large_table LIMIT 100;
```

### 4. Filter Early
```sql
-- Good: Filter in WHERE before JOIN
SELECT o.*, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.order_date >= '2024-01-01';
```

### 5. Use EXISTS Instead of IN for Large Sets
```sql
-- Better performance for large subquery results
SELECT name
FROM employees e
WHERE EXISTS (
    SELECT 1 FROM large_table l WHERE l.employee_id = e.id
);
```

### 6. UNION ALL vs UNION
```sql
-- UNION removes duplicates (slower)
SELECT id FROM table1 UNION SELECT id FROM table2;

-- UNION ALL keeps all rows (faster)
SELECT id FROM table1 UNION ALL SELECT id FROM table2;
```

### 7. Use CTEs for Readability
CTEs make complex queries more maintainable and sometimes enable better query planning.

---

## Query Execution Order

Remember the logical order of SQL operations:

1. **FROM** + **JOINs** - Determine table sources
2. **WHERE** - Filter rows
3. **GROUP BY** - Group rows
4. **HAVING** - Filter groups
5. **SELECT** - Compute expressions
6. **DISTINCT** - Remove duplicates
7. **ORDER BY** - Sort results
8. **LIMIT/OFFSET** - Paginate results

---

## Common Patterns

### Top N per Group
```sql
WITH ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
    FROM employees
)
SELECT * FROM ranked WHERE rn <= 3;
```

### Pivot Data
```sql
SELECT
    product,
    SUM(CASE WHEN quarter = 'Q1' THEN sales ELSE 0 END) as Q1,
    SUM(CASE WHEN quarter = 'Q2' THEN sales ELSE 0 END) as Q2,
    SUM(CASE WHEN quarter = 'Q3' THEN sales ELSE 0 END) as Q3,
    SUM(CASE WHEN quarter = 'Q4' THEN sales ELSE 0 END) as Q4
FROM sales
GROUP BY product;
```

### Cumulative Sum
```sql
SELECT
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as cumulative_total
FROM transactions
ORDER BY date;
```

### Gap Analysis
```sql
-- Find missing IDs
SELECT a.id + 1 as missing_id
FROM sequence_table a
LEFT JOIN sequence_table b ON a.id + 1 = b.id
WHERE b.id IS NULL;
```
