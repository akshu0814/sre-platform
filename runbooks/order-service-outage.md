# Runbook: Order Service Outage

## When to use this runbook
- Alert: OrderServiceDown fires
- Customers reporting cannot place orders
- /health endpoint not responding

## Quick Triage (first 5 commands)
```bash
# 1. Check if service is responding
curl http://order-service:3000/health

# 2. Check pod/container status
docker-compose ps

# 3. Check recent logs
docker-compose logs order-service --tail=50

# 4. Check resource usage
docker stats --no-stream

# 5. Check recent events
docker-compose logs --tail=20
```

## Common Causes and Fixes

### Cause 1: Container crashed
**Symptoms:** docker-compose ps shows "Exit 1"
**Fix:**
```bash
docker-compose restart order-service
# Verify
curl http://localhost:3000/health
```

### Cause 2: Port conflict
**Symptoms:** "port already allocated" in logs
**Fix:**
```bash
# Find what's using port 3000
lsof -i :3000
# Kill the process
kill -9 <PID>
# Restart service
docker-compose restart order-service
```

### Cause 3: Bad deployment
**Symptoms:** Service started after deployment
**Fix:**
```bash
# Rollback Helm deployment
helm rollback order-service 1
# Verify
curl http://localhost:3000/health
```

### Cause 4: Database connection failed
**Symptoms:** "connection refused" in logs to RDS
**Fix:**
```bash
# Check RDS status in AWS console
# Check security group allows port 5432
# Check RDS is not in maintenance window
```

## Verification Steps After Fix
```bash
# 1. Health check passes
curl http://localhost:3000/health
# Expected: {"status":"healthy"}

# 2. Orders endpoint works
curl http://localhost:3000/orders
# Expected: {"orders":[...]}

# 3. Metrics are flowing
curl http://localhost:3000/metrics
# Expected: prometheus metrics output

# 4. Run automated health check
python3 scripts/health-check.py
# Expected: ALL SYSTEMS HEALTHY
```

## Post Incident
1. Write PIR using template in runbooks/post-incident-report-template.md
2. Add action items to prevent recurrence
3. Update this runbook if new cause found