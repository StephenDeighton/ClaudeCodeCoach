---
slug: setup-phase
title: Setup Phase Deep Dive
category: psb-workflow
difficulty: intermediate
keywords: setup infrastructure scaffold prepare structure
commands: []
related: [psb-overview, planning-phase, execution-phase]
---

# Setup Phase Deep Dive

## Summary

The Setup phase prepares your project infrastructure after planning. Create file structure, install dependencies, configure tools, and write test scaffolding before implementation.

## Setup Phase Goals

1. **Create Structure**: Files, directories, modules
2. **Install Dependencies**: Required packages and tools
3. **Configure Tools**: Settings, environment variables
4. **Write Test Scaffolding**: Test files and fixtures
5. **Verify Setup**: Ensure everything works

## When to Setup

### Setup Required:
- New files or directories needed
- Dependencies to install
- Configuration changes
- Test structure needed
- Database migrations
- New services or modules

### Skip Setup:
- Editing existing files only
- No new dependencies
- No structural changes
- Quick one-file modifications

## Setup Workflow

### Step 1: Create Directory Structure

```bash
# From approved plan
mkdir -p src/auth
mkdir -p src/auth/types
mkdir -p tests/auth

# Verify structure
tree src/auth
```

### Step 2: Install Dependencies

```bash
# Add required packages
npm install jsonwebtoken bcryptjs

# Add dev dependencies
npm install --save-dev @types/jsonwebtoken @types/bcryptjs

# Verify installation
npm list jsonwebtoken
```

### Step 3: Create Files

```bash
# Create empty files with comments
cat > src/auth/service.ts << 'EOF'
/**
 * Authentication Service
 * Handles JWT generation, validation, and password hashing
 */

// TODO: Implement auth service
EOF

cat > src/auth/middleware.ts << 'EOF'
/**
 * Auth Middleware
 * Protects routes by validating JWT tokens
 */

// TODO: Implement middleware
EOF
```

### Step 4: Configuration

```bash
# Add environment variables
cat >> .env.example << 'EOF'
JWT_SECRET=your-secret-key-here
JWT_EXPIRES_IN=1h
EOF

# Update .env
echo "JWT_SECRET=$(openssl rand -hex 32)" >> .env
echo "JWT_EXPIRES_IN=1h" >> .env
```

### Step 5: Test Scaffolding

```typescript
// tests/auth/service.test.ts
import { describe, it, expect } from 'vitest';

describe('AuthService', () => {
  describe('generateToken', () => {
    it('should generate valid JWT token', () => {
      // TODO: Implement test
      expect(true).toBe(true);
    });
  });

  describe('verifyToken', () => {
    it('should verify valid token', () => {
      // TODO: Implement test
    });

    it('should reject invalid token', () => {
      // TODO: Implement test
    });
  });

  describe('hashPassword', () => {
    it('should hash password', () => {
      // TODO: Implement test
    });
  });
});
```

### Step 6: Type Definitions

```typescript
// src/auth/types.ts
export interface AuthToken {
  token: string;
  expiresIn: string;
}

export interface TokenPayload {
  userId: string;
  email: string;
  iat?: number;
  exp?: number;
}

export interface AuthRequest extends Request {
  user?: TokenPayload;
}
```

### Step 7: Verify Setup

```bash
# Verify files created
ls -la src/auth/
ls -la tests/auth/

# Verify dependencies
npm list | grep -E "jwt|bcrypt"

# Verify tests run (should pass empty tests)
npm test tests/auth/

# Verify TypeScript compiles
npm run type-check
```

## Setup Patterns

### TDD Setup Pattern

```typescript
// Write tests first
// tests/auth/service.test.ts

describe('AuthService', () => {
  it('generates JWT tokens', async () => {
    const service = new AuthService();
    const token = await service.generateToken({ userId: '123' });

    expect(token).toBeDefined();
    expect(typeof token).toBe('string');
  });
});

// Then create empty implementation
// src/auth/service.ts

export class AuthService {
  async generateToken(payload: any): Promise<string> {
    throw new Error('Not implemented');
  }
}
```

### Configuration First

```bash
# Set up all config before code
1. Environment variables
2. TypeScript config updates
3. Database connection strings
4. API keys and secrets
5. Tool configurations

# Then write code that uses config
```

### Bottom-Up Setup

```
1. Types and interfaces (no dependencies)
2. Utilities and helpers (basic functions)
3. Services (business logic)
4. Middleware (request handling)
5. Routes (HTTP layer)
6. Integration (wire it together)
```

## Setup Checklist

### File Structure
- [ ] Directories created
- [ ] Source files created with headers
- [ ] Test files created
- [ ] Type definition files
- [ ] Export index files

### Dependencies
- [ ] Production dependencies installed
- [ ] Dev dependencies installed
- [ ] Dependencies verified
- [ ] package.json updated

### Configuration
- [ ] Environment variables added
- [ ] Config files updated
- [ ] Secrets generated
- [ ] Settings documented

### Tests
- [ ] Test files created
- [ ] Test structure defined
- [ ] Test fixtures prepared
- [ ] Tests run (even if empty)

### Integration
- [ ] Imports work
- [ ] Types compile
- [ ] Build succeeds
- [ ] Ready for implementation

## Common Setup Tasks

### Database Setup

```bash
# Create migration
npm run migrate:create add_auth_tables

# Write migration
cat > migrations/20240101_add_auth_tables.sql << 'EOF'
CREATE TABLE user_sessions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  token TEXT NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_sessions_token ON user_sessions(token);
CREATE INDEX idx_sessions_user ON user_sessions(user_id);
EOF

# Run migration
npm run migrate:up
```

### API Setup

```typescript
// src/api/auth/index.ts
import { Router } from 'express';

const router = Router();

// POST /auth/register
router.post('/register', (req, res) => {
  res.status(501).json({ error: 'Not implemented' });
});

// POST /auth/login
router.post('/login', (req, res) => {
  res.status(501).json({ error: 'Not implemented' });
});

export default router;
```

### Documentation Setup

```markdown
<!-- docs/authentication.md -->
# Authentication

## Overview
JWT-based authentication system.

## Endpoints

### POST /auth/register
TODO: Document

### POST /auth/login
TODO: Document

## Implementation
TODO: Add details after build phase
```

## Setup Time Guidelines

### Quick Setup (5-15 min)
- Few new files
- No dependencies
- Simple structure

### Standard Setup (15-45 min)
- Multiple files
- Some dependencies
- Configuration changes
- Test scaffolding

### Complex Setup (1-2 hours)
- Many files and modules
- Multiple dependencies
- Database changes
- Extensive configuration
- Complex test setup

## Setup vs Build

### Setup Creates Structure:
```
src/auth/
├── service.ts      ← Empty with types/stubs
├── middleware.ts   ← Empty with types/stubs
└── utils.ts        ← Empty with types/stubs

tests/auth/
└── service.test.ts ← TODO tests defined
```

### Build Adds Implementation:
```
src/auth/
├── service.ts      ← Fully implemented ✓
├── middleware.ts   ← Fully implemented ✓
└── utils.ts        ← Fully implemented ✓

tests/auth/
└── service.test.ts ← Tests passing ✓
```

## Transitioning to Build

```bash
# Setup complete
Claude: Setup phase complete ✓

Files created: 8
Dependencies installed: 2
Configuration updated: Yes
Tests scaffolded: Yes
All files compile: Yes

Ready for build phase.

# Proceed to implementation
User: Great, implement the feature

Claude: Starting build phase...
# Now fills in the implementation
```

## Setup Best Practices

### ✅ Do:
- Follow project conventions
- Create complete structure before coding
- Write failing tests first (TDD)
- Verify setup works (build, test)
- Document configuration
- Use consistent naming

### ❌ Don't:
- Mix setup and implementation
- Skip test scaffolding
- Forget configuration
- Ignore existing patterns
- Rush through setup
- Leave broken state

## Key Takeaway

Setup phase creates project infrastructure before implementation. Create files, install dependencies, configure tools, and write test scaffolding. Verify everything compiles and runs before moving to build phase. Good setup makes implementation smooth and fast.
