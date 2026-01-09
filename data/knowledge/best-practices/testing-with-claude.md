---
slug: testing-with-claude
title: Testing with Claude Code
category: best-practices
difficulty: intermediate
keywords: testing TDD test-driven development best practices
commands: ["/test"]
related: [psb-overview, execution-phase]
---

# Testing with Claude Code

## Summary

Use test-driven development (TDD) with Claude: write tests first, implement to pass tests, refactor. Claude excels at generating comprehensive test suites and fixing test failures.

## TDD Workflow

```
1. Write failing test
2. Run test (should fail)
3. Implement minimum code to pass
4. Run test (should pass)
5. Refactor
6. Repeat
```

## Test-First with Claude

```bash
User: "Add user authentication"

# Step 1: Write tests first
Claude: "Let me write tests first"

// tests/auth.test.ts
describe('AuthService', () => {
  it('generates JWT tokens', () => {
    const service = new AuthService();
    const token = service.generateToken({ userId: '123' });
    expect(token).toBeDefined();
  });
});

# Step 2: Run (should fail)
npm test
✗ generates JWT tokens - Not implemented

# Step 3: Implement
// src/auth/service.ts
class AuthService {
  generateToken(payload) {
    return jwt.sign(payload, secret);
  }
}

# Step 4: Run (should pass)
npm test
✓ generates JWT tokens
```

## Test Coverage Goals

```
Minimum: 70%
Good: 80%
Excellent: 90%+

Focus on:
- Critical paths (auth, payments)
- Business logic
- Edge cases
```

## Types of Tests

### Unit Tests
```typescript
// Test single function
it('validates email format', () => {
  expect(validateEmail('user@example.com')).toBe(true);
  expect(validateEmail('invalid')).toBe(false);
});
```

### Integration Tests
```typescript
// Test components together
it('registers user with valid data', async () => {
  const response = await request(app)
    .post('/auth/register')
    .send({ email: 'user@example.com', password: 'pass123' });
  
  expect(response.status).toBe(201);
  expect(response.body.token).toBeDefined();
});
```

### E2E Tests
```typescript
// Test full user flow
it('complete purchase flow', async () => {
  await login();
  await addToCart(productId);
  await checkout();
  expect(orderConfirmed()).toBe(true);
});
```

## Testing Patterns

### Arrange-Act-Assert
```typescript
it('creates user', () => {
  // Arrange
  const userData = { email: 'test@example.com' };
  
  // Act
  const user = createUser(userData);
  
  // Assert
  expect(user.email).toBe('test@example.com');
});
```

### Test Fixtures
```typescript
// Reusable test data
const fixtures = {
  validUser: { email: 'valid@example.com', password: 'pass123' },
  invalidUser: { email: 'invalid', password: '123' }
};
```

## Using /test Skill

```bash
# Run tests and analyze failures
/test

Running tests...
✓ 142 passed
✗ 3 failed

Analyzing failures:
1. auth.test.ts:42 - Token expired
   Fix: Increase token TTL in test

2. api.test.ts:18 - CORS error
   Fix: Add test origin to CORS whitelist

3. db.test.ts:55 - Connection timeout
   Fix: Increase test timeout

Apply fixes? (y/n)
```

## Test Best Practices

### ✅ Do
- Write tests before code
- Test edge cases
- Use descriptive test names
- Keep tests independent
- Mock external dependencies
- Clean up test data

### ❌ Don't
- Skip tests
- Write tests after (only)
- Test implementation details
- Create test dependencies
- Leave failing tests
- Ignore flaky tests

## Test Organization

```
tests/
├── unit/
│   ├── auth.test.ts
│   └── api.test.ts
├── integration/
│   ├── auth-flow.test.ts
│   └── api-endpoints.test.ts
└── e2e/
    └── user-journey.test.ts
```

## Test Maintenance

```bash
# After code changes
npm test

# Fix failures immediately
# Don't accumulate technical debt

# Update tests when requirements change
```

## Key Takeaway

Write tests first with TDD approach. Claude generates comprehensive test suites and fixes failures. Aim for 80%+ coverage on critical paths. Use /test skill to run and analyze failures. Tests are safety net for confident refactoring.
