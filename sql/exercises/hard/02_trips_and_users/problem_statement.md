# Trips and Users - Hard

**Difficulty:** Hard
**Estimated Time:** 35 minutes
**Topics:** JOIN, CASE WHEN, GROUP BY, Date Filtering, Multiple Conditions

## Problem Description

Write a query to find the cancellation rate of ride requests with unbanned users (both client and driver must not be banned) for each day between '2024-10-01' and '2024-10-03'. The cancellation rate is the number of cancelled requests divided by total requests, rounded to 2 decimal places.

## Requirements

1. Return day and cancellation_rate (rounded to 2 decimal places)
2. Only include trips where both client AND driver are not banned
3. Only include days between '2024-10-01' and '2024-10-03' (inclusive)
4. A trip is cancelled if status starts with 'cancelled'
5. Order by day ascending

## Schema

### Trips
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| client_id | INTEGER |
| driver_id | INTEGER |
| city_id | INTEGER |
| status | TEXT |
| request_at | DATE |

### Users
| Column | Type |
|--------|------|
| users_id | INTEGER PRIMARY KEY |
| banned | TEXT |
| role | TEXT |

## Expected Output

| day | cancellation_rate |
|-----|-------------------|
| ... | ... |

## LeetCode Reference
Similar to: [Trips and Users](https://leetcode.com/problems/trips-and-users/) - LeetCode #262

## Hints

<details>
<summary>Hint 1</summary>
Join trips with users table twice: once for client, once for driver.
</details>

<details>
<summary>Hint 2</summary>
Filter WHERE both client.banned = 'No' AND driver.banned = 'No'.
</details>

<details>
<summary>Hint 3</summary>
Use SUM(CASE WHEN status LIKE 'cancelled%' THEN 1.0 ELSE 0.0 END) / COUNT(*) for the rate.
</details>
