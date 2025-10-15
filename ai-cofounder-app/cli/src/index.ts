#!/usr/bin/env node
/**
 * AI Cofounder CLI
 * 
 * Secure management tool for deployed nodes
 * Runs on the server, communicates with central AI Cofounder
 */

import { Command } from 'commander';
import chalk from 'chalk';
import { initNode } from './commands/init';
import { deployCommand } from './commands/deploy';
import { sslCommand } from './commands/ssl';
import { statusCommand } from './commands/status';
import { updateCommand } from './commands/update';
import { connectCommand } from './commands/connect';
import { agentCommand } from './commands/agent';

const program = new Command();

program
  .name('cofounder')
  .description('AI Cofounder CLI for secure node management')
  .version('0.1.0');

// Initialize node
program
  .command('init')
  .description('Initialize this node for AI Cofounder management')
  .option('-c, --central <url>', 'Central AI Cofounder URL')
  .option('-t, --token <token>', 'Authentication token')
  .action(initNode);

// Deploy application
program
  .command('deploy')
  .description('Deploy or update the application')
  .option('-e, --env <env>', 'Environment (staging/production)', 'production')
  .option('-b, --branch <branch>', 'Git branch to deploy', 'main')
  .action(deployCommand);

// SSL management
program
  .command('ssl')
  .description('Manage SSL certificates')
  .addCommand(
    new Command('setup')
      .description('Set up SSL with automatic certificate management')
      .requiredOption('-d, --domain <domain>', 'Domain name')
      .requiredOption('-e, --email <email>', 'Email for Let\'s Encrypt')
      .action(async (options) => {
        await sslCommand.setup(options);
      })
  )
  .addCommand(
    new Command('renew')
      .description('Manually renew SSL certificate')
      .action(async () => {
        await sslCommand.renew();
      })
  )
  .addCommand(
    new Command('status')
      .description('Check SSL certificate status')
      .action(async () => {
        await sslCommand.status();
      })
  );

// Node status
program
  .command('status')
  .description('Show node status and health')
  .option('-v, --verbose', 'Verbose output')
  .action(statusCommand);

// Update CLI
program
  .command('update')
  .description('Update the AI Cofounder CLI')
  .option('--version <version>', 'Specific version to install')
  .action(updateCommand);

// Connect to central AI
program
  .command('connect')
  .description('Establish secure connection to central AI Cofounder')
  .option('-d, --daemon', 'Run as daemon')
  .action(connectCommand);

// Agent management
program
  .command('agent')
  .description('Manage the local agent')
  .addCommand(
    new Command('start')
      .description('Start the agent')
      .option('-d, --daemon', 'Run as daemon')
      .action(async (options) => {
        await agentCommand.start(options);
      })
  )
  .addCommand(
    new Command('stop')
      .description('Stop the agent')
      .action(async () => {
        await agentCommand.stop();
      })
  )
  .addCommand(
    new Command('restart')
      .description('Restart the agent')
      .action(async () => {
        await agentCommand.restart();
      })
  )
  .addCommand(
    new Command('logs')
      .description('View agent logs')
      .option('-f, --follow', 'Follow logs')
      .option('-n, --lines <number>', 'Number of lines', '100')
      .action(async (options) => {
        await agentCommand.logs(options);
      })
  );

program.parse();
