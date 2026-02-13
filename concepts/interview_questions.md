# Interview Questions - Behavioral & Technical Q&A

## Behavioral Questions

### Tell Me About Yourself
**Framework**: Present > Past > Future (2 minutes max)

"I am a data engineer with experience building data pipelines and AI-powered systems. I have worked with petabyte-scale data infrastructure at PMO, where I developed SQL queries for complex data transformations and Python scripts for data processing. More recently, I built a RAG chatbot that combines data engineering with AI capabilities. I am excited about the Junior Data Engineer role at tasq.ai because your work at the intersection of AI and data quality directly aligns with my experience and interests."

### Why tasq.ai?
- Their mission of building trustworthy AI through human-AI collaboration resonates with me
- The tech stack (Python, SQL, AWS, Airflow, LangGraph) matches my skills and growth areas
- Working with clients like Meta and Amazon means real impact at scale
- The role involves diverse work: data pipelines, AI agents, web scrapers -- not just one thing
- Growth-stage company means I can wear multiple hats and learn fast

### Why Data Engineering?
- I enjoy building the infrastructure that makes data useful
- The combination of software engineering and data is compelling
- Data engineers are the backbone of any AI/ML system
- The field is evolving rapidly with new tools (DBT, Airflow, modern data stack)
- It is tangible work: you can see the pipelines running, data flowing, dashboards updating

### Tell Me About a Challenging Project
**STAR Format**:
- **Situation**: Developed a RAG chatbot for SoftLanding that needed to retrieve accurate information from a large document corpus
- **Task**: Build a reliable data pipeline for document ingestion, vectorization, and retrieval
- **Action**: Designed the pipeline architecture, implemented vector database storage, built validation layers for data quality, and handled edge cases in AI responses
- **Result**: Delivered a working system that accurately retrieves relevant information, demonstrating both data engineering and AI skills

### How Do You Handle Disagreements?
- I start by understanding the other person's perspective
- I focus on data and evidence rather than opinions
- I am willing to be wrong and change my approach
- If we cannot agree, I suggest prototyping both approaches and measuring results
- Example: "When I disagreed about a database schema design, I benchmarked both approaches and presented the results"

### What Is Your Biggest Weakness?
- I sometimes over-engineer solutions when simpler approaches would work
- I have been actively working on this by asking "what is the simplest thing that could work?" before designing
- This interview prep system is actually a good example of starting with the simplest version and iterating

---

## Technical Questions

### SQL Questions

**Q: What is the difference between DELETE, TRUNCATE, and DROP?**
A:
- DELETE: Removes specific rows, can use WHERE clause, logged (can rollback), slower
- TRUNCATE: Removes all rows, cannot use WHERE, minimally logged, faster, resets identity
- DROP: Removes the entire table structure and data, cannot be easily undone

**Q: Explain the SQL execution order.**
A: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT

**Q: When would you use a CTE vs a subquery?**
A:
- CTE: When the same subquery is referenced multiple times, for readability, for recursive queries
- Subquery: For simple one-off operations, when CTE is not supported, for correlated subqueries
- Performance is usually the same; CTEs improve readability

**Q: How do you optimize a slow SQL query?**
A:
1. Check the execution plan (EXPLAIN ANALYZE)
2. Add indexes on columns used in WHERE, JOIN, ORDER BY
3. Avoid SELECT * (select only needed columns)
4. Avoid functions on indexed columns in WHERE clauses
5. Use appropriate JOIN types
6. Consider partitioning for large tables
7. Use LIMIT for development/testing

### Python Questions

**Q: What is the difference between a list and a tuple?**
A:
- List: Mutable, slower, uses [], can add/remove elements
- Tuple: Immutable, faster, uses (), fixed after creation, hashable (can be dict key)
- Use tuples for fixed collections, lists for dynamic collections

**Q: Explain generators and when to use them.**
A:
- Generators produce items one at a time using yield
- They are memory-efficient for large datasets (lazy evaluation)
- Use when you do not need all items at once
- Example: Processing a 10GB file line by line instead of loading into memory

**Q: What is the GIL and how does it affect Python?**
A:
- Global Interpreter Lock: Only one thread executes Python bytecode at a time
- Affects CPU-bound tasks (no true parallelism with threads)
- Does not affect I/O-bound tasks (network, file operations)
- Workarounds: multiprocessing, asyncio, or using C extensions

**Q: How do you handle missing data in pandas?**
A:
- df.isna().sum() to find missing values
- df.dropna() to remove rows with missing values
- df.fillna(value) to replace with a specific value
- df.interpolate() for time series data
- df.fillna(method='ffill') for forward fill
- Choose strategy based on data context and downstream usage

### Data Engineering Questions

**Q: What is idempotency and why does it matter in data pipelines?**
A: Running the same operation multiple times produces the same result. Critical because pipelines fail and need retries. Implement with: MERGE/UPSERT instead of INSERT, checking if data already exists, using batch IDs.

**Q: Explain the difference between Airflow and Step Functions.**
A:
- Airflow: Open-source, Python DAGs, complex scheduling, rich UI, manages state, good for batch ETL
- Step Functions: AWS-native, JSON/YAML, event-driven, serverless, good for microservice orchestration
- Use Airflow for complex data pipelines, Step Functions for simpler AWS-native workflows

**Q: What is DBT and what problem does it solve?**
A: DBT (data build tool) manages SQL transformations in the warehouse. It brings software engineering practices (version control, testing, documentation) to SQL transformations. Models are SELECT statements, tests validate data quality, and it handles dependency ordering.

**Q: Describe a data pipeline you would build for tasq.ai.**
A: I would build a pipeline that:
1. Ingests annotation task data from multiple sources (APIs, uploads)
2. Validates and cleans the data (schema validation, deduplication)
3. Routes tasks to AI models or human annotators based on complexity
4. Collects results and runs quality checks
5. Aggregates metrics into Redshift for analytics
6. Uses Airflow for orchestration with retry logic and monitoring

---

## Questions About tasq.ai Specifics

**Q: What do you know about tasq.ai?**
A: tasq.ai is an Israeli AI company that provides the "Trust Layer for Global Enterprise AI." They combine AI models with a global network of 25,000+ human domain experts across 120+ languages. Their platform handles data annotation, model validation, content moderation, and product catalog enrichment for clients like Meta, Amazon, and PayPal. They recently acquired BLEND for multilingual capabilities.

**Q: How would you approach building a data pipeline for annotation tasks?**
A: I would design it with these components:
- Ingestion: S3 landing zone for raw annotation data
- Validation: Schema checks, deduplication, quality scoring
- Routing: Confidence-based routing (high confidence -> automated, low -> human review)
- Processing: DBT transformations for standardization
- Loading: PostgreSQL for serving, Redshift for analytics
- Monitoring: Airflow DAGs with SLA alerts, data quality dashboards

**Q: What interests you about building AI agents?**
A: AI agents are the next evolution of automation. With LangGraph, you can build agents that make decisions, use tools, and learn from feedback. The challenge is building reliable data infrastructure to support them -- ensuring they have access to the right data at the right time, tracking their decisions for auditability, and creating feedback loops for continuous improvement. This combines my data engineering skills with AI knowledge.
