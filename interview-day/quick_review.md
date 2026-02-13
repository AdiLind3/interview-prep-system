# 15-Minute Pre-Interview Quick Review

Read through this once, out loud if possible. Do not try to memorize --
just activate the patterns in your head.

---

## Top 10 SQL Patterns (5 minutes)

### 1. INNER JOIN
```sql
SELECT a.*, b.col FROM table_a a JOIN table_b b ON a.id = b.a_id;
```

### 2. LEFT JOIN + NULL check (find non-matching rows)
```sql
SELECT a.* FROM table_a a LEFT JOIN table_b b ON a.id = b.a_id WHERE b.a_id IS NULL;
```

### 3. ROW_NUMBER for Top-N per group
```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) rn FROM emp
) SELECT * FROM ranked WHERE rn <= 3;
```

### 4. CTE for readability
```sql
WITH summary AS (SELECT dept, AVG(salary) avg_sal FROM emp GROUP BY dept)
SELECT * FROM summary WHERE avg_sal > 80000;
```

### 5. LAG / LEAD for row comparison
```sql
SELECT date, revenue, revenue - LAG(revenue) OVER (ORDER BY date) AS growth FROM sales;
```

### 6. GROUP BY + HAVING
```sql
SELECT dept, COUNT(*) cnt FROM emp GROUP BY dept HAVING COUNT(*) > 5;
```

### 7. Conditional aggregation (pivot)
```sql
SELECT product,
  SUM(CASE WHEN quarter='Q1' THEN sales ELSE 0 END) AS Q1,
  SUM(CASE WHEN quarter='Q2' THEN sales ELSE 0 END) AS Q2
FROM sales GROUP BY product;
```

### 8. Running total
```sql
SELECT date, amount, SUM(amount) OVER (ORDER BY date) AS running_total FROM txn;
```

### 9. EXISTS (often faster than IN)
```sql
SELECT name FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.cust_id = c.id);
```

### 10. UNION ALL (keep duplicates, faster than UNION)
```sql
SELECT id FROM table1 UNION ALL SELECT id FROM table2;
```

**Remember the execution order:** FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT

---

## Top 10 Python / Pandas Patterns (5 minutes)

### 1. List comprehension with filter
```python
evens = [x for x in data if x % 2 == 0]
```

### 2. Dictionary comprehension
```python
d = {k: v for k, v in zip(keys, values)}
```

### 3. Read CSV and inspect
```python
df = pd.read_csv("file.csv"); df.shape; df.info(); df.describe()
```

### 4. Boolean filtering
```python
df[(df["age"] > 25) & (df["city"] == "NY")]
```

### 5. GroupBy + named aggregation
```python
df.groupby("dept").agg(avg_sal=("salary", "mean"), headcount=("id", "count"))
```

### 6. Merge (SQL-style join)
```python
pd.merge(df1, df2, on="key", how="left")
```

### 7. Apply for row-wise logic
```python
df["label"] = df.apply(lambda row: f"{row['first']} {row['last']}", axis=1)
```

### 8. Vectorized conditional (np.where)
```python
df["group"] = np.where(df["age"] < 30, "Young", "Senior")
```

### 9. Handle missing values
```python
df.fillna(0); df.dropna(subset=["col1"]); df["col"].fillna(df["col"].mean())
```

### 10. Pivot table
```python
df.pivot_table(values="sales", index="product", columns="month", aggfunc="sum")
```

---

## Top 5 System Design Concepts for Data Engineering (2 minutes)

| Concept               | One-Liner                                                                 |
|-----------------------|---------------------------------------------------------------------------|
| Batch vs Streaming    | Batch for high throughput on bounded data; streaming for low latency on unbounded data |
| ETL vs ELT            | ETL transforms before loading (traditional); ELT loads raw then transforms in the warehouse |
| Partitioning          | Split large tables by date or key to speed up queries and reduce scan cost |
| Idempotency           | Running a pipeline twice produces the same result -- critical for retries and backfills |
| Schema evolution      | Plan for column additions, type changes, and backward compatibility from day one |

**Bonus terms to drop naturally:** data lineage, SCD (slowly changing dimensions),
star schema vs snowflake, ACID properties, CAP theorem.

---

## Top 5 Behavioral Answer Frameworks (1 minute)

Use **STAR**: Situation, Task, Action, Result.

| Question Type            | Key Point to Hit                                                  |
|--------------------------|-------------------------------------------------------------------|
| Technical achievement    | Quantify the result (e.g., "reduced query time from 40s to 2s")  |
| Debugging story          | Show methodical approach: logs, hypotheses, root cause, fix       |
| Teamwork / conflict      | Emphasize listening, compromise, and shared outcome               |
| Failure / mistake        | Own it, explain what you learned, show how you changed behavior   |
| Why this company         | Connect your skills and interests to their specific mission/product|

---

## Key tasq.ai Talking Points (1 minute)

### What they do
tasq.ai works at the intersection of AI and data quality / data
operations. They build tools that help organizations manage, validate,
and improve their data workflows.

### Why you want to work there
- Genuinely interested in the overlap of AI agents and data engineering.
- Your experience building AI-assisted tools (this prep system, RAG
  chatbots) aligns with their product direction.
- Want to grow as a data engineer in a company where data quality is the
  core mission, not an afterthought.

### What you would build
- Automated data validation pipelines.
- Monitoring and alerting for data freshness and schema drift.
- Internal tooling to accelerate onboarding of new data sources.

### Questions to ask them
- "What does your core data pipeline architecture look like today?"
- "How do you approach data quality validation at scale?"
- "What does a typical first project look like for a new data engineer?"
- "How does the team balance building new features vs. maintaining
  reliability?"

---

## Common Pitfalls to Avoid

| Pitfall                              | What to Do Instead                                          |
|--------------------------------------|-------------------------------------------------------------|
| Jumping into code without a plan     | Restate the problem, discuss approach, then code            |
| Staying silent while thinking        | Narrate your thought process out loud                       |
| Saying "I don't know" and stopping   | Say "I haven't worked with X directly, but here is how I would approach it..." |
| Giving vague behavioral answers      | Use specific numbers, names, and outcomes (STAR)            |
| Not asking any questions at the end  | Always have 2-3 prepared; it shows genuine interest         |
| Over-engineering a solution          | Start simple, mention optimizations you would add with more time |
| Forgetting edge cases               | Explicitly mention NULLs, empty inputs, duplicates, large scale |
| Rushing through system design        | Clarify requirements first, then draw the big picture       |

---

**You prepared well. Trust the work you put in. Good luck.**
