<div align="center">

# ⚡ TaskFlow

### Cloud & DevOps Automation on AWS

[![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=white)](https://aws.amazon.com)
[![Terraform](https://img.shields.io/badge/Terraform-844FBA?style=for-the-badge&logo=terraform&logoColor=white)](https://www.terraform.io)
[![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white)](https://www.jenkins.io)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)

*End-to-end DevOps pipeline with Terraform-provisioned AWS infrastructure, Jenkins CI/CD, containerized deployment, and full observability stack.*

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Infrastructure](#-infrastructure)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Monitoring & Observability](#-monitoring--observability)
- [API Endpoints](#-api-endpoints)
- [Getting Started](#-getting-started)

---

## 🔍 Overview

TaskFlow is a production-grade DevOps automation project demonstrating a complete infrastructure-to-deployment pipeline on AWS. It features Infrastructure as Code, automated CI/CD, containerized microservices, and real-time monitoring — built with AI-assisted engineering for accelerated delivery.

### Key Highlights

| Metric | Detail |
|--------|--------|
| **Infrastructure** | Terraform-provisioned custom VPC (`10.20.0.0/16`) on AWS |
| **CI/CD** | 5-stage Jenkins pipeline with GitHub webhook integration |
| **Containers** | 4-service Docker Compose stack with health checks |
| **Monitoring** | Prometheus metrics + Grafana dashboards (15s scrape interval) |
| **AI-Assisted** | 40% faster environment setup via AI engineering agents |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                        AWS Cloud                          │
│  ┌─────────────────── VPC (10.20.0.0/16) ──────────────┐ │
│  │                                                      │ │
│  │  ┌──────────────┐         ┌──────────────────────┐  │ │
│  │  │   Jenkins    │─webhook─│   GitHub Repository   │  │ │
│  │  │  (t3.micro)  │         └──────────────────────┘  │ │
│  │  └──────┬───────┘                                    │ │
│  │         │ deploy                                     │ │
│  │         ▼                                            │ │
│  │  ┌──────────────────────────────────┐               │ │
│  │  │      Application EC2 Instance    │               │ │
│  │  │  ┌─────────┐  ┌──────────────┐  │               │ │
│  │  │  │ FastAPI  │  │  PostgreSQL  │  │               │ │
│  │  │  │   App    │  │   Database   │  │               │ │
│  │  │  └────┬─────┘  └──────────────┘  │               │ │
│  │  │       │                           │               │ │
│  │  │  ┌────▼──────┐  ┌─────────────┐  │               │ │
│  │  │  │Prometheus │──│   Grafana   │  │               │ │
│  │  │  └───────────┘  └─────────────┘  │               │ │
│  │  └──────────────────────────────────┘               │ │
│  │         │                                            │ │
│  │    Internet Gateway ─── Public Subnet               │ │
│  └──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Cloud** | AWS EC2, VPC, IAM, Security Groups, EBS (encrypted gp3) |
| **IaC** | Terraform (VPC, Subnet, IGW, Route Tables, SGs, EC2) |
| **CI/CD** | Jenkins (5-stage pipeline), GitHub Webhooks |
| **Containers** | Docker, Docker Compose (4 services) |
| **Application** | Python, FastAPI, Pydantic, PostgreSQL |
| **Testing** | Pytest (endpoint behavior + input validation) |
| **Monitoring** | Prometheus (custom metrics), Grafana (dashboards) |

---

## ☁️ Infrastructure

Provisioned entirely with **Terraform**:

- **VPC**: Custom `10.20.0.0/16` with public subnet
- **Networking**: Internet Gateway, route tables, security groups
- **Compute**: `t3.micro` EC2 instances
- **Storage**: Encrypted `gp3` EBS volumes
- **Security**: Least-privilege IAM, restricted security groups

---

## 🔄 CI/CD Pipeline

**5-stage Jenkins pipeline** triggered via GitHub webhooks:

```
┌───────────┐    ┌──────────┐    ┌───────────┐    ┌─────────────┐    ┌──────────┐
│ Checkout  │───▶│  Test    │───▶│  Build    │───▶│ Smoke Test  │───▶│  Deploy  │
│  (Git)    │    │ (Pytest) │    │ (Docker)  │    │  (Health)   │    │(Compose) │
└───────────┘    └──────────┘    └───────────┘    └─────────────┘    └──────────┘
```

1. **Checkout** — Clone repository from GitHub
2. **Test** — Run containerized Pytest suite
3. **Build** — Build Docker image
4. **Smoke Test** — Validate container health
5. **Deploy** — Docker Compose deployment across all services

---

## 📊 Monitoring & Observability

- **Prometheus**: Custom request counter + latency histogram metrics with 15-second scrape intervals
- **Grafana**: Real-time dashboards for availability and request traffic monitoring
- **Health Checks**: Docker Compose health-check dependencies ensuring service startup order

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/ready` | Readiness probe |
| `GET` | `/tasks` | List all tasks |
| `POST` | `/tasks` | Create a task |
| `GET` | `/tasks/{id}` | Get task by ID |
| `PUT` | `/tasks/{id}` | Update a task |
| `DELETE` | `/tasks/{id}` | Delete a task |

---

## 🚀 Getting Started

### Prerequisites

- AWS account with CLI configured
- Terraform ≥ 1.0
- Docker & Docker Compose
- Jenkins (for CI/CD)

### Deploy Infrastructure

```bash
cd terraform/
terraform init
terraform plan
terraform apply
```

### Run Locally

```bash
docker-compose up -d
```

### Run Tests

```bash
docker-compose run --rm app pytest
```

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ☁️ by <a href="https://github.com/senthamizhvelan04">Senthamizhvelan M</a>
</p>
