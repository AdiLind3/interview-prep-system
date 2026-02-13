# Customers Who Never Order - Easy

**Difficulty:** Easy
**Estimated Time:** 10 minutes
**Topics:** LEFT JOIN, IS NULL, Subquery

## Problem Description

You have two tables: `customers` and `orders`. Write a query to find all customers who have never placed an order.

## Requirements

1. Return only the customer name column (aliased as "customers")
2. Only include customers with no matching orders
3. Order results by name ascending

## Schema

### Customers
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| name | TEXT |

### Orders
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| customerId | INTEGER (FK) |

## Expected Output

| customers |
|-----------|
| ... |

## LeetCode Reference
Similar to: [Customers Who Never Order](https://leetcode.com/problems/customers-who-never-order/) - LeetCode #183

## Hints

<details>
<summary>Hint 1</summary>
Use LEFT JOIN to keep all customers, even those without orders.
</details>

<details>
<summary>Hint 2</summary>
After LEFT JOIN, filter for rows where the order id IS NULL.
</details>

<details>
<summary>Hint 3</summary>
Alternatively, use a subquery with NOT IN or NOT EXISTS.
</details>
