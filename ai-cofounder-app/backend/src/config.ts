import { cleanEnv, str, num, url } from 'envalid';

/**
 * Application configuration loaded from environment variables
 * 
 * Uses envalid for validation - will fail fast if required secrets missing
 */
export const config = cleanEnv(process.env, {
  // Model API Keys
  OPENAI_API_KEY: str({ desc: 'OpenAI API key for AI models' }),
  ANTHROPIC_API_KEY: str({ default: '', desc: 'Optional Anthropic API key' }),
  
  // Database
  DATABASE_URL: str({ default: 'file:./data/ai-cofounder.db' }),
  DATABASE_ENCRYPTION_KEY: str({ default: '', desc: 'Optional DB encryption key' }),
  
  // OAuth (optional)
  GITHUB_CLIENT_ID: str({ default: '' }),
  GITHUB_CLIENT_SECRET: str({ default: '' }),
  
  // Data Lake
  S3_ENDPOINT: url({ default: 'https://s3.amazonaws.com' }),
  S3_ACCESS_KEY: str({ default: '' }),
  S3_SECRET_KEY: str({ default: '' }),
  S3_BUCKET: str({ default: 'ai-cofounder-data' }),
  S3_REGION: str({ default: 'us-east-1' }),
  
  // Monitoring
  SENTRY_DSN: str({ default: '' }),
  
  // Application
  NODE_ENV: str({ choices: ['development', 'test', 'staging', 'production'], default: 'development' }),
  PORT: num({ default: 3000 }),
  FRONTEND_URL: url({ default: 'http://localhost:5173' }),
  CORS_ORIGIN: str({ default: 'http://localhost:5173' }),
  
  // Session
  SESSION_SECRET: str({ desc: 'Secret for signing sessions' }),
  
  // Deployment
  DEPLOY_ENV: str({ default: 'development' }),
  LOG_LEVEL: str({ choices: ['debug', 'info', 'warn', 'error'], default: 'info' }),
});

// Log config on startup (redact sensitive values)
export function logConfig() {
  const safe = {
    ...config,
    OPENAI_API_KEY: config.OPENAI_API_KEY ? 'sk-***' : undefined,
    ANTHROPIC_API_KEY: config.ANTHROPIC_API_KEY ? 'sk-ant-***' : undefined,
    DATABASE_ENCRYPTION_KEY: config.DATABASE_ENCRYPTION_KEY ? '***' : undefined,
    GITHUB_CLIENT_SECRET: config.GITHUB_CLIENT_SECRET ? '***' : undefined,
    S3_SECRET_KEY: config.S3_SECRET_KEY ? '***' : undefined,
    SESSION_SECRET: '***',
  };
  
  console.log('Configuration loaded:', JSON.stringify(safe, null, 2));
}
