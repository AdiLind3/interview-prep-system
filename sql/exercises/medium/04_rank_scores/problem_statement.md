# Rank Scores - Medium

**Difficulty:** Medium
**Estimated Time:** 15 minutes
**Topics:** DENSE_RANK, Window Functions, ORDER BY

## Problem Description

Write a query to rank scores. The ranking should be continuous (no gaps). If two scores are the same, they should have the same ranking, and the next ranking should be the next consecutive integer.

## Requirements

1. Return score and rank (aliased as "dense_rank")
2. Use dense ranking (no gaps between ranks)
3. Order by score descending

## Schema

### Scores
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| score | REAL |

## Expected Output

| score | dense_rank |
|-------|------------|
| ... | ... |

## LeetCode Reference
Similar to: [Rank Scores](https://leetcode.com/problems/rank-scores/) - LeetCode #178

## Hints

<details>
<summary>Hint 1</summary>
Use the DENSE_RANK() window function.
</details>

<details>
<summary>Hint 2</summary>
DENSE_RANK() OVER (ORDER BY score DESC) gives continuous ranking.
</details>

<details>
<summary>Hint 3</summary>
DENSE_RANK differs from RANK in that it does not skip numbers after ties.
</details>
