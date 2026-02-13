# Managers with at Least Five Direct Reports - Medium

**Difficulty:** Medium
**Estimated Time:** 15 minutes
**Topics:** Self JOIN, GROUP BY, HAVING, COUNT

## Problem Description

Write a query to find managers who have at least five direct reports. A manager is someone whose id appears as the managerId of at least five other employees.

## Requirements

1. Return the name of managers with 5 or more direct reports
2. Order results by name ascending

## Schema

### Employee
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| name | TEXT |
| department | TEXT |
| managerId | INTEGER |

## Expected Output

| name |
|------|
| ... |

## LeetCode Reference
Similar to: [Managers with at Least Five Direct Reports](https://leetcode.com/problems/managers-with-at-least-five-direct-reports/) - LeetCode #570

## Hints

<details>
<summary>Hint 1</summary>
Count how many employees report to each manager using GROUP BY managerId.
</details>

<details>
<summary>Hint 2</summary>
Use HAVING COUNT(*) >= 5 to filter managers with enough reports.
</details>

<details>
<summary>Hint 3</summary>
Join back with the employee table to get the manager's name.
</details>
