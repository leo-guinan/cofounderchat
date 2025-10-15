# GitHub Integration

## Overview

The AI Cofounder uses GitHub for version control with automated code review and standards enforcement.

## Git Workflow

### Branch Strategy

```
main
├── develop
│   ├── feature/ai-generated-component
│   ├── feature/user-requested-feature
│   └── fix/bug-123
```

- **`main`**: Production-ready code
- **`develop`**: Integration branch
- **`feature/*`**: New features
- **`fix/*`**: Bug fixes
- **`docs/*`**: Documentation updates

### Commit Convention

```
type(scope): description

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Example**:
```
feat(possible-futures): add goal validation

- Implement numeric_threshold validator
- Add percentage validator
- Update tests

Closes #123
REQ-ABC456
```

## Pull Request Process

### 1. Create Branch

```bash
# AI Cofounder creates branch from requirement
git checkout -b feature/add-user-auth
```

### 2. Make Changes

```bash
# AI generates code
# Commits with descriptive messages
git commit -m "feat(auth): implement JWT authentication"
```

### 3. Pre-Commit Checks

Automatically run before commit:
- ✓ Prettier formatting
- ✓ ESLint
- ✓ TypeScript type check
- ✓ Unit tests
- ✓ No secrets in code

### 4. Push and Create PR

```bash
git push origin feature/add-user-auth
```

AI creates PR with:
- Description of changes
- Link to requirement/issue
- Test results
- Screenshots (if UI changes)

### 5. Automated Pre-Review

GitHub Actions run:
- ✓ All tests
- ✓ Coverage check (80% minimum)
- ✓ Security scan
- ✓ Dependency audit
- ✓ Bundle size check
- ✓ Complexity analysis

### 6. AI Code Review

AI Code Review Agent:
- Reviews code against requirements
- Checks code standards
- Identifies potential issues
- Posts review comments

### 7. Human Review (if needed)

Code owners notified for:
- Critical path changes
- Security changes
- Breaking changes

### 8. Merge

Once approved:
- Squash and merge to `develop`
- Delete feature branch
- Auto-deploy to staging

## Pre-Review Checks

### What Gets Checked

| Check | Tool | Blocks PR | Auto-Fix |
|-------|------|-----------|----------|
| **Formatting** | Prettier | Yes | Yes |
| **Linting** | ESLint | Yes | Partial |
| **Types** | TypeScript | Yes | No |
| **Tests** | Vitest | Yes | No |
| **Coverage** | Vitest | Yes | No |
| **Security** | Trufflehog | Yes | No |
| **Dependencies** | npm audit | Warning | No |
| **Complexity** | ESLint | Warning | No |
| **Bundle Size** | Custom | Warning | No |

### Running Locally

```bash
# Run all pre-commit checks
npm run pre-commit

# Individual checks
npm run format:check    # Prettier
npm run lint            # ESLint
npm run type-check      # TypeScript
npm run test            # Tests
npm run security:check  # Security scan
```

## AI Code Review Agent

### What It Reviews

1. **Requirements Compliance**
   - Does code meet Possible Futures requirements?
   - Are all specified components implemented?
   - Do goals pass validation?

2. **Code Standards**
   - Follows style guide?
   - Proper TypeScript types?
   - No `any` types?
   - Error handling present?

3. **Security**
   - No hardcoded secrets?
   - Input validation?
   - SQL injection protection?
   - XSS prevention?

4. **Best Practices**
   - DRY (Don't Repeat Yourself)?
   - SOLID principles?
   - Proper abstraction?
   - Performance concerns?

5. **Testing**
   - Unit tests added?
   - Integration tests if needed?
   - Test coverage maintained?

### Review Comments

The AI posts comments like:

```
🔒 **Security**: Potential secret hardcoded on line 42
Consider using environment variable instead:
  const apiKey = process.env.API_KEY;

📝 **Type Safety**: Avoid using `any` on line 15
Use specific type for better type safety:
  function processData(data: UserData): Result { ... }

⚠️ **Code Quality**: Function exceeds 50 lines
Consider breaking into smaller functions for better maintainability.
```

### Approval Criteria

AI approves if:
- ✓ All pre-review checks pass
- ✓ No security issues
- ✓ Meets requirements
- ✓ Follows code standards
- ✓ Has adequate tests

AI requests changes if:
- ❌ Security issues found
- ❌ Requirements not met
- ❌ Tests missing or failing
- ❌ Code quality issues

## Code Standards

### TypeScript

- Use explicit types (avoid `any`)
- Interfaces for data structures
- Enums for fixed sets
- Async/await over promises
- Error handling with try/catch

### Functions

- Max 50 lines
- Max complexity: 10
- Single responsibility
- Clear naming
- JSDoc comments for public APIs

### Files

- Max 300 lines per file
- One component per file
- Related code co-located
- Clear directory structure

### Testing

- One test file per source file
- AAA pattern (Arrange, Act, Assert)
- Descriptive test names
- 80% coverage minimum

## Bypassing Checks

### When Allowed

- Documentation-only changes
- Emergency hotfixes (with approval)
- Generated code (with validation)

### How to Bypass

```bash
# Skip pre-commit (use sparingly!)
git commit --no-verify -m "docs: update README"

# Note: CI checks still run
```

## Troubleshooting

### Pre-commit fails

```bash
# Fix formatting
npm run format

# Fix linting
npm run lint:fix

# Check what's failing
npm run pre-commit
```

### Coverage drops below 80%

```bash
# Generate coverage report
npm run test:coverage

# Identify uncovered code
open coverage/index.html

# Add tests for uncovered areas
```

### AI review comments

Review each comment:
- Address security issues immediately
- Fix code quality issues
- Respond with explanation if disagree
- Request human review if needed

## Configuration Files

- `.prettierrc.json` - Formatting rules
- `.eslintrc.json` - Linting rules
- `.github/workflows/` - CI/CD pipelines
- `.github/CODEOWNERS` - Review assignments
- `.github/pull_request_template.md` - PR template
