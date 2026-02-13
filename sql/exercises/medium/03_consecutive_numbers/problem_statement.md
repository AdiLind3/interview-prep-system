# Consecutive Numbers - Medium

**Difficulty:** Medium
**Estimated Time:** 20 minutes
**Topics:** Self JOIN, LAG/LEAD, Consecutive Pattern

## Problem Description

Write a query to find all numbers that appear at least three times consecutively in the `logs` table. The rows are ordered by id.

## Requirements

1. Return distinct numbers that appear at least 3 times consecutively (aliased as "ConsecutiveNums")
2. Consecutive means the id values are sequential (id, id+1, id+2) with the same num
3. Order results by ConsecutiveNums ascending

## Schema

### Logs
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| num | INTEGER |

## Expected Output

| ConsecutiveNums |
|-----------------|
| ... |

## LeetCode Reference
Similar to: [Consecutive Numbers](https://leetcode.com/problems/consecutive-numbers/) - LeetCode #180

## Hints

<details>
<summary>Hint 1</summary>
Join the logs table with itself three times on consecutive ids.
</details>

<details>
<summary>Hint 2</summary>
l1.id = l2.id - 1 AND l2.id = l3.id - 1 AND l1.num = l2.num AND l2.num = l3.num
</details>

<details>
<summary>Hint 3</summary>
Alternatively, use LAG() and LEAD() window functions.
</details>
