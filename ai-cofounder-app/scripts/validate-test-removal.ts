#!/usr/bin/env tsx
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
