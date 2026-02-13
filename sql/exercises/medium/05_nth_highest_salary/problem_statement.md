# Nth Highest Salary - Medium

**Difficulty:** Medium
**Estimated Time:** 20 minutes
**Topics:** DISTINCT, LIMIT, OFFSET, Window Functions, Subquery

## Problem Description

Write a query to find the second highest distinct salary from the `employee` table. If there is no second highest salary, return NULL.

## Requirements

1. Return the second highest distinct salary (aliased as "SecondHighestSalary")
2. If there is no second highest salary, return NULL
3. Duplicate salaries should be treated as one

## Schema

### Employee
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| salary | INTEGER |

## Expected Output

| SecondHighestSalary |
|---------------------|
| ... |

## LeetCode Reference
Similar to: [Nth Highest Salary](https://leetcode.com/problems/nth-highest-salary/) - LeetCode #177

## Hints

<details>
<summary>Hint 1</summary>
Use DISTINCT to handle duplicate salaries first.
</details>

<details>
<summary>Hint 2</summary>
ORDER BY salary DESC LIMIT 1 OFFSET 1 gives the second highest.
</details>

<details>
<summary>Hint 3</summary>
Wrap in a subquery with IFNULL or use SELECT (subquery) to return NULL when no result.
</details>
