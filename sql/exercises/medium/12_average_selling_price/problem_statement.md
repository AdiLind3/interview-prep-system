# Average Selling Price - Medium

**Difficulty:** Medium
**Estimated Time:** 25 minutes
**Topics:** JOIN with Date Range, Weighted Average, ROUND

## Problem Description

Write a query to find the average selling price for each product. The average selling price is calculated as the total revenue divided by total units sold. Prices vary over different date periods.

## Requirements

1. Return product_id and average_price (rounded to 2 decimal places)
2. The price of a unit depends on when it was purchased (based on date ranges in prices table)
3. If a product has no sales, the average_price should be 0
4. Order by product_id ascending

## Schema

### Prices
| Column | Type |
|--------|------|
| product_id | INTEGER |
| start_date | DATE |
| end_date | DATE |
| price | INTEGER |

### UnitsSold
| Column | Type |
|--------|------|
| product_id | INTEGER |
| purchase_date | DATE |
| units | INTEGER |

## Expected Output

| product_id | average_price |
|------------|---------------|
| ... | ... |

## LeetCode Reference
Similar to: [Average Selling Price](https://leetcode.com/problems/average-selling-price/) - LeetCode #1251

## Hints

<details>
<summary>Hint 1</summary>
JOIN prices with units_sold where purchase_date falls between start_date and end_date.
</details>

<details>
<summary>Hint 2</summary>
Weighted average = SUM(price * units) / SUM(units).
</details>

<details>
<summary>Hint 3</summary>
Use IFNULL to handle products with no sales (return 0).
</details>
