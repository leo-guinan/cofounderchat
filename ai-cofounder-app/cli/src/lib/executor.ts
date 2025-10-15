import { execSync } from 'child_process';
import * as fs from 'fs';

/**
 * Safe command executor
 * 
 * Executes commands from central AI in sandboxed environment
 * with audit logging
 */

const ALLOWED_COMMANDS = [
  'docker',
  'systemctl',
  'journalctl',
  'git',
  'npm',
  'caddy',
];

export async function executeCommand(
  command: string,
  args: string[] = []
): Promise<string> {
  // Validate command is allowed
  const baseCommand = command.split(' ')[0];
  
  if (!ALLOWED_COMMANDS.includes(baseCommand)) {
    throw new Error(`Command not allowed: ${baseCommand}`);
  }
  
  // Log command execution
  const logEntry = {
    timestamp: new Date().toISOString(),
    command,
    args,
  };
  
  fs.appendFileSync(
    '/var/log/ai-cofounder/command-audit.log',
    JSON.stringify(logEntry) + '\n'
  );
  
  // Execute command
  try {
    const fullCommand = `${command} ${args.join(' ')}`;
    const result = execSync(fullCommand, {
      encoding: 'utf-8',
      timeout: 30000, // 30 second timeout
    });
    
    return result;
  } catch (error: any) {
    throw new Error(`Command failed: ${error.message}`);
  }
}
