# Restaurant SRE Platform 🍕🌮🍗

A production-grade Site Reliability Engineering platform 
simulating global fast-food chain infrastructure 
(inspired by Yum Brands: KFC, Pizza Hut, Taco Bell).

Built as a hands-on SRE portfolio project covering 
infrastructure, CI/CD, monitoring, incident response, 
and automation.

---

## Architecture

```mermaid
graph TD
    Dev[Developer Laptop] -->|git push| GitHub[GitHub Repository]
    GitHub -->|triggers| Actions[GitHub Actions CI/CD]
    Actions -->|runs| Tests[Jest Unit Tests]
    Actions -->|scans| Trivy[Trivy Security Scan]
    Actions -->|builds| Docker[Docker Image]
    Actions -->|pushes| Registry[GitHub Container Registry]
    Actions -->|deploys| EKS[AWS EKS Cluster]

    EKS -->|runs| OrderService[Order Service Pod]
    OrderService -->|reads/writes| RDS[AWS RDS PostgreSQL]
    OrderService -->|exposes| Metrics[/metrics endpoint]

    Prometheus[Prometheus] -->|scrapes every 15s| Metrics
    Grafana[Grafana] -->|reads| Prometheus
    Prometheus -->|fires alerts| Alertmanager[Alertmanager]
    Alertmanager -->|pages| OnCall[On-Call Engineer]

    VPC[AWS VPC] -->|contains| EKS
    VPC -->|contains| RDS
```

---

## What This Project Demonstrates

| Skill | Implementation |
|-------|---------------|
| Infrastructure as Code | Terraform modules for VPC, EKS, RDS |
| CI/CD Pipeline | GitHub Actions with test, scan, build, deploy |
| Containerization | Multi-stage Docker builds |
| Kubernetes | Helm charts with HPA, probes, ingress |
| Monitoring | Prometheus + Grafana with RED metrics |
| Alerting | 5 production-grade alert rules |
| Incident Response | Simulation scripts + PIR template |
| Automation | Python health-check with auto-remediation |
| Security | Trivy scanning, non-root containers, private subnets |
| Documentation | Runbooks, SLOs, ADRs, on-call guide |

---

## Project Structure

restaurant-sre-platform/
├── .github/workflows/
│   ├── deploy.yml            # CI/CD pipeline
│   └── pr-check.yml          # PR validation
├── apps/
│   └── order-service/
│       ├── __tests__/
│       │   └── orders.test.js # Unit tests
│       ├── server.js          # Express API
│       ├── Dockerfile         # Multi-stage build
│       └── package.json
├── helm/order-service/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yml
│       ├── service.yml
│       ├── hpa.yml
│       └── ingress.yml
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yml     # Scrape config
│   │   └── alert-rules.yml    # 5 alert rules
│   └── grafana/dashboards/
│       └── order-service.json # Dashboard
├── scripts/
│   ├── health-check.py        # Auto-remediation
│   ├── cert-rotation-check.py # Cert expiry check
│   ├── cost-report.sh         # AWS cost report
│   └── simulate-failures/     # Incident simulation
├── terraform/
│   ├── modules/
│   │   ├── vpc/               # Network infrastructure
│   │   ├── eks/               # Kubernetes cluster
│   │   └── rds/               # PostgreSQL database
│   └── environments/dev/      # Dev environment
├── runbooks/                  # Incident response guides
├── docs/                      # Architecture + SLOs
└── docker-compose.yaml        # Local development

---

## Quick Start

### Prerequisites
- Node.js 18+
- Terraform 1.5+
- Docker Desktop
- kubectl + Helm
- AWS CLI

### Run locally
```bash
# Clone the repo
git clone https://github.com/akshu0814/sre-platform.git
cd sre-platform

# Start all services
docker-compose up --build

# Run health check
source venv/bin/activate
python3 scripts/health-check.py
```

### Run tests
```bash
cd apps/order-service
npm test
```

### Deploy infrastructure
```bash
cd terraform/environments/dev
terraform init
terraform plan
terraform apply
```

---

## Monitoring

| Tool | URL | Purpose |
|------|-----|---------|
| Order Service | http://localhost:3000 | REST API |
| Prometheus | http://localhost:9090 | Metrics |
| Grafana | http://localhost:3001 | Dashboards |

### Key Metrics (RED Method)
- **Rate:** `sum(rate(http_requests_total[5m]))`
- **Errors:** `rate(http_requests_total{status_code=~"5.."}[5m]) / rate(http_requests_total[5m]) * 100`
- **Duration:** `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))`

---

## Alert Rules

| Alert | Condition | Severity |
|-------|-----------|----------|
| OrderServiceDown | Service unreachable > 1min | Critical |
| OrderServiceHighErrorRate | Error rate > 5% for 2min | Critical |
| OrderServiceHighLatency | p99 > 500ms for 5min | Critical |
| NodeCPUHigh | CPU > 85% for 10min | Warning |
| PodCrashLooping | Restarts > 5 in 15min | Critical |

---

## Runbooks

- [Order Service Outage](runbooks/order-service-outage.md)
- [Deployment Rollback](runbooks/deployment-rollback.md)
- [Alert Response Guide](runbooks/alert-response.md)
- [On-Call Guide](runbooks/on-call-guide.md)
- [Sample Post Incident Report](runbooks/sample-pir-high-error-rate.md)

---

## Tech Stack

- **Cloud:** AWS (EKS, RDS, VPC)
- **IaC:** Terraform
- **Container:** Docker
- **Orchestration:** Kubernetes + Helm
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus + Grafana
- **Language:** Node.js, Python, Bash
- **Database:** PostgreSQL