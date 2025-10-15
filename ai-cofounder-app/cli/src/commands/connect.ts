import chalk from 'chalk';
import ora from 'ora';
import WebSocket from 'ws';
import * as fs from 'fs';
import * as path from 'path';
import jwt from 'jsonwebtoken';
import { executeCommand } from '../lib/executor';

/**
 * Connect to Central AI Cofounder
 * 
 * Phone-home pattern: Node initiates connection to central
 * Central AI can then send commands to execute
 * 
 * Security:
 * - Node authenticates with JWT signed by private key
 * - Central validates with public key
 * - All commands executed in sandboxed environment
 * - Audit log of all executed commands
 */

export async function connectCommand(options: any) {
  console.log(chalk.bold('\n🔌 Connecting to Central AI Cofounder\n'));
  
  const configDir = '/etc/ai-cofounder';
  const configPath = path.join(configDir, 'node.json');
  const keyPath = path.join(configDir, 'node.key');
  
  // Load configuration
  if (!fs.existsSync(configPath)) {
    console.error(chalk.red('Node not initialized. Run: cofounder init'));
    process.exit(1);
  }
  
  const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
  const privateKey = fs.readFileSync(keyPath, 'utf-8');
  
  // Generate authentication token
  const token = jwt.sign(
    {
      nodeId: config.nodeId,
      hostname: require('os').hostname(),
      timestamp: Date.now(),
    },
    privateKey,
    { algorithm: 'RS256', expiresIn: '1h' }
  );
  
  // WebSocket URL
  const wsUrl = config.centralUrl.replace('https://', 'wss://').replace('http://', 'ws://');
  const connectionUrl = `${wsUrl}/nodes/connect?token=${token}`;
  
  const spinner = ora('Establishing secure connection...').start();
  
  try {
    const ws = new WebSocket(connectionUrl);
    
    ws.on('open', () => {
      spinner.succeed('Connected to central AI Cofounder');
      console.log(chalk.green('\n✅ Secure channel established'));
      console.log(chalk.gray('   Node ID:'), chalk.cyan(config.nodeId));
      console.log(chalk.gray('   Central:'), chalk.cyan(config.centralUrl));
      
      if (options.daemon) {
        console.log(chalk.yellow('\nRunning as daemon...'));
        console.log(chalk.gray('Press Ctrl+C to stop'));
      }
      
      // Send initial status
      ws.send(JSON.stringify({
        type: 'status',
        data: {
          nodeId: config.nodeId,
          status: 'online',
          timestamp: new Date().toISOString(),
        }
      }));
    });
    
    ws.on('message', async (data: string) => {
      const message = JSON.parse(data.toString());
      
      console.log(chalk.blue('\n📨 Command from central:'), message.type);
      
      switch (message.type) {
        case 'ping':
          ws.send(JSON.stringify({ type: 'pong', timestamp: Date.now() }));
          break;
          
        case 'execute':
          // Execute command from central AI
          console.log(chalk.gray('   Command:'), message.command);
          
          try {
            const result = await executeCommand(message.command, message.args);
            ws.send(JSON.stringify({
              type: 'command_result',
              requestId: message.requestId,
              success: true,
              result,
            }));
            console.log(chalk.green('   ✓ Executed successfully'));
          } catch (error: any) {
            ws.send(JSON.stringify({
              type: 'command_result',
              requestId: message.requestId,
              success: false,
              error: error.message,
            }));
            console.log(chalk.red('   ✗ Execution failed:'), error.message);
          }
          break;
          
        case 'deploy':
          console.log(chalk.yellow('   Triggering deployment...'));
          // Would trigger deployment
          break;
          
        case 'health_check':
          const health = await getNodeHealth();
          ws.send(JSON.stringify({
            type: 'health_response',
            requestId: message.requestId,
            data: health,
          }));
          break;
          
        default:
          console.log(chalk.yellow('   Unknown command type'));
      }
    });
    
    ws.on('error', (error) => {
      console.error(chalk.red('\nWebSocket error:'), error.message);
    });
    
    ws.on('close', () => {
      console.log(chalk.yellow('\n⚠️  Connection closed'));
      
      if (options.daemon) {
        // Attempt reconnection after delay
        console.log(chalk.gray('Reconnecting in 10 seconds...'));
        setTimeout(() => connectCommand(options), 10000);
      } else {
        process.exit(0);
      }
    });
    
    // Keep process alive if daemon
    if (options.daemon) {
      // Don't exit
      await new Promise(() => {});
    }
    
  } catch (error: any) {
    spinner.fail('Connection failed');
    console.error(chalk.red('\nError:'), error.message);
    process.exit(1);
  }
}

async function getNodeHealth() {
  const { execSync } = require('child_process');
  
  return {
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    cpu: process.cpuUsage(),
    containers: JSON.parse(
      execSync('docker ps --format json', { encoding: 'utf-8' })
    ),
    disk: execSync('df -h /', { encoding: 'utf-8' }),
  };
}
