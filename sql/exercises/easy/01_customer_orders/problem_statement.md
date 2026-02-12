# Customer Orders - Easy

**Difficulty:** Easy
**Estimated Time:** 15 minutes
**Topics:** INNER JOIN, Basic SELECT

## Problem Description

You are given two tables: `customers` and `orders`. Write a query to return all customers who have placed at least one order, along with the total number of orders they've placed.

## Requirements

1. Include customer ID, name, and email
2. Include count of orders for each customer
3. Only include customers who have placed orders (at least 1)
4. Order results by order count (descending)

## Schema

### Customers
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| name | TEXT |
| email | TEXT |

### Orders
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| customer_id | INTEGER (FK) |
| order_date | DATE |
| total_amount | DECIMAL |

## Expected Output

| customer_id | name | email | order_count |
|-------------|------|-------|-------------|
| 1 | Alice Johnson | alice@email.com | 3 |
| 2 | Bob Smith | bob@email.com | 2 |
| ... | ... | ... | ... |

## Hints

<details>
<summary>Hint 1</summary>
You'll need to use INNER JOIN to combine the two tables.
</details>

<details>
<summary>Hint 2</summary>
Use COUNT() with GROUP BY to count orders per customer.
</details>

<details>
<summary>Hint 3</summary>
Use ORDER BY with DESC to sort by count in descending order.
</details>
