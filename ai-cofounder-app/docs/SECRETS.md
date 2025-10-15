# Secrets Management

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
