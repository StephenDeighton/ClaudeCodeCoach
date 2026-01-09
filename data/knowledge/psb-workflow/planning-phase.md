---
slug: planning-phase
title: Planning Phase Deep Dive
category: psb-workflow
difficulty: intermediate
keywords: planning explore design architecture analysis
commands: []
related: [psb-overview, plan-mode, setup-phase]
---

# Planning Phase Deep Dive

## Summary

The Planning phase is where you explore the codebase, understand requirements, and design the optimal approach before writing code. Use Plan mode for read-only exploration and get user approval before proceeding.

## Planning Phase Goals

1. **Understand Requirements**: Clarify what needs to be built
2. **Explore Codebase**: Find existing patterns and dependencies
3. **Design Approach**: Determine best implementation strategy
4. **Identify Risks**: Spot potential problems early
5. **Create Plan**: Document step-by-step approach
6. **Get Approval**: User confirms plan before build

## When to Plan

### Always Plan For:
- New features with unclear approach
- Working in unfamiliar code
- Multiple implementation options
- Complex architectural changes
- Significant refactoring

### Can Skip Planning For:
- Trivial changes (typos, comments)
- Bug fixes in familiar code
- Well-defined, simple tasks
- Repetitive work following established pattern

## Planning in Plan Mode

### Enter Plan Mode

```bash
# Use Shift+Tab to cycle to Plan Mode
Shift+Tab → [Plan Mode]

# Or specify at startup
claude --permission-mode plan
```

### What Plan Mode Allows

✅ Read files
✅ Search code
✅ List directories
✅ View git history
✅ Analyze patterns

❌ Write files
❌ Edit code
❌ Run commands
❌ Modify anything

## Planning Workflow

### Step 1: Requirements Analysis

```bash
User: "Add user authentication with JWT"

Claude Questions:
- What type of authentication? (JWT, sessions, OAuth)
- Where to store tokens? (localStorage, cookies, memory)
- Token expiration? (15min access, 7day refresh)
- Protected routes? (Which endpoints need auth)
- User model? (Existing or new table)
```

**Output**: Clear requirements document

### Step 2: Codebase Exploration

```bash
# Find existing auth code
grep -r "auth" src/

# Check database schema
cat database/schema.sql

# Review API structure
tree src/api/

# Find similar implementations
grep -r "middleware" src/
```

**Output**: Understanding of existing code

### Step 3: Pattern Analysis

```bash
# How are other features structured?
ls src/features/

# What testing patterns exist?
cat tests/users/user.test.ts

# How is error handling done?
grep -r "try.*catch" src/

# What's the coding style?
cat .eslintrc.json
```

**Output**: Identified patterns to follow

### Step 4: Dependency Review

```bash
# What's already installed?
cat package.json

# Check for auth libraries
grep -E "jwt|auth|bcrypt" package.json

# Review existing dependencies
npm list
```

**Output**: Know what to add/reuse

### Step 5: Design Architecture

```
Based on exploration, design:

1. File Structure
   src/auth/
   ├── middleware.ts
   ├── service.ts
   ├── types.ts
   └── utils.ts

2. Data Flow
   Login → Validate → Generate JWT → Return Token
   Request → Check JWT → Decode → Allow/Deny

3. Dependencies
   - jsonwebtoken (new)
   - bcryptjs (existing)

4. Testing Strategy
   - Unit tests for service
   - Integration tests for endpoints
   - E2E tests for full flow
```

**Output**: Architectural design

### Step 6: Risk Identification

```
Potential Issues:
1. Token refresh logic complex
   → Start with access tokens only, add refresh later
2. Password hashing performance
   → Use bcrypt rounds: 10 (balance speed/security)
3. CORS for tokens
   → Add withCredentials: true to fetch calls
4. Testing authenticated endpoints
   → Create test helper for auth tokens
```

**Output**: Risk mitigation strategies

### Step 7: Implementation Plan

```markdown
## Implementation Plan

### Phase 1: Setup (15 min)
1. Install jsonwebtoken, @types/jsonwebtoken
2. Create auth directory structure
3. Set up test files
4. Add JWT_SECRET to .env

### Phase 2: Core Auth (1 hour)
1. Create auth service
   - generateToken()
   - verifyToken()
   - hashPassword()
   - comparePassword()
2. Write unit tests
3. Create auth middleware
4. Test middleware

### Phase 3: Endpoints (45 min)
1. POST /auth/register
   - Validate input
   - Hash password
   - Create user
   - Return token
2. POST /auth/login
   - Validate credentials
   - Generate token
   - Return token
3. GET /auth/me (protected)
   - Test auth middleware

### Phase 4: Integration (30 min)
1. Protect existing routes
2. Update API client
3. Integration tests
4. E2E tests

### Phase 5: Documentation (15 min)
1. Add inline comments
2. Update API docs
3. Create AUTHENTICATION.md

Total Estimate: 3 hours
```

**Output**: Detailed implementation roadmap

### Step 8: User Review

```bash
Claude: Here's my implementation plan:
[Shares plan above]

Key decisions:
- JWT for stateless auth
- bcrypt for password hashing
- Middleware pattern following existing code
- Test coverage for all auth flows

Questions:
1. Should I add refresh tokens now or later?
2. Token expiration: 1h or 24h?
3. Rate limiting on auth endpoints?

User: Plan looks good. 1h tokens, add rate limiting.

Claude: ✓ Plan approved, ready for setup phase
```

## Planning Techniques

### Code Tracing

```bash
# Find entry point
cat src/index.ts

# Trace request flow
# index.ts → router.ts → handler.ts → service.ts → db.ts

# Document the path
# Useful for knowing where to add auth
```

### Pattern Matching

```bash
# Find similar features
ls src/features/

# Study one as template
cat src/features/users/service.ts

# Copy pattern for auth
```

### Dependency Mapping

```
Draw dependency graph:

auth/service
  ├── depends on: database/users
  ├── depends on: utils/crypto
  └── used by: auth/middleware
                  └── used by: api/routes
```

### Test-First Planning

```markdown
## Tests to Write

1. Auth Service Tests
   - ✓ Generates valid JWT
   - ✓ Verifies valid JWT
   - ✓ Rejects invalid JWT
   - ✓ Rejects expired JWT
   - ✓ Hashes password correctly
   - ✓ Compares passwords correctly

2. Middleware Tests
   - ✓ Allows with valid token
   - ✓ Blocks without token
   - ✓ Blocks with invalid token
   - ✓ Adds user to request

3. Endpoint Tests
   - ✓ Register creates user
   - ✓ Register returns token
   - ✓ Login with valid creds
   - ✓ Login rejects invalid creds
   - ✓ Protected route works
```

## Planning Output Format

### Minimal Plan

```markdown
## Plan: Add User Auth

**Approach**: JWT tokens, bcrypt passwords

**Files**:
- NEW: src/auth/service.ts
- NEW: src/auth/middleware.ts
- MODIFY: src/api/routes.ts
- MODIFY: package.json

**Steps**:
1. Install jwt, bcrypt
2. Create auth service
3. Add middleware
4. Protect routes
5. Write tests

**Time**: ~2 hours
```

### Detailed Plan

```markdown
## Implementation Plan: User Authentication

### Requirements
- JWT-based authentication
- 1-hour token expiration
- Protected API routes
- Rate limiting on auth endpoints

### Architecture
[File structure diagram]
[Data flow diagram]
[Dependency graph]

### Implementation Steps
[Detailed step-by-step]

### Testing Strategy
[Test cases and coverage plan]

### Risks & Mitigations
[Identified issues and solutions]

### Timeline
- Setup: 15 min
- Core: 1 hour
- Endpoints: 45 min
- Integration: 30 min
- Docs: 15 min
Total: ~3 hours

### Questions for User
1. Token expiration preference?
2. Refresh tokens now or later?
```

## Planning Best Practices

### ✅ Do:
- Use Plan mode for read-only exploration
- Explore thoroughly before designing
- Follow existing codebase patterns
- Identify risks and edge cases
- Get user approval before building
- Create clear, actionable plan

### ❌ Don't:
- Start coding during planning
- Make assumptions without checking
- Ignore existing patterns
- Over-plan simple tasks
- Skip user approval
- Create vague plans

## Planning Time Guidelines

### Quick Planning (5-10 min)
- Small bug fix in familiar code
- Simple feature following known pattern
- Minor refactoring

### Standard Planning (15-30 min)
- New feature in familiar domain
- Moderate complexity
- Some unknowns to resolve

### Deep Planning (1-2 hours)
- Major new feature
- Unfamiliar codebase area
- Complex architectural decisions
- Multiple dependencies

## Transitioning to Setup

```bash
# Planning complete
Claude: Plan approved ✓

# Exit plan mode
Shift+Tab → Normal Mode

# Proceed to setup
Claude: Moving to setup phase...
# Now can create files, install packages
```

## Key Takeaway

Planning phase is about exploration and design before coding. Use Plan mode to read code, identify patterns, and create a detailed implementation plan. Spend 10-30% of total time planning to minimize rework. Always get user approval before proceeding to setup and build phases.
