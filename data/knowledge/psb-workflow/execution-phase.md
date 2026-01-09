---
slug: execution-phase
title: Build/Execution Phase
category: psb-workflow
difficulty: intermediate
keywords: build execution implementation coding testing
commands: []
related: [psb-overview, setup-phase, scaling-phase]
---

# Build/Execution Phase

## Summary

The Build phase is where you implement the feature, guided by your plan and working within the structure created during setup. Write code, run tests, fix issues, and document as you go.

## Build Phase Goals

1. **Implement Features**: Write the actual code
2. **Pass Tests**: Make all tests pass
3. **Handle Errors**: Add error handling
4. **Refine Code**: Clean up and optimize
5. **Document**: Add comments and docs

## Build Workflow

### Step 1: Start with Tests (TDD)

```typescript
// tests/auth/service.test.ts
it('generates valid JWT token', async () => {
  const service = new AuthService();
  const payload = { userId: '123', email: 'user@example.com' };

  const token = await service.generateToken(payload);

  // Token should be non-empty string
  expect(token).toBeDefined();
  expect(typeof token).toBe('string');
  expect(token.length).toBeGreaterThan(0);

  // Should be valid JWT format (3 base64 parts)
  const parts = token.split('.');
  expect(parts).toHaveLength(3);
});

// Run test - should fail
npm test
// ✗ generates valid JWT token - Not implemented
```

### Step 2: Implement to Pass Test

```typescript
// src/auth/service.ts
import jwt from 'jsonwebtoken';

export class AuthService {
  private secret = process.env.JWT_SECRET!;

  async generateToken(payload: TokenPayload): Promise<string> {
    return jwt.sign(payload, this.secret, {
      expiresIn: '1h'
    });
  }
}

// Run test - should pass
npm test
// ✓ generates valid JWT token
```

### Step 3: Add More Tests

```typescript
it('verifies valid token', async () => {
  const service = new AuthService();
  const payload = { userId: '123', email: 'user@example.com' };

  const token = await service.generateToken(payload);
  const decoded = await service.verifyToken(token);

  expect(decoded.userId).toBe('123');
  expect(decoded.email).toBe('user@example.com');
});

it('rejects invalid token', async () => {
  const service = new AuthService();

  await expect(
    service.verifyToken('invalid.token.here')
  ).rejects.toThrow('Invalid token');
});

it('rejects expired token', async () => {
  const service = new AuthService();

  // Create token that expires immediately
  const token = jwt.sign(
    { userId: '123' },
    process.env.JWT_SECRET!,
    { expiresIn: '0s' }
  );

  await expect(
    service.verifyToken(token)
  ).rejects.toThrow('Token expired');
});
```

### Step 4: Implement Features

```typescript
async verifyToken(token: string): Promise<TokenPayload> {
  try {
    const decoded = jwt.verify(token, this.secret) as TokenPayload;
    return decoded;
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      throw new Error('Token expired');
    }
    throw new Error('Invalid token');
  }
}
```

### Step 5: Run All Tests

```bash
npm test

Auth Service
  ✓ generates valid JWT token (12ms)
  ✓ verifies valid token (8ms)
  ✓ rejects invalid token (5ms)
  ✓ rejects expired token (3ms)
  ✓ hashes password (245ms)
  ✓ compares passwords correctly (248ms)

Test Suites: 1 passed, 1 total
Tests:       6 passed, 6 total
```

### Step 6: Add Error Handling

```typescript
async generateToken(payload: TokenPayload): Promise<string> {
  if (!payload.userId || !payload.email) {
    throw new Error('Missing required fields');
  }

  if (!this.secret) {
    throw new Error('JWT_SECRET not configured');
  }

  try {
    return jwt.sign(payload, this.secret, {
      expiresIn: process.env.JWT_EXPIRES_IN || '1h'
    });
  } catch (error) {
    throw new Error(`Token generation failed: ${error.message}`);
  }
}
```

### Step 7: Integration

```typescript
// src/api/auth/routes.ts
import { Router } from 'express';
import { AuthService } from '../../auth/service';

const router = Router();
const authService = new AuthService();

router.post('/register', async (req, res) => {
  try {
    const { email, password, name } = req.body;

    // Validate input
    if (!email || !password) {
      return res.status(400).json({ error: 'Missing credentials' });
    }

    // Check if user exists
    const existing = await userService.findByEmail(email);
    if (existing) {
      return res.status(409).json({ error: 'User already exists' });
    }

    // Create user
    const user = await userService.create({ email, password, name });

    // Generate token
    const token = await authService.generateToken({
      userId: user.id,
      email: user.email
    });

    res.json({ token, user });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
```

### Step 8: Integration Tests

```typescript
// tests/auth/integration.test.ts
describe('Auth API', () => {
  it('registers new user', async () => {
    const response = await request(app)
      .post('/api/auth/register')
      .send({
        email: 'test@example.com',
        password: 'Password123!',
        name: 'Test User'
      });

    expect(response.status).toBe(200);
    expect(response.body.token).toBeDefined();
    expect(response.body.user.email).toBe('test@example.com');
  });

  it('rejects duplicate registration', async () => {
    // Register once
    await request(app)
      .post('/api/auth/register')
      .send({ email: 'test@example.com', password: 'pass' });

    // Try again
    const response = await request(app)
      .post('/api/auth/register')
      .send({ email: 'test@example.com', password: 'pass' });

    expect(response.status).toBe(409);
  });

  it('logs in existing user', async () => {
    // Register
    await request(app)
      .post('/api/auth/register')
      .send({ email: 'test@example.com', password: 'Password123!' });

    // Login
    const response = await request(app)
      .post('/api/auth/login')
      .send({ email: 'test@example.com', password: 'Password123!' });

    expect(response.status).toBe(200);
    expect(response.body.token).toBeDefined();
  });
});
```

## Build Strategies

### Red-Green-Refactor (TDD)

```
1. RED: Write failing test
2. GREEN: Write minimal code to pass
3. REFACTOR: Clean up and optimize

Repeat for each feature
```

### Bottom-Up Build

```
1. Utility functions (no dependencies)
2. Services (use utilities)
3. Middleware (use services)
4. Routes (use middleware)
5. Integration (wire everything)
```

### Feature-by-Feature

```
1. Complete Feature A (unit + integration)
2. Complete Feature B (unit + integration)
3. Complete Feature C (unit + integration)
4. System integration tests
```

### Layer-by-Layer

```
1. All data models
2. All services
3. All middleware
4. All routes
5. Integration tests
```

## Handling Test Failures

### Debug Process

```bash
# Test fails
npm test
# ✗ verifies valid token - Cannot read property 'userId'

# Add debug logging
console.log('Token:', token);
console.log('Decoded:', decoded);

# Run single test
npm test -- --grep "verifies valid token"

# Fix issue
# Re-run
npm test
# ✓ verifies valid token
```

### Common Issues

**Issue**: Async not awaited
```typescript
// Wrong
const result = service.generateToken(payload);
// result is Promise, not string

// Right
const result = await service.generateToken(payload);
```

**Issue**: Missing mocks
```typescript
// Mock external dependencies
jest.mock('../../database/users');
```

**Issue**: Test pollution
```typescript
// Clean up after each test
afterEach(async () => {
  await database.clean();
});
```

## Build Checklist

### Implementation
- [ ] All functions implemented
- [ ] Error handling added
- [ ] Edge cases covered
- [ ] Validation in place
- [ ] Logging added

### Testing
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Edge case tests passing
- [ ] Error case tests passing
- [ ] Coverage target met

### Code Quality
- [ ] No lint errors
- [ ] TypeScript compiles
- [ ] Code formatted
- [ ] No console.logs left
- [ ] No commented code

### Documentation
- [ ] Inline comments added
- [ ] Function docs written
- [ ] README updated
- [ ] API docs updated
- [ ] Examples added

## Build Time Guidelines

### Quick Build (30-60 min)
- Simple feature
- Few files
- Straightforward logic

### Standard Build (2-4 hours)
- Moderate complexity
- Multiple files
- Integration work

### Complex Build (1-2 days)
- Complex logic
- Many integrations
- Extensive testing

## Permission Modes for Build

### Normal Mode (Recommended)
```bash
# Confirm each operation
# Good for careful implementation
# Catch issues early
```

### Auto Mode (Advanced)
```bash
# For repetitive work
# When confident in approach
# Trusted, tested code
```

## Build Best Practices

### ✅ Do:
- Write tests first (TDD)
- Run tests frequently
- Commit working code often
- Handle errors properly
- Add logging for debugging
- Keep functions small
- Follow existing patterns

### ❌ Don't:
- Skip tests
- Ignore test failures
- Commit broken code
- Skip error handling
- Leave debug code
- Write giant functions
- Reinvent patterns

## Key Takeaway

Build phase is where you implement features using TDD: write test, make it pass, refactor. Run tests frequently, handle errors properly, and follow existing patterns. Keep commits small and working. Most project time (50-70%) should be in build phase after good planning.
