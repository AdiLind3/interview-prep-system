# Students and Examinations - Medium

**Difficulty:** Medium
**Estimated Time:** 25 minutes
**Topics:** CROSS JOIN, LEFT JOIN, COUNT, GROUP BY

## Problem Description

Write a query to find the number of times each student attended each exam subject. The result should show every student-subject combination, even if the student never attended that subject's exam (show 0 in that case).

## Requirements

1. Return student_id, student_name, subject_name, attended_exams
2. Include all student-subject combinations (even with 0 attendances)
3. Order by student_id, then subject_name

## Schema

### Students
| Column | Type |
|--------|------|
| student_id | INTEGER PRIMARY KEY |
| student_name | TEXT |

### Subjects
| Column | Type |
|--------|------|
| subject_name | TEXT PRIMARY KEY |

### Examinations
| Column | Type |
|--------|------|
| student_id | INTEGER |
| subject_name | TEXT |

## Expected Output

| student_id | student_name | subject_name | attended_exams |
|------------|--------------|--------------|----------------|
| ... | ... | ... | ... |

## LeetCode Reference
Similar to: [Students and Examinations](https://leetcode.com/problems/students-and-examinations/) - LeetCode #1280

## Hints

<details>
<summary>Hint 1</summary>
Use CROSS JOIN between students and subjects to get all combinations.
</details>

<details>
<summary>Hint 2</summary>
LEFT JOIN the examinations table onto the cross-joined result.
</details>

<details>
<summary>Hint 3</summary>
Use COUNT(e.subject_name) instead of COUNT(*) to get 0 for no attendance.
</details>
