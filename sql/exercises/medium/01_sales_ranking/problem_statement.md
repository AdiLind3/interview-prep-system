# Sales Ranking by Department - Medium

**Difficulty:** Medium
**Estimated Time:** 25 minutes
**Topics:** Window Functions, ROW_NUMBER, PARTITION BY

## Problem Description

You are analyzing employee sales performance across different departments. Write a query that ranks employees by their total sales within each department and shows their sales growth compared to the previous period.

## Requirements

1. Calculate total sales for each employee
2. Rank employees within their department (highest sales = rank 1)
3. Calculate the sales growth from the previous month using LAG()
4. Only include employees with sales > 0
5. Order by department, then by rank

## Schema

### Employees
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| name | TEXT |
| department | TEXT |

### Sales
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| employee_id | INTEGER (FK) |
| month | TEXT |
| amount | DECIMAL |

## Expected Output

| employee_id | name | department | total_sales | rank_in_dept | prev_month_sales | growth |
|-------------|------|------------|-------------|--------------|------------------|--------|
| ... | ... | ... | ... | ... | ... | ... |

## LeetCode Reference
Similar to: [Rank Scores](https://leetcode.com/problems/rank-scores/) - LeetCode #178 (uses similar window function concepts)

## Hints

<details>
<summary>Hint 1</summary>
Use ROW_NUMBER() OVER (PARTITION BY department ORDER BY total_sales DESC) for ranking.
</details>

<details>
<summary>Hint 2</summary>
You'll need a subquery or CTE to first aggregate total sales per employee.
</details>

<details>
<summary>Hint 3</summary>
LAG() can access the previous row's value: LAG(amount, 1) OVER (PARTITION BY employee_id ORDER BY month)
</details>

<details>
<summary>Hint 4</summary>
Growth calculation: current_amount - prev_amount (or calculate percentage)
</details>
