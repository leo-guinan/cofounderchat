/**
 * Test setup - runs before all tests
 */

import { beforeAll, afterAll, beforeEach, afterEach } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';

// Setup test database
beforeAll(() => {
  console.log('Setting up test environment...');
  
  // Ensure test data directory exists
  const testDataDir = path.join(__dirname, '../data/test');
  if (!fs.existsSync(testDataDir)) {
    fs.mkdirSync(testDataDir, { recursive: true });
  }
  
  // Clear test database if exists
  const testDbPath = path.join(testDataDir, 'test.db');
  if (fs.existsSync(testDbPath)) {
    fs.unlinkSync(testDbPath);
  }
});

// Clean up after all tests
afterAll(() => {
  console.log('Cleaning up test environment...');
});

// Reset before each test
beforeEach(() => {
  // Clear any global state
});

// Cleanup after each test
afterEach(() => {
  // Ensure clean state for next test
});
