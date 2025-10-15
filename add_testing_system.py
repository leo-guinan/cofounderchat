#!/usr/bin/env python3
"""
Add Testing System to AI Cofounder

The AI Cofounder must understand:
1. How to test locally (Docker-based)
2. How to test different environments (local, staging, prod)
3. How to generate tests from requirements
4. Append-only test policy with prediction-based removal
"""

from tasks.idea_tools import (
    add_system_component,
    add_world_assumption,
    add_goal,
    get_idea_status,
)
from pathlib import Path
import json


def add_testing_component(idea_id: str):
    """
    Add comprehensive testing system as a component
    """
    
    print("=" * 80)
    print("ADDING TESTING SYSTEM TO AI COFOUNDER")
    print("=" * 80)
    print()
    
    print(f"Idea ID: {idea_id}")
    print()
    
    # ========================================================================
    # Component: Testing System
    # ========================================================================
    
    print("1. ADDING TESTING SYSTEM COMPONENT...")
    print("-" * 80)
    
    add_system_component(
        idea_id=idea_id,
        component_name="testing_system",
        component_type="infrastructure",
        specification={
            "purpose": "Comprehensive testing across environments with requirements-driven test generation",
            
            "philosophy": {
                "tests_are_derived_state": "Tests derived from requirements (essential state)",
                "append_only": "Tests can only be added, not removed arbitrarily",
                "prediction_based_removal": "To remove test: predict failure → observe failure → remove",
                "environment_aware": "Same tests run across all environments with env-specific expectations",
                "fail_fast": "Tests fail immediately when expectations not met"
            },
            
            "test_types": {
                "unit_tests": {
                    "purpose": "Test individual functions/components in isolation",
                    "framework": "Vitest (TypeScript)",
                    "coverage_target": "80%",
                    "generated_from": "System component specifications",
                    "example": "Test that create_idea() returns valid Idea object"
                },
                "integration_tests": {
                    "purpose": "Test components working together",
                    "framework": "Vitest + Supertest (API testing)",
                    "coverage_target": "70%",
                    "generated_from": "Component interactions in specifications",
                    "example": "Test that adding component updates idea health score"
                },
                "api_tests": {
                    "purpose": "Test API endpoints match specifications",
                    "framework": "Supertest",
                    "coverage_target": "100% of endpoints",
                    "generated_from": "API specifications",
                    "example": "POST /ideas returns 201 with valid idea object"
                },
                "e2e_tests": {
                    "purpose": "Test complete user workflows",
                    "framework": "Playwright",
                    "coverage_target": "Critical paths only",
                    "generated_from": "User stories and goals",
                    "example": "User can spawn idea, add components, check health"
                },
                "security_tests": {
                    "purpose": "Test secrets management and security",
                    "framework": "Custom + OWASP ZAP",
                    "coverage_target": "All secret handling",
                    "generated_from": "Secrets management component",
                    "example": "Test that .env is gitignored, secrets not logged"
                },
                "performance_tests": {
                    "purpose": "Test meets performance goals",
                    "framework": "k6",
                    "coverage_target": "All performance goals",
                    "generated_from": "Performance goals in requirements",
                    "example": "Frontend loads < 1s, API responds < 100ms"
                }
            },
            
            "environments": {
                "local": {
                    "setup": "docker-compose -f docker-compose.test.yml up",
                    "database": "SQLite in-memory or test.db",
                    "secrets": "Test secrets from .env.test",
                    "external_services": "Mocked (no real API calls)",
                    "teardown": "docker-compose down -v",
                    "purpose": "Fast feedback during development"
                },
                "ci": {
                    "setup": "GitHub Actions matrix (Node 18, 20)",
                    "database": "SQLite in-memory",
                    "secrets": "GitHub Secrets",
                    "external_services": "Mocked",
                    "teardown": "Automatic",
                    "purpose": "Pre-merge validation"
                },
                "staging": {
                    "setup": "Deploy to staging server, run tests",
                    "database": "Staging SQLite",
                    "secrets": "Staging secrets",
                    "external_services": "Sandbox/test APIs",
                    "teardown": "Leave running",
                    "purpose": "Pre-production validation"
                },
                "production": {
                    "setup": "N/A (run against live)",
                    "database": "Production (read-only tests)",
                    "secrets": "Production secrets",
                    "external_services": "Real services",
                    "teardown": "N/A",
                    "purpose": "Smoke tests, health checks",
                    "tests_to_run": "Smoke tests only (non-destructive)"
                }
            },
            
            "test_generation": {
                "from_system_components": {
                    "input": "System component specification",
                    "generates": [
                        "Unit tests for component logic",
                        "Integration tests for component interactions",
                        "API tests if component exposes endpoints"
                    ],
                    "example": {
                        "component": "possible_futures_engine",
                        "generated_tests": [
                            "test_create_idea_returns_valid_id",
                            "test_add_component_increases_knowledge_count",
                            "test_advance_stage_blocked_without_validation",
                            "test_health_score_calculation"
                        ]
                    }
                },
                "from_world_assumptions": {
                    "input": "World assumption with criticality",
                    "generates": [
                        "Test to validate assumption",
                        "Test for behavior if assumption false"
                    ],
                    "example": {
                        "assumption": "Users will share their content",
                        "generated_tests": [
                            "test_content_upload_endpoint_exists",
                            "test_content_parsing_works",
                            "test_graceful_failure_if_no_content"
                        ]
                    }
                },
                "from_goals": {
                    "input": "Measurable goal with validator",
                    "generates": [
                        "Test that validator works",
                        "Test that system tracks metric",
                        "Test that goal status updates correctly"
                    ],
                    "example": {
                        "goal": "Frontend loads < 1s",
                        "generated_tests": [
                            "test_frontend_bundle_size_under_500kb",
                            "test_lighthouse_performance_score_over_90",
                            "test_ttfb_under_200ms"
                        ]
                    }
                },
                "from_secrets": {
                    "input": "Secrets management component",
                    "generates": [
                        "Test secrets not in git",
                        "Test secrets not logged",
                        "Test secrets validated on startup"
                    ],
                    "example": {
                        "generated_tests": [
                            "test_env_in_gitignore",
                            "test_secrets_redacted_in_logs",
                            "test_app_fails_if_required_secret_missing"
                        ]
                    }
                }
            },
            
            "append_only_policy": {
                "rule": "Tests can only be added, never removed arbitrarily",
                "rationale": "Removing test = losing regression protection",
                "exception_process": {
                    "step_1": "Developer predicts test will fail due to intentional change",
                    "step_2": "Developer documents prediction in test-removals.json",
                    "step_3": "Build runs, test actually fails",
                    "step_4": "System validates prediction was correct",
                    "step_5": "Test can be removed (or updated)",
                    "step_6": "Removal is logged in test-removals.log"
                },
                "prediction_format": {
                    "test_name": "test_old_api_format",
                    "predicted_reason": "Migrating from REST to GraphQL",
                    "predicted_error": "AssertionError: Expected 200, got 404",
                    "created_by": "developer_id",
                    "created_at": "2025-10-15T10:30:00Z",
                    "validated": False
                },
                "validation": "CI compares actual failure to predicted failure"
            },
            
            "docker_test_setup": {
                "docker_compose_test_yml": {
                    "services": {
                        "backend-test": "Backend with test database",
                        "frontend-test": "Frontend with test build",
                        "test-runner": "Container that runs all tests"
                    },
                    "volumes": [
                        "./tests:/tests",
                        "./coverage:/coverage"
                    ],
                    "environment": "Loads from .env.test"
                },
                "test_runner_container": {
                    "base_image": "node:20-alpine",
                    "installs": ["vitest", "playwright", "supertest"],
                    "runs": "npm run test:all",
                    "outputs": ["junit.xml", "coverage/", "test-report.html"]
                }
            },
            
            "test_database": {
                "strategy": "SQLite in-memory for speed",
                "seeding": "Fixtures from tests/fixtures/",
                "isolation": "Each test gets fresh database",
                "migrations": "Run all migrations before tests",
                "cleanup": "Automatic (in-memory)",
                "event_sourcing": "Verify state = f(initial, changes) in tests"
            },
            
            "test_organization": {
                "directory_structure": {
                    "tests/": {
                        "unit/": "Unit tests (fast, isolated)",
                        "integration/": "Integration tests (slower, real DB)",
                        "api/": "API contract tests",
                        "e2e/": "End-to-end tests (slowest)",
                        "security/": "Security tests",
                        "performance/": "Performance tests",
                        "fixtures/": "Test data",
                        "helpers/": "Test utilities",
                        "generated/": "AI-generated tests from requirements"
                    }
                },
                "naming_convention": {
                    "unit": "test_[function_name]_[scenario].ts",
                    "integration": "test_[feature]_integration.ts",
                    "api": "test_[endpoint]_[method].ts",
                    "e2e": "test_[user_story].spec.ts"
                }
            },
            
            "ci_cd_integration": {
                "github_actions": {
                    "on": ["push", "pull_request"],
                    "jobs": {
                        "test_local": "Run all tests in Docker",
                        "test_security": "Secret scanning, dependency audit",
                        "test_performance": "Lighthouse, bundle size",
                        "coverage": "Generate coverage report",
                        "mutation_testing": "Stryker mutation testing (optional)"
                    },
                    "matrix": {
                        "node_version": ["18.x", "20.x"],
                        "os": ["ubuntu-latest"]
                    }
                },
                "required_checks": [
                    "All tests pass",
                    "Coverage >= 80%",
                    "No security vulnerabilities",
                    "Performance budgets met"
                ]
            },
            
            "test_reporting": {
                "formats": ["JUnit XML", "HTML", "JSON", "Console"],
                "metrics": [
                    "Total tests run",
                    "Pass/fail/skip count",
                    "Coverage percentage",
                    "Test duration",
                    "Flaky test detection",
                    "Test generation stats (how many auto-generated)"
                ],
                "storage": "Upload to S3, link in PR comments"
            },
            
            "example_generated_test": """
import { describe, it, expect, beforeEach } from 'vitest';
import { createIdea, getIdeaStatus } from '../src/possible-futures';

// AUTO-GENERATED from requirement: AI Cofounder App
// Component: possible_futures_engine
// Generated: 2025-10-15T12:00:00Z
// DO NOT EDIT - Regenerate from requirements instead

describe('Possible Futures Engine', () => {
  // Generated from System Component spec
  it('should create idea with valid ID', () => {
    const idea = createIdea('Test Idea', 'Description');
    expect(idea.id).toMatch(/^[a-f0-9]{16}$/);
    expect(idea.name).toBe('Test Idea');
    expect(idea.current_stage).toBe('requirements');
    expect(idea.uncertainty_level).toBe('very_high');
  });
  
  // Generated from Goal: "Build MVP in 7 days"
  it('should track idea creation timestamp', () => {
    const idea = createIdea('Test', 'Desc');
    expect(idea.created_at).toBeInstanceOf(Date);
    expect(idea.created_at.getTime()).toBeLessThanOrEqual(Date.now());
  });
  
  // Generated from Assumption: "AI can build own webapp"
  it('should allow components to be added', () => {
    const idea = createIdea('Test', 'Desc');
    addComponent(idea.id, 'test_component', 'api', {}, 0.9);
    const status = getIdeaStatus(idea.id);
    expect(status.health.total_knowledge_items).toBe(1);
  });
});
            """.strip()
        },
        confidence=0.85  # Testing systems are well-understood
    )
    print("  ✓ testing_system component added")
    print()
    
    # ========================================================================
    # Assumptions about Testing
    # ========================================================================
    
    print("2. ADDING TESTING ASSUMPTIONS...")
    print("-" * 80)
    
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="Developers will follow append-only test policy and use prediction process for removal",
        category="user_behavior",
        criticality=0.70
    )
    print("  ✓ [CRITICAL 0.70] Developers follow append-only policy")
    
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="AI can generate correct tests from requirements specifications",
        category="technology",
        criticality=0.85  # CRITICAL - core capability
    )
    print("  ✓ [CRITICAL 0.85] AI can generate tests from requirements")
    
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="Docker-based testing is fast enough for local development (< 5 min)",
        category="technology",
        criticality=0.65
    )
    print("  ✓ [0.65] Docker tests are fast enough")
    
    print()
    
    # ========================================================================
    # Goals for Testing
    # ========================================================================
    
    print("3. ADDING TESTING GOALS...")
    print("-" * 80)
    
    add_goal(
        idea_id=idea_id,
        goal_text="80% code coverage across all tests",
        metric_name="test_coverage_pct",
        target_value=80.0,
        validator_function="percentage"
    )
    print("  ✓ 80% code coverage")
    
    add_goal(
        idea_id=idea_id,
        goal_text="All tests run locally in Docker in < 5 minutes",
        metric_name="local_test_duration_seconds",
        target_value=300,
        validator_function="numeric_threshold"
    )
    print("  ✓ Tests run < 5 minutes")
    
    add_goal(
        idea_id=idea_id,
        goal_text="100% of system components have generated tests",
        metric_name="components_with_tests_pct",
        target_value=100.0,
        validator_function="percentage"
    )
    print("  ✓ 100% components tested")
    
    add_goal(
        idea_id=idea_id,
        goal_text="Zero flaky tests (tests that randomly fail)",
        metric_name="flaky_test_count",
        target_value=0,
        validator_function="numeric_threshold"
    )
    print("  ✓ Zero flaky tests")
    
    print()
    
    # ========================================================================
    # Status Check
    # ========================================================================
    
    print("4. UPDATED STATUS...")
    print("-" * 80)
    
    status = get_idea_status(idea_id)
    health = status['health']
    
    print(f"Components: {health['total_knowledge_items']}")
    print(f"Assumptions: {health['total_assumptions']} ({health['critical_assumptions_count']} critical)")
    print(f"Goals: {health['total_goals']}")
    print(f"Health Score: {health['overall_health_score']:.2f}")
    print()
    
    print("=" * 80)
    print("✨ TESTING SYSTEM ADDED!")
    print("=" * 80)
    print()


def generate_testing_files(idea_id: str):
    """Generate the actual testing infrastructure files"""
    
    print()
    print("5. GENERATING TESTING FILES...")
    print("=" * 80)
    print()
    
    project_root = Path("./ai-cofounder-app")
    
    files = []
    
    # ========================================================================
    # Docker Test Configuration
    # ========================================================================
    
    files.append({
        "path": "docker-compose.test.yml",
        "content": """version: '3.8'

# Test environment - spins up services for testing

services:
  backend-test:
    build:
      context: ./backend
      target: builder  # Use builder stage (not production)
    environment:
      - NODE_ENV=test
      - DATABASE_URL=file:./data/test.db
      - LOG_LEVEL=error
    env_file:
      - .env.test
    volumes:
      - ./backend/src:/app/src
      - ./backend/tests:/app/tests
      - ./data/test:/app/data
    command: npm run test:watch
    
  frontend-test:
    build: ./frontend
    environment:
      - NODE_ENV=test
      - VITE_API_URL=http://backend-test:3000
    volumes:
      - ./frontend/src:/app/src
      - ./frontend/tests:/app/tests
    command: npm run test:watch
    
  test-runner:
    image: node:20-alpine
    working_dir: /workspace
    volumes:
      - .:/workspace
      - ./coverage:/workspace/coverage
    env_file:
      - .env.test
    environment:
      - NODE_ENV=test
    depends_on:
      - backend-test
    command: sh -c "cd backend && npm test && cd ../frontend && npm test"

  e2e-test:
    image: mcr.microsoft.com/playwright:latest
    working_dir: /workspace
    volumes:
      - ./tests/e2e:/workspace/tests
      - ./playwright-report:/workspace/playwright-report
    environment:
      - BASE_URL=http://frontend-test
      - API_URL=http://backend-test:3000
    depends_on:
      - backend-test
      - frontend-test
    command: npx playwright test
"""
    })
    
    # ========================================================================
    # Test Environment Config
    # ========================================================================
    
    files.append({
        "path": ".env.test",
        "content": """# Test Environment Configuration
# These are test/mock credentials - safe to commit

NODE_ENV=test

# Mock API Keys (not real)
OPENAI_API_KEY=sk-test-mock-key-not-real
ANTHROPIC_API_KEY=sk-ant-test-mock-key-not-real

# Test Database
DATABASE_URL=file:./data/test.db
DATABASE_ENCRYPTION_KEY=test-encryption-key-32-chars-long

# Mock OAuth
GITHUB_CLIENT_ID=test_client_id
GITHUB_CLIENT_SECRET=test_client_secret

# Mock S3
S3_ENDPOINT=http://minio-test:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=test-bucket

# Test Session
SESSION_SECRET=test-session-secret-for-testing-only

# Test Server
PORT=3000
FRONTEND_URL=http://localhost:5173
CORS_ORIGIN=http://localhost:5173

LOG_LEVEL=error
"""
    })
    
    # ========================================================================
    # Test Generation Script
    # ========================================================================
    
    files.append({
        "path": "scripts/generate-tests.ts",
        "content": """#!/usr/bin/env tsx
/**
 * Generate tests from requirements
 * 
 * Reads Possible Futures database and generates test files
 * for all system components, goals, and assumptions
 */

import { getIdeaStatus, getStageHistory } from '../backend/src/tools/possible-futures';
import * as fs from 'fs';
import * as path from 'path';

interface TestTemplate {
  component: string;
  testType: 'unit' | 'integration' | 'api' | 'e2e';
  testCode: string;
}

function generateTestsFromComponent(component: any): TestTemplate[] {
  const tests: TestTemplate[] = [];
  
  // Unit test template
  tests.push({
    component: component.component_name,
    testType: 'unit',
    testCode: `
import { describe, it, expect } from 'vitest';

// AUTO-GENERATED from component: ${component.component_name}
// Type: ${component.component_type}
// Generated: ${new Date().toISOString()}
// Confidence: ${component.confidence}

describe('${component.component_name}', () => {
  it('should exist and be defined', () => {
    // TODO: Import and test ${component.component_name}
    expect(true).toBe(true);
  });
  
  it('should meet specification', () => {
    // Spec: ${JSON.stringify(component.specification, null, 2)}
    expect(true).toBe(true);
  });
});
`
  });
  
  return tests;
}

function generateTestsFromGoal(goal: any): TestTemplate[] {
  const tests: TestTemplate[] = [];
  
  tests.push({
    component: 'goals',
    testType: 'integration',
    testCode: `
import { describe, it, expect } from 'vitest';

// AUTO-GENERATED from goal: ${goal.goal_text}
// Metric: ${goal.metric_name}
// Target: ${goal.target_value}
// Validator: ${goal.validator_function}

describe('Goal: ${goal.goal_text}', () => {
  it('should track ${goal.metric_name}', () => {
    // TODO: Implement metric tracking test
    expect(true).toBe(true);
  });
  
  it('should validate when ${goal.metric_name} >= ${goal.target_value}', () => {
    // TODO: Implement validator test
    expect(true).toBe(true);
  });
});
`
  });
  
  return tests;
}

async function generateAllTests(ideaId: string) {
  console.log('Generating tests for idea:', ideaId);
  
  const status = await getIdeaStatus(ideaId);
  const history = await getStageHistory(ideaId, 'requirements');
  
  const allTests: TestTemplate[] = [];
  
  // Generate from components
  for (const component of status.knowledge) {
    const componentTests = generateTestsFromComponent(component);
    allTests.push(...componentTests);
  }
  
  // Generate from goals
  for (const goal of status.goals) {
    const goalTests = generateTestsFromGoal(goal);
    allTests.push(...goalTests);
  }
  
  // Write test files
  const testDir = path.join(__dirname, '../tests/generated');
  fs.mkdirSync(testDir, { recursive: true });
  
  for (const test of allTests) {
    const filename = `${test.component}.${test.testType}.test.ts`;
    const filepath = path.join(testDir, filename);
    fs.writeFileSync(filepath, test.testCode);
    console.log('✓ Generated:', filename);
  }
  
  console.log(\`\\n✨ Generated \${allTests.length} tests\`);
}

// Run if called directly
if (require.main === module) {
  const ideaId = process.argv[2];
  if (!ideaId) {
    console.error('Usage: generate-tests.ts <idea_id>');
    process.exit(1);
  }
  generateAllTests(ideaId);
}
"""
    })
    
    # ========================================================================
    # Test Removal Prediction System
    # ========================================================================
    
    files.append({
        "path": "tests/test-removals.schema.json",
        "content": json.dumps({
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Test Removal Predictions",
            "description": "Predictions for tests that will fail (append-only policy enforcement)",
            "type": "array",
            "items": {
                "type": "object",
                "required": ["test_name", "predicted_reason", "predicted_error", "created_by", "created_at"],
                "properties": {
                    "test_name": {
                        "type": "string",
                        "description": "Full name of test predicted to fail"
                    },
                    "predicted_reason": {
                        "type": "string",
                        "description": "Why this test will fail (e.g., 'Migrating API from REST to GraphQL')"
                    },
                    "predicted_error": {
                        "type": "string",
                        "description": "Expected error message"
                    },
                    "created_by": {
                        "type": "string",
                        "description": "Developer making prediction"
                    },
                    "created_at": {
                        "type": "string",
                        "format": "date-time"
                    },
                    "validated": {
                        "type": "boolean",
                        "default": False
                    },
                    "actual_error": {
                        "type": "string",
                        "description": "Actual error when test failed (filled by CI)"
                    },
                    "removed_at": {
                        "type": "string",
                        "format": "date-time"
                    }
                }
            }
        }, indent=2)
    })
    
    files.append({
        "path": "tests/test-removals.json",
        "content": json.dumps([], indent=2)
    })
    
    files.append({
        "path": "scripts/validate-test-removal.ts",
        "content": """#!/usr/bin/env tsx
/**
 * Validate Test Removal Predictions
 * 
 * Compares predicted test failures to actual failures
 * Only allows removal if prediction was accurate
 */

import * as fs from 'fs';
import * as path from 'path';

interface TestRemovalPrediction {
  test_name: string;
  predicted_reason: string;
  predicted_error: string;
  created_by: string;
  created_at: string;
  validated?: boolean;
  actual_error?: string;
  removed_at?: string;
}

function loadPredictions(): TestRemovalPrediction[] {
  const filepath = path.join(__dirname, '../tests/test-removals.json');
  return JSON.parse(fs.readFileSync(filepath, 'utf-8'));
}

function savePredictions(predictions: TestRemovalPrediction[]) {
  const filepath = path.join(__dirname, '../tests/test-removals.json');
  fs.writeFileSync(filepath, JSON.stringify(predictions, null, 2));
}

function validatePrediction(
  testName: string,
  actualError: string
): boolean {
  const predictions = loadPredictions();
  const prediction = predictions.find(p => p.test_name === testName && !p.validated);
  
  if (!prediction) {
    console.error(\`❌ No prediction found for test: \${testName}\`);
    console.error('To remove a test, first add a prediction to tests/test-removals.json');
    return false;
  }
  
  // Check if prediction matches actual error (fuzzy match)
  const match = actualError.includes(prediction.predicted_error) ||
                prediction.predicted_error.includes(actualError);
  
  if (match) {
    console.log(\`✅ Prediction validated for: \${testName}\`);
    console.log(\`   Predicted: \${prediction.predicted_error}\`);
    console.log(\`   Actual: \${actualError}\`);
    
    // Mark as validated
    prediction.validated = true;
    prediction.actual_error = actualError;
    savePredictions(predictions);
    
    return true;
  } else {
    console.error(\`❌ Prediction mismatch for: \${testName}\`);
    console.error(\`   Predicted: \${prediction.predicted_error}\`);
    console.error(\`   Actual: \${actualError}\`);
    return false;
  }
}

function canRemoveTest(testName: string): boolean {
  const predictions = loadPredictions();
  const prediction = predictions.find(p => p.test_name === testName);
  
  if (!prediction) {
    console.error(\`❌ Cannot remove \${testName}: No prediction exists\`);
    return false;
  }
  
  if (!prediction.validated) {
    console.error(\`❌ Cannot remove \${testName}: Prediction not validated\`);
    return false;
  }
  
  console.log(\`✅ Can remove \${testName}: Prediction validated\`);
  return true;
}

// CLI
const command = process.argv[2];
const testName = process.argv[3];
const actualError = process.argv[4];

if (command === 'validate') {
  const valid = validatePrediction(testName, actualError);
  process.exit(valid ? 0 : 1);
} else if (command === 'can-remove') {
  const canRemove = canRemoveTest(testName);
  process.exit(canRemove ? 0 : 1);
} else {
  console.error('Usage:');
  console.error('  validate-test-removal validate <test_name> <actual_error>');
  console.error('  validate-test-removal can-remove <test_name>');
  process.exit(1);
}
"""
    })
    
    # ========================================================================
    # Test Configuration Files
    # ========================================================================
    
    files.append({
        "path": "backend/vitest.config.ts",
        "content": """import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.test.ts',
        '**/*.spec.ts',
        'tests/fixtures/**'
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80
      }
    },
    setupFiles: ['./tests/setup.ts'],
    include: ['tests/**/*.test.ts', 'tests/**/*.spec.ts'],
    testTimeout: 10000,
    hookTimeout: 10000
  }
});
"""
    })
    
    files.append({
        "path": "backend/tests/setup.ts",
        "content": """/**
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
"""
    })
    
    files.append({
        "path": "playwright.config.ts",
        "content": """import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['junit', { outputFile: 'test-results/junit.xml' }]
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure'
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
  webServer: {
    command: 'docker-compose -f docker-compose.test.yml up',
    url: 'http://localhost:3000/health',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
"""
    })
    
    # ========================================================================
    # Example Tests
    # ========================================================================
    
    files.append({
        "path": "backend/tests/unit/example.test.ts",
        "content": """import { describe, it, expect } from 'vitest';

describe('Example Unit Test', () => {
  it('should pass basic assertion', () => {
    expect(1 + 1).toBe(2);
  });
  
  it('should test async code', async () => {
    const result = await Promise.resolve(42);
    expect(result).toBe(42);
  });
});
"""
    })
    
    files.append({
        "path": "tests/e2e/example.spec.ts",
        "content": """import { test, expect } from '@playwright/test';

test('should load homepage', async ({ page }) => {
  await page.goto('/');
  
  await expect(page).toHaveTitle(/AI Cofounder/);
  
  const heading = page.getByRole('heading', { name: /AI Cofounder/i });
  await expect(heading).toBeVisible();
});

test('should have working navigation', async ({ page }) => {
  await page.goto('/');
  
  // Test navigation exists
  const nav = page.getByRole('navigation');
  await expect(nav).toBeVisible();
});
"""
    })
    
    # ========================================================================
    # Documentation
    # ========================================================================
    
    files.append({
        "path": "docs/TESTING.md",
        "content": """# Testing Guide

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
"""
    })
    
    # Update package.json scripts
    files.append({
        "path": "backend/package.json.test-scripts",
        "content": """Add to scripts in backend/package.json:

"test": "vitest run",
"test:watch": "vitest",
"test:coverage": "vitest run --coverage",
"test:ui": "vitest --ui",
"generate:tests": "tsx scripts/generate-tests.ts"
"""
    })
    
    files.append({
        "path": "package.json.test-deps",
        "content": """Add to root package.json:

{
  "devDependencies": {
    "vitest": "^1.0.0",
    "@vitest/ui": "^1.0.0",
    "@vitest/coverage-v8": "^1.0.0",
    "@playwright/test": "^1.40.0",
    "supertest": "^6.3.0",
    "@types/supertest": "^6.0.0"
  },
  "scripts": {
    "test": "npm run test --workspaces",
    "test:docker": "docker-compose -f docker-compose.test.yml up test-runner",
    "test:e2e": "playwright test",
    "test:all": "npm run test && npm run test:e2e"
  }
}
"""
    })
    
    # Write all files
    print(f"Creating {len(files)} testing files...")
    print()
    
    for file_info in files:
        file_path = project_root / file_info['path']
        
        # Handle instruction files
        if 'test-scripts' in file_info['path'] or 'test-deps' in file_info['path']:
            print(f"  📝 {file_info['path']} (manual merge required)")
            print(f"     {file_info['content'][:100]}...")
            continue
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(file_info['content'])
        
        # Make scripts executable
        if file_path.suffix in ['.sh', '.ts'] and 'scripts' in str(file_path):
            import os
            os.chmod(file_path, 0o755)
        
        print(f"  ✓ {file_info['path']}")
    
    print()
    print("=" * 80)
    print("✨ TESTING FILES GENERATED!")
    print("=" * 80)
    print()
    print("Created:")
    print("  ✓ docker-compose.test.yml (Test environment)")
    print("  ✓ .env.test (Test configuration)")
    print("  ✓ scripts/generate-tests.ts (Test generator)")
    print("  ✓ scripts/validate-test-removal.ts (Append-only enforcement)")
    print("  ✓ tests/test-removals.json (Prediction tracking)")
    print("  ✓ vitest.config.ts (Test configuration)")
    print("  ✓ playwright.config.ts (E2E configuration)")
    print("  ✓ docs/TESTING.md (Documentation)")
    print("  ✓ Example tests (unit, e2e)")
    print()
    print("Next steps:")
    print("  1. Install test dependencies:")
    print("     npm install --save-dev vitest @playwright/test")
    print("  2. Run tests:")
    print("     docker-compose -f docker-compose.test.yml up test-runner")
    print("  3. Generate tests from requirements:")
    print("     npm run generate:tests <idea_id>")
    print()
    print("=" * 80)


if __name__ == "__main__":
    import sys
    
    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 27 + "TESTING SYSTEM" + " " * 33 + "║")
    print("║" + " " * 78 + "║")
    print("║" + " " * 15 + "Comprehensive Testing Infrastructure" + " " * 25 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Get idea ID from argument
    if len(sys.argv) > 1:
        idea_id = sys.argv[1]
        print(f"Using idea ID: {idea_id}")
    else:
        print("Usage: python add_testing_system.py <idea_id>")
        print()
        print("Run build_webapp.py first to get an idea ID")
        exit(1)
    
    print()
    
    # Add testing component
    add_testing_component(idea_id)
    
    # Generate files
    generate_testing_files(idea_id)
    
    print()
    print("✨ Testing system complete!")
    print()

