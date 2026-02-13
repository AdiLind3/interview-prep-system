# Confirmation Rate - Medium

**Difficulty:** Medium
**Estimated Time:** 20 minutes
**Topics:** LEFT JOIN, AVG, CASE WHEN, ROUND

## Problem Description

Write a query to find the confirmation rate for each user. The confirmation rate is the number of 'confirmed' messages divided by the total number of confirmation requests. If a user has no requests, their rate is 0.00. Round to 2 decimal places.

## Requirements

1. Return user_id and confirmation_rate
2. Rate = confirmed messages / total messages (or 0.00 if no messages)
3. Round to 2 decimal places
4. Order by user_id ascending

## Schema

### Signups
| Column | Type |
|--------|------|
| user_id | INTEGER PRIMARY KEY |
| time_stamp | DATETIME |

### Confirmations
| Column | Type |
|--------|------|
| user_id | INTEGER |
| time_stamp | DATETIME |
| action | TEXT |

## Expected Output

| user_id | confirmation_rate |
|---------|-------------------|
| ... | ... |

## LeetCode Reference
Similar to: [Confirmation Rate](https://leetcode.com/problems/confirmation-rate/) - LeetCode #1934

## Hints

<details>
<summary>Hint 1</summary>
LEFT JOIN signups with confirmations to keep all users.
</details>

<details>
<summary>Hint 2</summary>
Use AVG(CASE WHEN action = 'confirmed' THEN 1.0 ELSE 0.0 END) for the rate.
</details>

<details>
<summary>Hint 3</summary>
Use IFNULL or COALESCE to handle users with no confirmation requests (return 0.00).
</details>
