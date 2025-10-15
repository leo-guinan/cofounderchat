# Docker Build Standards

## Purpose
This document defines the standards for Docker builds in this project. Following these standards prevents "works on my machine" issues and ensures consistent, reproducible builds across all environments.

## Core Principles

### 1. Lock Files Are Mandatory
- **ALWAYS** commit `pnpm-lock.yaml` to version control
- **ALWAYS** use `--frozen-lockfile` in Dockerfiles
- **NEVER** allow Docker builds without lock files
- Lock files ensure identical dependency versions in dev, staging, and production

### 2. Use pnpm, Not npm
- This project uses **pnpm** for dependency management
- **NEVER** use `npm install` or `npm ci` in Dockerfiles
- Use Node's built-in corepack to enable pnpm
- Pattern:
  ```dockerfile
  RUN corepack enable && corepack prepare pnpm@latest --activate
  RUN pnpm install --frozen-lockfile
  ```

### 3. Proper .dockerignore Files
- Every service with a Dockerfile **must** have a `.dockerignore`
- Explicitly exclude development files (`node_modules`, `dist`, `*.log`, `.env*`)
- Explicitly **include** critical files (`package.json`, `pnpm-lock.yaml`, config files)
- Use `!filename` to ensure files aren't accidentally excluded

### 4. Multi-Stage Builds
- Use multi-stage builds for services that need compilation (backend, frontend)
- Builder stage: Install all dependencies, build the application
- Production stage: Install only production dependencies, copy built artifacts
- This reduces final image size and attack surface

### 5. Node Version Consistency
- Use `node:20-alpine` for all services (specified in Dockerfiles)
- Alpine variant keeps images small
- Node 20 is LTS and stable

## Dockerfile Template

### Backend/API Services
```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm run build

FROM node:20-alpine

WORKDIR /app

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --prod --frozen-lockfile

COPY --from=builder /app/dist ./dist

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

### Frontend Services (with nginx)
```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Simple Services (no build step)
```dockerfile
FROM node:20-alpine

WORKDIR /app

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --prod --frozen-lockfile

COPY src ./src

CMD ["node", "src/index.ts"]
```

## .dockerignore Template

```dockerignore
# Dependencies
node_modules

# Build output
dist

# Development
*.log
*.md
.env*

# Git
.git
.gitignore

# IDE
.vscode
.idea

# IMPORTANT: Never ignore these files
!package.json
!pnpm-lock.yaml
!tsconfig.json
```

## Common Mistakes to Avoid

### ❌ DON'T: Use npm instead of pnpm
```dockerfile
RUN npm install  # Wrong!
```

### ✅ DO: Use pnpm with frozen lockfile
```dockerfile
RUN corepack enable && corepack prepare pnpm@latest --activate
RUN pnpm install --frozen-lockfile
```

### ❌ DON'T: Make lock files optional
```dockerfile
COPY package*.json pnpm-lock.yaml* ./  # Wrong - makes lock file optional!
```

### ✅ DO: Require lock files
```dockerfile
COPY package.json pnpm-lock.yaml ./  # Right - build fails without lock file
```

### ❌ DON'T: Install without frozen lockfile
```dockerfile
RUN pnpm install  # Wrong - allows dependency resolution to change
```

### ✅ DO: Use frozen lockfile
```dockerfile
RUN pnpm install --frozen-lockfile  # Right - uses exact versions from lock
```

## Updating Dependencies

When updating dependencies:

1. **Update locally first:**
   ```bash
   cd backend  # or frontend, telemetry
   pnpm update <package-name>
   # or for all packages: pnpm update
   ```

2. **Test the changes:**
   ```bash
   pnpm run build
   pnpm run test
   ```

3. **Commit the updated lock file:**
   ```bash
   git add pnpm-lock.yaml package.json
   git commit -m "chore: update dependencies"
   ```

4. **Docker build will use new versions:**
   The `--frozen-lockfile` flag ensures Docker uses your tested versions

## Troubleshooting

### "No pnpm-lock.yaml found"
**Cause:** Lock file not committed to git or not present in directory

**Fix:**
```bash
cd <service-directory>
pnpm install  # generates lock file
git add pnpm-lock.yaml
git commit -m "Add pnpm lock file"
```

### "Native module won't compile locally"
**Cause:** Node version mismatch (e.g., better-sqlite3 on Node 23)

**Fix:**
```bash
pnpm install --ignore-scripts  # generates lock, skips native builds
# Docker will build correctly with Node 20
```

### "pnpm not found"
**Cause:** Corepack not enabled in Dockerfile

**Fix:** Add before pnpm commands:
```dockerfile
RUN corepack enable && corepack prepare pnpm@latest --activate
```

## When to Update This Document

Update this document when:
- Changing Node version used in Dockerfiles
- Switching package managers
- Adopting new Docker optimization techniques
- Discovering new common mistakes

## Enforcement

These standards are **not optional**. They exist to prevent:
- Production bugs from dependency version mismatches
- "Works on my machine" debugging sessions
- Wasted time troubleshooting preventable build failures
- Security vulnerabilities from unverified dependencies

**Move fast by doing it right the first time.**

---

Last updated: 2025-10-15

