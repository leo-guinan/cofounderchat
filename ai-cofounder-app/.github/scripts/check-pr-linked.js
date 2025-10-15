#!/usr/bin/env node
/**
 * Check if PR is linked to an issue or requirement
 * 
 * PRs should reference:
 * - GitHub issue (#123)
 * - Requirement ID (REQ-123)
 * - Idea ID from Possible Futures
 */

const fs = require('fs');
const { execSync } = require('child_process');

const prBody = process.env.PR_BODY || '';
const prTitle = process.env.PR_TITLE || '';

const checks = {
  hasIssueReference: /(?:#|GH-)\d+/.test(prBody + prTitle),
  hasRequirementId: /REQ-[A-Z0-9]+/.test(prBody + prTitle),
  hasIdeaId: /[a-f0-9]{16}/.test(prBody + prTitle),
};

console.log('PR Linkage Check:');
console.log('  Issue reference:', checks.hasIssueReference ? '✓' : '✗');
console.log('  Requirement ID:', checks.hasRequirementId ? '✓' : '✗');
console.log('  Idea ID:', checks.hasIdeaId ? '✓' : '✗');

if (!checks.hasIssueReference && !checks.hasRequirementId && !checks.hasIdeaId) {
  console.error('\n❌ PR must be linked to an issue, requirement, or idea');
  console.error('Add one of:');
  console.error('  - Issue: #123 or GH-123');
  console.error('  - Requirement: REQ-ABC123');
  console.error('  - Idea ID: abc123def456 (from Possible Futures)');
  process.exit(1);
}

console.log('\n✓ PR is properly linked');
