import chalk from 'chalk';
import ora from 'ora';
import { execSync } from 'child_process';

export async function updateCommand(options: { version?: string }) {
  console.log(chalk.bold('\n⬆️  Updating AI Cofounder CLI\n'));
  
  const spinner = ora('Checking for updates...').start();
  
  try {
    const currentVersion = require('../../package.json').version;
    console.log(chalk.gray('Current version:'), chalk.cyan(currentVersion));
    
    // Update via npm
    spinner.text = 'Installing latest version...';
    
    const version = options.version || 'latest';
    const cmd = `npm install -g @ai-cofounder/cli@${version}`;
    
    execSync(cmd, { stdio: 'ignore' });
    
    const newVersion = execSync('cofounder --version', { encoding: 'utf-8' }).trim();
    
    spinner.succeed('CLI updated successfully');
    
    console.log(chalk.green('\n✅ Updated to version:'), chalk.cyan(newVersion));
    console.log();
    
  } catch (error: any) {
    spinner.fail('Update failed');
    console.error(chalk.red('\nError:'), error.message);
    process.exit(1);
  }
}
