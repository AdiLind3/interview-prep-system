# Big Countries - Easy

**Difficulty:** Easy
**Estimated Time:** 5 minutes
**Topics:** WHERE, OR, Basic Filtering

## Problem Description

A country is considered "big" if it has an area of at least 3,000,000 square kilometers, or it has a population of at least 25,000,000. Write a query to find the name, population, and area of all big countries.

## Requirements

1. Return name, population, and area
2. Include countries with area >= 3000000 OR population >= 25000000
3. Order results by name ascending

## Schema

### World
| Column | Type |
|--------|------|
| name | TEXT PRIMARY KEY |
| continent | TEXT |
| area | INTEGER |
| population | INTEGER |
| gdp | INTEGER |

## Expected Output

| name | population | area |
|------|------------|------|
| ... | ... | ... |

## LeetCode Reference
Similar to: [Big Countries](https://leetcode.com/problems/big-countries/) - LeetCode #595

## Hints

<details>
<summary>Hint 1</summary>
Use the WHERE clause with OR to check multiple conditions.
</details>

<details>
<summary>Hint 2</summary>
You can also use UNION to combine results from two separate queries.
</details>
