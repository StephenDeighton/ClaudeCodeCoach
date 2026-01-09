---
slug: documentation-patterns
title: Documentation Best Practices
category: best-practices
difficulty: intermediate
keywords: documentation docs comments API guides
commands: ["/docs"]
related: [automated-docs]
---

# Documentation Best Practices

## Summary

Maintain documentation alongside code: inline comments for complex logic, function/class docs, API documentation, and guides. Use automation to keep docs synchronized with code.

## Documentation Layers

### 1. Inline Comments
```typescript
// For complex logic only
function calculateDiscount(user: User, items: Item[]): number {
  // Premium users get 20% on orders > $100
  // Regular users get 10% on orders > $50
  const threshold = user.isPremium ? 100 : 50;
  const discount = user.isPremium ? 0.20 : 0.10;
  
  const total = items.reduce((sum, item) => sum + item.price, 0);
  return total > threshold ? total * discount : 0;
}
```

### 2. Function Documentation
```typescript
/**
 * Calculates discount for user's order
 * 
 * @param user - The user making purchase
 * @param items - Items in cart
 * @returns Discount amount in dollars
 * 
 * @example
 * const discount = calculateDiscount(user, cartItems);
 */
```

### 3. API Documentation
```markdown
## POST /api/auth/login

Authenticates user and returns JWT token.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "token": "eyJhbGc...",
  "user": { "id": "123", "email": "user@example.com" }
}
```

**Errors:**
- 400: Invalid credentials
- 429: Too many attempts
\```
```

### 4. Guides
```markdown
# Authentication Guide

## Setup
1. Install dependencies
2. Configure JWT secret
3. Add middleware to routes

## Usage
See examples in /examples/auth
```

## What to Document

### ✅ Always Document
- Public APIs
- Complex algorithms
- Non-obvious decisions
- Workarounds
- Security considerations
- Performance implications

### ❌ Don't Document
- Obvious code
- Self-explanatory functions
- Temporary code
- Generated code

## Documentation Workflow

```bash
# 1. Write code with inline docs
class AuthService {
  /**
   * Generates JWT token
   * @param payload - User data to encode
   * @returns Signed JWT token
   */
  generateToken(payload: TokenPayload): string {
    return jwt.sign(payload, this.secret);
  }
}

# 2. Generate API docs
npm run docs:generate

# 3. Review and enhance
# Add examples, guides, tutorials

# 4. Commit with code
git add src/ docs/
git commit -m "feat(auth): add token generation with docs"
```

## Using /docs Skill

```bash
# Generate documentation
/docs

Claude:
1. Scans source files
2. Extracts JSDoc/docstrings
3. Generates API documentation
4. Updates README examples
5. Creates usage guides

Documentation updated:
- docs/api/auth.md
- docs/api/users.md
- README.md (examples updated)
```

## Auto-Generated Docs

```bash
# Setup auto-generation
npm install --save-dev typedoc

# Configure
"scripts": {
  "docs": "typedoc src/ --out docs/"
}

# Generate
npm run docs
```

## Documentation Standards

### Function Docs
```typescript
/**
 * Brief description
 * 
 * Detailed explanation if needed
 * 
 * @param name - Parameter description
 * @returns Return value description
 * @throws Error conditions
 * 
 * @example
 * // Usage example
 * const result = myFunction(arg);
 */
```

### Class Docs
```typescript
/**
 * Brief class description
 * 
 * Detailed explanation of purpose and usage
 * 
 * @example
 * const service = new MyService();
 * await service.doSomething();
 */
class MyService {
  // ...
}
```

## README Template

```markdown
# Project Name

Brief description

## Installation
...

## Usage
```bash
# Quick start
```
\```

## API Reference
See [API Documentation](docs/api/)

## Examples
See [Examples](examples/)

## Contributing
...

## License
...
```

## Key Takeaway

Document code as you write it: inline comments for complex logic, function docs for all public APIs, generate API documentation automatically, and maintain guides for common tasks. Use /docs skill to automate and synchronize documentation with code changes.
