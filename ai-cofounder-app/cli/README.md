# AI Cofounder CLI

Secure management CLI for AI Cofounder deployed nodes.

## Installation

### On Server (Production)

```bash
# Install globally
npm install -g @ai-cofounder/cli

# Or build from source
cd cli
npm install
npm run build
npm link
```

## Usage

### Initialize Node

```bash
# First time setup
cofounder init

# You'll be prompted for:
# - Central AI Cofounder URL
# - Authentication token
```

This:
- Generates unique node ID
- Creates secure keys (RSA 4096-bit)
- Registers with central AI
- Saves configuration to `/etc/ai-cofounder/`

### Set Up SSL

```bash
# Automatic SSL with Let's Encrypt (via Caddy)
cofounder ssl setup -d yourdomain.com -e you@email.com
```

This:
- Installs Caddy (automatic HTTPS)
- Configures reverse proxy
- Obtains SSL certificate
- Enables auto-renewal

### Deploy Application

```bash
# Deploy production
cofounder deploy

# Deploy from specific branch
cofounder deploy -b develop

# Deploy to staging
cofounder deploy -e staging
```

This:
- Pulls latest code
- Builds Docker containers
- Stops old containers
- Starts new containers
- Runs health checks

### Start Agent

```bash
# Run as daemon (systemd service)
cofounder agent start --daemon

# Run in foreground (for debugging)
cofounder agent start
```

The agent:
- Maintains connection to central AI
- Reports telemetry every 60s
- Executes commands from central
- Monitors application health

### Check Status

```bash
# Basic status
cofounder status

# Detailed status
cofounder status --verbose
```

Shows:
- Node information
- Agent status
- Application containers
- SSL status
- System resources

### Manage Agent

```bash
# Start as daemon
cofounder agent start --daemon

# Stop
cofounder agent stop

# Restart
cofounder agent restart

# View logs
cofounder agent logs

# Follow logs
cofounder agent logs --follow
```

## Architecture

### Phone-Home Pattern

```
Deployed Node                    Central AI Cofounder
    │                                    │
    │  1. Initiate connection (WSS)     │
    ├────────────────────────────────────>│
    │                                    │
    │  2. Send telemetry (every 60s)    │
    ├────────────────────────────────────>│
    │                                    │
    │  3. Receive command                │
    │<────────────────────────────────────┤
    │                                    │
    │  4. Execute & respond              │
    ├────────────────────────────────────>│
    │                                    │
```

**Security**:
- Node initiates connection (no inbound ports)
- JWT authentication with RSA keys
- mTLS (mutual TLS)
- Command whitelist
- Audit logging

### No SSH Required

Traditional approach:
```
User → SSH → Server → Execute commands
```

AI Cofounder approach:
```
AI → Central → WebSocket → Node Agent → Execute
```

**Benefits**:
- No SSH keys to manage
- No exposed SSH port (22)
- Centralized access control
- Complete audit trail
- Works through firewalls

## Security

### Authentication

- **Node → Central**: JWT signed with node's private key
- **Central validates**: Using node's public key
- **Keys**: RSA 4096-bit, generated per node
- **Rotation**: Keys can be rotated via `cofounder init --rotate`

### Communication

- **Protocol**: WebSocket over TLS (wss://)
- **Encryption**: TLS 1.3
- **Certificate**: Let's Encrypt (auto-renewed)
- **Validation**: Certificate pinning (optional)

### Command Execution

- **Whitelist**: Only allowed commands can run
- **Sandbox**: Commands run in restricted environment
- **Timeout**: 30 second maximum
- **Audit**: All commands logged

### Secrets

- **Never transmitted**: Secrets stay on node
- **Environment only**: Loaded from `/etc/ai-cofounder/secrets.env`
- **Permissions**: 600 (root only)

## Configuration

### Node Configuration (`/etc/ai-cofounder/node.json`)

```json
{
  "nodeId": "uuid-here",
  "centralUrl": "https://central.aicofounder.com",
  "createdAt": "2025-10-15T10:00:00Z",
  "publicKey": "-----BEGIN PUBLIC KEY-----\n..."
}
```

### Private Key (`/etc/ai-cofounder/node.key`)

```
-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----
```

Permissions: 600 (root:root)

## Commands Reference

| Command | Purpose | Flags |
|---------|---------|-------|
| `init` | Initialize node | `-c <url>`, `-t <token>` |
| `deploy` | Deploy application | `-e <env>`, `-b <branch>` |
| `ssl setup` | Set up SSL | `-d <domain>`, `-e <email>` |
| `ssl renew` | Renew certificate | - |
| `ssl status` | Check certificate | - |
| `status` | Show node status | `-v` (verbose) |
| `update` | Update CLI | `--version <ver>` |
| `connect` | Connect to central | `-d` (daemon) |
| `agent start` | Start agent | `-d` (daemon) |
| `agent stop` | Stop agent | - |
| `agent restart` | Restart agent | - |
| `agent logs` | View logs | `-f`, `-n <lines>` |

## Troubleshooting

### Agent won't connect

```bash
# Check configuration
cat /etc/ai-cofounder/node.json

# Check logs
cofounder agent logs --follow

# Check network
curl -I <central-url>

# Restart agent
cofounder agent restart
```

### SSL certificate issues

```bash
# Check status
cofounder ssl status

# Check Caddy logs
journalctl -u caddy -n 100

# Restart Caddy
systemctl restart caddy
```

### Deployment fails

```bash
# Check Docker
docker ps

# Check logs
docker-compose logs

# Manual deploy
cd /opt/ai-cofounder
docker-compose -f docker-compose.prod.yml up -d
```

## Development

```bash
cd cli

# Install dependencies
npm install

# Development
npm run dev

# Build
npm run build

# Test
node dist/index.js --help
```
