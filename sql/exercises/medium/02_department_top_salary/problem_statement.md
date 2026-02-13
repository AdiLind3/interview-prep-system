# Department Highest Salary - Medium

**Difficulty:** Medium
**Estimated Time:** 20 minutes
**Topics:** JOIN, Subquery, MAX, GROUP BY

## Problem Description

Write a query to find employees who have the highest salary in each department. If multiple employees share the highest salary in a department, include all of them.

## Requirements

1. Return department name, employee name, and salary
2. Only include employees whose salary is the maximum in their department
3. Order by department name ascending

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
Similar to: [Department Highest Salary](https://leetcode.com/problems/department-highest-salary/) - LeetCode #184

## Hints

<details>
<summary>Hint 1</summary>
First find the maximum salary per department using a subquery or CTE.
</details>

<details>
<summary>Hint 2</summary>
Join employees with departments and filter where salary matches the department max.
</details>

<details>
<summary>Hint 3</summary>
Use (departmentId, salary) IN (SELECT departmentId, MAX(salary)...) pattern.
</details>
