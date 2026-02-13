# Recyclable and Low Fat Products - Easy

**Difficulty:** Easy
**Estimated Time:** 5 minutes
**Topics:** WHERE, AND, Basic Filtering

## Problem Description

Write a query to find the ids of products that are both low fat and recyclable.

## Requirements

1. Return only the product_id column
2. Include products where low_fats = 'Y' AND is_recyclable = 'Y'
3. Order results by product_id ascending

## Schema

### Products
| Column | Type |
|--------|------|
| product_id | INTEGER PRIMARY KEY |
| low_fats | TEXT |
| is_recyclable | TEXT |

## Expected Output

| product_id |
|------------|
| ... |

## LeetCode Reference
Similar to: [Recyclable and Low Fat Products](https://leetcode.com/problems/recyclable-and-low-fat-products/) - LeetCode #1757

## Hints

<details>
<summary>Hint 1</summary>
Use WHERE with the AND operator to filter on two conditions.
</details>

<details>
<summary>Hint 2</summary>
Both conditions must be true: low_fats = 'Y' AND is_recyclable = 'Y'.
</details>
