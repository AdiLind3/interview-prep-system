# System Design: Data Lake Architecture for AI Platform

**Difficulty**: Hard
**Time**: 45 minutes
**Topics**: Data Lake, S3, Schema Evolution, Data Governance
**Relevance**: Core infrastructure pattern for tasq.ai's AI data platform

---

## Problem Statement

Design a data lake architecture for an AI platform that handles diverse data types (structured, semi-structured, unstructured) from multiple sources. The platform needs to support both batch analytics and real-time model training pipelines while maintaining data quality and governance.

---

## Requirements

### Functional Requirements
1. Store raw data from 50+ data sources in various formats
2. Support schema evolution without breaking downstream consumers
3. Enable self-service data discovery and access
4. Track data lineage end-to-end
5. Support both SQL analytics and ML training workloads
6. Implement role-based access control

### Non-Functional Requirements
1. **Scale**: 10TB ingested daily, 500TB total storage
2. **Cost**: Optimize storage costs with tiered approach
3. **Query Performance**: Interactive queries on recent data (< 30 seconds)
4. **Compliance**: GDPR-compatible data retention and deletion

---

## Solution: Medallion Architecture (Bronze/Silver/Gold)

### High-Level Architecture

```
[Data Sources] --> [Bronze Layer] --> [Silver Layer] --> [Gold Layer]
    Raw data       Ingested as-is     Cleaned/validated   Business-ready
    Any format     Append-only        Deduplicated        Aggregated
    No schema      Schema-on-read     Schema enforced     Modeled
```

### Bronze Layer (Raw Zone)
- S3 bucket: `s3://datalake-bronze/`
- Partitioned by: `source/year/month/day/`
- Formats: JSON, CSV, Parquet, images, text
- Retention: 2 years, then Glacier
- Purpose: Immutable raw data archive

### Silver Layer (Cleaned Zone)
- S3 bucket: `s3://datalake-silver/`
- Format: Parquet (columnar, compressed)
- Schema: Enforced via AWS Glue Data Catalog
- Deduplicated, validated, typed
- Retention: 5 years

### Gold Layer (Business Zone)
- S3 bucket: `s3://datalake-gold/`
- Format: Parquet, optimized for queries
- Modeled: Star schema or wide tables
- Pre-aggregated for common queries
- Also loaded into Redshift for interactive queries

### Schema Evolution Strategy

Using Apache Avro schema registry pattern:
1. Each source registers its schema
2. New fields: Added with defaults (backward compatible)
3. Removed fields: Keep in schema, mark deprecated
4. Type changes: Version the schema, transform in Silver layer

### Data Catalog & Discovery

AWS Glue Data Catalog:
- Automatic schema crawling
- Business metadata tags
- Data quality scores
- Column-level lineage
- Search interface for data discovery

### Access Control

- IAM roles per team/project
- S3 bucket policies for layer separation
- Column-level masking for PII
- Audit logging via CloudTrail

### Cost Optimization

| Storage Tier | Data Age | Cost/GB/month |
|---|---|---|
| S3 Standard | 0-30 days | $0.023 |
| S3 Infrequent Access | 30-180 days | $0.0125 |
| S3 Glacier | 180+ days | $0.004 |

S3 Lifecycle policies automate tier transitions.

---

## Follow-up Questions

1. How do you handle PII data across all layers?
2. What if a source changes its schema without notice?
3. How do you ensure exactly-once processing from Bronze to Silver?
4. How would you implement data lineage tracking?
5. What is your approach to data quality monitoring at each layer?
