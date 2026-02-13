# Mind Map: Data Engineering Concepts

## Data Engineering Landscape

```
                        DATA ENGINEERING
                             |
        +--------------------+--------------------+
        |                    |                    |
    INGESTION           PROCESSING            STORAGE
        |                    |                    |
   +----+----+          +----+----+          +----+----+
   |    |    |          |    |    |          |    |    |
  API  File Stream    Batch Real  ETL      Lake  WH   DB
       |               |   time   |              |
      CSV/JSON     Spark Flink   ELT         Redshift
      Parquet      EMR   Kafka   DBT         BigQuery
                   Glue  Kinesis             Snowflake
```

---

## Data Pipeline Architecture

```
DATA SOURCES                    PROCESSING                      DESTINATIONS
+------------+                  +------------+                  +------------+
| APIs       |                  | Clean      |                  | Data       |
| Databases  | --> Ingestion -> | Transform  | --> Loading ---> | Warehouse  |
| Files      |    (Extract)     | Validate   |    (Load)       | Data Lake  |
| Streams    |                  | Enrich     |                  | APIs       |
+------------+                  +------------+                  +------------+
                                      |
                                 Orchestration
                                 (Airflow/Step Functions)
```

---

## Storage Layer Decision Tree

```
What kind of data?
|
+-- Structured (tables, rows)
|   |
|   +-- Transactional (OLTP)? --> PostgreSQL, MySQL, RDS
|   |
|   +-- Analytical (OLAP)? --> Redshift, BigQuery, Snowflake
|
+-- Semi-structured (JSON, XML)
|   |
|   +-- Need fast lookups? --> DynamoDB, MongoDB
|   |
|   +-- Need analytics? --> S3 (Parquet) + Athena
|
+-- Unstructured (images, text, video)
    |
    +-- Object storage --> S3, GCS, Azure Blob
    |
    +-- Need search? --> Elasticsearch, OpenSearch
```

---

## ETL vs ELT Decision

```
ETL (Extract-Transform-Load)          ELT (Extract-Load-Transform)
|                                      |
+-- Transform BEFORE loading           +-- Transform AFTER loading
+-- Staging area handles compute       +-- Warehouse handles compute
+-- Good for legacy systems            +-- Good for modern cloud DW
+-- More control over what loads       +-- More flexible, raw data preserved
+-- Tools: Informatica, SSIS           +-- Tools: DBT, Spark SQL
```

---

## Data Quality Dimensions

```
DATA QUALITY
|
+-- Completeness: Are all required fields present?
|
+-- Accuracy: Does the data reflect reality?
|
+-- Consistency: Same data, same format across sources?
|
+-- Timeliness: Is the data fresh enough for its purpose?
|
+-- Uniqueness: No unwanted duplicates?
|
+-- Validity: Does data conform to defined rules/formats?
```

---

## AWS Services for Data Engineering

```
AWS DATA STACK
|
+-- STORAGE
|   +-- S3 (object storage, data lake)
|   +-- RDS/Aurora (relational, OLTP)
|   +-- Redshift (warehouse, OLAP)
|   +-- DynamoDB (NoSQL, key-value)
|
+-- PROCESSING
|   +-- Lambda (serverless compute)
|   +-- Glue (managed ETL)
|   +-- EMR (Spark/Hadoop)
|   +-- ECS (containers)
|
+-- STREAMING
|   +-- Kinesis Data Streams
|   +-- Kinesis Firehose
|   +-- MSK (Managed Kafka)
|
+-- ORCHESTRATION
|   +-- Step Functions
|   +-- MWAA (Managed Airflow)
|   +-- EventBridge (scheduling)
|
+-- ANALYTICS
|   +-- Athena (serverless SQL on S3)
|   +-- QuickSight (BI dashboards)
|   +-- Redshift Spectrum (query S3 from Redshift)
|
+-- INFRASTRUCTURE
    +-- CDK (infrastructure as code)
    +-- CloudFormation
    +-- IAM (access control)
```

---

## Orchestration Concepts

```
AIRFLOW CONCEPTS
|
+-- DAG: Directed Acyclic Graph (workflow definition)
|
+-- Task: Single unit of work (Python, SQL, Bash)
|
+-- Operator: Template for a task type
|   +-- PythonOperator
|   +-- BashOperator
|   +-- S3ToRedshiftOperator
|
+-- Sensor: Wait for external condition
|   +-- S3KeySensor (wait for file)
|   +-- HttpSensor (wait for API)
|
+-- XCom: Cross-communication between tasks
|
+-- Schedule: Cron expression (e.g., "0 2 * * *" = daily at 2am)
|
+-- Backfill: Re-run past DAG runs for historical data
```
