# Node Agent Protocol

## Communication Protocol

### Message Types

#### Node → Central

```typescript
// Telemetry (every 60s)
{
  type: 'telemetry',
  nodeId: 'uuid',
  timestamp: '2025-10-15T10:00:00Z',
  data: {
    system: { ... },
    containers: [ ... ],
    application: { ... }
  }
}

// Command result
{
  type: 'command_result',
  requestId: 'uuid',
  success: true,
  result: 'output',
  timestamp: '2025-10-15T10:00:00Z'
}

// Status update
{
  type: 'status',
  nodeId: 'uuid',
  status: 'online' | 'degraded' | 'offline',
  timestamp: '2025-10-15T10:00:00Z'
}

// Alert
{
  type: 'alert',
  severity: 'critical' | 'warning' | 'info',
  message: 'High CPU usage detected',
  data: { cpu: 95 }
}
```

#### Central → Node

```typescript
// Execute command
{
  type: 'execute',
  requestId: 'uuid',
  command: 'docker',
  args: ['ps'],
  timeout: 30000
}

// Deploy application
{
  type: 'deploy',
  requestId: 'uuid',
  env: 'production',
  branch: 'main'
}

// Health check request
{
  type: 'health_check',
  requestId: 'uuid'
}

// Update agent
{
  type: 'update_agent',
  version: '0.2.0'
}

// Ping (keepalive)
{
  type: 'ping',
  timestamp: Date.now()
}
```

### Connection Lifecycle

```
1. Node connects
   → Sends JWT for auth
   → Central validates
   → Connection established

2. Heartbeat (every 30s)
   → Node sends ping
   → Central responds pong
   → Connection kept alive

3. Telemetry (every 60s)
   → Node collects metrics
   → Node sends telemetry
   → Central stores in data lake

4. Command execution (on demand)
   → Central sends command
   → Node validates & executes
   → Node sends result
   → Central processes

5. Disconnection
   → Network issue or restart
   → Node attempts reconnect (10s delay)
   → Exponential backoff (max 5 min)
```

## Error Handling

### Connection Errors

- **Network failure**: Retry with exponential backoff
- **Auth failure**: Log error, notify admin
- **Invalid message**: Log and ignore

### Command Errors

- **Timeout**: Kill process, return timeout error
- **Permission denied**: Return error, log
- **Invalid command**: Block and log

### Recovery

- **Connection lost**: Auto-reconnect
- **Agent crashed**: Systemd auto-restart
- **Application down**: Alert central AI

## Monitoring

### Health Checks

```typescript
// Node → Central (every 5 min)
{
  type: 'health',
  checks: {
    agent: 'ok',
    containers: 'ok',
    disk: 'ok',
    memory: 'ok',
    database: 'ok'
  },
  details: { ... }
}
```

### Alerts

```typescript
// Critical: CPU > 90% for 5 min
{
  type: 'alert',
  severity: 'critical',
  message: 'High CPU usage',
  data: { cpu: 95, duration: 300 }
}

// Warning: Disk > 80%
{
  type: 'alert',
  severity: 'warning',
  message: 'Low disk space',
  data: { disk: 85, available: '3GB' }
}
```

## Protocol Security

### Encryption

- **TLS 1.3**: All communication encrypted
- **Perfect Forward Secrecy**: Session keys rotated
- **Certificate Validation**: Prevent MITM

### Authentication

- **JWT**: Signed with node's private key
- **Expiration**: 1 hour (refreshed automatically)
- **Scope**: Limited to node operations

### Authorization

- **Whitelist**: Only allowed commands
- **Sandbox**: Restricted execution environment
- **Audit**: All actions logged

## Scalability

### Single Node

- WebSocket connection (persistent)
- Telemetry every 60s
- Bandwidth: ~1KB/min

### 100 Nodes

- 100 WebSocket connections
- Telemetry: 100KB/min
- Bandwidth: ~140MB/day

### 10,000 Nodes

- 10,000 connections
- Consider: Redis pub/sub for commands
- Consider: Time-series DB for telemetry
- Bandwidth: ~14GB/day

## Future Protocol Extensions

### v0.2: Command Approval

```typescript
// Central → Node
{
  type: 'execute',
  command: 'docker',
  requiresApproval: true,
  approver: 'user@example.com'
}

// User approves via UI
// Central → Node
{
  type: 'execute_approved',
  command: 'docker',
  approvedBy: 'user@example.com'
}
```

### v0.3: Multi-Node Commands

```typescript
// Deploy to all nodes
{
  type: 'broadcast',
  command: 'deploy',
  targets: ['node-1', 'node-2', 'node-3']
}
```

### v0.4: Streaming Logs

```typescript
// Central requests logs
{
  type: 'stream_logs',
  service: 'backend',
  follow: true
}

// Node streams back
{
  type: 'log_line',
  line: '2025-10-15T10:00:00Z [INFO] Server started',
  timestamp: '2025-10-15T10:00:00Z'
}
```
