# Employee Bonus - Easy

**Difficulty:** Easy
**Estimated Time:** 10 minutes
**Topics:** LEFT JOIN, NULL Check

## Problem Description

You have two tables: `employee` and `bonus`. Write a query to report the name and bonus amount of each employee whose bonus is less than 1000, or who has no bonus at all.

## Requirements

1. Return employee name and bonus amount
2. Include employees with bonus less than 1000
3. Include employees who have no bonus record (show NULL for bonus)
4. Order results by name ascending

## Schema

### Employee
| Column | Type |
|--------|------|
| empId | INTEGER PRIMARY KEY |
| name | TEXT |
| supervisor | INTEGER |
| salary | INTEGER |

### Bonus
| Column | Type |
|--------|------|
| empId | INTEGER PRIMARY KEY |
| bonus | INTEGER |

## Expected Output

| name | bonus |
|------|-------|
| ... | ... |

## LeetCode Reference
Similar to: [Employee Bonus](https://leetcode.com/problems/employee-bonus/) - LeetCode #577

## Hints

<details>
<summary>Hint 1</summary>
Use LEFT JOIN to keep employees even if they have no bonus record.
</details>

<details>
<summary>Hint 2</summary>
Remember that NULL values need special handling - NULL < 1000 evaluates to NULL, not TRUE.
</details>

<details>
<summary>Hint 3</summary>
Use (bonus < 1000 OR bonus IS NULL) in your WHERE clause.
</details>
