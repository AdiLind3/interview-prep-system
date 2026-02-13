# Invalid Tweets - Easy

**Difficulty:** Easy
**Estimated Time:** 5 minutes
**Topics:** LENGTH, String Functions, WHERE

## Problem Description

Write a query to find the IDs of tweets that are invalid. A tweet is invalid if the number of characters in the content exceeds 140.

## Requirements

1. Return only the tweet_id column
2. Include only tweets where content length is strictly greater than 140
3. Order results by tweet_id ascending

## Schema

### Tweets
| Column | Type |
|--------|------|
| tweet_id | INTEGER PRIMARY KEY |
| content | TEXT |

## Expected Output

| tweet_id |
|----------|
| ... |

## LeetCode Reference
Similar to: [Invalid Tweets](https://leetcode.com/problems/invalid-tweets/) - LeetCode #1683

## Hints

<details>
<summary>Hint 1</summary>
Use the LENGTH() function to count characters in the content.
</details>

<details>
<summary>Hint 2</summary>
Filter with WHERE LENGTH(content) > 140.
</details>
