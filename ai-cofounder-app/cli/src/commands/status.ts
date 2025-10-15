import chalk from 'chalk';
import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

export async function statusCommand(options: { verbose?: boolean }) {
  console.log(chalk.bold('\n📊 Node Status\n'));
  
  try {
    // 1. Load node config
    const configPath = '/etc/ai-cofounder/node.json';
    if (!fs.existsSync(configPath)) {
      console.log(chalk.yellow('⚠️  Node not initialized'));
      console.log(chalk.gray('\nRun:'), chalk.cyan('cofounder init'));
      return;
    }
    
    const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    
    console.log(chalk.green('Node Information:'));
    console.log(chalk.gray('   Node ID:'), chalk.cyan(config.nodeId));
    console.log(chalk.gray('   Hostname:'), require('os').hostname());
    console.log(chalk.gray('   Central:'), chalk.cyan(config.centralUrl));
    console.log();
    
    // 2. Check agent status
    try {
      const agentStatus = execSync('systemctl is-active ai-cofounder-agent 2>/dev/null || echo inactive', {
        encoding: 'utf-8'
      }).trim();
      
      console.log(chalk.green('Agent Status:'));
      console.log(
        chalk.gray('   Service:'),
        agentStatus === 'active' ? chalk.green('running') : chalk.red(agentStatus)
      );
      
      if (agentStatus === 'active') {
        const uptime = execSync(
          'systemctl show ai-cofounder-agent --property=ActiveEnterTimestamp --value',
          { encoding: 'utf-8' }
        ).trim();
        console.log(chalk.gray('   Started:'), uptime);
      }
    } catch {
      console.log(chalk.gray('   Service:'), chalk.yellow('not installed'));
    }
    console.log();
    
    // 3. Check application containers
    try {
      const containers = execSync('docker ps --format "{{.Names}}\t{{.Status}}"', {
        encoding: 'utf-8'
      });
      
      console.log(chalk.green('Application Containers:'));
      containers.trim().split('\n').forEach(line => {
        const [name, status] = line.split('\t');
        const isUp = status.includes('Up');
        console.log(
          chalk.gray(`   ${isUp ? '✓' : '✗'} ${name}:`),
          isUp ? chalk.green(status) : chalk.red(status)
        );
      });
    } catch {
      console.log(chalk.yellow('   No containers running'));
    }
    console.log();
    
    // 4. Check SSL
    try {
      execSync('caddy version', { stdio: 'ignore' });
      const caddyStatus = execSync('systemctl is-active caddy 2>/dev/null || echo inactive', {
        encoding: 'utf-8'
      }).trim();
      
      console.log(chalk.green('SSL (Caddy):'));
      console.log(
        chalk.gray('   Status:'),
        caddyStatus === 'active' ? chalk.green('active') : chalk.red(caddyStatus)
      );
    } catch {
      console.log(chalk.gray('SSL:'), chalk.yellow('not configured'));
    }
    console.log();
    
    // 5. System resources (if verbose)
    if (options.verbose) {
      console.log(chalk.green('System Resources:'));
      
      const memInfo = execSync('free -h | grep Mem', { encoding: 'utf-8' });
      const [, total, used, free] = memInfo.trim().split(/\s+/);
      console.log(chalk.gray('   Memory:'), `${used} / ${total} (${free} free)`);
      
      const diskInfo = execSync('df -h / | tail -1', { encoding: 'utf-8' });
      const diskParts = diskInfo.trim().split(/\s+/);
      console.log(chalk.gray('   Disk:'), `${diskParts[2]} / ${diskParts[1]} (${diskParts[4]} used)`);
      
      const loadAvg = require('os').loadavg();
      console.log(chalk.gray('   Load:'), loadAvg.map(l => l.toFixed(2)).join(', '));
      console.log();
    }
    
  } catch (error: any) {
    console.error(chalk.red('Error:'), error.message);
    process.exit(1);
  }
}
