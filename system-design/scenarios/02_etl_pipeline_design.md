# System Design: ETL Pipeline for Product Catalog Enrichment

**Difficulty**: Medium
**Time**: 45 minutes
**Topics**: ETL, Data Quality, Pipeline Orchestration, AWS
**Relevance**: Directly related to tasq.ai's product catalog enrichment work

---

## Problem Statement

Design a scalable ETL pipeline that enriches product catalogs for an e-commerce platform. The pipeline ingests raw product data from multiple sources, enriches it with AI-generated descriptions and human annotations, validates quality, and loads it into a data warehouse for analytics.

This is directly relevant to what tasq.ai does with their Product Catalog Enrichment platform.

---

## Requirements

### Functional Requirements
1. Ingest product data from multiple sources (APIs, CSV files, web scraping)
2. Clean and standardize product attributes (names, categories, prices)
3. Enrich products with AI-generated descriptions
4. Route low-confidence enrichments to human annotators (human-in-the-loop)
5. Validate data quality before loading into warehouse
6. Support incremental updates (new products, price changes)
7. Track data lineage (which source, which AI model, which annotator)

### Non-Functional Requirements
1. **Scale**: Handle 1M products per day
2. **Latency**: End-to-end processing within 4 hours
3. **Quality**: 99% accuracy on enriched attributes
4. **Reliability**: No data loss, idempotent operations
5. **Observability**: Full visibility into pipeline health

---

## Solution Template

### 1. High-Level Architecture

```
[Data Sources]
  |-- APIs (supplier feeds)
  |-- S3 (CSV/JSON uploads)
  |-- Web Scrapers
       |
       v
[Ingestion Layer - S3 Raw Zone]
       |
       v
[Orchestration - Airflow DAGs]
       |
       v
[Transform Layer]
  |-- Cleaning & Standardization (Python/Spark)
  |-- AI Enrichment (LLM API calls)
  |-- Human Review Queue (low-confidence items)
       |
       v
[Validation Layer]
  |-- Schema validation
  |-- Business rules checks
  |-- Quality scoring
       |
       v
[Load Layer]
  |-- S3 Curated Zone (Parquet)
  |-- Redshift (Data Warehouse)
  |-- PostgreSQL (Serving DB)
```

### 2. Detailed Components

#### Ingestion Layer
**Technology**: AWS Lambda + S3

- Lambda triggers on S3 upload events
- API connectors run on schedule via Airflow
- Web scrapers run on ECS tasks with rate limiting
- All raw data lands in S3 Raw Zone with source metadata

**Data Format**:
```json
{
  "product_id": "SKU-12345",
  "source": "supplier_api",
  "raw_name": "LAPTOP DELL INSPIRON 15 3520",
  "raw_category": "electronics/computers",
  "price": 599.99,
  "currency": "USD",
  "attributes": {"ram": "8GB", "storage": "256GB SSD"},
  "ingested_at": "2026-02-12T10:00:00Z"
}
```

#### Orchestration Layer
**Technology**: Apache Airflow (AWS MWAA)

DAG structure:
```
ingest_supplier_feeds >> clean_and_standardize >> ai_enrichment >> human_review >> validate >> load_warehouse
```

Key Airflow patterns:
- **Sensors**: Wait for upstream data to arrive in S3
- **Branching**: Route to human review if confidence < 0.85
- **Retries**: Exponential backoff on API failures
- **SLAs**: Alert if pipeline exceeds 4-hour window

#### Transform Layer

**Step 1: Cleaning (DBT models)**
```sql
-- models/staging/stg_products.sql
SELECT
    product_id,
    TRIM(UPPER(raw_name)) as product_name,
    standardize_category(raw_category) as category,
    COALESCE(price, 0) as price,
    ingested_at,
    source
FROM {{ source('raw', 'products') }}
WHERE product_id IS NOT NULL
  AND price > 0
```

**Step 2: AI Enrichment (Python on ECS)**
```python
def enrich_product(product: dict) -> dict:
    """Call AI model to generate enriched description."""
    response = ai_model.generate(
        prompt=f"Enrich product: {product['product_name']}",
        attributes=product['attributes']
    )
    return {
        **product,
        "enriched_description": response.text,
        "ai_confidence": response.confidence,
        "model_version": response.model_id
    }
```

**Step 3: Human Review (for confidence < 0.85)**
- Route to tasq.ai NanoTasking platform
- Human annotators verify/correct enrichments
- Results feed back into pipeline

#### Validation Layer
**Technology**: Great Expectations or DBT tests

Checks:
- No NULL product_ids
- Prices within expected ranges
- Category values from allowed set
- Enriched descriptions have minimum length
- No duplicate products in batch
- Cross-source consistency checks

#### Load Layer
- **S3 Curated Zone**: Parquet, partitioned by category and date
- **Redshift**: Analytical queries, reporting
- **PostgreSQL**: Serving layer for APIs

### 3. Data Quality Strategy

| Dimension | Check | Action on Failure |
|---|---|---|
| Completeness | Required fields present | Reject record, alert |
| Accuracy | Price within 2 std devs of category average | Flag for review |
| Consistency | Same product, same attributes across sources | Merge with priority rules |
| Timeliness | Data less than 24 hours old | Skip stale records |
| Uniqueness | No duplicate product_ids | Deduplicate, keep latest |

### 4. Idempotency Strategy

- Each batch has a unique batch_id
- Use MERGE/UPSERT instead of INSERT
- Track processed batches to avoid re-processing
- Partition output by date for easy replay

### 5. Monitoring & Alerts

- Pipeline duration (alert if > 3 hours)
- Record counts per stage (detect data loss)
- AI enrichment quality scores (detect model degradation)
- Human review queue depth (detect bottleneck)
- Data freshness in warehouse

### 6. Trade-offs

| Decision | Chosen | Alternative | Rationale |
|---|---|---|---|
| Orchestration | Airflow | Step Functions | More flexible, better for complex DAGs |
| Processing | ECS + DBT | Spark/EMR | Simpler for 1M records/day scale |
| Human Review | Async queue | Synchronous | Does not block pipeline for most items |
| Storage | S3 + Redshift | Snowflake | AWS-native, matches team skills |

---

## Follow-up Questions

1. How would you handle a supplier sending malformed data?
2. What if the AI model starts producing lower quality enrichments?
3. How do you handle products that exist in multiple sources with conflicting data?
4. How would you scale this to 100M products per day?
5. What is your disaster recovery strategy?
