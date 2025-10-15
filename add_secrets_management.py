#!/usr/bin/env python3
"""
Add Secrets Management to AI Cofounder Webapp

The AI Cofounder must understand:
1. What secrets are needed
2. Where they should be stored
3. How to deploy them securely
4. Different environments (dev, staging, prod)
"""

from tasks.idea_tools import (
    add_system_component,
    add_world_assumption,
    add_goal,
    get_idea_status,
    list_all_ideas
)


def add_secrets_management_component(idea_id: str):
    """
    Add secrets management as a system component
    
    This teaches the AI Cofounder how to handle sensitive data
    """
    
    print("=" * 80)
    print("ADDING SECRETS MANAGEMENT TO AI COFOUNDER")
    print("=" * 80)
    print()
    
    print(f"Idea ID: {idea_id}")
    print()
    
    # ========================================================================
    # Component: Secrets Management System
    # ========================================================================
    
    print("1. ADDING SECRETS MANAGEMENT COMPONENT...")
    print("-" * 80)
    
    add_system_component(
        idea_id=idea_id,
        component_name="secrets_management",
        component_type="infrastructure",
        specification={
            "purpose": "Secure management and deployment of sensitive configuration",
            
            "secrets_inventory": {
                "model_api_keys": {
                    "examples": ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"],
                    "used_by": ["cofounder_agent", "builder_agent"],
                    "environments": ["dev", "staging", "prod"],
                    "rotation": "90 days recommended"
                },
                "database_credentials": {
                    "examples": ["DATABASE_ENCRYPTION_KEY"],
                    "used_by": ["backend"],
                    "environments": ["prod only"],
                    "rotation": "Not required (key derivation)"
                },
                "oauth_secrets": {
                    "examples": ["GITHUB_CLIENT_SECRET", "GOOGLE_CLIENT_SECRET"],
                    "used_by": ["backend auth"],
                    "environments": ["staging", "prod"],
                    "rotation": "Manual on compromise"
                },
                "webhook_secrets": {
                    "examples": ["STRIPE_WEBHOOK_SECRET"],
                    "used_by": ["backend webhooks"],
                    "environments": ["prod"],
                    "rotation": "On provider rotation"
                },
                "data_lake_credentials": {
                    "examples": ["S3_ACCESS_KEY", "S3_SECRET_KEY"],
                    "used_by": ["telemetry_agent", "backup_service"],
                    "environments": ["all"],
                    "rotation": "90 days"
                },
                "deployment_tokens": {
                    "examples": ["GITHUB_DEPLOY_TOKEN", "DOCKER_REGISTRY_TOKEN"],
                    "used_by": ["CI/CD", "deployment scripts"],
                    "environments": ["CI only"],
                    "rotation": "On team changes"
                },
                "monitoring_keys": {
                    "examples": ["SENTRY_DSN", "ANALYTICS_KEY"],
                    "used_by": ["all services"],
                    "environments": ["staging", "prod"],
                    "rotation": "Annually"
                }
            },
            
            "storage_strategy": {
                "local_dev": {
                    "method": ".env file (gitignored)",
                    "template": ".env.example committed to git",
                    "loading": "dotenv library",
                    "security": "File permissions 600, never commit actual .env"
                },
                "docker_dev": {
                    "method": "docker-compose.yml environment section",
                    "source": "Reads from .env file",
                    "security": "Never commit secrets in docker-compose.yml"
                },
                "production_simple": {
                    "method": "Environment variables",
                    "source": "Set in systemd/Docker/hosting platform",
                    "security": "Platform-managed, not in code"
                },
                "production_advanced": {
                    "method": "HashiCorp Vault or similar",
                    "source": "Vault API at runtime",
                    "security": "Centralized, audited, rotated",
                    "when": "Multiple services, compliance requirements"
                },
                "kubernetes": {
                    "method": "Kubernetes Secrets",
                    "source": "kubectl create secret",
                    "security": "Encrypted at rest (if configured)",
                    "mount": "As env vars or files"
                }
            },
            
            "deployment_flow": {
                "never_commit": [
                    "Never commit actual secrets to git",
                    "Never put secrets in Dockerfile",
                    "Never log secrets",
                    "Never return secrets in API responses"
                ],
                "development": [
                    "1. Developer creates .env from .env.example",
                    "2. Populates with dev/test credentials",
                    "3. Application loads via dotenv",
                    "4. .env is gitignored"
                ],
                "staging": [
                    "1. Secrets stored in hosting platform (Hetzner env vars or Vault)",
                    "2. Docker container receives as env vars",
                    "3. Application reads from process.env",
                    "4. Logged access (who accessed what when)"
                ],
                "production": [
                    "1. Secrets in production secret store (Vault preferred)",
                    "2. Injected at container start",
                    "3. Rotated regularly",
                    "4. Audit trail maintained",
                    "5. Access restricted by IAM/RBAC"
                ]
            },
            
            "ai_cofounder_awareness": {
                "detection": [
                    "AI should detect when user mentions API keys, passwords, tokens",
                    "AI should recognize environment-specific config",
                    "AI should identify services that require authentication"
                ],
                "planning": [
                    "When generating code, AI creates .env.example",
                    "AI documents what secrets are needed",
                    "AI includes secrets in deployment checklist",
                    "AI suggests appropriate storage method per environment"
                ],
                "guidance": [
                    "AI warns if secrets might be committed",
                    "AI suggests rotation policies",
                    "AI recommends least-privilege access",
                    "AI helps debug secret-related issues"
                ],
                "validation": [
                    "Check: Are all required secrets documented?",
                    "Check: Is .env in .gitignore?",
                    "Check: Are production secrets separate from dev?",
                    "Check: Is there a secrets rotation plan?"
                ]
            },
            
            "implementation": {
                "files_to_generate": {
                    ".env.example": "Template with placeholder values",
                    ".env": "Actual secrets (gitignored)",
                    ".gitignore": "Must include .env",
                    "docker-compose.yml": "References ${ENV_VARS} from .env",
                    "docker-compose.prod.yml": "Expects secrets from platform",
                    "docs/SECRETS.md": "Documentation of all secrets",
                    "scripts/check-secrets.sh": "Validates secrets are set"
                },
                "backend_code": {
                    "config.ts": "Central config loading from env",
                    "validation": "Fail fast if required secrets missing",
                    "types": "TypeScript types for config",
                    "defaults": "Safe defaults for non-secrets only"
                },
                "deployment_scripts": {
                    "deploy.sh": "Checks secrets before deploying",
                    "rotate-secrets.sh": "Helper for rotation",
                    "backup-vault.sh": "Backup Vault data if used"
                }
            },
            
            "security_best_practices": {
                "principle_of_least_privilege": "Each service gets only secrets it needs",
                "environment_separation": "Dev secrets ≠ Prod secrets",
                "rotation": "Regular rotation schedule",
                "encryption_at_rest": "Secrets encrypted in storage",
                "encryption_in_transit": "HTTPS/TLS for secret transmission",
                "audit_logging": "Track who accessed what when",
                "access_control": "RBAC/IAM for secret access",
                "secret_scanning": "Automated scanning for leaked secrets",
                "expiration": "Secrets should expire and rotate",
                "revocation": "Ability to immediately revoke compromised secrets"
            },
            
            "tools_and_libraries": {
                "development": {
                    "dotenv": "Load .env files in Node.js",
                    "env-var": "Type-safe env var parsing",
                    "envalid": "Validation of environment variables"
                },
                "production": {
                    "hashicorp_vault": "Enterprise secret management",
                    "aws_secrets_manager": "AWS-native solution",
                    "google_secret_manager": "GCP-native solution",
                    "doppler": "Modern secrets platform",
                    "infisical": "Open-source secrets management"
                },
                "security_scanning": {
                    "trufflehog": "Scan git for secrets",
                    "gitleaks": "Detect hardcoded secrets",
                    "git-secrets": "Prevent committing secrets"
                }
            },
            
            "hetzner_vps_deployment": {
                "method": "Environment variables in systemd service",
                "setup": [
                    "1. Create /etc/ai-cofounder/secrets.env (root:root 600)",
                    "2. Populate with production secrets",
                    "3. Reference in systemd service: EnvironmentFile=/etc/ai-cofounder/secrets.env",
                    "4. Docker reads from host environment",
                    "5. Backup secrets.env securely (encrypted)"
                ],
                "rotation": [
                    "1. Update secrets.env",
                    "2. Restart services: systemctl restart ai-cofounder",
                    "3. Verify new secrets work",
                    "4. Revoke old secrets"
                ]
            },
            
            "example_env_file": """# AI Cofounder - Environment Configuration
# Copy this to .env and fill in actual values
# NEVER commit .env to git!

# === Model API Keys ===
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# === Database ===
DATABASE_URL=file:./data/ai-cofounder.db
DATABASE_ENCRYPTION_KEY=generate-with-crypto.randomBytes(32)

# === OAuth (if using) ===
GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=your_client_secret

# === Data Lake ===
S3_ENDPOINT=https://s3.amazonaws.com
S3_ACCESS_KEY=your_access_key
S3_SECRET_KEY=your_secret_key
S3_BUCKET=ai-cofounder-data

# === Monitoring ===
SENTRY_DSN=https://...@sentry.io/...

# === Application ===
NODE_ENV=development
PORT=3000
CORS_ORIGIN=http://localhost:5173

# === Session ===
SESSION_SECRET=generate-random-string-min-32-chars

# === Deployment ===
DEPLOY_ENV=development
""",
            
            "deployment_checklist_template": {
                "pre_deployment": [
                    "[ ] All required secrets documented in SECRETS.md",
                    "[ ] .env.example up to date with placeholders",
                    "[ ] .env in .gitignore",
                    "[ ] No secrets in Dockerfile or docker-compose.yml",
                    "[ ] Production secrets stored securely (Vault/platform)",
                    "[ ] Secrets rotation schedule defined",
                    "[ ] Access control configured (who can access secrets)",
                    "[ ] Backup plan for secrets",
                    "[ ] Incident response plan for secret compromise"
                ],
                "deployment": [
                    "[ ] Verify all required env vars are set",
                    "[ ] Test application starts with production secrets",
                    "[ ] Verify no secrets logged",
                    "[ ] Check file permissions on secrets.env (600)",
                    "[ ] Confirm HTTPS/TLS for all external communication",
                    "[ ] Audit log enabled for secret access"
                ],
                "post_deployment": [
                    "[ ] Monitor for unusual secret access patterns",
                    "[ ] Schedule first secret rotation",
                    "[ ] Document rotation procedure",
                    "[ ] Test secret rotation process",
                    "[ ] Review access logs weekly"
                ]
            }
        },
        confidence=0.9  # Secrets management is well-understood domain
    )
    print("  ✓ secrets_management component added")
    print()
    
    # ========================================================================
    # Assumptions about Secrets Management
    # ========================================================================
    
    print("2. ADDING SECRETS MANAGEMENT ASSUMPTIONS...")
    print("-" * 80)
    
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="Users will properly secure their API keys and not expose them publicly",
        category="user_behavior",
        criticality=0.85  # CRITICAL - security depends on this
    )
    print("  ✓ [CRITICAL 0.85] Users will secure their API keys")
    
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="Hetzner VPS provides sufficient security for /etc/ai-cofounder/secrets.env (file permissions + firewall)",
        category="technology",
        criticality=0.75
    )
    print("  ✓ [CRITICAL 0.75] VPS security is sufficient")
    
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="AI can correctly identify when code needs secrets and suggest appropriate storage",
        category="technology",
        criticality=0.80  # CRITICAL - core capability
    )
    print("  ✓ [CRITICAL 0.80] AI can identify secret requirements")
    
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="Simple .env approach is acceptable for MVP, won't need Vault immediately",
        category="technology",
        criticality=0.60
    )
    print("  ✓ [0.60] .env sufficient for MVP")
    
    print()
    
    # ========================================================================
    # Goals for Secrets Management
    # ========================================================================
    
    print("3. ADDING SECRETS MANAGEMENT GOALS...")
    print("-" * 80)
    
    add_goal(
        idea_id=idea_id,
        goal_text="Zero secrets committed to git (verified by git-secrets scan)",
        metric_name="secrets_in_git_count",
        target_value=0,
        validator_function="numeric_threshold"
    )
    print("  ✓ Zero secrets in git")
    
    add_goal(
        idea_id=idea_id,
        goal_text="All required secrets documented in SECRETS.md",
        metric_name="documented_secrets_complete",
        target_value=True,
        validator_function="boolean"
    )
    print("  ✓ All secrets documented")
    
    add_goal(
        idea_id=idea_id,
        goal_text="Production deployment uses separate secrets from dev",
        metric_name="prod_dev_secrets_separated",
        target_value=True,
        validator_function="boolean"
    )
    print("  ✓ Prod/dev secrets separated")
    
    add_goal(
        idea_id=idea_id,
        goal_text="AI correctly identifies 100% of required secrets when generating code",
        metric_name="ai_secret_detection_pct",
        target_value=100.0,
        validator_function="percentage"
    )
    print("  ✓ AI detects 100% of secrets")
    
    print()
    
    # ========================================================================
    # Status Check
    # ========================================================================
    
    print("4. UPDATED STATUS...")
    print("-" * 80)
    
    status = get_idea_status(idea_id)
    health = status['health']
    
    print(f"Components: {health['total_knowledge_items']}")
    print(f"Assumptions: {health['total_assumptions']} ({health['critical_assumptions_count']} critical)")
    print(f"Goals: {health['total_goals']}")
    print(f"Health Score: {health['overall_health_score']:.2f}")
    print()
    
    print("=" * 80)
    print("✨ SECRETS MANAGEMENT ADDED!")
    print("=" * 80)
    print()
    print("The AI Cofounder now understands:")
    print("  ✓ What secrets are needed (7 categories)")
    print("  ✓ Where to store them (.env, env vars, Vault)")
    print("  ✓ How to deploy securely (never commit, separate environments)")
    print("  ✓ Security best practices (rotation, least privilege, audit)")
    print("  ✓ Deployment flow for each environment")
    print("  ✓ How to validate secrets are secure")
    print()
    print("Next: Generate actual secrets management code")
    print("=" * 80)


def generate_secrets_files(idea_id: str):
    """Generate the actual secrets management files"""
    
    print()
    print("5. GENERATING SECRETS MANAGEMENT FILES...")
    print("=" * 80)
    print()
    
    from pathlib import Path
    
    project_root = Path("./ai-cofounder-app")
    
    files = []
    
    # .env.example
    files.append({
        "path": ".env.example",
        "content": """# AI Cofounder - Environment Configuration Template
# Copy this to .env and fill in actual values
# NEVER commit .env to git!

# === Model API Keys ===
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-...

# Get from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-api03-...

# === Database ===
DATABASE_URL=file:./data/ai-cofounder.db
# Generate with: node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
DATABASE_ENCRYPTION_KEY=

# === OAuth (for user authentication) ===
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=

# === Data Lake (S3-compatible storage) ===
S3_ENDPOINT=https://s3.amazonaws.com
S3_ACCESS_KEY=
S3_SECRET_KEY=
S3_BUCKET=ai-cofounder-data
S3_REGION=us-east-1

# === Monitoring ===
# Get from: https://sentry.io/
SENTRY_DSN=

# === Application ===
NODE_ENV=development
PORT=3000
FRONTEND_URL=http://localhost:5173
CORS_ORIGIN=http://localhost:5173

# === Session ===
# Generate with: node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
SESSION_SECRET=

# === Deployment ===
DEPLOY_ENV=development
LOG_LEVEL=info
"""
    })
    
    # SECRETS.md documentation
    files.append({
        "path": "docs/SECRETS.md",
        "content": """# Secrets Management

This document describes all secrets used by the AI Cofounder system and how to manage them.

## Required Secrets

### Model API Keys

| Secret | Purpose | Where to Get | Rotation |
|--------|---------|--------------|----------|
| `OPENAI_API_KEY` | AI model access | https://platform.openai.com/api-keys | 90 days |
| `ANTHROPIC_API_KEY` | Alternative AI model | https://console.anthropic.com/ | 90 days |

### Database

| Secret | Purpose | Generation | Rotation |
|--------|---------|------------|----------|
| `DATABASE_ENCRYPTION_KEY` | Encrypt sensitive data | `crypto.randomBytes(32).toString('hex')` | Never (key derivation) |

### OAuth (Optional)

| Secret | Purpose | Where to Get | Rotation |
|--------|---------|--------------|----------|
| `GITHUB_CLIENT_ID` | GitHub OAuth | https://github.com/settings/developers | On compromise |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth secret | Same as above | On compromise |

### Data Lake

| Secret | Purpose | Where to Get | Rotation |
|--------|---------|--------------|----------|
| `S3_ACCESS_KEY` | S3 access | AWS Console or MinIO | 90 days |
| `S3_SECRET_KEY` | S3 secret | Same as above | 90 days |

### Monitoring

| Secret | Purpose | Where to Get | Rotation |
|--------|---------|--------------|----------|
| `SENTRY_DSN` | Error tracking | https://sentry.io/ | Annually |

### Application

| Secret | Purpose | Generation | Rotation |
|--------|---------|------------|----------|
| `SESSION_SECRET` | Session signing | `crypto.randomBytes(32).toString('base64')` | 30 days |

## Environment Setup

### Development

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Fill in development values (can use test/sandbox credentials)

3. Verify `.env` is in `.gitignore`

### Production (Hetzner VPS)

1. SSH into server:
   ```bash
   ssh root@your-server.com
   ```

2. Create secrets directory:
   ```bash
   mkdir -p /etc/ai-cofounder
   ```

3. Create secrets file:
   ```bash
   nano /etc/ai-cofounder/secrets.env
   ```

4. Paste production secrets (see `.env.example` for format)

5. Secure file permissions:
   ```bash
   chmod 600 /etc/ai-cofounder/secrets.env
   chown root:root /etc/ai-cofounder/secrets.env
   ```

6. Update `docker-compose.prod.yml` to reference:
   ```yaml
   env_file:
     - /etc/ai-cofounder/secrets.env
   ```

## Security Checklist

Before deploying:

- [ ] `.env` is in `.gitignore`
- [ ] No secrets in `docker-compose.yml` (uses env vars)
- [ ] No secrets in Dockerfiles
- [ ] Production secrets ≠ development secrets
- [ ] File permissions on prod secrets: `600`
- [ ] Secrets rotation schedule defined
- [ ] Backup of production secrets (encrypted)

## Secret Rotation

### API Keys (90 day rotation)

1. Generate new key at provider
2. Update `/etc/ai-cofounder/secrets.env`
3. Restart services: `docker-compose restart`
4. Verify services working
5. Revoke old key at provider

### Session Secret (30 day rotation)

1. Generate new secret:
   ```bash
   node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
   ```

2. Update `SESSION_SECRET` in secrets.env
3. Restart: `docker-compose restart backend`
4. Note: This will invalidate all active sessions

## Incident Response

If secrets are compromised:

1. **Immediately** revoke compromised secrets at provider
2. Generate new secrets
3. Update production secrets.env
4. Restart all services
5. Review logs for unauthorized access
6. Rotate all related secrets
7. Document incident
8. Review access controls

## Tools

### Check for leaked secrets

```bash
# Install trufflehog
docker run --rm -v $(pwd):/scan trufflesecurity/trufflehog filesystem /scan

# Install gitleaks
docker run --rm -v $(pwd):/repo zricethezav/gitleaks detect --source /repo
```

### Validate secrets are set

```bash
./scripts/check-secrets.sh
```

## Advanced: HashiCorp Vault

For production systems requiring:
- Multiple services
- Compliance (SOC2, HIPAA, etc.)
- Centralized secret management
- Audit trails

Consider migrating to HashiCorp Vault.

See `docs/VAULT_MIGRATION.md` (when needed).
"""
    })
    
    # check-secrets.sh script
    files.append({
        "path": "scripts/check-secrets.sh",
        "content": """#!/bin/bash
# Check that all required secrets are set

set -e

REQUIRED_SECRETS=(
  "OPENAI_API_KEY"
  "DATABASE_URL"
  "SESSION_SECRET"
)

OPTIONAL_SECRETS=(
  "ANTHROPIC_API_KEY"
  "GITHUB_CLIENT_SECRET"
  "S3_ACCESS_KEY"
  "SENTRY_DSN"
)

echo "Checking required secrets..."
MISSING=0

for secret in "${REQUIRED_SECRETS[@]}"; do
  if [ -z "${!secret}" ]; then
    echo "❌ Missing required secret: $secret"
    MISSING=1
  else
    echo "✓ $secret is set"
  fi
done

echo ""
echo "Checking optional secrets..."

for secret in "${OPTIONAL_SECRETS[@]}"; do
  if [ -z "${!secret}" ]; then
    echo "⚠️  Optional secret not set: $secret"
  else
    echo "✓ $secret is set"
  fi
done

if [ $MISSING -eq 1 ]; then
  echo ""
  echo "❌ Some required secrets are missing!"
  echo "See docs/SECRETS.md for setup instructions"
  exit 1
fi

echo ""
echo "✅ All required secrets are set!"
"""
    })
    
    # backend config.ts
    files.append({
        "path": "backend/src/config.ts",
        "content": """import { cleanEnv, str, num, url } from 'envalid';

/**
 * Application configuration loaded from environment variables
 * 
 * Uses envalid for validation - will fail fast if required secrets missing
 */
export const config = cleanEnv(process.env, {
  // Model API Keys
  OPENAI_API_KEY: str({ desc: 'OpenAI API key for AI models' }),
  ANTHROPIC_API_KEY: str({ default: '', desc: 'Optional Anthropic API key' }),
  
  // Database
  DATABASE_URL: str({ default: 'file:./data/ai-cofounder.db' }),
  DATABASE_ENCRYPTION_KEY: str({ default: '', desc: 'Optional DB encryption key' }),
  
  // OAuth (optional)
  GITHUB_CLIENT_ID: str({ default: '' }),
  GITHUB_CLIENT_SECRET: str({ default: '' }),
  
  // Data Lake
  S3_ENDPOINT: url({ default: 'https://s3.amazonaws.com' }),
  S3_ACCESS_KEY: str({ default: '' }),
  S3_SECRET_KEY: str({ default: '' }),
  S3_BUCKET: str({ default: 'ai-cofounder-data' }),
  S3_REGION: str({ default: 'us-east-1' }),
  
  // Monitoring
  SENTRY_DSN: str({ default: '' }),
  
  // Application
  NODE_ENV: str({ choices: ['development', 'test', 'staging', 'production'], default: 'development' }),
  PORT: num({ default: 3000 }),
  FRONTEND_URL: url({ default: 'http://localhost:5173' }),
  CORS_ORIGIN: str({ default: 'http://localhost:5173' }),
  
  // Session
  SESSION_SECRET: str({ desc: 'Secret for signing sessions' }),
  
  // Deployment
  DEPLOY_ENV: str({ default: 'development' }),
  LOG_LEVEL: str({ choices: ['debug', 'info', 'warn', 'error'], default: 'info' }),
});

// Log config on startup (redact sensitive values)
export function logConfig() {
  const safe = {
    ...config,
    OPENAI_API_KEY: config.OPENAI_API_KEY ? 'sk-***' : undefined,
    ANTHROPIC_API_KEY: config.ANTHROPIC_API_KEY ? 'sk-ant-***' : undefined,
    DATABASE_ENCRYPTION_KEY: config.DATABASE_ENCRYPTION_KEY ? '***' : undefined,
    GITHUB_CLIENT_SECRET: config.GITHUB_CLIENT_SECRET ? '***' : undefined,
    S3_SECRET_KEY: config.S3_SECRET_KEY ? '***' : undefined,
    SESSION_SECRET: '***',
  };
  
  console.log('Configuration loaded:', JSON.stringify(safe, null, 2));
}
"""
    })
    
    # Update backend package.json to include envalid
    files.append({
        "path": "backend/package.json.patch",
        "content": """Add to dependencies:
  "envalid": "^7.3.1"
"""
    })
    
    # Update .gitignore
    files.append({
        "path": ".gitignore.patch",
        "content": """# Secrets
.env
.env.local
.env.*.local
secrets.env

# Sensitive files
*.pem
*.key
*.crt
"""
    })
    
    # Write all files
    print(f"Creating {len(files)} secrets management files...")
    print()
    
    for file_info in files:
        file_path = project_root / file_info['path']
        
        # Handle patch files differently
        if file_info['path'].endswith('.patch'):
            print(f"  📝 {file_info['path']} (manual merge required)")
            print(f"     {file_info['content'].strip()}")
            continue
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(file_info['content'])
        
        # Make scripts executable
        if file_path.suffix == '.sh':
            import os
            os.chmod(file_path, 0o755)
        
        print(f"  ✓ {file_info['path']}")
    
    print()
    print("=" * 80)
    print("✨ SECRETS MANAGEMENT FILES GENERATED!")
    print("=" * 80)
    print()
    print("Created:")
    print("  ✓ .env.example (template)")
    print("  ✓ docs/SECRETS.md (documentation)")
    print("  ✓ scripts/check-secrets.sh (validation)")
    print("  ✓ backend/src/config.ts (configuration loading)")
    print()
    print("Next steps:")
    print("  1. cp ai-cofounder-app/.env.example ai-cofounder-app/.env")
    print("  2. Fill in your API keys in .env")
    print("  3. Run: cd ai-cofounder-app && ./scripts/check-secrets.sh")
    print()
    print("=" * 80)


if __name__ == "__main__":
    import sys
    
    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 25 + "SECRETS MANAGEMENT" + " " * 31 + "║")
    print("║" + " " * 78 + "║")
    print("║" + " " * 15 + "Teaching AI Cofounder About Security" + " " * 25 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Get idea ID from argument or find it
    if len(sys.argv) > 1:
        idea_id = sys.argv[1]
        print(f"Using idea ID: {idea_id}")
    else:
        # Find the webapp idea
        all_ideas = list_all_ideas()
        webapp_idea = next((i for i in all_ideas if 'Webapp' in i['name']), None)
        
        if not webapp_idea:
            print("ERROR: Webapp idea not found!")
            print("Run build_webapp.py first or pass idea ID as argument")
            print("Usage: python add_secrets_management.py <idea_id>")
            exit(1)
        
        idea_id = webapp_idea['id']
        print(f"Webapp Idea: {webapp_idea['name']} ({idea_id[:8]}...)")
    
    print()
    
    # Add secrets management component
    add_secrets_management_component(idea_id)
    
    # Generate files
    generate_secrets_files(idea_id)

