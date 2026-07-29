#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# Rafeeq Kernel v2.3.0 — Database Seeding Script
# ═══════════════════════════════════════════════════════════════════

set -e

echo "🌱 Rafeeq Database Seeder"
echo "========================="

# Load environment
if [ -f .env ]; then
  export $(cat .env | grep -v '^#' | xargs)
fi

if [ -z "$DATABASE_URL" ]; then
  echo "❌ DATABASE_URL not set"
  exit 1
fi

echo "🗄️  Seeding database..."

psql "$DATABASE_URL" << 'EOF'
-- Seed admin user (change password in production!)
INSERT INTO users (username, email, password_hash, role, status, email_verified, full_name)
VALUES 
  ('admin', 'admin@rafeeq.ai', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYA.qGZvKG6G', 'superadmin', 'active', TRUE, 'System Administrator'),
  ('demo', 'demo@rafeeq.ai', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYA.qGZvKG6G', 'user', 'active', TRUE, 'Demo User')
ON CONFLICT (username) DO NOTHING;

-- Seed system metrics
INSERT INTO system_metrics (metric_type, metric_name, value, unit, labels)
VALUES 
  ('system', 'initial_setup', 1, 'boolean', '{"version": "2.3.0"}'),
  ('system', 'deployment_count', 1, 'count', '{"environment": "production"}')
ON CONFLICT DO NOTHING;

-- Seed evolution log
INSERT INTO evolution_logs (version, action, target_file, change_summary, status)
VALUES 
  ('2.3.0', 'initial_setup', 'system', 'Database initialized with seed data', 'success')
ON CONFLICT DO NOTHING;

EOF

echo "✅ Database seeded successfully"
echo "   Admin user: admin / admin123"
echo "   Demo user:  demo / admin123"
echo "   ⚠️  CHANGE PASSWORDS IN PRODUCTION!"
