# Product Sales Analysis III - Medium

**Difficulty:** Medium
**Estimated Time:** 25 minutes
**Topics:** CTE, Window Functions, First Value

## Problem Description

Write a query to select the product id, year, quantity, and price for the first year each product was sold.

## Requirements

1. Return product_id, first_year, quantity, price
2. first_year is the earliest year the product was sold
3. Order by product_id ascending

## Schema

### Sales
| Column | Type |
|--------|------|
| sale_id | INTEGER PRIMARY KEY |
| product_id | INTEGER |
| year | INTEGER |
| quantity | INTEGER |
| price | INTEGER |

### Product
| Column | Type |
|--------|------|
| product_id | INTEGER PRIMARY KEY |
| product_name | TEXT |

## Expected Output

| product_id | first_year | quantity | price |
|------------|------------|----------|-------|
| ... | ... | ... | ... |

## LeetCode Reference
Similar to: [Product Sales Analysis III](https://leetcode.com/problems/product-sales-analysis-iii/) - LeetCode #1070

## Hints

<details>
<summary>Hint 1</summary>
Find the minimum year per product first using a subquery or CTE.
</details>

<details>
<summary>Hint 2</summary>
Use RANK() or ROW_NUMBER() partitioned by product_id ordered by year.
</details>

<details>
<summary>Hint 3</summary>
Filter for rank = 1 to get only the first year records.
</details>
