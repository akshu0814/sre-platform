# Architecture Decision Records (ADRs)

## What is an ADR?

An Architecture Decision Record documents WHY a technical 
decision was made — not just what was decided. This helps 
future engineers understand the reasoning behind choices.

---

## ADR-001: Why EKS over ECS for Container Orchestration

**Status:** Accepted
**Date:** 2026-06-04

### Context
We needed a container orchestration platform to run the 
order-service at scale across multiple restaurant regions.

### Options Considered
- AWS ECS (Elastic Container Service)
- AWS EKS (Elastic Kubernetes Service)
- Self-managed Kubernetes

### Decision
We chose EKS.

### Reasons
- Kubernetes is industry standard — engineers already know it
- Helm charts make deployments reusable across environments
- HPA (autoscaling) is more flexible than ECS autoscaling
- Easier to migrate to other clouds if needed
- Most enterprise companies use Kubernetes

### Consequences
- More complex setup than ECS
- Higher learning curve for new engineers
- AWS manages the control plane — reducing operational burden

---

## ADR-002: Why Prometheus and Grafana over CloudWatch

**Status:** Accepted
**Date:** 2026-06-04

### Context
We needed a monitoring solution for our order-service 
running on EKS.

### Options Considered
- AWS CloudWatch (native AWS monitoring)
- Prometheus + Grafana (open source)
- Datadog (commercial SaaS)

### Decision
We chose Prometheus + Grafana.

### Reasons
- Open source — no per-metric cost
- Industry standard for Kubernetes monitoring
- PromQL is powerful and flexible
- Grafana dashboards are highly customizable
- Works across any cloud — not AWS specific
- kube-prometheus-stack makes installation easy

### Consequences
- Need to manage Prometheus storage ourselves
- More setup than CloudWatch
- No built-in AWS service metrics (need exporters)

---

## ADR-003: Why Helm for Kubernetes Deployments

**Status:** Accepted
**Date:** 2026-06-04

### Context
We needed a way to deploy the order-service to Kubernetes 
consistently across dev, staging, and production.

### Options Considered
- Raw kubectl apply with YAML files
- Helm charts
- Kustomize

### Decision
We chose Helm.

### Reasons
- Single command deployment: helm install
- Easy rollback: helm rollback
- Values files allow different configs per environment
- Version history built in
- Industry standard — most companies use Helm
- Large ecosystem of pre-built charts

### Consequences
- Need to learn Helm templating syntax
- Extra abstraction layer over Kubernetes YAML
- Chart versioning needs to be managed carefully

---

## ADR-004: Why Multi-Stage Docker Builds

**Status:** Accepted
**Date:** 2026-06-04

### Context
We needed to containerize the order-service for deployment.

### Options Considered
- Single stage Dockerfile
- Multi-stage Dockerfile

### Decision
We chose multi-stage builds.

### Reasons
- Production image is 60% smaller
- No build tools in production image
- Better security — smaller attack surface
- Faster deployments — smaller images pull faster
- Industry best practice for Node.js apps

### Consequences
- Slightly more complex Dockerfile
- Build takes marginally longer
- Worth it for security and size benefits

---

## ADR-005: Why Terraform Modules over Single File

**Status:** Accepted
**Date:** 2026-06-04

### Context
We needed to provision AWS infrastructure for VPC, EKS, 
and RDS.

### Options Considered
- Single large Terraform file
- Separate Terraform modules per resource type

### Decision
We chose separate modules.

### Reasons
- Reusable across environments (dev, staging, prod)
- Each module can be versioned independently
- Easier to test individual components
- Different teams can own different modules
- Follows DRY (Don't Repeat Yourself) principle

### Consequences
- More files to manage
- Need to understand module inputs and outputs
- Worth it for reusability and maintainability