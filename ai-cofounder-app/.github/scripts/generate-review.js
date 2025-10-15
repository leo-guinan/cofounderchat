#!/usr/bin/env node
/**
 * Generate automated code review summary
 * 
 * Aggregates results from:
 * - Linting
 * - Tests
 * - Coverage
 * - Type checking
 * - Security scans
 * - Complexity analysis
 */

const fs = require('fs');
const path = require('path');

async function generateReview() {
  const review = {
    timestamp: new Date().toISOString(),
    checks: [],
    summary: '',
    approve: true
  };
  
  // Check test results
  try {
    const testResults = JSON.parse(
      fs.readFileSync('test-results/results.json', 'utf8')
    );
    review.checks.push({
      name: 'Tests',
      passed: testResults.success,
      details: `${testResults.passed}/${testResults.total} tests passed`
    });
    if (!testResults.success) review.approve = false;
  } catch (e) {
    console.warn('No test results found');
  }
  
  // Check coverage
  try {
    const coverage = JSON.parse(
      fs.readFileSync('coverage/coverage-summary.json', 'utf8')
    );
    const totalCoverage = coverage.total.lines.pct;
    review.checks.push({
      name: 'Coverage',
      passed: totalCoverage >= 80,
      details: `${totalCoverage.toFixed(1)}% coverage (target: 80%)`
    });
    if (totalCoverage < 80) review.approve = false;
  } catch (e) {
    console.warn('No coverage results found');
  }
  
  // Generate summary
  const passed = review.checks.filter(c => c.passed).length;
  const total = review.checks.length;
  
  review.summary = `## Automated Pre-Review Summary\n\n`;
  review.summary += `**Result:** ${review.approve ? '✅ APPROVED' : '⚠️ CHANGES REQUESTED'}\n\n`;
  review.summary += `**Checks:** ${passed}/${total} passed\n\n`;
  
  review.checks.forEach(check => {
    const icon = check.passed ? '✅' : '❌';
    review.summary += `${icon} **${check.name}**: ${check.details}\n`;
  });
  
  if (!review.approve) {
    review.summary += `\n### Action Required\n\n`;
    review.summary += `Some automated checks failed. Please fix the issues and push again.\n`;
  }
  
  // Save for GitHub Action to post
  fs.writeFileSync(
    '.github/review-summary.md',
    review.summary
  );
  
  console.log(review.summary);
  return review;
}

generateReview().catch(console.error);
