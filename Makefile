# ═══════════════════════════════════════════════════════════════════
# Rafeeq Kernel v2.3.0 — Makefile
# Quick commands for development & deployment
# ═══════════════════════════════════════════════════════════════════

.PHONY: help setup dev prod stop logs test lint clean backup health seed migrate shell redis-cli psql deploy rollback

help: ## Show this help
	@echo "🐺 Rafeeq Kernel v2.3.0 — Available Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  [36m%-15s[0m %s
", $$1, $$2}'

setup: ## One-time setup (creates .env, SSL certs, directories)
	@chmod +x scripts/setup.sh && ./scripts/setup.sh

dev: ## Start development environment with hot-reload
	@docker-compose -f docker-compose.dev.yml up -d
	@echo "🚀 Dev environment running on http://localhost:8001"
	@echo "   API Docs: http://localhost:8001/api/docs"

prod: ## Start production environment
	@docker-compose up -d
	@echo "🚀 Production environment running!"
	@echo "   🌐 App:       https://localhost"
	@echo "   📊 Grafana:   http://localhost:3000 (admin/rafeeq_grafana_2026)"
	@echo "   📈 Prometheus: http://localhost:9090"
	@echo "   🔌 API Docs:  https://localhost/api/docs"

stop: ## Stop all containers
	@docker-compose down
	@docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
	@echo "🛑 All containers stopped"

logs: ## Follow application logs
	@docker-compose logs -f app

test: ## Run all tests
	@docker-compose exec app pytest -v --cov=. --cov-report=term

test-unit: ## Run unit tests only
	@docker-compose exec app pytest -v -m unit

test-integration: ## Run integration tests only
	@docker-compose exec app pytest -v -m integration

lint: ## Run linting
	@docker-compose exec app black --check .
	@docker-compose exec app flake8 .
	@docker-compose exec app isort --check-only .

format: ## Format code with black and isort
	@docker-compose exec app black .
	@docker-compose exec app isort .

security: ## Run security scans
	@docker-compose exec app bandit -r . -f json -o bandit-report.json
	@echo "🔒 Security scan complete"

backup: ## Run backup script
	@chmod +x scripts/backup.sh && ./scripts/backup.sh

health: ## Run health check
	@chmod +x scripts/health-check.sh && ./scripts/health-check.sh

clean: ## Clean Docker volumes, images, and cache
	@docker-compose down -v
	@docker system prune -f
	@echo "🧹 Cleanup complete"

migrate: ## Run database migrations
	@chmod +x scripts/migrate.sh && ./scripts/migrate.sh

seed: ## Seed database with initial data
	@chmod +x scripts/seed.sh && ./scripts/seed.sh

shell: ## Open shell in app container
	@docker-compose exec app /bin/bash

redis-cli: ## Open Redis CLI
	@docker-compose exec redis redis-cli

psql: ## Open PostgreSQL CLI
	@docker-compose exec postgres psql -U rafeeq -d rafeeq

deploy: ## Deploy to production (Docker)
	@chmod +x scripts/deploy.sh && ./scripts/deploy.sh docker

deploy-k8s: ## Deploy to Kubernetes
	@chmod +x scripts/deploy.sh && ./scripts/deploy.sh k8s

deploy-helm: ## Deploy with Helm
	@chmod +x scripts/deploy.sh && ./scripts/deploy.sh helm

rollback: ## Rollback deployment
	@chmod +x scripts/rollback.sh && ./scripts/rollback.sh docker

update-deps: ## Update Python dependencies
	@pip install -r requirements.txt --upgrade
	@pip freeze > requirements.txt
	@echo "📦 Dependencies updated"
