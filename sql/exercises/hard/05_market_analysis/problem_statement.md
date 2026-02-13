# Market Analysis - Hard

**Difficulty:** Hard
**Estimated Time:** 40 minutes
**Topics:** Complex Multi-Table JOINs, Date Logic, Aggregation, CTE

## Problem Description

You are analyzing an e-commerce marketplace. Write a query that provides a comprehensive analysis for each seller: their join date, total number of items sold in 2024, the category of their second item sold (by order date), and whether that category matches their favorite category.

## Requirements

1. Return seller_id, join_date, items_sold_2024, second_item_category, and category_match ('yes' or 'no')
2. items_sold_2024 is the count of items sold in 2024 (0 if none)
3. second_item_category is the item_category of the 2nd item sold by the seller (NULL if fewer than 2 items sold)
4. category_match is 'yes' if second_item_category equals the seller's favorite_category, 'no' otherwise (or 'no' if NULL)
5. Order by seller_id ascending

## Schema

### Users
| Column | Type |
|--------|------|
| user_id | INTEGER PRIMARY KEY |
| join_date | DATE |
| favorite_category | TEXT |

### Orders
| Column | Type |
|--------|------|
| order_id | INTEGER PRIMARY KEY |
| order_date | DATE |
| item_id | INTEGER |
| buyer_id | INTEGER |
| seller_id | INTEGER |

### Items
| Column | Type |
|--------|------|
| item_id | INTEGER PRIMARY KEY |
| item_category | TEXT |

## Expected Output

| seller_id | join_date | items_sold_2024 | second_item_category | category_match |
|-----------|-----------|-----------------|----------------------|----------------|
| ... | ... | ... | ... | ... |

## LeetCode Reference
Similar to: [Market Analysis II](https://leetcode.com/problems/market-analysis-ii/) - LeetCode #1159

## Hints

<details>
<summary>Hint 1</summary>
Use a CTE to count items sold per seller in 2024.
</details>

<details>
<summary>Hint 2</summary>
Use ROW_NUMBER() to rank each seller's orders by date and find the second one.
</details>

<details>
<summary>Hint 3</summary>
LEFT JOIN everything back to the users table to include sellers with no sales.
</details>

<details>
<summary>Hint 4</summary>
Use CASE WHEN to compare second_item_category with favorite_category.
</details>
