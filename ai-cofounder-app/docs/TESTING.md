# Testing Guide

## Overview

The AI Cofounder has a comprehensive testing system that:
- Generates tests from requirements
- Runs in Docker for consistency
- Supports multiple environments (local, CI, staging, prod)
- Enforces append-only test policy

## Running Tests

### Local (Docker)

```bash
# All tests
docker-compose -f docker-compose.test.yml up test-runner

# Watch mode
docker-compose -f docker-compose.test.yml up backend-test frontend-test

# E2E tests
docker-compose -f docker-compose.test.yml up e2e-test
```

### Local (Direct)

```bash
# Backend tests
cd backend
npm test                # Run once
npm run test:watch      # Watch mode
npm run test:coverage   # With coverage

# Frontend tests
cd frontend
npm test

# E2E tests
npx playwright test
```

### CI

Tests run automatically on push/PR via GitHub Actions.

## Test Types

### Unit Tests
- **Location**: `backend/tests/unit/`
- **Purpose**: Test individual functions
- **Speed**: Fast (< 1s per test)
- **Coverage**: 80% target

### Integration Tests
- **Location**: `backend/tests/integration/`
- **Purpose**: Test components together
- **Speed**: Medium (< 5s per test)
- **Coverage**: 70% target

### API Tests
- **Location**: `backend/tests/api/`
- **Purpose**: Test API contracts
- **Speed**: Medium
- **Coverage**: 100% of endpoints

### E2E Tests
- **Location**: `tests/e2e/`
- **Purpose**: Test user workflows
- **Speed**: Slow (10-30s per test)
- **Coverage**: Critical paths only

## Test Generation

Tests are generated from Possible Futures requirements:

```bash
# Generate tests for an idea
npm run generate:tests <idea_id>
```

This reads the idea's:
- System components → Unit/integration tests
- Goals → Validation tests
- Assumptions → Behavior tests
- Secrets → Security tests

## Append-Only Policy

Tests can only be added, not removed arbitrarily.

### To Remove a Test

1. **Predict** the test will fail:
   ```json
   // Add to tests/test-removals.json
   {
     "test_name": "test_old_feature",
     "predicted_reason": "Removing old feature",
     "predicted_error": "Expected 200, got 404",
     "created_by": "developer@example.com",
     "created_at": "2025-10-15T10:00:00Z"
   }
   ```

2. **Make the change** that causes failure

3. **Build fails** with predicted error

4. **CI validates** prediction matches actual error

5. **Test can be removed**

This ensures deliberate test removal with documented reasoning.

## Environment-Specific Tests

### Local
- Uses `.env.test` (mock credentials)
- SQLite in-memory database
- All external services mocked

### CI
- GitHub Actions
- Matrix testing (Node 18, 20)
- Security scans included

### Staging
- Real sandbox APIs
- Staging database
- Integration tests

### Production
- **Smoke tests only** (non-destructive)
- Health checks
- Read-only validation

## Coverage

```bash
# Generate coverage report
npm run test:coverage

# View HTML report
open coverage/index.html
```

Target: 80% coverage

## Writing Tests

### Unit Test Template

```typescript
import { describe, it, expect } from 'vitest';
import { functionToTest } from '../src/module';

describe('functionToTest', () => {
  it('should do expected thing', () => {
    const result = functionToTest(input);
    expect(result).toBe(expected);
  });
  
  it('should handle edge case', () => {
    expect(() => functionToTest(invalid)).toThrow();
  });
});
```

### E2E Test Template

```typescript
import { test, expect } from '@playwright/test';

test('user can complete workflow', async ({ page }) => {
  await page.goto('/');
  await page.click('button[data-testid="start"]');
  await expect(page).toHaveURL(/\/workflow/);
});
```

## Continuous Improvement

- Tests are living documentation
- Update tests when requirements change
- Generate new tests for new features
- Monitor test duration and flakiness
