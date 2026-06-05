# On-Call Guide — Restaurant SRE Platform

## Overview
This guide is for engineers on the on-call rotation.
When an alert fires, follow this guide to respond quickly
and confidently.

## Access Links
| Tool | URL | Credentials |
|------|-----|-------------|
| Grafana | http://grafana:3001 | admin/admin123 |
| Prometheus | http://prometheus:9090 | no auth |
| AWS Console | https://console.aws.amazon.com | SSO login |

## Alert Severity Levels

| Severity | Response Time | Example |
|----------|--------------|---------|
| P1 Critical | 5 minutes | Service down, 100% error rate |
| P2 High | 15 minutes | Error rate > 5%, p99 > 500ms |
| P3 Medium | 1 hour | CPU > 85%, pod restarting |
| P4 Low | Next business day | Disk usage > 70% |

## First 5 Minutes Checklist
When any alert fires, always do these steps first:

```bash
# 1. Check if service is responding
curl http://order-service:3000/health

# 2. Check pod status
kubectl get pods -l app=order-service

# 3. Check recent logs
kubectl logs -l app=order-service --tail=50

# 4. Check recent events
kubectl get events --sort-by='.lastTimestamp'

# 5. Check resource usage
kubectl top pods
kubectl top nodes
```

## Escalation Path