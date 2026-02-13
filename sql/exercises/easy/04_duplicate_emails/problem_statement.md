# Duplicate Emails - Easy

**Difficulty:** Easy
**Estimated Time:** 10 minutes
**Topics:** GROUP BY, HAVING, COUNT

## Problem Description

Write a query to find all duplicate email addresses in the `person` table. An email is considered duplicate if it appears more than once.

## Requirements

1. Return only the email column
2. Only include emails that appear more than once
3. Order results by email ascending

## Schema

### Person
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| email | TEXT |

## Expected Output

| email |
|-------|
| ... |

## LeetCode Reference
Similar to: [Duplicate Emails](https://leetcode.com/problems/duplicate-emails/) - LeetCode #182

## Hints

<details>
<summary>Hint 1</summary>
Use GROUP BY to group rows by email address.
</details>

<details>
<summary>Hint 2</summary>
Use HAVING with COUNT() to filter groups that have more than one row.
</details>
