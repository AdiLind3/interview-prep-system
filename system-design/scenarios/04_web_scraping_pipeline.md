# System Design: Scalable Web Scraping Pipeline

**Difficulty**: Medium
**Time**: 30 minutes
**Topics**: Web Scraping, Rate Limiting, Data Pipeline, Error Handling
**Relevance**: The tasq.ai job posting specifically mentions building web scrapers

---

## Problem Statement

Design a scalable web scraping system that collects product data from 100+ e-commerce websites, handles anti-scraping measures, and feeds clean data into downstream processing pipelines.

---

## Requirements

### Functional Requirements
1. Scrape product data (name, price, description, images) from 100+ websites
2. Handle different website structures (each site has a custom parser)
3. Detect and handle anti-scraping measures (rate limits, CAPTCHAs, IP blocks)
4. Deduplicate products across sources
5. Schedule recurring scrapes (daily, hourly for price changes)
6. Track scraping success rates per source

### Non-Functional Requirements
1. **Scale**: 1M pages per day
2. **Freshness**: Price data updated every 6 hours
3. **Reliability**: Retry failed scrapes, no data loss
4. **Compliance**: Respect robots.txt, rate limits

---

## Solution Architecture

```
[Scheduler (Airflow)]
       |
       v
[URL Queue (SQS)]
       |
       v
[Scraper Workers (ECS Fargate)]
  |-- Proxy rotation
  |-- Rate limiter per domain
  |-- Custom parsers per site
       |
       v
[Raw Storage (S3)]
       |
       v
[Parser/Extractor (Lambda)]
       |
       v
[Deduplication + Validation]
       |
       v
[Clean Data (PostgreSQL + S3)]
```

### Key Components

#### 1. URL Management
- URL queue in SQS with priority (high-value sites first)
- Bloom filter for URL deduplication
- Sitemap parser for discovering new pages

#### 2. Scraper Workers
```python
class ScraperWorker:
    def __init__(self, config: SiteConfig):
        self.rate_limiter = RateLimiter(
            requests_per_second=config.max_rps,
            domain=config.domain
        )
        self.proxy_pool = ProxyPool(size=50)
        self.parser = config.parser_class()

    def scrape(self, url: str) -> dict:
        self.rate_limiter.wait()
        proxy = self.proxy_pool.get_next()

        response = requests.get(
            url,
            proxies={"https": proxy},
            headers=self.get_random_headers(),
            timeout=10
        )

        if response.status_code == 429:  # Rate limited
            self.rate_limiter.backoff()
            raise RetryableError("Rate limited")

        return self.parser.extract(response.text)
```

#### 3. Rate Limiting Strategy
- Per-domain rate limits (respect robots.txt Crawl-delay)
- Exponential backoff on 429/503 responses
- Rotating user agents and proxy IPs
- Random delays between requests (1-5 seconds)
- Time-of-day scheduling (scrape during off-peak hours)

#### 4. Error Handling
- Retry queue for transient failures (network, rate limits)
- Dead letter queue for permanent failures (404, parse errors)
- Alert on success rate drops below 90%
- Circuit breaker per domain (stop scraping if blocked)

#### 5. Anti-Scraping Countermeasures
- Proxy rotation (residential proxies for strict sites)
- Browser fingerprint randomization
- JavaScript rendering for dynamic sites (Playwright on ECS)
- CAPTCHA detection and routing to human solvers

### Monitoring

- Success rate per domain (alert if < 90%)
- Average response time per domain
- Proxy health and rotation metrics
- Data freshness per source
- Cost per page scraped

---

## Follow-up Questions

1. How do you handle websites that change their HTML structure?
2. What is your approach to ethical scraping?
3. How do you scale from 100 to 10,000 websites?
4. How do you handle JavaScript-heavy single-page applications?
5. What is your strategy for monitoring data quality from scraped sources?
