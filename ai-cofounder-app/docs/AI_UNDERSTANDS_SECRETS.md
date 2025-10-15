# AI Cofounder Understands Secrets & Secure Deployment

## Overview

The AI Cofounder has been trained to understand secrets management and secure deployment practices. This document demonstrates what the AI knows and how it applies that knowledge.

---

## 🔐 What the AI Cofounder Understands

### 1. Secrets Inventory

The AI knows **7 categories** of secrets that applications need:

| Category | Examples | Used By | Rotation Schedule |
|----------|----------|---------|-------------------|
| **Model API Keys** | `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` | AI agents | 90 days |
| **Database Credentials** | `DATABASE_ENCRYPTION_KEY` | Backend | Never (key derivation) |
| **OAuth Secrets** | `GITHUB_CLIENT_SECRET` | Auth system | On compromise |
| **Webhook Secrets** | `STRIPE_WEBHOOK_SECRET` | Payment webhooks | On provider rotation |
| **Data Lake Credentials** | `S3_ACCESS_KEY`, `S3_SECRET_KEY` | Telemetry, backups | 90 days |
| **Deployment Tokens** | `GITHUB_DEPLOY_TOKEN` | CI/CD | On team changes |
| **Monitoring Keys** | `SENTRY_DSN` | Error tracking | Annually |

### 2. Storage Strategies Per Environment

The AI understands **different storage methods** for different environments:

#### Local Development
```bash
# .env file (gitignored)
OPENAI_API_KEY=sk-proj-test...
DATABASE_URL=file:./data/dev.db
```
- **Method**: `.env` file loaded by `dotenv`
- **Template**: `.env.example` committed to git
- **Security**: File permissions `600`, never commit actual `.env`

#### Docker Development
```yaml
# docker-compose.yml
services:
  backend:
    env_file: .env  # Reads from .env file
```
- **Method**: Environment section in docker-compose
- **Source**: Reads from `.env` file
- **Security**: Never commit secrets in `docker-compose.yml`

#### Production (Hetzner VPS)
```bash
# /etc/ai-cofounder/secrets.env
OPENAI_API_KEY=sk-proj-prod...
DATABASE_URL=file:./data/prod.db
```
- **Method**: SystemD environment file
- **File**: `/etc/ai-cofounder/secrets.env` (root:root 600)
- **Loading**: Docker reads from host environment
- **Backup**: Encrypted off-site backup

#### Production (Advanced)
- **Method**: HashiCorp Vault or AWS Secrets Manager
- **Access**: API calls at runtime
- **Security**: Centralized, audited, auto-rotated
- **When**: Multiple services, compliance requirements

### 3. Deployment Flow

The AI knows the **complete deployment flow** for secrets:

```
Development:
1. Developer copies .env.example → .env
2. Fills in dev/test credentials
3. Application loads via dotenv
4. .env is gitignored

Production:
1. Secrets stored in Vault or platform
2. Injected at container start
3. Rotated automatically
4. Audit trail maintained
5. Access via IAM/RBAC
```

### 4. Security Best Practices

The AI enforces **10 security principles**:

- **Least Privilege**: Each service gets only the secrets it needs
- **Environment Separation**: Dev secrets ≠ Staging ≠ Prod
- **Rotation**: Regular rotation schedule (see table above)
- **Encryption at Rest**: Secrets encrypted in storage
- **Encryption in Transit**: HTTPS/TLS always
- **Audit Logging**: Track who accessed what when
- **Access Control**: RBAC/IAM for secret access
- **Secret Scanning**: Automated git scanning
- **Expiration**: Secrets should expire and rotate
- **Revocation**: Immediate revocation on compromise

### 5. Never Do This

The AI knows to **never**:

- ❌ Commit secrets to git
- ❌ Put secrets in Dockerfile
- ❌ Put secrets in docker-compose.yml
- ❌ Log secrets
- ❌ Return secrets in API responses
- ❌ Use same secrets for dev and prod
- ❌ Hard-code secrets in source
- ❌ Share secrets via Slack/email
- ❌ Commit `.env` file

### 6. Validation Checklist

The AI validates **9 requirements** before deployment:

```
Pre-Deployment:
[ ] All secrets documented in SECRETS.md
[ ] .env.example up to date
[ ] .env in .gitignore
[ ] No secrets in Dockerfile/docker-compose
[ ] Production secrets stored securely
[ ] Rotation schedule defined
[ ] Access control configured
[ ] Backup plan for secrets
[ ] Incident response plan

Deployment:
[ ] All required env vars set
[ ] Application starts with prod secrets
[ ] No secrets logged
[ ] File permissions correct (600)
[ ] HTTPS/TLS enabled
[ ] Audit logging enabled

Post-Deployment:
[ ] Monitor access patterns
[ ] First rotation scheduled
[ ] Rotation procedure documented
[ ] Test rotation process
[ ] Review logs weekly
```

---

## 🤖 AI Awareness & Planning

### Detection

When generating code, the AI **automatically detects**:

- ✓ API key mentions in requirements
- ✓ Environment-specific configuration
- ✓ Services requiring authentication
- ✓ Third-party integrations needing secrets

### Planning

The AI **automatically creates**:

- ✓ `.env.example` template with all required secrets
- ✓ Documentation of what secrets are needed
- ✓ Secrets in deployment checklist
- ✓ Appropriate storage method per environment
- ✓ Rotation policies per secret type

### Guidance

The AI **warns about**:

- ⚠️ Secrets that might be committed
- ⚠️ Missing rotation policies
- ⚠️ Overly permissive access
- ⚠️ Secret-related security issues

### Validation

The AI **checks**:

- ✓ Are all required secrets documented?
- ✓ Is `.env` in `.gitignore`?
- ✓ Are production secrets separate from dev?
- ✓ Is there a rotation plan?

---

## 📁 Generated Files

The AI generated these files for secrets management:

### 1. `.env.example`
Template with placeholder values:
```env
OPENAI_API_KEY=sk-proj-...
DATABASE_URL=file:./data/ai-cofounder.db
SESSION_SECRET=generate-random-string
# ... 15+ secrets documented
```

### 2. `docs/SECRETS.md`
Complete documentation:
- All 15+ secrets listed
- Where to get each secret
- Rotation schedules
- Setup instructions per environment
- Security checklist
- Incident response plan

### 3. `scripts/check-secrets.sh`
Validation script:
```bash
#!/bin/bash
# Checks all required secrets are set
# Fails if any missing
```

### 4. `backend/src/config.ts`
Type-safe configuration loading:
```typescript
import { cleanEnv, str, num, url } from 'envalid';

export const config = cleanEnv(process.env, {
  OPENAI_API_KEY: str({ desc: 'OpenAI API key' }),
  DATABASE_URL: str({ default: 'file:./data/db' }),
  // ... validates all secrets
});
```

### 5. Updated `.gitignore`
Ensures secrets never committed:
```gitignore
.env
.env.local
.env.*.local
secrets.env
*.pem
*.key
*.crt
```

### 6. Updated `package.json`
Added dependencies:
```json
"envalid": "^7.3.1",
"dotenv": "^16.3.0"
```

---

## 🚀 Deployment Planning

### Hetzner VPS Setup

The AI knows the **exact deployment steps**:

```bash
# 1. SSH to server
ssh root@your-server.com

# 2. Create secrets directory
mkdir -p /etc/ai-cofounder
chmod 700 /etc/ai-cofounder

# 3. Create secrets file
nano /etc/ai-cofounder/secrets.env

# 4. Paste production secrets
# (AI provides template)

# 5. Secure permissions
chmod 600 /etc/ai-cofounder/secrets.env
chown root:root /etc/ai-cofounder/secrets.env

# 6. Update docker-compose.prod.yml
env_file:
  - /etc/ai-cofounder/secrets.env

# 7. Deploy
docker-compose -f docker-compose.prod.yml up -d

# 8. Verify
docker logs ai-cofounder-backend | grep "Configuration loaded"
```

### Secret Rotation Process

The AI knows **how to rotate** each secret type:

```bash
# API Keys (90 day rotation)
1. Generate new key at provider
2. Update /etc/ai-cofounder/secrets.env
3. Restart: systemctl restart ai-cofounder
4. Verify: curl http://localhost:3000/health
5. Revoke old key

# Session Secret (30 day rotation)
1. Generate: node -e "console.log(crypto.randomBytes(32))"
2. Update SESSION_SECRET
3. Restart: docker-compose restart backend
4. Note: Invalidates all active sessions
```

### Backup & Recovery

The AI understands **backup requirements**:

```bash
# Backup secrets (encrypted)
gpg --encrypt /etc/ai-cofounder/secrets.env > secrets.env.gpg
scp secrets.env.gpg backup-server:/backups/

# Restore
scp backup-server:/backups/secrets.env.gpg .
gpg --decrypt secrets.env.gpg > /etc/ai-cofounder/secrets.env
chmod 600 /etc/ai-cofounder/secrets.env
```

---

## 🔍 Security Scanning

### Tools the AI Recommends

```bash
# Scan git history for leaked secrets
docker run --rm -v $(pwd):/scan \
  trufflesecurity/trufflehog \
  filesystem /scan

# Detect hardcoded secrets
docker run --rm -v $(pwd):/repo \
  zricethezav/gitleaks \
  detect --source /repo

# Prevent committing secrets
git secrets --install
git secrets --register-aws
```

### Pre-commit Hook

The AI can generate a pre-commit hook:

```bash
#!/bin/bash
# .git/hooks/pre-commit

if git diff --cached --name-only | grep -q "\.env$"; then
  echo "❌ Attempting to commit .env file!"
  exit 1
fi

# Scan for API keys
if git diff --cached | grep -E "(API_KEY|SECRET|PASSWORD)" > /dev/null; then
  echo "⚠️  Potential secret detected - please review"
  git diff --cached | grep -E "(API_KEY|SECRET|PASSWORD)"
  read -p "Continue? (y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi
```

---

## 🎯 Example: AI Generates New Feature

When adding a new Stripe integration, the AI:

### 1. Identifies Required Secrets

```typescript
// AI detects need for Stripe secrets
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
```

### 2. Updates `.env.example`

```env
# === Payment Processing ===
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
```

### 3. Updates `SECRETS.md`

```markdown
### Stripe Secrets

| Secret | Purpose | Get From | Rotation |
|--------|---------|----------|----------|
| STRIPE_SECRET_KEY | API access | stripe.com/dashboard | On compromise |
| STRIPE_WEBHOOK_SECRET | Webhook verification | Webhook settings | On provider rotation |
```

### 4. Updates `config.ts`

```typescript
export const config = cleanEnv(process.env, {
  // ... existing secrets
  STRIPE_SECRET_KEY: str({ desc: 'Stripe API secret key' }),
  STRIPE_WEBHOOK_SECRET: str({ desc: 'Stripe webhook secret' }),
});
```

### 5. Adds to Deployment Checklist

```markdown
### New Secrets for Stripe Integration

- [ ] Get Stripe API keys from dashboard
- [ ] Add to production secrets.env
- [ ] Configure webhook endpoint
- [ ] Test webhook signature verification
- [ ] Set up webhook secret rotation schedule
```

---

## 📊 Metrics & Monitoring

### The AI Tracks

- **Secrets Count**: How many secrets the system uses
- **Rotation Status**: Which secrets are due for rotation
- **Access Patterns**: Who accessed which secrets when
- **Failed Validations**: Attempts to start with missing secrets
- **Security Scans**: Results of secret scanning

### Example Dashboard

```
Secrets Management Status:

Total Secrets: 15
  Required: 7
  Optional: 8

Rotation Status:
  ✓ Up to date: 12
  ⚠ Due soon (< 30 days): 2
  ❌ Overdue: 1 (SESSION_SECRET - 45 days old)

Security:
  ✓ No secrets in git (last scan: 2 hours ago)
  ✓ All prod secrets separated from dev
  ✓ File permissions correct
  ⚠ Rotation policy missing for 2 secrets

Actions Required:
  1. Rotate SESSION_SECRET (overdue)
  2. Schedule OPENAI_API_KEY rotation (due in 15 days)
  3. Document rotation policy for SENTRY_DSN
```

---

## 🎓 Teaching the AI

To teach the AI about a new secret:

```python
# In requirements spec
add_system_component(
    idea_id,
    component_name="new_integration",
    specification={
        "secrets_required": {
            "NEW_API_KEY": {
                "purpose": "Access to NewService API",
                "get_from": "https://newservice.com/keys",
                "rotation": "90 days",
                "environments": ["staging", "prod"],
                "used_by": ["backend_service"]
            }
        }
    }
)
```

The AI will automatically:
1. Add to `.env.example`
2. Document in `SECRETS.md`
3. Add validation to `config.ts`
4. Include in deployment checklist
5. Set up rotation schedule

---

## ✅ Summary

The AI Cofounder **fully understands**:

- ✓ **What** secrets are (7 categories, 15+ types)
- ✓ **Where** to store them (4 strategies per environment)
- ✓ **How** to deploy them securely (complete flow)
- ✓ **When** to rotate them (per-secret schedules)
- ✓ **Why** security matters (10 best practices)

The AI **automatically**:

- ✓ Detects secret requirements
- ✓ Generates configuration files
- ✓ Creates documentation
- ✓ Validates security
- ✓ Warns about issues

The AI **never**:

- ❌ Commits secrets to git
- ❌ Logs sensitive data
- ❌ Uses same secrets across environments
- ❌ Skips security validation

---

**Generated**: October 15, 2025
**System**: AI Cofounder using Possible Futures methodology
**Security Level**: Production-ready
**Compliance**: SOC2-ready secret management practices

*The AI Cofounder knows how to keep your secrets secret.* 🔐

