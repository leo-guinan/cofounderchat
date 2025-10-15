import chalk from 'chalk';
import ora from 'ora';
import { execSync, spawn } from 'child_process';
import * as fs from 'fs';

/**
 * Agent Management
 * 
 * The local agent runs as a daemon and:
 * - Maintains connection to central AI
 * - Collects and reports telemetry
 * - Executes commands from central
 * - Monitors application health
 */

async function startAgent(options: { daemon?: boolean }) {
  console.log(chalk.bold('\n🤖 Starting AI Cofounder Agent\n'));
  
  const spinner = ora('Starting agent...').start();
  
  try {
    // Create systemd service for daemon mode
    if (options.daemon) {
      const serviceFile = `/etc/systemd/system/ai-cofounder-agent.service`;
      
      const service = `[Unit]
Description=AI Cofounder Agent
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/ai-cofounder
ExecStart=/usr/bin/cofounder connect --daemon
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
`;
      
      fs.writeFileSync(serviceFile, service);
      
      execSync('systemctl daemon-reload', { stdio: 'ignore' });
      execSync('systemctl enable ai-cofounder-agent', { stdio: 'ignore' });
      execSync('systemctl start ai-cofounder-agent', { stdio: 'ignore' });
      
      spinner.succeed('Agent started as daemon');
      
      console.log(chalk.green('\n✅ Agent Status:'));
      console.log(chalk.gray('   Service:'), chalk.cyan('ai-cofounder-agent'));
      console.log(chalk.gray('   Status:'), chalk.green('running'));
      console.log(chalk.gray('   Mode:'), chalk.cyan('daemon'));
      console.log('\n' + chalk.yellow('Manage agent:'));
      console.log(chalk.gray('   View logs:'), chalk.cyan('cofounder agent logs'));
      console.log(chalk.gray('   Restart:'), chalk.cyan('cofounder agent restart'));
      console.log(chalk.gray('   Stop:'), chalk.cyan('cofounder agent stop'));
      
    } else {
      // Run in foreground
      spinner.succeed('Agent started in foreground');
      console.log(chalk.yellow('\nPress Ctrl+C to stop\n'));
      
      // Import and run connect command
      const { connectCommand } = await import('./connect');
      await connectCommand({ daemon: false });
    }
    
  } catch (error: any) {
    spinner.fail('Agent start failed');
    console.error(chalk.red('\nError:'), error.message);
    process.exit(1);
  }
}

async function stopAgent() {
  console.log(chalk.bold('\n🛑 Stopping AI Cofounder Agent\n'));
  
  const spinner = ora('Stopping agent...').start();
  
  try {
    execSync('systemctl stop ai-cofounder-agent', { stdio: 'ignore' });
    spinner.succeed('Agent stopped');
    
  } catch (error: any) {
    spinner.fail('Agent stop failed');
    console.error(chalk.red('\nError:'), error.message);
    process.exit(1);
  }
}

async function restartAgent() {
  console.log(chalk.bold('\n🔄 Restarting AI Cofounder Agent\n'));
  
  const spinner = ora('Restarting agent...').start();
  
  try {
    execSync('systemctl restart ai-cofounder-agent', { stdio: 'ignore' });
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const status = execSync('systemctl is-active ai-cofounder-agent', { encoding: 'utf-8' }).trim();
    
    if (status === 'active') {
      spinner.succeed('Agent restarted successfully');
    } else {
      throw new Error(`Agent is ${status}`);
    }
    
  } catch (error: any) {
    spinner.fail('Agent restart failed');
    console.error(chalk.red('\nError:'), error.message);
    process.exit(1);
  }
}

async function viewLogs(options: { follow?: boolean; lines?: string }) {
  console.log(chalk.bold('\n📜 Agent Logs\n'));
  
  const lines = options.lines || '100';
  const followFlag = options.follow ? '-f' : '';
  
  try {
    const cmd = `journalctl -u ai-cofounder-agent -n ${lines} ${followFlag}`;
    execSync(cmd, { stdio: 'inherit' });
    
  } catch (error: any) {
    console.error(chalk.red('\nError:'), error.message);
    process.exit(1);
  }
}

export const agentCommand = {
  start: startAgent,
  stop: stopAgent,
  restart: restartAgent,
  logs: viewLogs,
};
