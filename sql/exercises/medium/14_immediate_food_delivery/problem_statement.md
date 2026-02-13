# Immediate Food Delivery II - Medium

**Difficulty:** Medium
**Estimated Time:** 25 minutes
**Topics:** GROUP BY, CASE WHEN, First Order, ROUND

## Problem Description

Write a query to find the percentage of immediate orders in each customer's first order. An order is "immediate" if the customer's preferred delivery date equals the order date. Each customer's first order is the one with the earliest order_date.

## Requirements

1. Return a single value: immediate_percentage (rounded to 2 decimal places)
2. First order per customer = earliest order_date
3. Immediate = order_date equals customer_pref_delivery_date
4. Calculate: (immediate first orders / total customers) * 100

## Schema

### Delivery
| Column | Type |
|--------|------|
| delivery_id | INTEGER PRIMARY KEY |
| customer_id | INTEGER |
| order_date | DATE |
| customer_pref_delivery_date | DATE |

## Expected Output

| immediate_percentage |
|----------------------|
| ... |

## LeetCode Reference
Similar to: [Immediate Food Delivery II](https://leetcode.com/problems/immediate-food-delivery-ii/) - LeetCode #1174

## Hints

<details>
<summary>Hint 1</summary>
Find each customer's first order using MIN(order_date) grouped by customer_id.
</details>

<details>
<summary>Hint 2</summary>
Join back to get the full order details for each customer's first order.
</details>

<details>
<summary>Hint 3</summary>
Use AVG(CASE WHEN...) * 100 to calculate the percentage of immediate first orders.
</details>
