# Human Traffic of Stadium - Hard

**Difficulty:** Hard
**Estimated Time:** 40 minutes
**Topics:** Consecutive Rows, Self JOIN, Window Functions, Complex Filtering

## Problem Description

Write a query to display records from the stadium table where there are three or more consecutive rows with people >= 100. Return all the rows that are part of such consecutive groups.

## Requirements

1. Return id, visit_date, and people
2. Only include rows that are part of 3+ consecutive rows with people >= 100
3. The rows are considered consecutive based on id values
4. Order by visit_date ascending

## Schema

### Stadium
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| visit_date | DATE |
| people | INTEGER |

## Expected Output

| id | visit_date | people |
|----|------------|--------|
| ... | ... | ... |

## LeetCode Reference
Similar to: [Human Traffic of Stadium](https://leetcode.com/problems/human-traffic-of-stadium/) - LeetCode #601

## Hints

<details>
<summary>Hint 1</summary>
First, identify rows where people >= 100.
</details>

<details>
<summary>Hint 2</summary>
Use a technique to identify consecutive groups: row_number vs id difference stays constant for consecutive rows.
</details>

<details>
<summary>Hint 3</summary>
Group by the difference and count groups with 3+ members.
</details>

<details>
<summary>Hint 4</summary>
Alternatively, self-join three times to find any row that is part of a consecutive triple.
</details>
