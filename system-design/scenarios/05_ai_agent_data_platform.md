# System Design: Data Platform for AI Agents

**Difficulty**: Hard
**Time**: 45 minutes
**Topics**: AI Agents, LangGraph, Data Pipeline, Vector DB
**Relevance**: tasq.ai job posting mentions building AI agents with LangGraph

---

## Problem Statement

Design a data platform that powers AI agents for automated data annotation and quality assessment. The agents need access to structured data, unstructured documents, and real-time feedback from human reviewers to make annotation decisions.

---

## Requirements

### Functional Requirements
1. AI agents can query structured data (PostgreSQL) and unstructured data (documents, images)
2. Agents route tasks to human reviewers when confidence is low
3. Human feedback loops back to improve agent decisions
4. Support multiple agent types (annotation, quality check, enrichment)
5. Track agent performance metrics and decision audit trail
6. Support parallel agent execution at scale

### Non-Functional Requirements
1. **Scale**: 100K agent decisions per hour
2. **Latency**: Agent decisions within 2 seconds
3. **Quality**: 95% agreement with human annotators
4. **Cost**: Minimize LLM API calls through caching and routing

---

## Solution Architecture

```
[Task Queue (SQS)]
       |
       v
[Agent Router]
  |-- Simple tasks --> Rule-based agent (no LLM)
  |-- Medium tasks --> LLM agent (cached)
  |-- Complex tasks --> LLM agent + human review
       |
       v
[LangGraph Agent Framework]
  |-- State management
  |-- Tool access (DB queries, API calls)
  |-- Decision logging
       |
       v
[Human Review Queue] <--> [Annotation Platform]
       |
       v
[Results Store (PostgreSQL)]
  |-- Decisions
  |-- Audit trail
  |-- Performance metrics
```

### Key Design Decisions

#### Agent Architecture (LangGraph)
```python
from langgraph.graph import StateGraph

class AnnotationState:
    task: dict
    context: list[dict]
    decision: str | None
    confidence: float
    needs_human_review: bool

def build_agent_graph():
    graph = StateGraph(AnnotationState)

    graph.add_node("fetch_context", fetch_context)
    graph.add_node("check_cache", check_cache)
    graph.add_node("llm_decide", llm_decide)
    graph.add_node("route_to_human", route_to_human)
    graph.add_node("save_result", save_result)

    graph.add_edge("fetch_context", "check_cache")
    graph.add_conditional_edges(
        "check_cache",
        lambda s: "save_result" if s.decision else "llm_decide"
    )
    graph.add_conditional_edges(
        "llm_decide",
        lambda s: "route_to_human" if s.confidence < 0.85 else "save_result"
    )
    graph.add_edge("route_to_human", "save_result")

    return graph.compile()
```

#### Data Layer
- **PostgreSQL**: Structured task data, results, audit trail
- **Redis**: Agent decision cache, session state
- **S3**: Unstructured documents, images
- **Vector DB (pgvector)**: Semantic search for similar past decisions

#### Cost Optimization
- Cache similar decisions (Redis, 30-minute TTL)
- Route simple tasks to rule-based agents (no LLM cost)
- Batch similar tasks for single LLM call
- Use smaller models for easy tasks, larger for complex

#### Feedback Loop
1. Human reviews agent decisions (agree/disagree)
2. Agreement data stored in PostgreSQL
3. Nightly batch: retrain routing model on new feedback
4. Update confidence thresholds per task type
5. Agent improves over time (fewer human reviews needed)

### Monitoring

- Agent accuracy vs human reviewers
- Average confidence scores (trending up = good)
- Human review queue depth
- LLM API costs per task type
- Cache hit rate
- End-to-end latency percentiles

---

## Follow-up Questions

1. How do you prevent agent decision loops?
2. What if the LLM model degrades in quality?
3. How do you handle disagreements between agents and human reviewers?
4. How would you A/B test a new agent model?
5. How do you ensure data privacy when agents access customer data?
