# Exchange Seats - Medium

**Difficulty:** Medium
**Estimated Time:** 20 minutes
**Topics:** CASE WHEN, MOD, Odd/Even Logic

## Problem Description

Write a query to swap the seat ids of every two consecutive students. If the number of students is odd, the last student's id stays the same.

## Requirements

1. Return id and student name
2. Swap adjacent ids: 1<->2, 3<->4, 5<->6, etc.
3. If total count is odd, the last student keeps their id
4. Order by id ascending

## Schema

### Seat
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| student | TEXT |

## Expected Output

| id | student |
|----|---------|
| ... | ... |

## LeetCode Reference
Similar to: [Exchange Seats](https://leetcode.com/problems/exchange-seats/) - LeetCode #626

## Hints

<details>
<summary>Hint 1</summary>
Use CASE WHEN with MOD (or %) to check if id is odd or even.
</details>

<details>
<summary>Hint 2</summary>
If id is odd, set new id = id + 1. If even, set new id = id - 1.
</details>

<details>
<summary>Hint 3</summary>
Handle the edge case where the last student has an odd id (use a subquery to get total count).
</details>
