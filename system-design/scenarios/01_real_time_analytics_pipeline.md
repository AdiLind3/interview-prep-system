# System Design: Real-Time Analytics Pipeline

**Difficulty**: Medium
**Time**: 45 minutes
**Topics**: Streaming, Data Pipeline, Scalability

---

## Problem Statement

Design a real-time analytics system that processes user clickstream events from a high-traffic e-commerce website and provides near real-time analytics dashboards for the business team.

---

## Requirements

### Functional Requirements
1. Ingest clickstream events from web/mobile applications
2. Process and aggregate events in near real-time (< 1 minute latency)
3. Provide analytics dashboard showing:
   - Active users (last 5 minutes)
   - Page views by category
   - Conversion funnel metrics
   - Top products viewed
4. Store raw events for historical analysis
5. Handle schema evolution (new event types)

### Non-Functional Requirements
1. **Scale**: Handle 10,000 events/second (peak: 50,000/second)
2. **Latency**: Dashboard updates within 60 seconds
3. **Availability**: 99.9% uptime
4. **Data Retention**: Raw events for 2 years, aggregates for 5 years
5. **Cost**: Optimize for cost-effectiveness

---

## Constraints

- Use AWS ecosystem primarily
- Budget: $10,000/month
- Team: 3 data engineers
- Cannot lose events (at-least-once delivery)

---

## Solution Template

### 1. High-Level Architecture

```
[Web/Mobile Apps]
       |
       v
[API Gateway / Load Balancer]
       |
       v
[Event Collection Service]
       |
       v
[Message Queue / Stream]
       |
       +--> [Stream Processor] --> [Real-time Aggregates] --> [Dashboard]
       |
       +--> [Batch Storage] --> [Data Warehouse] --> [Historical Analysis]
```

### 2. Detailed Components

#### Ingestion Layer
**Chosen Technology**: Amazon Kinesis Data Streams
**Rationale**:
- Handles high throughput (1MB/sec per shard, can scale)
- Built-in retry and durability
- Preserves event ordering within partition
- Pay for what you use

**Alternative Considered**: Apache Kafka
- Pros: More flexible, open-source, better for complex event routing
- Cons: More operational overhead, need to manage cluster

**Scaling Strategy**:
- Start with 10 shards (100,000 events/sec capacity)
- Auto-scale based on incoming data rate
- Partition key: user_id (ensures user session ordering)

#### Processing Layer
**Chosen Technology**: AWS Lambda + Kinesis Data Analytics
**Rationale**:
- Serverless (no infrastructure management)
- Auto-scaling
- Cost-effective for variable workload
- Built-in Kinesis integration

**Processing Logic**:
```python
# Pseudocode for stream processor
def process_events(events):
    # 1. Parse and validate events
    valid_events = validate_schema(events)

    # 2. Enrich with additional data
    enriched = enrich_with_product_metadata(valid_events)

    # 3. Aggregate in 1-minute windows
    aggregates = {
        'active_users': count_distinct(enriched, 'user_id', window='1min'),
        'page_views': count(enriched, group_by='category'),
        'top_products': top_k(enriched, k=10, by='view_count')
    }

    # 4. Write to real-time database
    write_to_dynamodb(aggregates)

    # 5. Write raw events to S3 for batch processing
    write_to_s3(enriched)
```

#### Storage Layer

**Real-time Storage**: Amazon DynamoDB
- Key-value store for low-latency reads
- Schema: `{metric_name}#{timestamp}` as partition key
- TTL: 24 hours (only keep recent aggregates)

**Historical Storage**: Amazon S3
- Store raw events in Parquet format
- Partitioned by date: `s3://bucket/year=2024/month=02/day=12/`
- Compress with Snappy (good balance of compression/speed)

**Data Warehouse**: Amazon Redshift
- Load daily batches from S3
- Optimized for analytical queries
- Materialized views for common queries

#### Serving Layer

**Dashboard Backend**: AWS AppSync (GraphQL API)
- Reads from DynamoDB for real-time metrics
- Reads from Redshift for historical analysis
- Caches frequently accessed data

**Dashboard Frontend**: React + Recharts
- WebSocket connection for live updates
- Responsive charts and visualizations

### 3. Data Flow

1. **Event Generation**:
   ```json
   {
     "event_id": "uuid",
     "user_id": "user123",
     "session_id": "session456",
     "event_type": "page_view",
     "timestamp": "2024-02-12T10:30:00Z",
     "page": "/products/laptop",
     "category": "electronics",
     "device": "mobile"
   }
   ```

2. **Ingestion**: API Gateway → Kinesis Data Streams (buffering)

3. **Real-time Processing**:
   - Lambda triggered by Kinesis
   - Aggregate in 1-minute tumbling windows
   - Write to DynamoDB

4. **Batch Processing**:
   - Raw events → S3 (Parquet)
   - Nightly ETL job → Redshift
   - Update historical aggregates

### 4. Handling Scale

**Current**: 10K events/sec
**Peak**: 50K events/sec

Scaling strategies:
- **Kinesis**: Add shards dynamically (10 shards → 50 shards)
- **Lambda**: Auto-scales to 1000 concurrent executions
- **DynamoDB**: On-demand capacity mode (auto-scaling)
- **S3**: Virtually unlimited scale

**Cost at Peak**:
- Kinesis: 50 shards × $0.015/hr × 730hr = ~$550/month
- Lambda: 50K events/sec × 100ms × $0.0000166667/GB-sec ≈ $500/month
- DynamoDB: On-demand, ~$1000/month
- S3: 10TB/year × $0.023/GB = $235/month
- Redshift: ra3.xlplus (4 nodes) = ~$8,000/month
**Total**: ~$10,285/month (within budget with optimization)

### 5. Data Quality & Monitoring

**Schema Validation**:
- Use JSON Schema or Apache Avro
- Reject invalid events (dead letter queue)
- Alert on schema changes

**Monitoring**:
- CloudWatch metrics: event throughput, processing latency, error rate
- Alert on anomalies (sudden drop/spike in events)
- Dashboard health check (data freshness)

**Testing**:
- Unit tests for processing logic
- Integration tests with sample events
- Load testing with 50K events/sec

### 6. Trade-offs

| Decision | Pros | Cons | Why Chosen |
|----------|------|------|------------|
| Kinesis vs Kafka | Less operational overhead, AWS-native | Less flexible, vendor lock-in | Team size (3 people), AWS ecosystem |
| Lambda vs ECS | Serverless, auto-scaling | Cold starts, 15min limit | Variable workload, cost |
| DynamoDB vs Redis | Managed, durable | Higher latency than Redis | Durability important, less ops |
| Parquet vs JSON | 10x compression, faster queries | Requires schema | Cost savings, query performance |

### 7. Future Improvements

**Phase 2** (6 months):
- Add machine learning for anomaly detection
- Implement A/B testing framework
- Add personalization engine

**Phase 3** (1 year):
- Multi-region deployment
- Advanced event correlation
- Predictive analytics

---

## Evaluation Rubric

Rate your solution on:

- [ ] **Completeness**: Covers all requirements (5/5)
- [ ] **Scalability**: Handles scale requirements (5/5)
- [ ] **Availability**: Meets SLA (5/5)
- [ ] **Cost**: Within budget (5/5)
- [ ] **Trade-offs**: Discusses alternatives (5/5)
- [ ] **Monitoring**: Includes observability (5/5)
- [ ] **Data Quality**: Addresses validation (5/5)
- [ ] **Communication**: Clear and organized (5/5)

**Total**: __/40

---

## Key Takeaways

1. **Start with requirements**: Functional + non-functional
2. **Discuss trade-offs**: No perfect solution, explain choices
3. **Consider the full lifecycle**: Ingestion → Processing → Storage → Serving
4. **Think about scale**: What breaks at 10x? 100x?
5. **Monitoring matters**: How do you know it's working?
6. **Iterate**: MVP first, then improvements

---

## Follow-up Questions

Be prepared to answer:
1. How would you handle duplicate events?
2. What if DynamoDB becomes a bottleneck?
3. How do you handle late-arriving data?
4. What's your disaster recovery plan?
5. How do you ensure exactly-once processing?
6. How would you add a new event type without breaking existing dashboards?
