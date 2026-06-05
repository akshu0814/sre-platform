# Runbook: Deployment Rollback

## When to use this runbook
- New deployment caused errors
- Error rate spiked after deployment
- Customers reporting issues after release

## Decision: Rollback vs Hotfix

| Situation | Action |
|-----------|--------|
| Error rate > 5% | Rollback immediately |
| Service completely down | Rollback immediately |
| Minor bug, workaround exists | Hotfix |
| Data migration involved | Consult senior engineer |

## Rollback Steps

### Step 1: Confirm deployment caused the issue
```bash
# Check when error rate started
# Compare with deployment time in GitHub Actions
# If they match → rollback!
```

### Step 2: Rollback Helm deployment
```bash
# See deployment history
helm history order-service

# Rollback to previous version
helm rollback order-service 1

# Watch rollout status
kubectl rollout status deployment/order-service
```

### Step 3: Verify rollback worked
```bash
# Check health
curl http://localhost:3000/health

# Check error rate in Grafana
# Query: rate(http_requests_total{status_code=~"5.."}[5m])
# Should drop back to 0%

# Run full health check
python3 scripts/health-check.py
```

### Step 4: Communicate to stakeholders
Post in #incidents Slack channel: