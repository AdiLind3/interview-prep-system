# Friend Requests Acceptance Rate - Medium

**Difficulty:** Medium
**Estimated Time:** 25 minutes
**Topics:** COUNT, DISTINCT, UNION, Division, ROUND

## Problem Description

Write a query to find the overall acceptance rate of friend requests. The acceptance rate is the number of accepted requests divided by the number of total requests sent. Round to 2 decimal places. If there are no requests, return 0.00.

Note: Duplicate requests (same sender-receiver pair) should only be counted once.

## Requirements

1. Return a single value: accept_rate (rounded to 2 decimal places)
2. Count distinct sender-receiver pairs for requests sent
3. Count distinct sender-receiver pairs for requests accepted
4. Rate = accepted / sent (or 0.00 if no requests)

## Schema

### FriendRequest
| Column | Type |
|--------|------|
| sender_id | INTEGER |
| send_to_id | INTEGER |
| request_date | DATE |

### RequestAccepted
| Column | Type |
|--------|------|
| requester_id | INTEGER |
| accepter_id | INTEGER |
| accept_date | DATE |

## Expected Output

| accept_rate |
|-------------|
| ... |

## LeetCode Reference
Similar to: [Friend Requests I: Overall Acceptance Rate](https://leetcode.com/problems/friend-requests-i-overall-acceptance-rate/) - LeetCode #597

## Hints

<details>
<summary>Hint 1</summary>
Count distinct (sender_id, send_to_id) pairs for total requests.
</details>

<details>
<summary>Hint 2</summary>
Count distinct (requester_id, accepter_id) pairs for accepted requests.
</details>

<details>
<summary>Hint 3</summary>
Use IFNULL to handle the case when there are no requests (avoid division by zero).
</details>
