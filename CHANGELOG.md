# Changelog

All notable changes to Rafeeq Kernel will be documented in this file.

## [2.3.0] - 2026-07-29

### Added
- 🐳 **Docker & Compose** — Multi-stage Dockerfile, production & dev compose files
- ☸️ **Kubernetes** — Full K8s manifests (Namespace, Deployment, Service, Ingress, HPA, Redis)
- ⛵ **Helm Chart** — Complete Helm chart with templates for all resources
- 🏗️ **Terraform** — DigitalOcean infrastructure as code
- 📊 **Monitoring Stack** — Prometheus + Grafana + Alert Rules + 6 Exporters
- 🌐 **Nginx** — Reverse proxy with SSL, rate limiting, compression, WebSocket
- 🚀 **CI/CD** — GitHub Actions (Lint → Test → Security → Build → Deploy)
- ❤️ **Health Monitor** — Automated health checks every 15 minutes
- 🔐 **Security** — CodeQL, Dependabot, Bandit, Trivy, pre-commit hooks
- 🧪 **Testing** — pytest, tox, 16+ tests across health, auth, API, WebSocket, evolution
- 🔌 **WebSocket API** — Real-time chat and agent endpoints
- 🧬 **Evolution API** — Dedicated router for self-evolution engine
- 🛡️ **Middleware** — Rate limiting, logging, security headers
- 🏥 **Health Endpoints** — 7 health checks + Prometheus metrics + K8s probes
- 🔧 **Scripts** — setup, deploy, rollback, backup, health-check, migrate, seed, certbot
- 📄 **Documentation** — README (EN/AR), CONTRIBUTING, SECURITY, full docs

### Fixed
- Removed `.env` from Git tracking (security fix)
- Fixed TODO in ai_engine.py template
- Added Redis optional initialization (fail-open)
- Fixed render.yaml for Render Free Plan (workers 2→1)

### Infrastructure
- PostgreSQL 16 + Redis 7 + Prometheus + Grafana + Node Exporter
- Auto-scaling HPA (3-10 replicas)
- Rolling updates with zero downtime
- SSL/TLS with Let's Encrypt
- Daily backups with S3 upload

## [2.2.1] - 2026-07-21

### Fixed
- Fixed Render deployment issues
- Updated database connection handling

## [2.2.0] - 2026-07-20

### Added
- Self-evolution engine
- Multi-agent orchestration
- GitHub integration
- Workspace management

## [2.1.0] - 2026-07-18

### Added
- FastAPI backend
- PostgreSQL database
- JWT authentication
- Session management

## [2.0.0] - 2026-07-12

### Added
- Initial release
- HTML frontend pages
- Basic API endpoints
