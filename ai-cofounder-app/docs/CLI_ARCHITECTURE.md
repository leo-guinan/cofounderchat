# AI Cofounder CLI Architecture

## Overview

The AI Cofounder CLI enables secure, agent-based management of deployed nodes **without SSH**.

## Design Principles

### 1. Phone-Home Pattern

The node **initiates** connection to central AI:

```
Traditional (SSH):
User → SSH → Server → Execute
❌ Requires open port 22
❌ Requires key management
❌ Requires user to connect

AI Cofounder:
Node → WebSocket → Central AI → Command → Node executes
✅ No inbound ports
✅ Automated key management
✅ AI controls, user approves
```

### 2. Zero-Trust Security

- Each node has unique RSA key pair (4096-bit)
- Node authenticates with JWT signed by private key
- Central validates with public key
- All commands require authentication
- All commands audited

### 3. Self-Sufficient Nodes

Each node can:
- Deploy applications
- Manage SSL certificates
- Monitor health
- Update itself
- Communicate securely

**No human SSH required.**

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CENTRAL AI COFOUNDER                     │
│                                                             │
│  • Receives telemetry from all nodes                       │
│  • Sends commands to nodes                                 │
│  • Validates node authentication                           │
│  • Manages node registry                                   │
└─────────────────┬───────────────────────────────────────────┘
                  │
            WebSocket (WSS)
         mTLS + JWT Auth
                  │
    ┌─────────────┴─────────────┬──────────────────┐
    │                           │                  │
┌───▼─────────┐         ┌───────▼───┐      ┌──────▼──────┐
│   NODE 1    │         │   NODE 2  │      │   NODE 3    │
│             │         │           │      │             │
│ • Agent     │         │ • Agent   │      │ • Agent     │
│ • CLI       │         │ • CLI     │      │ • CLI       │
│ • App       │         │ • App     │      │ • App       │
│ • Caddy     │         │ • Caddy   │      │ • Caddy     │
└─────────────┘         └───────────┘      └─────────────┘
```

## Security Model

### Node Registration

```
1. User runs: cofounder init
2. CLI generates RSA key pair (4096-bit)
3. CLI sends public key + node info to central
4. Central validates token
5. Central stores public key
6. Node saves private key (600 permissions)
7. Registration complete
```

### Authentication Flow

```
1. Node creates JWT:
   {
     nodeId: "uuid",
     hostname: "server1",
     timestamp: 1234567890
   }
   
2. Node signs with private key (RS256)

3. Node sends JWT in connection request

4. Central validates JWT with public key

5. If valid, connection established
```

### Command Execution

```
1. Central sends command:
   {
     type: "execute",
     command: "docker",
     args: ["ps"],
     requestId: "uuid"
   }

2. Node validates command in whitelist

3. Node executes in sandboxed environment

4. Node logs to audit log

5. Node sends result back to central

6. Central receives and processes
```

## Components

### 1. CLI Commands

| Command | Purpose | Runs On |
|---------|---------|---------|
| `init` | Initialize node | Server (once) |
| `deploy` | Deploy/update app | Server |
| `ssl setup` | Configure SSL | Server (once) |
| `agent start` | Start monitoring agent | Server |
| `status` | Show node info | Server |
| `connect` | Connect to central | Server/daemon |

### 2. Agent (Daemon)

Runs as systemd service:
- Maintains WebSocket connection to central
- Reports telemetry every 60s
- Executes commands from central
- Monitors application health
- Auto-reconnects if disconnected

### 3. Central API

Endpoints for nodes:
- `POST /api/nodes/register` - Register new node
- `WS /nodes/connect` - Establish WebSocket
- `POST /api/nodes/:id/command` - Send command (for manual use)
- `GET /api/nodes/:id/status` - Get node status

## SSL Management (Caddy)

### Why Caddy?

- Automatic HTTPS (Let's Encrypt)
- Auto-renewal (no manual intervention)
- HTTP/2 and HTTP/3 support
- Simple configuration
- Zero maintenance

### Caddyfile

```caddyfile
yourdomain.com {
  tls you@email.com
  reverse_proxy localhost:3000
  
  # Security headers
  header Strict-Transport-Security "max-age=31536000"
  
  # Rate limiting
  rate_limit {
    zone dynamic {
      key {remote_host}
      events 100
      window 1m
    }
  }
}
```

### Certificate Lifecycle

```
Day 1:   Caddy obtains certificate (Let's Encrypt)
Day 60:  Caddy auto-renews (30 days before expiry)
Day 90:  Old certificate expires (but already renewed)
```

**Zero manual intervention required.**

## Telemetry

### What's Reported

```json
{
  "nodeId": "uuid",
  "timestamp": "2025-10-15T10:00:00Z",
  "system": {
    "uptime": 86400,
    "memory": {
      "total": 2147483648,
      "used": 1073741824,
      "free": 1073741824
    },
    "cpu": {
      "user": 100000,
      "system": 50000
    },
    "disk": {
      "total": "20G",
      "used": "5G",
      "available": "15G"
    },
    "load": [0.5, 0.7, 0.6]
  },
  "containers": [
    {
      "name": "ai-cofounder-backend",
      "status": "running",
      "uptime": "2 days"
    }
  ],
  "application": {
    "version": "0.1.0",
    "health": "ok",
    "requests": 1500,
    "errors": 2
  }
}
```

### Frequency

- **Telemetry**: Every 60 seconds
- **Health check**: Every 5 minutes
- **Full snapshot**: Every 6 hours

## Deployment Flow

### Via CLI

```bash
cofounder deploy
```

Executes:
1. Pull latest code (git pull)
2. Build containers (docker-compose build)
3. Stop old containers
4. Start new containers
5. Health check
6. Report to central

### Via Central AI

```
Central AI decides to deploy
    ↓
Sends command to node via WebSocket
    ↓
Node agent receives command
    ↓
Executes: cofounder deploy
    ↓
Reports result to central
```

## Firewall Configuration

### Required Outbound

- **Port 443**: HTTPS to central AI (wss://)
- **Port 80/443**: Let's Encrypt (certificate validation)

### Required Inbound

- **Port 443**: HTTPS traffic (user access)
- **Port 80**: HTTP (redirect to HTTPS)

### Not Required

- ❌ **Port 22**: SSH (not needed!)
- ❌ **Custom ports**: Everything through 80/443

## Comparison to SSH

| Aspect | SSH | AI Cofounder CLI |
|--------|-----|------------------|
| **Access** | User initiates | Node initiates |
| **Port** | 22 (inbound) | 443 (outbound) |
| **Keys** | User manages | Auto-managed |
| **Audit** | Optional | Always logged |
| **Security** | User responsibility | Enforced |
| **Firewall** | Open port 22 | No inbound needed |
| **Management** | Manual | AI-controlled |

## Advanced Features

### Command Whitelist

Only these commands can be executed remotely:
- `docker` - Container management
- `systemctl` - Service management
- `journalctl` - Log viewing
- `git` - Code updates
- `npm` - Dependency management
- `caddy` - SSL management

Everything else is blocked.

### Audit Logging

All commands logged to:
```
/var/log/ai-cofounder/command-audit.log
```

Format:
```json
{"timestamp":"2025-10-15T10:00:00Z","command":"docker ps","args":[],"result":"success"}
```

### Emergency Access

If agent fails, you can still:
```bash
# 1. SSH to server (if you kept SSH)
# 2. Check logs
journalctl -u ai-cofounder-agent

# 3. Restart manually
systemctl restart ai-cofounder-agent
```

## Future Enhancements

- [ ] Certificate pinning
- [ ] Command approval workflow
- [ ] Multi-node orchestration
- [ ] Automatic rollback on failure
- [ ] Blue-green deployments
- [ ] A/B testing support
