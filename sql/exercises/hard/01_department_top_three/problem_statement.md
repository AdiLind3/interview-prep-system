# Department Top Three Salaries - Hard

**Difficulty:** Hard
**Estimated Time:** 30 minutes
**Topics:** DENSE_RANK, PARTITION BY, Window Functions, JOIN

## Problem Description

Write a query to find employees who earn one of the top three unique salaries in each department. If a department has fewer than three unique salary levels, include all employees.

## Requirements

1. Return department name, employee name, and salary
2. Include employees in the top 3 distinct salary tiers per department
3. If multiple employees share a salary, include all of them
4. Order by department name ascending, then salary descending, then employee name ascending

## Schema

### Department
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| name | TEXT |

### Employee
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| name | TEXT |
| salary | INTEGER |
| departmentId | INTEGER (FK) |

## Expected Output

| department | employee | salary |
|------------|----------|--------|
| ... | ... | ... |

## LeetCode Reference
Similar to: [Department Top Three Salaries](https://leetcode.com/problems/department-top-three-salaries/) - LeetCode #185

## Hints

<details>
<summary>Hint 1</summary>
Use DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC) to rank salaries.
</details>

<details>
<summary>Hint 2</summary>
DENSE_RANK handles ties correctly - same salary gets same rank.
</details>

<details>
<summary>Hint 3</summary>
Filter for DENSE_RANK <= 3 to get top three salary tiers.
</details>

<details>
<summary>Hint 4</summary>
JOIN with department table to get department names.
</details>
