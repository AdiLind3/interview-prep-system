# Monthly Transactions I - Medium

**Difficulty:** Medium
**Estimated Time:** 25 minutes
**Topics:** GROUP BY, CASE WHEN, Date Functions, Aggregation

## Problem Description

Write a query to find for each month and country: the number of transactions, the number of approved transactions, the total amount, and the total approved amount.

## Requirements

1. Return month, country, trans_count, approved_count, trans_total_amount, approved_total_amount
2. Month should be formatted as YYYY-MM
3. Group by month and country
4. Order by month, then country

## Schema

### Transactions
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| country | TEXT |
| state | TEXT |
| amount | INTEGER |
| trans_date | DATE |

## Expected Output

| month | country | trans_count | approved_count | trans_total_amount | approved_total_amount |
|-------|---------|-------------|----------------|--------------------|-----------------------|
| ... | ... | ... | ... | ... | ... |

## LeetCode Reference
Similar to: [Monthly Transactions I](https://leetcode.com/problems/monthly-transactions-i/) - LeetCode #1193

## Hints

<details>
<summary>Hint 1</summary>
Use STRFTIME('%Y-%m', trans_date) to extract year-month in SQLite.
</details>

<details>
<summary>Hint 2</summary>
Use SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) for approved count.
</details>

<details>
<summary>Hint 3</summary>
Similarly use CASE WHEN inside SUM for approved amounts.
</details>
