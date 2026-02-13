# Article Views I - Easy

**Difficulty:** Easy
**Estimated Time:** 10 minutes
**Topics:** DISTINCT, Self-Referencing, WHERE

## Problem Description

Write a query to find all authors who viewed their own articles. Return the distinct author ids, sorted in ascending order.

## Requirements

1. Return distinct author_id (aliased as "id")
2. An author views their own article when author_id = viewer_id
3. Order results by id ascending

## Schema

### Views
| Column | Type |
|--------|------|
| article_id | INTEGER |
| author_id | INTEGER |
| viewer_id | INTEGER |
| view_date | DATE |

## Expected Output

| id |
|----|
| ... |

## LeetCode Reference
Similar to: [Article Views I](https://leetcode.com/problems/article-views-i/) - LeetCode #1148

## Hints

<details>
<summary>Hint 1</summary>
Compare author_id with viewer_id to find self-views.
</details>

<details>
<summary>Hint 2</summary>
Use DISTINCT to remove duplicate author ids.
</details>
