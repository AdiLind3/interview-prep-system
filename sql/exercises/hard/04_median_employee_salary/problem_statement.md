# Median Employee Salary - Hard

**Difficulty:** Hard
**Estimated Time:** 35 minutes
**Topics:** Window Functions, ROW_NUMBER, COUNT, Median Calculation

## Problem Description

Write a query to find the median salary for each company. The median is the middle value when salaries are sorted. If there is an even number of employees, return both middle values.

## Requirements

1. Return id, company, and salary for employees whose salary is the median in their company
2. For odd count: return the single middle value
3. For even count: return both middle values
4. Order by company ascending, then salary ascending

## Schema

### Employee
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| company | TEXT |
| salary | INTEGER |

## Expected Output

| id | company | salary |
|----|---------|--------|
| ... | ... | ... |

## LeetCode Reference
Similar to: [Median Employee Salary](https://leetcode.com/problems/median-employee-salary/) - LeetCode #569

## Hints

<details>
<summary>Hint 1</summary>
Use ROW_NUMBER() to rank employees by salary within each company.
</details>

<details>
<summary>Hint 2</summary>
Use COUNT() OVER to get total employees per company.
</details>

<details>
<summary>Hint 3</summary>
The median position(s): for count n, the median rows are at positions FLOOR((n+1)/2) and CEIL((n+1)/2).
</details>

<details>
<summary>Hint 4</summary>
Filter where row_number is between those two positions (they are the same for odd n).
</details>
