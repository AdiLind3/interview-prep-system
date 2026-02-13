# Find Customer Referee - Easy

**Difficulty:** Easy
**Estimated Time:** 10 minutes
**Topics:** NULL Handling, WHERE, NOT Equal

## Problem Description

Write a query to find the names of customers who are NOT referred by the customer with id = 2. Include customers who have no referee at all (NULL referee_id).

## Requirements

1. Return only the name column
2. Exclude customers whose referee_id is 2
3. Include customers with NULL referee_id
4. Order results by name ascending

## Schema

### Customer
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| name | TEXT |
| referee_id | INTEGER |

## Expected Output

| name |
|------|
| ... |

## LeetCode Reference
Similar to: [Find Customer Referee](https://leetcode.com/problems/find-customer-referee/) - LeetCode #584

## Hints

<details>
<summary>Hint 1</summary>
Be careful with NULL values. The expression referee_id != 2 does NOT include NULL rows.
</details>

<details>
<summary>Hint 2</summary>
Use (referee_id != 2 OR referee_id IS NULL) or COALESCE/IFNULL.
</details>

<details>
<summary>Hint 3</summary>
Alternatively: WHERE IFNULL(referee_id, 0) != 2
</details>
