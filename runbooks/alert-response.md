# Alert Response Runbook

## OrderServiceHighErrorRate

### What it means
More than 5% of requests are returning 5xx errors.
This means customers cannot place orders successfully.

### How to investigate
```bash
# Check pod status
kubectl get pods -n default

# Check pod logs
kubectl logs -l app=order-service --tail=100

# Check recent events
kubectl get events --sort-by='.lastTimestamp'

# Check error rate in Prometheus
# Query: rate(http_requests_total{status_code=~"5.."}[5m])
```

### How to resolve
1. Check logs for error messages
2. Check if database is reachable
3. Check if recent deployment caused the issue
4. If deployment caused it: helm rollback order-service
5. If database issue: check RDS status in AWS console

---

## OrderServiceHighLatency

### What it means
99% of requests are taking more than 500ms.
Customers are experiencing slow response times.

### How to investigate
```bash
# Check resource usage
kubectl top pods -l app=order-service

# Check HPA status
kubectl get hpa

# Check node resources
kubectl top nodes
```

### How to resolve
1. Check if pods are CPU throttled
2. Check if HPA has scaled up enough
3. Check database query performance
4. If CPU throttled: increase resource limits in values.yaml

---

## OrderServiceDown

### What it means
Order service is completely unreachable.
All customers cannot place orders.

### How to investigate
```bash
# Check pod status immediately
kubectl get pods -l app=order-service

# Describe the pod for more details
kubectl describe pod -l app=order-service

# Check logs
kubectl logs -l app=order-service --previous
```

### How to resolve
1. If CrashLoopBackOff: check logs for startup errors
2. If Pending: check node resources
3. If ImagePullBackOff: check image name in values.yaml
4. Emergency rollback: helm rollback order-service 1

---

## NodeCPUHigh

### What it means
A Kubernetes node is using more than 85% CPU.
Risk of pods being throttled or evicted.

### How to investigate
```bash
# Check which node is affected
kubectl top nodes

# Check which pods are using most CPU
kubectl top pods --all-namespaces

# Check HPA status
kubectl get hpa --all-namespaces
```

### How to resolve
1. Check if HPA has reached maximum replicas
2. If yes: increase maxReplicas in values.yaml
3. If persistent: add more nodes to EKS node group
4. Update Terraform: increase max_size in eks module

---

## PodCrashLooping

### What it means
A pod is repeatedly crashing and restarting.
Something is wrong with the application startup.

### How to investigate
```bash
# Find the crashing pod
kubectl get pods --all-namespaces

# Check logs from previous crashed container
kubectl logs <pod-name> --previous

# Describe pod for events
kubectl describe pod <pod-name>
```

### How to resolve
1. Check logs for error messages
2. Check if environment variables are set correctly
3. Check if database connection is working
4. Check if image has a bug: review recent commits
5. Rollback if needed: helm rollback order-service 1