# Rising Temperature - Easy

**Difficulty:** Easy
**Estimated Time:** 15 minutes
**Topics:** Self JOIN, Date Comparison

## Problem Description

Write a query to find all dates where the temperature was higher than the previous day's temperature. Return the id of those records.

## Requirements

1. Return the id of days where temperature is higher than the previous day
2. Use date comparison to find consecutive days
3. Order results by id ascending

## Schema

### Weather
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| recordDate | DATE |
| temperature | INTEGER |

## Expected Output

| id |
|----|
| ... |

## LeetCode Reference
Similar to: [Rising Temperature](https://leetcode.com/problems/rising-temperature/) - LeetCode #197

## Hints

<details>
<summary>Hint 1</summary>
Join the weather table with itself to compare each day with its previous day.
</details>

<details>
<summary>Hint 2</summary>
In SQLite, you can use DATE(w1.recordDate, '-1 day') to get the previous day.
</details>

<details>
<summary>Hint 3</summary>
Alternatively, use julianday() to calculate date differences.
</details>
