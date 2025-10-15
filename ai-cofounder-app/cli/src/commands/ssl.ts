import chalk from 'chalk';
import ora from 'ora';
import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

/**
 * SSL Certificate Management using Caddy
 * 
 * Caddy automatically handles Let's Encrypt certificates
 * with auto-renewal. No manual certificate management needed.
 */

async function setupSSL(options: { domain: string; email: string }) {
  console.log(chalk.bold('\n🔒 Setting up SSL Certificates\n'));
  
  const spinner = ora('Installing Caddy...').start();
  
  try {
    // 1. Install Caddy if not present
    try {
      execSync('caddy version', { stdio: 'ignore' });
      spinner.text = 'Caddy already installed';
    } catch {
      spinner.text = 'Installing Caddy...';
      
      if (process.platform === 'linux') {
        execSync(
          'curl -1sLf https://dl.cloudsmith.io/public/caddy/stable/gpg.key | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg && ' +
          'curl -1sLf https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt | tee /etc/apt/sources.list.d/caddy-stable.list && ' +
          'apt update && apt install -y caddy',
          { stdio: 'ignore' }
        );
      } else {
        throw new Error('Automatic Caddy installation only supported on Linux. Install manually: https://caddyserver.com/docs/install');
      }
    }
    
    // 2. Create Caddyfile
    spinner.text = 'Configuring Caddy...';
    
    const caddyfile = `${options.domain} {
  # Automatic HTTPS with Let's Encrypt
  tls ${options.email}
  
  # Reverse proxy to AI Cofounder backend
  reverse_proxy localhost:3000
  
  # Security headers
  header {
    Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    X-Content-Type-Options "nosniff"
    X-Frame-Options "DENY"
    Referrer-Policy "strict-origin-when-cross-origin"
  }
  
  # Rate limiting
  rate_limit {
    zone dynamic {
      key {remote_host}
      events 100
      window 1m
    }
  }
  
  # Logging
  log {
    output file /var/log/caddy/access.log
    format json
  }
}

# Admin API (localhost only)
localhost:2019 {
  # Caddy admin endpoint for certificate management
}
`;
    
    const caddyfilePath = '/etc/caddy/Caddyfile';
    fs.writeFileSync(caddyfilePath, caddyfile);
    
    // 3. Create log directory
    if (!fs.existsSync('/var/log/caddy')) {
      fs.mkdirSync('/var/log/caddy', { recursive: true });
    }
    
    // 4. Enable and start Caddy
    spinner.text = 'Starting Caddy...';
    execSync('systemctl enable caddy', { stdio: 'ignore' });
    execSync('systemctl restart caddy', { stdio: 'ignore' });
    
    // 5. Wait for certificate
    spinner.text = 'Obtaining SSL certificate (may take 30-60s)...';
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    // 6. Verify certificate
    try {
      const certInfo = execSync(
        `curl -sI https://${options.domain} | grep -i 'strict-transport-security'`,
        { encoding: 'utf-8' }
      );
      
      if (certInfo) {
        spinner.succeed('SSL certificate obtained and active!');
      } else {
        throw new Error('Certificate verification failed');
      }
    } catch {
      spinner.warn('SSL setup complete, but certificate verification pending');
      console.log(chalk.yellow('\nNote: Certificate may take a few minutes to propagate'));
    }
    
    console.log('\n' + chalk.green('✅ SSL Configuration:'));
    console.log(chalk.gray('   Domain:'), chalk.cyan(options.domain));
    console.log(chalk.gray('   Email:'), chalk.cyan(options.email));
    console.log(chalk.gray('   Caddyfile:'), chalk.cyan(caddyfilePath));
    console.log(chalk.gray('   Auto-renewal:'), chalk.green('Enabled'));
    console.log('\n' + chalk.yellow('Access your app at:'));
    console.log(chalk.cyan(`   https://${options.domain}`));
    console.log();
    
  } catch (error: any) {
    spinner.fail('SSL setup failed');
    console.error(chalk.red('\nError:'), error.message);
    process.exit(1);
  }
}

async function renewSSL() {
  console.log(chalk.bold('\n🔄 Renewing SSL Certificate\n'));
  
  const spinner = ora('Requesting renewal...').start();
  
  try {
    // Caddy auto-renews, but we can force it
    execSync('systemctl reload caddy', { stdio: 'ignore' });
    
    spinner.succeed('Certificate renewal triggered');
    console.log(chalk.gray('\nCaddy will automatically renew when needed'));
    console.log(chalk.gray('Certificates are valid for 90 days and renew at 60 days'));
    
  } catch (error: any) {
    spinner.fail('Renewal failed');
    console.error(chalk.red('\nError:'), error.message);
    process.exit(1);
  }
}

async function checkSSLStatus() {
  console.log(chalk.bold('\n📊 SSL Certificate Status\n'));
  
  try {
    // Get certificate info from Caddy
    const certList = execSync(
      'curl -s http://localhost:2019/pki/certificates/local',
      { encoding: 'utf-8' }
    );
    
    const certs = JSON.parse(certList);
    
    console.log(chalk.green('Certificates:'));
    for (const cert of certs) {
      console.log(chalk.gray('\n  Domain:'), chalk.cyan(cert.subjects[0]));
      console.log(chalk.gray('  Expires:'), chalk.yellow(new Date(cert.not_after).toLocaleDateString()));
      console.log(chalk.gray('  Issuer:'), cert.issuer_common_name);
      console.log(chalk.gray('  Auto-renew:'), chalk.green('Yes'));
    }
    
  } catch (error: any) {
    console.error(chalk.red('Error:'), error.message);
    console.log(chalk.yellow('\nCaddy may not be running or no certificates issued yet'));
    process.exit(1);
  }
}

export const sslCommand = {
  setup: setupSSL,
  renew: renewSSL,
  status: checkSSLStatus,
};
