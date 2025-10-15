import inquirer from 'inquirer';
import chalk from 'chalk';
import ora from 'ora';
import * as fs from 'fs';
import * as path from 'path';
import { v4 as uuidv4 } from 'uuid';
import { generateNodeKeys, registerNode } from '../lib/security';

export async function initNode(options: any) {
  console.log(chalk.bold('\n🤖 AI Cofounder Node Initialization\n'));
  
  // Get configuration
  let config = {
    centralUrl: options.central,
    token: options.token,
    nodeId: uuidv4(),
  };
  
  if (!config.centralUrl || !config.token) {
    const answers = await inquirer.prompt([
      {
        type: 'input',
        name: 'centralUrl',
        message: 'Central AI Cofounder URL:',
        default: 'https://central.aicofounder.com',
        when: !config.centralUrl,
      },
      {
        type: 'password',
        name: 'token',
        message: 'Authentication token:',
        when: !config.token,
      },
    ]);
    config = { ...config, ...answers };
  }
  
  const spinner = ora('Initializing node...').start();
  
  try {
    // 1. Generate node-specific keys (mTLS)
    spinner.text = 'Generating secure keys...';
    const keys = await generateNodeKeys(config.nodeId);
    
    // 2. Create config directory
    const configDir = '/etc/ai-cofounder';
    if (!fs.existsSync(configDir)) {
      fs.mkdirSync(configDir, { recursive: true, mode: 0o700 });
    }
    
    // 3. Save node configuration
    const configPath = path.join(configDir, 'node.json');
    fs.writeFileSync(
      configPath,
      JSON.stringify(
        {
          nodeId: config.nodeId,
          centralUrl: config.centralUrl,
          createdAt: new Date().toISOString(),
          publicKey: keys.publicKey,
        },
        null,
        2
      ),
      { mode: 0o600 }
    );
    
    // 4. Save private key
    const keyPath = path.join(configDir, 'node.key');
    fs.writeFileSync(keyPath, keys.privateKey, { mode: 0o600 });
    
    // 5. Register with central AI
    spinner.text = 'Registering with central AI Cofounder...';
    await registerNode(config.centralUrl, config.token, {
      nodeId: config.nodeId,
      publicKey: keys.publicKey,
      hostname: require('os').hostname(),
      platform: process.platform,
      arch: process.arch,
    });
    
    spinner.succeed('Node initialized successfully!');
    
    console.log('\n' + chalk.green('✅ Node Configuration:'));
    console.log(chalk.gray('   Node ID:'), chalk.cyan(config.nodeId));
    console.log(chalk.gray('   Central:'), chalk.cyan(config.centralUrl));
    console.log(chalk.gray('   Config:'), chalk.cyan(configPath));
    console.log('\n' + chalk.yellow('Next steps:'));
    console.log(chalk.gray('   1.'), 'Set up SSL:', chalk.cyan('cofounder ssl setup -d yourdomain.com -e you@email.com'));
    console.log(chalk.gray('   2.'), 'Deploy app:', chalk.cyan('cofounder deploy'));
    console.log(chalk.gray('   3.'), 'Start agent:', chalk.cyan('cofounder agent start --daemon'));
    console.log();
    
  } catch (error: any) {
    spinner.fail('Initialization failed');
    console.error(chalk.red('\nError:'), error.message);
    process.exit(1);
  }
}
