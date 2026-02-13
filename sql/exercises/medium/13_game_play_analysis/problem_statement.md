# Game Play Analysis IV - Medium

**Difficulty:** Medium
**Estimated Time:** 30 minutes
**Topics:** Self JOIN, First Login, Retention, ROUND

## Problem Description

Write a query to report the fraction of players who logged in again on the day after their first login, rounded to 2 decimal places. This is a basic "day 1 retention" metric.

## Requirements

1. Return a single value: fraction (rounded to 2 decimal places)
2. First, find each player's first login date
3. Then check if they logged in the very next day
4. Calculate: count of retained players / total players

## Schema

### Activity
| Column | Type |
|--------|------|
| player_id | INTEGER |
| device_id | INTEGER |
| event_date | DATE |
| games_played | INTEGER |

## Expected Output

| fraction |
|----------|
| ... |

## LeetCode Reference
Similar to: [Game Play Analysis IV](https://leetcode.com/problems/game-play-analysis-iv/) - LeetCode #550

## Hints

<details>
<summary>Hint 1</summary>
Use a CTE or subquery to find each player's first login date with MIN(event_date).
</details>

<details>
<summary>Hint 2</summary>
Check if there exists a record with event_date = first_login + 1 day for each player.
</details>

<details>
<summary>Hint 3</summary>
In SQLite, use DATE(first_date, '+1 day') to add one day.
</details>
