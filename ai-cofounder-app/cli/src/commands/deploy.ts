import chalk from 'chalk';
import ora from 'ora';
import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

export async function deployCommand(options: any) {
  console.log(chalk.bold('\n🚀 Deploying AI Cofounder\n'));
  console.log(chalk.gray('Environment:'), chalk.cyan(options.env));
  console.log(chalk.gray('Branch:'), chalk.cyan(options.branch));
  console.log();
  
  const spinner = ora('Checking prerequisites...').start();
  
  try {
    // 1. Check Docker is running
    try {
      execSync('docker ps', { stdio: 'ignore' });
      spinner.text = 'Docker is running ✓';
    } catch {
      throw new Error('Docker is not running. Start with: systemctl start docker');
    }
    
    // 2. Check secrets are configured
    const secretsPath = '/etc/ai-cofounder/secrets.env';
    if (!fs.existsSync(secretsPath)) {
      throw new Error(`Secrets not found at ${secretsPath}. Run: cofounder init`);
    }
    spinner.text = 'Secrets configured ✓';
    
    // 3. Pull latest code
    spinner.text = `Pulling ${options.branch} branch...`;
    const appDir = '/opt/ai-cofounder';
    
    if (!fs.existsSync(appDir)) {
      // Clone repo
      spinner.text = 'Cloning repository...';
      execSync(
        `git clone -b ${options.branch} <REPO_URL> ${appDir}`,
        { stdio: 'ignore' }
      );
    } else {
      // Pull updates
      process.chdir(appDir);
      execSync(`git fetch origin ${options.branch}`, { stdio: 'ignore' });
      execSync(`git checkout ${options.branch}`, { stdio: 'ignore' });
      execSync(`git pull origin ${options.branch}`, { stdio: 'ignore' });
    }
    
    // 4. Build and deploy
    spinner.text = 'Building containers...';
    process.chdir(appDir);
    
    const composeFile = options.env === 'production' 
      ? 'docker-compose.prod.yml' 
      : 'docker-compose.yml';
    
    execSync(
      `docker-compose -f ${composeFile} build --no-cache`,
      { stdio: 'ignore' }
    );
    
    // 5. Stop old containers
    spinner.text = 'Stopping old containers...';
    try {
      execSync(`docker-compose -f ${composeFile} down`, { stdio: 'ignore' });
    } catch {
      // Might not exist yet
    }
    
    // 6. Start new containers
    spinner.text = 'Starting containers...';
    execSync(
      `docker-compose -f ${composeFile} up -d`,
      { stdio: 'inherit' }
    );
    
    // 7. Wait for health check
    spinner.text = 'Waiting for health check...';
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    const healthCheck = execSync(
      'curl -sf http://localhost:3000/health || echo "FAILED"',
      { encoding: 'utf-8' }
    );
    
    if (healthCheck.includes('FAILED')) {
      throw new Error('Health check failed');
    }
    
    spinner.succeed('Deployment complete!');
    
    console.log('\n' + chalk.green('✅ Application Status:'));
    
    // Get container status
    const containers = execSync(
      `docker-compose -f ${composeFile} ps --format json`,
      { encoding: 'utf-8' }
    );
    
    const containerList = containers.trim().split('\n').map(line => JSON.parse(line));
    
    for (const container of containerList) {
      const icon = container.State === 'running' ? '✓' : '✗';
      console.log(
        chalk.gray(`   ${icon} ${container.Service}:`),
        container.State === 'running' ? chalk.green('running') : chalk.red(container.State)
      );
    }
    
    console.log('\n' + chalk.yellow('Access the application:'));
    console.log(chalk.cyan('   http://localhost:3000/health'));
    console.log();
    
  } catch (error: any) {
    spinner.fail('Deployment failed');
    console.error(chalk.red('\nError:'), error.message);
    process.exit(1);
  }
}
