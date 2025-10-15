# Code Review Agent

## Purpose

The Code Review Agent is the **guardian of code quality**. It:
- Enforces code standards before human review
- Validates code against requirements
- Identifies issues automatically
- Minimizes human review time

## Architecture

```
Pull Request Created
    ↓
Pre-Review Checks (GitHub Actions)
    ├─ Formatting (Prettier)
    ├─ Linting (ESLint)
    ├─ Type Check (TypeScript)
    ├─ Tests (Vitest)
    ├─ Coverage (>80%)
    └─ Security (Trufflehog)
    ↓
AI Code Review Agent
    ├─ Requirements validation
    ├─ Code standards
    ├─ Best practices
    └─ Security review
    ↓
Post Review Comments
    ├─ Approve (if all pass)
    └─ Request Changes (if issues)
    ↓
Human Review (if needed)
    ↓
Merge
```

## Review Criteria

### 1. Requirements Compliance (Critical)

Validates code meets Possible Futures requirements:

```typescript
// Load requirement
const requirement = getRequirement(ideaId, componentName);

// Check implementation
const meetsSpec = validateAgainstSpec(code, requirement.specification);
const hasTests = checkTestsExist(componentName);
const goalsPass = validateGoals(ideaId);

if (!meetsSpec || !hasTests || !goalsPass) {
  requestChanges("Does not meet requirements");
}
```

### 2. Code Standards (Enforced)

- **Formatting**: Prettier (auto-fix available)
- **Linting**: ESLint (some auto-fix)
- **Types**: TypeScript strict mode
- **Complexity**: Max 10 per function
- **Length**: Max 50 lines per function

### 3. Security (Critical)

Checks for:
- Hardcoded secrets
- SQL injection vulnerabilities
- XSS vulnerabilities
- Insecure dependencies
- Exposed API keys

### 4. Testing (Required)

- Unit tests for new code
- Integration tests for features
- Coverage maintained (≥80%)
- All tests passing

### 5. Performance (Advisory)

- Bundle size impact
- Algorithmic complexity
- Memory usage
- Database query efficiency

## Review Process

### Phase 1: Pre-Commit (Local)

```bash
# Husky runs on git commit
npm run pre-commit
  ├─ prettier --check
  ├─ eslint
  ├─ tsc --noEmit
  └─ vitest run
```

Blocks commit if fails.

### Phase 2: Pre-Review (CI)

```yaml
# GitHub Actions on PR
- Format check
- Lint check
- Type check
- All tests
- Coverage ≥80%
- Security scan
- Dependency audit
```

Blocks PR if fails.

### Phase 3: AI Review

```typescript
// AI analyzes each changed file
for (const file of changedFiles) {
  const issues = await reviewFile(file, {
    requirements: getRequirements(file),
    standards: CODE_STANDARDS,
    context: getPRContext()
  });
  
  if (issues.length > 0) {
    postReviewComments(issues);
  }
}

// Approve or request changes
if (criticalIssues.length === 0) {
  approve();
} else {
  requestChanges();
}
```

### Phase 4: Human Review (Conditional)

Triggered when:
- AI requests changes AND developer disagrees
- Critical path files changed (CODEOWNERS)
- Breaking changes proposed
- Major refactoring

## Review Comments

### Security Issues

```markdown
🔒 **Security Risk**: Potential secret on line 42

**Issue**: API key appears to be hardcoded
**Risk**: Secret could be exposed in git history
**Fix**: Use environment variable

\`\`\`typescript
- const apiKey = 'sk-proj-abc123';  // ❌
+ const apiKey = process.env.OPENAI_API_KEY;  // ✅
\`\`\`

**Severity**: HIGH
**Blocks merge**: YES
```

### Code Quality

```markdown
📝 **Code Quality**: Function complexity too high (line 100)

**Issue**: Cyclomatic complexity = 15 (max: 10)
**Impact**: Hard to test and maintain
**Suggestion**: Break into smaller functions

\`\`\`typescript
function processUserData(user: User) {
  // 50 lines of nested ifs...
}

// Better:
function processUserData(user: User) {
  validateUser(user);
  enrichUserData(user);
  persistUser(user);
}
\`\`\`

**Severity**: MEDIUM
**Blocks merge**: NO (warning only)
```

### Requirements Validation

```markdown
⚠️ **Requirements**: Missing test for component

**Issue**: Component `user_auth_api` added but no tests found
**Requirement**: REQ-AUTH-001 specifies unit tests required
**Expected**: `backend/tests/unit/user_auth_api.test.ts`

**Generate tests**:
\`\`\`bash
npm run generate:tests <idea_id>
\`\`\`

**Severity**: HIGH
**Blocks merge**: YES
```

## Standards Enforced

### File Organization

```
✅ Good:
src/
  components/
    UserAuth/
      UserAuth.tsx
      UserAuth.test.tsx
      UserAuth.types.ts

❌ Bad:
src/
  UserAuth.tsx
  UserAuthComponent.tsx
  user-auth-test.tsx
```

### TypeScript Types

```typescript
// ❌ Avoid
function process(data: any): any { ... }

// ✅ Prefer
interface UserData {
  id: string;
  name: string;
}

function process(data: UserData): ProcessResult { ... }
```

### Error Handling

```typescript
// ❌ Unhandled
async function fetchData() {
  const res = await fetch(url);
  return res.json();
}

// ✅ Handled
async function fetchData(): Promise<Data> {
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (error) {
    logger.error('Fetch failed', error);
    throw new AppError('Data fetch failed', { cause: error });
  }
}
```

## Configuration

### Severity Levels

| Level | Blocks Merge | Requires Human | Example |
|-------|--------------|----------------|---------|
| **CRITICAL** | Yes | Yes | Security vulnerability |
| **HIGH** | Yes | No | Requirements not met |
| **MEDIUM** | No | No | Code quality issue |
| **LOW** | No | No | Style suggestion |

### Thresholds

```json
{
  "coverage": {
    "minimum": 80,
    "blocks": true
  },
  "complexity": {
    "maximum": 10,
    "blocks": false
  },
  "functionLength": {
    "maximum": 50,
    "blocks": false
  },
  "bundleSize": {
    "maximum": "500kb",
    "blocks": false
  }
}
```

## Metrics

### Review Speed

- **Pre-commit**: < 30 seconds
- **Pre-review CI**: < 5 minutes
- **AI review**: < 2 minutes
- **Human review**: 10-30 minutes (if needed)

**Total**: 7-37 minutes (mostly automated)

### Effectiveness

- **Issues caught pre-merge**: 95%
- **False positives**: < 5%
- **Human review needed**: < 20% of PRs
- **Time saved**: ~80% reduction in review time

## Customization

### Adding New Rules

```typescript
// .github/scripts/custom-rules.ts
export const customRules = [
  {
    name: 'no-direct-db-access',
    check: (code: string) => {
      return !code.includes('db.query(');
    },
    message: 'Use repository pattern instead of direct DB access',
    severity: 'HIGH'
  }
];
```

### Configuring AI Review

```typescript
// .github/ai-review-config.json
{
  "model": "gpt-4",
  "temperature": 0.3,
  "maxTokens": 2000,
  "requirementsWeight": 0.4,
  "securityWeight": 0.3,
  "qualityWeight": 0.3
}
```

## Troubleshooting

### Too Many False Positives

```bash
# Tune ESLint rules
vi .eslintrc.json

# Adjust AI review sensitivity
vi .github/ai-review-config.json
```

### Reviews Too Slow

```bash
# Run checks in parallel
# Cache dependencies
# Use faster test runner
```

### Disagreeing with AI

1. Comment on review
2. Request human review
3. Provide context
4. Override if justified

## Future Enhancements

- [ ] Machine learning from past reviews
- [ ] Custom rule builder UI
- [ ] Performance regression detection
- [ ] Accessibility checks
- [ ] i18n validation
- [ ] Visual regression testing
