#!/usr/bin/env python3
"""
AI Cofounder Builds Its Own Webapp

The AI Cofounder uses Possible Futures to design and build itself.
This is Test #4: Can AI build its own webapp?

Tech Stack (User Requirements):
- Backend: Mastra (TypeScript) for agents and tools
- Frontend: React + Tailwind
- Database: SQLite on host
- Deployment: Docker (local + Hetzner VPS)
- Telemetry: Each node sends data back to AI Cofounder
- Data Lake: Periodic updates for versioning
"""

from tasks.idea_tools import (
    create_idea,
    add_system_component,
    add_world_assumption,
    add_goal,
    get_idea_status,
    list_all_ideas
)


def spawn_webapp_build_idea(parent_idea_id: str):
    """
    Spawn the webapp build as a child idea of AI Cofounder
    
    This allows us to track the build process separately while maintaining
    the relationship to the parent vision.
    """
    
    print("=" * 80)
    print("AI COFOUNDER BUILDS ITSELF - WEBAPP V1")
    print("=" * 80)
    print()
    
    # ========================================================================
    # STEP 1: Spawn Child Idea
    # ========================================================================
    
    print("1. SPAWNING WEBAPP BUILD IDEA (Child of AI Cofounder)...")
    print("-" * 80)
    
    idea = create_idea(
        name="AI Cofounder Webapp v1",
        description="""
First production version of the AI Cofounder webapp.

Tech Stack:
- Backend: Mastra (TypeScript) - Agent orchestration and tool execution
- Frontend: React + Tailwind - Modern, fast UI
- Database: SQLite - Simple, event-sourced, local-first
- Deployment: Docker - Containerized for easy deployment
- Infrastructure: Hetzner VPS - Cost-effective production hosting
- Telemetry: Agent-based monitoring of all deployed nodes
- Data Lake: Centralized versioned storage of all node data

Architecture Philosophy:
- Local-first: Works offline, syncs when online
- Event-sourced: All state changes tracked
- Self-monitoring: Agents watch themselves
- Simple deployment: docker-compose up
- FRP principles: Essential/Accidental separation
        """.strip(),
        parent_idea_id=parent_idea_id
    )
    
    idea_id = idea['id']
    print(f"✓ Created idea: {idea_id}")
    if parent_idea_id:
        print(f"  Parent: {parent_idea_id[:8]}...")
    print(f"  Stage: {idea['current_stage']}")
    print()
    
    # ========================================================================
    # STEP 2: Define Architecture Components
    # ========================================================================
    
    print("2. DEFINING ARCHITECTURE COMPONENTS...")
    print("-" * 80)
    
    # Component 1: Mastra Backend
    add_system_component(
        idea_id=idea_id,
        component_name="mastra_backend",
        component_type="api",
        specification={
            "framework": "Mastra",
            "language": "TypeScript",
            "purpose": "Agent orchestration and tool execution",
            "features": [
                "Agent definitions (AI Cofounder agent)",
                "Tool registry (Possible Futures tools)",
                "Workflow engine (requirement → production pipeline)",
                "Event bus (state change notifications)",
                "API endpoints (REST + WebSocket)"
            ],
            "agents": [
                {
                    "name": "cofounder_agent",
                    "role": "Primary AI Cofounder",
                    "tools": [
                        "create_idea", "add_system_component", "add_world_assumption",
                        "add_goal", "check_goals", "get_idea_status", 
                        "advance_idea_stage", "list_all_ideas", "get_stage_history"
                    ],
                    "model": "Your trained model",
                    "system_prompt": "You are an AI Cofounder using Possible Futures methodology"
                },
                {
                    "name": "telemetry_agent",
                    "role": "Monitor deployed node health",
                    "tools": ["report_metrics", "check_health", "alert_issues"],
                    "model": "Lightweight model or rule-based",
                    "runs_on": "Each deployed node"
                },
                {
                    "name": "builder_agent",
                    "role": "Generate code from requirements",
                    "tools": ["generate_component", "update_schema", "run_tests"],
                    "model": "Code-specialized model",
                    "system_prompt": "You build software following FRP principles"
                }
            ],
            "tools": [
                "All 9 Possible Futures tools",
                "Code generation tools",
                "Deployment tools",
                "Monitoring tools"
            ],
            "directory_structure": {
                "src/": {
                    "agents/": ["cofounder.ts", "telemetry.ts", "builder.ts"],
                    "tools/": ["possible-futures.ts", "deployment.ts", "monitoring.ts"],
                    "workflows/": ["idea-to-production.ts", "telemetry-collection.ts"],
                    "api/": ["routes.ts", "websocket.ts"],
                    "db/": ["sqlite.ts", "migrations/", "queries.ts"]
                }
            }
        },
        confidence=0.8  # Mastra is new but well-documented
    )
    print("  ✓ mastra_backend (TypeScript/Mastra)")
    
    # Component 2: React Frontend
    add_system_component(
        idea_id=idea_id,
        component_name="react_frontend",
        component_type="ui",
        specification={
            "framework": "React 18+",
            "language": "TypeScript",
            "styling": "Tailwind CSS",
            "build": "Vite",
            "purpose": "User interface for AI Cofounder",
            "pages": [
                {
                    "route": "/",
                    "name": "Dashboard",
                    "components": [
                        "CurrentBusinessState",
                        "PossibleFuturesList", 
                        "ChatInterface",
                        "QuickCapture"
                    ]
                },
                {
                    "route": "/ideas/:id",
                    "name": "Idea Detail",
                    "components": [
                        "IdeaOverview",
                        "SystemComponents",
                        "WorldAssumptions",
                        "Goals",
                        "EventHistory"
                    ]
                },
                {
                    "route": "/monitor",
                    "name": "System Monitor",
                    "components": [
                        "DeployedNodes",
                        "TelemetryDashboard",
                        "HealthChecks",
                        "Alerts"
                    ]
                }
            ],
            "components": {
                "ChatInterface": "Real-time chat with AI Cofounder",
                "PossibleFuturesList": "All active ideas with health scores",
                "IdeaDetail": "Deep dive into single idea",
                "BusinessMetrics": "Current state metrics",
                "TelemetryDashboard": "All deployed nodes status"
            },
            "state_management": "React Query + Zustand",
            "real_time": "WebSocket connection to backend",
            "directory_structure": {
                "src/": {
                    "pages/": ["Dashboard.tsx", "IdeaDetail.tsx", "Monitor.tsx"],
                    "components/": ["Chat/", "Ideas/", "Metrics/", "Telemetry/"],
                    "hooks/": ["useIdeas.ts", "useChat.ts", "useTelemetry.ts"],
                    "stores/": ["ideas.ts", "chat.ts", "telemetry.ts"],
                    "api/": ["client.ts", "websocket.ts"],
                    "types/": ["idea.ts", "telemetry.ts", "chat.ts"]
                }
            }
        },
        confidence=0.9  # React + Tailwind is well-known
    )
    print("  ✓ react_frontend (React/TypeScript/Tailwind)")
    
    # Component 3: SQLite Database Layer
    add_system_component(
        idea_id=idea_id,
        component_name="sqlite_database",
        component_type="database",
        specification={
            "database": "SQLite",
            "orm": "Drizzle ORM (TypeScript-first)",
            "purpose": "Local-first event-sourced storage",
            "schema": {
                "ideas": "All spawned possible futures",
                "state_changes": "Event sourcing events",
                "system_knowledge": "Known components per idea",
                "world_assumptions": "Assumptions per idea",
                "goals": "Measurable goals per idea",
                "chat_messages": "Chat history with AI Cofounder",
                "business_metrics": "User's business state over time",
                "telemetry": "Health data from deployed nodes",
                "user_content": "Ingested user content for learning"
            },
            "migrations": "Drizzle Kit for schema migrations",
            "event_sourcing": "State = f(initial_state, changes)",
            "file_location": "./data/ai-cofounder.db",
            "backup_strategy": "Periodic sync to data lake"
        },
        confidence=1.0  # SQLite + event sourcing already proven
    )
    print("  ✓ sqlite_database (SQLite + Drizzle ORM)")
    
    # Component 4: Docker Deployment
    add_system_component(
        idea_id=idea_id,
        component_name="docker_deployment",
        component_type="infrastructure",
        specification={
            "containerization": "Docker + Docker Compose",
            "services": [
                {
                    "name": "backend",
                    "image": "ai-cofounder-backend",
                    "build": "./backend",
                    "ports": ["3000:3000"],
                    "volumes": ["./data:/app/data"],
                    "env": ["NODE_ENV", "DATABASE_URL", "MODEL_API_KEY"]
                },
                {
                    "name": "frontend",
                    "image": "ai-cofounder-frontend",
                    "build": "./frontend",
                    "ports": ["80:80"],
                    "depends_on": ["backend"]
                },
                {
                    "name": "telemetry-agent",
                    "image": "ai-cofounder-telemetry",
                    "build": "./telemetry",
                    "volumes": ["./data:/app/data"],
                    "env": ["NODE_ID", "CENTRAL_URL"]
                }
            ],
            "deployment_targets": {
                "local": "docker-compose up",
                "production": "docker-compose -f docker-compose.prod.yml up -d",
                "hetzner_vps": {
                    "setup": "Ubuntu 22.04 LTS",
                    "docker_install": "curl -fsSL https://get.docker.com | sh",
                    "deploy": "git pull && docker-compose up -d --build",
                    "ssl": "Caddy reverse proxy",
                    "monitoring": "Telemetry agent on each node"
                }
            },
            "files": {
                "Dockerfile.backend": "Multi-stage Node.js build",
                "Dockerfile.frontend": "Nginx with React build",
                "Dockerfile.telemetry": "Minimal Node.js runtime",
                "docker-compose.yml": "Local development",
                "docker-compose.prod.yml": "Production config"
            }
        },
        confidence=0.9  # Docker is standard
    )
    print("  ✓ docker_deployment (Docker + Compose)")
    
    # Component 5: Telemetry System
    add_system_component(
        idea_id=idea_id,
        component_name="telemetry_system",
        component_type="business_logic",
        specification={
            "purpose": "Monitor all deployed nodes and report to central AI Cofounder",
            "architecture": "Agent-based monitoring",
            "telemetry_agent": {
                "runs_on": "Each deployed node",
                "collects": [
                    "System health (CPU, memory, disk)",
                    "Application metrics (requests, errors, latency)",
                    "Database stats (size, query performance)",
                    "Business metrics (users active, ideas created)",
                    "Event counts (state changes per minute)"
                ],
                "reports_to": "Central AI Cofounder API",
                "frequency": "Every 60 seconds",
                "storage": "Local SQLite + central data lake"
            },
            "central_collection": {
                "endpoint": "POST /telemetry/report",
                "storage": "Data lake (S3-compatible or local dir)",
                "processing": "AI Cofounder analyzes for anomalies",
                "alerting": "Auto-message user if issues detected"
            },
            "node_identification": {
                "node_id": "UUID per deployment",
                "metadata": "hostname, region, version, user_id"
            }
        },
        confidence=0.75  # New pattern but straightforward
    )
    print("  ✓ telemetry_system (Agent-based monitoring)")
    
    # Component 6: Data Lake
    add_system_component(
        idea_id=idea_id,
        component_name="data_lake",
        component_type="database",
        specification={
            "purpose": "Centralized versioned storage of all node data",
            "storage": "S3-compatible (MinIO for self-hosted or Cloudflare R2)",
            "structure": {
                "telemetry/": "node_id/date/metrics.json",
                "databases/": "node_id/date/backup.db",
                "events/": "node_id/date/events.jsonl",
                "snapshots/": "node_id/date/full-state.json"
            },
            "sync_strategy": {
                "telemetry": "Push every 60s",
                "database": "Incremental backup every 6 hours",
                "events": "Append-only log, sync every 5 minutes",
                "snapshots": "Full snapshot daily"
            },
            "versioning": "All files are immutable, timestamped",
            "querying": "DuckDB for local analytics on lake data",
            "cost": "MinIO self-hosted = free, R2 = pennies/month"
        },
        confidence=0.7  # New but proven patterns
    )
    print("  ✓ data_lake (S3-compatible storage)")
    
    # Component 7: Requirement-to-Production Pipeline
    add_system_component(
        idea_id=idea_id,
        component_name="req_to_prod_pipeline",
        component_type="business_logic",
        specification={
            "purpose": "Link requirements changes through to possible production systems",
            "workflow": [
                "1. User/AI adds requirement (system component)",
                "2. AI analyzes requirement → generates code/config",
                "3. Code committed to git branch",
                "4. Tests run automatically",
                "5. If tests pass, create deployment preview",
                "6. User approves → merge and deploy",
                "7. Telemetry monitors new deployment",
                "8. AI reports back on deployment health"
            ],
            "tools": {
                "requirement_parser": "Extract specs from natural language",
                "code_generator": "Generate TypeScript/React from specs",
                "test_generator": "Generate tests from requirements",
                "deployer": "Create preview deployments",
                "validator": "Check if deployment meets requirements"
            },
            "integration": "Ties into Possible Futures waterfall stages",
            "git_workflow": "Feature branch per requirement",
            "preview_deployments": "Unique URL per branch"
        },
        confidence=0.5  # Very novel - this is the hard part
    )
    print("  ✓ req_to_prod_pipeline (Novel - AI-driven deployments)")
    
    print()
    
    # ========================================================================
    # STEP 3: Define Assumptions (Unknowns)
    # ========================================================================
    
    print("3. DEFINING ASSUMPTIONS (What Could Go Wrong)...")
    print("-" * 80)
    
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="Mastra is stable enough for production use and has good TypeScript support",
        category="technology",
        criticality=0.80
    )
    print("  ✓ [0.80] Mastra is production-ready")
    
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="SQLite can handle concurrent writes from telemetry + app without corruption",
        category="technology",
        criticality=0.75
    )
    print("  ✓ [0.75] SQLite handles concurrent writes")
    
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="Hetzner VPS has sufficient resources (2GB RAM, 2 vCPU) to run all services",
        category="resources",
        criticality=0.70
    )
    print("  ✓ [0.70] Hetzner VPS is sufficient")
    
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="Telemetry data size won't explode storage costs (< 10GB/month per node)",
        category="resources",
        criticality=0.65
    )
    print("  ✓ [0.65] Telemetry storage is manageable")
    
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="React + Tailwind gives fast enough UI (< 100ms interactions)",
        category="technology",
        criticality=0.60
    )
    print("  ✓ [0.60] React/Tailwind is fast enough")
    
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="AI can generate production-quality code from requirements (>80% usable)",
        category="technology",
        criticality=0.90  # CRITICAL - this is the whole point!
    )
    print("  ✓ [CRITICAL 0.90] AI can generate quality code")
    
    print()
    
    # ========================================================================
    # STEP 4: Define Goals
    # ========================================================================
    
    print("4. DEFINING MEASURABLE GOALS...")
    print("-" * 80)
    
    add_goal(
        idea_id=idea_id,
        goal_text="Generate working boilerplate in < 1 hour (Mastra + React + Docker)",
        metric_name="boilerplate_generation_minutes",
        target_value=60,
        validator_function="numeric_threshold"
    )
    print("  ✓ Boilerplate in < 1 hour")
    
    add_goal(
        idea_id=idea_id,
        goal_text="Local deployment works first try (docker-compose up succeeds)",
        metric_name="local_deploy_success",
        target_value=True,
        validator_function="boolean"
    )
    print("  ✓ Local deployment works first try")
    
    add_goal(
        idea_id=idea_id,
        goal_text="Frontend loads in < 1 second on local dev",
        metric_name="frontend_load_ms",
        target_value=1000,
        validator_function="numeric_threshold"
    )
    print("  ✓ Frontend loads < 1s")
    
    add_goal(
        idea_id=idea_id,
        goal_text="Telemetry agent successfully reports metrics every 60s",
        metric_name="telemetry_reports_per_minute",
        target_value=1,
        validator_function="numeric_threshold"
    )
    print("  ✓ Telemetry reports every 60s")
    
    add_goal(
        idea_id=idea_id,
        goal_text="Production deployment to Hetzner VPS in < 30 minutes",
        metric_name="production_deploy_minutes",
        target_value=30,
        validator_function="numeric_threshold"
    )
    print("  ✓ Production deploy < 30 min")
    
    add_goal(
        idea_id=idea_id,
        goal_text="Full stack uses < 1GB RAM total",
        metric_name="total_ram_usage_mb",
        target_value=1024,
        validator_function="numeric_threshold"
    )
    print("  ✓ Uses < 1GB RAM total")
    
    print()
    
    # ========================================================================
    # STEP 5: Check Status
    # ========================================================================
    
    print("5. CHECKING STATUS...")
    print("-" * 80)
    
    status = get_idea_status(idea_id)
    health = status['health']
    
    print(f"Stage: {status['idea']['current_stage']}")
    print(f"Uncertainty: {status['idea']['uncertainty_level']}")
    print(f"Health: {health['overall_health_score']:.2f}")
    print(f"Components: {health['total_knowledge_items']}")
    print(f"Assumptions: {health['total_assumptions']} ({health['critical_assumptions_count']} critical)")
    print(f"Goals: {health['total_goals']}")
    print()
    
    return idea_id


def generate_project_structure(idea_id: str):
    """
    Generate the actual project structure and files
    
    This is where the AI Cofounder starts building itself!
    """
    
    print("6. GENERATING PROJECT STRUCTURE...")
    print("=" * 80)
    print()
    
    import os
    import json
    from pathlib import Path
    
    # Root directory
    project_root = Path("./ai-cofounder-app")
    project_root.mkdir(exist_ok=True)
    
    print(f"Creating project at: {project_root.absolute()}")
    print()
    
    # Directory structure
    dirs = [
        "backend/src/agents",
        "backend/src/tools",
        "backend/src/workflows",
        "backend/src/api",
        "backend/src/db/migrations",
        "frontend/src/pages",
        "frontend/src/components/Chat",
        "frontend/src/components/Ideas",
        "frontend/src/components/Metrics",
        "frontend/src/components/Telemetry",
        "frontend/src/hooks",
        "frontend/src/stores",
        "frontend/src/api",
        "frontend/src/types",
        "frontend/public",
        "telemetry/src",
        "data",
        "docs"
    ]
    
    for dir_path in dirs:
        (project_root / dir_path).mkdir(parents=True, exist_ok=True)
    
    print(f"✓ Created {len(dirs)} directories")
    print()
    
    # Track files we'll create
    files_to_create = []
    
    # =======================================================================
    # Root Files
    # =======================================================================
    
    files_to_create.append({
        "path": "README.md",
        "content": f"""# AI Cofounder App

This webapp was designed and built by the AI Cofounder itself using the Possible Futures methodology.

**Idea ID**: `{idea_id}`

## Architecture

- **Backend**: Mastra (TypeScript) - Agent orchestration
- **Frontend**: React + Tailwind
- **Database**: SQLite (event-sourced)
- **Deployment**: Docker + Docker Compose
- **Monitoring**: Telemetry agents on each node
- **Data Lake**: S3-compatible storage

## Quick Start

```bash
# Local development
docker-compose up

# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

## Project Structure

```
backend/          Mastra backend with agents and tools
frontend/         React + Tailwind UI
telemetry/        Monitoring agent
data/             SQLite database and local storage
docs/             Architecture documentation
```

## Generated By

This entire project structure was generated by `build_webapp.py` using the Possible Futures system.
The AI Cofounder designed itself!
"""
    })
    
    files_to_create.append({
        "path": ".gitignore",
        "content": """# Dependencies
node_modules/
*.log

# Build outputs
dist/
build/
.next/

# Environment
.env
.env.local

# Database
*.db
*.db-shm
*.db-wal
data/

# Docker
.dockerignore

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    })
    
    files_to_create.append({
        "path": "docker-compose.yml",
        "content": """version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "3000:3000"
    volumes:
      - ./data:/app/data
      - ./backend/src:/app/src
    environment:
      - NODE_ENV=development
      - DATABASE_URL=file:./data/ai-cofounder.db
    depends_on:
      - telemetry

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    volumes:
      - ./frontend/src:/app/src
    environment:
      - VITE_API_URL=http://localhost:3000
    depends_on:
      - backend

  telemetry:
    build: ./telemetry
    volumes:
      - ./data:/app/data
    environment:
      - NODE_ID=local-dev
      - CENTRAL_URL=http://backend:3000
"""
    })
    
    # =======================================================================
    # Backend Files
    # =======================================================================
    
    files_to_create.append({
        "path": "backend/package.json",
        "content": json.dumps({
            "name": "ai-cofounder-backend",
            "version": "0.1.0",
            "type": "module",
            "scripts": {
                "dev": "tsx watch src/index.ts",
                "build": "tsc",
                "start": "node dist/index.js",
                "db:migrate": "drizzle-kit push:sqlite",
                "db:studio": "drizzle-kit studio"
            },
            "dependencies": {
                "@mastra/core": "latest",
                "drizzle-orm": "^0.29.0",
                "better-sqlite3": "^9.2.0",
                "fastify": "^4.25.0",
                "@fastify/websocket": "^8.0.0",
                "@fastify/cors": "^8.4.0",
                "zod": "^3.22.0"
            },
            "devDependencies": {
                "typescript": "^5.3.0",
                "tsx": "^4.7.0",
                "@types/node": "^20.10.0",
                "@types/better-sqlite3": "^7.6.0",
                "drizzle-kit": "^0.20.0"
            }
        }, indent=2)
    })
    
    files_to_create.append({
        "path": "backend/tsconfig.json",
        "content": json.dumps({
            "compilerOptions": {
                "target": "ES2022",
                "module": "ESNext",
                "moduleResolution": "bundler",
                "lib": ["ES2022"],
                "outDir": "./dist",
                "rootDir": "./src",
                "strict": True,
                "esModuleInterop": True,
                "skipLibCheck": True,
                "forceConsistentCasingInFileNames": True,
                "resolveJsonModule": True
            },
            "include": ["src/**/*"],
            "exclude": ["node_modules", "dist"]
        }, indent=2)
    })
    
    files_to_create.append({
        "path": "backend/Dockerfile",
        "content": """FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --production

COPY --from=builder /app/dist ./dist

EXPOSE 3000

CMD ["node", "dist/index.js"]
"""
    })
    
    # Backend source files (minimal for now - will expand)
    files_to_create.append({
        "path": "backend/src/index.ts",
        "content": """import Fastify from 'fastify';
import cors from '@fastify/cors';
import websocket from '@fastify/websocket';

const fastify = Fastify({ logger: true });

// Plugins
await fastify.register(cors);
await fastify.register(websocket);

// Routes
fastify.get('/health', async () => ({ status: 'ok' }));

// Start server
const start = async () => {
  try {
    await fastify.listen({ port: 3000, host: '0.0.0.0' });
    console.log('🚀 AI Cofounder Backend running on http://localhost:3000');
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();
"""
    })
    
    # =======================================================================
    # Frontend Files
    # =======================================================================
    
    files_to_create.append({
        "path": "frontend/package.json",
        "content": json.dumps({
            "name": "ai-cofounder-frontend",
            "version": "0.1.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "tsc && vite build",
                "preview": "vite preview"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.21.0",
                "@tanstack/react-query": "^5.14.0",
                "zustand": "^4.4.0",
                "tailwindcss": "^3.4.0",
                "autoprefixer": "^10.4.0",
                "postcss": "^8.4.0"
            },
            "devDependencies": {
                "@types/react": "^18.2.0",
                "@types/react-dom": "^18.2.0",
                "@vitejs/plugin-react": "^4.2.0",
                "typescript": "^5.3.0",
                "vite": "^5.0.0"
            }
        }, indent=2)
    })
    
    files_to_create.append({
        "path": "frontend/tsconfig.json",
        "content": json.dumps({
            "compilerOptions": {
                "target": "ES2020",
                "useDefineForClassFields": True,
                "lib": ["ES2020", "DOM", "DOM.Iterable"],
                "module": "ESNext",
                "skipLibCheck": True,
                "moduleResolution": "bundler",
                "allowImportingTsExtensions": True,
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True,
                "jsx": "react-jsx",
                "strict": True,
                "noUnusedLocals": True,
                "noUnusedParameters": True,
                "noFallthroughCasesInSwitch": True
            },
            "include": ["src"],
            "references": [{ "path": "./tsconfig.node.json" }]
        }, indent=2)
    })
    
    files_to_create.append({
        "path": "frontend/Dockerfile",
        "content": """FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
"""
    })
    
    files_to_create.append({
        "path": "frontend/vite.config.ts",
        "content": """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true
  }
});
"""
    })
    
    files_to_create.append({
        "path": "frontend/tailwind.config.js",
        "content": """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
    })
    
    files_to_create.append({
        "path": "frontend/index.html",
        "content": """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI Cofounder</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""
    })
    
    files_to_create.append({
        "path": "frontend/src/main.tsx",
        "content": """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
"""
    })
    
    files_to_create.append({
        "path": "frontend/src/App.tsx",
        "content": """import React from 'react';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          AI Cofounder
        </h1>
        <p className="text-gray-600">
          This webapp was built by the AI Cofounder itself using Possible Futures.
        </p>
        <div className="mt-8 p-6 bg-white rounded-lg shadow">
          <h2 className="text-2xl font-semibold mb-4">Status: Building...</h2>
          <ul className="space-y-2 text-gray-700">
            <li>✓ Project structure generated</li>
            <li>✓ Docker configuration created</li>
            <li>✓ TypeScript + React setup complete</li>
            <li>⏳ Mastra agents initializing...</li>
            <li>⏳ Possible Futures tools integrating...</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;
"""
    })
    
    files_to_create.append({
        "path": "frontend/src/index.css",
        "content": """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
"""
    })
    
    # =======================================================================
    # Telemetry Files
    # =======================================================================
    
    files_to_create.append({
        "path": "telemetry/package.json",
        "content": json.dumps({
            "name": "ai-cofounder-telemetry",
            "version": "0.1.0",
            "type": "module",
            "scripts": {
                "dev": "tsx watch src/index.ts",
                "build": "tsc",
                "start": "node dist/index.js"
            },
            "dependencies": {
                "node-fetch": "^3.3.0"
            },
            "devDependencies": {
                "typescript": "^5.3.0",
                "tsx": "^4.7.0",
                "@types/node": "^20.10.0"
            }
        }, indent=2)
    })
    
    files_to_create.append({
        "path": "telemetry/src/index.ts",
        "content": """const NODE_ID = process.env.NODE_ID || 'unknown';
const CENTRAL_URL = process.env.CENTRAL_URL || 'http://localhost:3000';

async function collectMetrics() {
  const metrics = {
    nodeId: NODE_ID,
    timestamp: new Date().toISOString(),
    cpu: process.cpuUsage(),
    memory: process.memoryUsage(),
    uptime: process.uptime()
  };
  
  console.log('Collected metrics:', metrics);
  
  try {
    // Would send to central server
    // await fetch(`${CENTRAL_URL}/telemetry/report`, {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify(metrics)
    // });
    console.log('Metrics reported (simulated)');
  } catch (error) {
    console.error('Failed to report metrics:', error);
  }
}

// Collect metrics every 60 seconds
setInterval(collectMetrics, 60000);

// Initial collection
collectMetrics();

console.log(`🔍 Telemetry agent started for node: ${NODE_ID}`);
"""
    })
    
    files_to_create.append({
        "path": "telemetry/Dockerfile",
        "content": """FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --production

COPY src ./src

CMD ["node", "src/index.ts"]
"""
    })
    
    # =======================================================================
    # Write All Files
    # =======================================================================
    
    print(f"Creating {len(files_to_create)} files...")
    print()
    
    for file_info in files_to_create:
        file_path = project_root / file_info['path']
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(file_info['content'])
        
        print(f"  ✓ {file_info['path']}")
    
    print()
    print("=" * 80)
    print("✨ PROJECT STRUCTURE GENERATED!")
    print("=" * 80)
    print()
    print(f"Location: {project_root.absolute()}")
    print()
    print("Next steps:")
    print()
    print("1. Install dependencies:")
    print("   cd ai-cofounder-app/backend && npm install")
    print("   cd ../frontend && npm install")
    print("   cd ../telemetry && npm install")
    print()
    print("2. Start development:")
    print("   cd ai-cofounder-app")
    print("   docker-compose up")
    print()
    print("3. Access:")
    print("   Frontend: http://localhost")
    print("   Backend:  http://localhost:3000")
    print()
    print("=" * 80)


if __name__ == "__main__":
    import sys
    
    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "AI COFOUNDER BUILDS ITSELF" + " " * 32 + "║")
    print("║" + " " * 78 + "║")
    print("║" + " " * 15 + "Test #4: Can AI Build Its Own Webapp?" + " " * 22 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Parent ID can be passed as argument or we create without parent
    if len(sys.argv) > 1:
        parent_id = sys.argv[1]
        print(f"Using parent idea: {parent_id}")
    else:
        # Try to find it from active ideas, or just create without parent
        all_ideas = list_all_ideas()
        parent_idea = next((i for i in all_ideas if i['name'] == 'AI Cofounder App'), None)
        
        if parent_idea:
            parent_id = parent_idea['id']
            print(f"Found parent idea: {parent_idea['name']} ({parent_id[:8]}...)")
        else:
            print("No parent idea found - creating standalone webapp idea")
            parent_id = None
    
    print()
    
    # Spawn webapp build idea
    webapp_idea_id = spawn_webapp_build_idea(parent_id)
    
    # Generate actual project
    generate_project_structure(webapp_idea_id)
    
    print()
    print("🎉 THE AI COFOUNDER HAS BUILT ITSELF!")
    print()
    print(f"Webapp Idea ID: {webapp_idea_id}")
    if parent_id:
        print(f"Parent Idea ID: {parent_id}")
    print()

