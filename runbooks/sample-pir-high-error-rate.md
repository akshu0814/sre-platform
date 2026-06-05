# Post Incident Report — High Error Rate
**Date:** 2026-06-04  
**Severity:** P1 — Critical  
**Duration:** 10 minutes  
**Service:** order-service  
**Author:** Akshu Patel  

## Incident Summary
The order-service experienced a 100% error rate on POST /orders 
endpoint during dinner rush. All customer orders were failing 
with 400 Bad Request errors. The issue was detected via Grafana 
alert and resolved within 10 minutes.

## Timeline
| Time  | Event |
|-------|-------|
| 10:40 | Alert fires — error rate > 5% |
| 10:41 | On-call engineer paged |
| 10:42 | Engineer checks /health → service is UP |
| 10:43 | Engineer checks error logs → bad request data |
| 10:44 | Root cause identified — missing required fields |
| 10:45 | Identified bad deployment from frontend team |
| 10:48 | Frontend team rolled back their deployment |
| 10:50 | Error rate back to 0% — incident resolved |

## Root Cause Analysis (5 Whys)
**Why** did customers get errors?
→ POST /orders was returning 400 errors

**Why** were 400 errors returned?
→ Requests were missing required fields (item, restaurant)

**Why** were fields missing?
→ Frontend deployed a new version with wrong API payload

**Why** was wrong payload deployed?
→ Frontend team changed field names without checking API contract

**Why** was there no check?
→ No integration tests between frontend and order-service

## Impact
- Customers affected: All customers during 10:40-10:50
- Orders lost: ~500 orders (estimated)
- Revenue impact: ~$2,500 lost revenue
- SLA breach: Yes — availability dropped below 99.9%

## Resolution
Frontend team rolled back their deployment to previous version.
Order-service required no changes — it was working correctly.

## Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| Add integration tests between frontend and order-service | Dev Team | 2026-06-11 |
| Add API contract testing to CI/CD pipeline | SRE Team | 2026-06-11 |
| Add alert for sudden spike in 400 errors | SRE Team | 2026-06-07 |
| Document API payload format for all teams | Dev Team | 2026-06-07 |

## Lessons Learned
1. Service being healthy does not mean requests are correct
2. Always check logs and make a test request before escalating
3. Integration tests would have caught this before deployment