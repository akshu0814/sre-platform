# SLO Definitions — Restaurant SRE Platform

## What is an SLO?

A Service Level Objective (SLO) is a target reliability 
goal for a service. It defines how reliable your service 
needs to be and helps you make decisions about when to 
prioritize reliability vs new features.

SLA = contract with customers (external)
SLO = internal target we aim for
SLI = the actual measurement

Example:
SLI: current availability = 99.95%
SLO: target availability = 99.9%
SLA: promised availability = 99.5%

---

## Order Service SLOs

### SLO 1 — Availability
Target:     99.9% availability per month
Measurement: % of time /health returns 200

PromQL:
sum(rate(http_requests_total{status_code="200"}[30d]))
/
sum(rate(http_requests_total[30d])) * 100

Error Budget:
99.9% SLO = 0.1% allowed downtime
Per month  = 43.8 minutes downtime allowed
Per week   = 10.1 minutes downtime allowed
Per day    = 1.44 minutes downtime allowed

### SLO 2 — Latency
Target:     99% of requests complete in under 500ms
Measurement: p99 latency over 30 days

PromQL:
histogram_quantile(0.99,
  rate(http_request_duration_seconds_bucket[30d])
) < 0.5

Breakdown:
p50 target: under 100ms (50% of requests)
p95 target: under 300ms (95% of requests)
p99 target: under 500ms (99% of requests)

### SLO 3 — Error Rate
Target:     under 0.1% error rate per day
Measurement: % of requests returning 5xx

PromQL:
rate(http_requests_total{status_code=~"5.."}[1d])
/
rate(http_requests_total[1d]) * 100 < 0.1

---

## Error Budget

Error budget = how much unreliability you can afford

Example for 99.9% availability SLO:
Total minutes in month = 43,800
Allowed downtime = 43,800 * 0.001 = 43.8 minutes

If you spent 30 minutes down this month:
Remaining budget = 43.8 - 30 = 13.8 minutes

Policy:
Budget over 50% remaining  → deploy freely
Budget under 50% remaining → be careful with deployments
Budget exhausted           → freeze deployments
                             focus only on reliability

---

## SLO Dashboard Queries

Current availability %:
sum(rate(http_requests_total{status_code="200"}[7d]))
/
sum(rate(http_requests_total[7d])) * 100

Current p99 latency:
histogram_quantile(0.99,
  rate(http_request_duration_seconds_bucket[1h]))

Current error rate:
rate(http_requests_total{status_code=~"5.."}[1h])
/
rate(http_requests_total[1h]) * 100

Error budget remaining %:
100 - (
  sum(rate(http_requests_total{status_code=~"5.."}[30d]))
  /
  sum(rate(http_requests_total[30d])) * 100
  /
  0.1 * 100
)

---

## What Happens When SLO is Breached?

Step 1: Alert fires immediately
Step 2: On-call engineer investigates
Step 3: Incident declared if not resolved in 5 minutes
Step 4: Post Incident Report written
Step 5: Error budget reviewed
Step 6: If budget exhausted:
        → No new feature deployments
        → All hands on reliability improvements
        → Weekly review until budget recovered