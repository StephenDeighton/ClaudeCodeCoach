---
title: CLAUDE.md Best Practices
category: best-practices
commands: []
keywords: CLAUDE.md best-practices optimization structure content
related_topics: [claude-md-basics, context-efficiency]
difficulty: intermediate
---

# CLAUDE.md Best Practices

## Summary

An effective CLAUDE.md file is concise, scannable, and focuses on what Claude needs to work effectively with your codebase. Learn what to include, what to skip, and how to structure it.

## The Golden Rules

1. **Keep it under 200 lines** - Longer = more context consumed
2. **Make it scannable** - Use headers, bullets, code blocks
3. **Focus on patterns** - Not exhaustive documentation
4. **Update regularly** - Outdated info is worse than no info

## Essential Sections

### Project Overview (Required)
```markdown
# Project Name

## Overview
2-3 sentence description of what this project does.

## Tech Stack
- Python 3.11 + FastAPI
- PostgreSQL database
- Redis for caching
```

**Why**: Gives Claude immediate context about your tools and approach.

### Project Structure (Required)
```markdown
## Project Structure
```
src/
  models/      # SQLAlchemy models
  api/         # API endpoints
  services/    # Business logic
  utils/       # Helper functions
tests/         # pytest tests
```
```

**Why**: Helps Claude navigate and place new code correctly.

### Code Standards (Highly Recommended)
```markdown
## Code Standards
- Style: PEP 8, enforced with black
- Testing: pytest, aim for >80% coverage
- Type hints required for public functions
- Docstrings: Google style
```

**Why**: Ensures consistent code style without having to specify each time.

### Development Workflow (Recommended)
```markdown
## Development Workflow
1. Create feature branch from main
2. Write code + tests
3. Run `pytest && black .` before committing
4. Create PR with description
```

**Why**: Claude can follow your git and testing practices automatically.

## Optional but Useful Sections

### File Conventions
```markdown
## File Conventions
- Models: `{entity}_model.py` (e.g., `user_model.py`)
- Services: `{entity}_service.py`
- Tests: `test_{module}.py`
```

### Architecture Patterns
```markdown
## Architecture
Three-tier: API → Service → Model

Services are singletons:
```python
def get_user_service():
    return UserService(get_db())
```
```

### Key Dependencies
```markdown
## Key Dependencies
- SQLAlchemy: ORM for database
- Pydantic: Request/response validation
- Celery: Background tasks
```

## What to Exclude

### ❌ Things Claude Already Knows
Don't explain Python basics, common frameworks, or general programming concepts.

**Bad**:
```markdown
## Python
Python is a high-level programming language...
```

**Good**:
```markdown
## Python Version
Using Python 3.11 for match statements and improved error messages
```

### ❌ API Documentation
Don't list every endpoint and parameter.

**Bad**:
```markdown
## API Endpoints
GET /users - Returns list of users
POST /users - Creates a new user
  Body: {name: string, email: string}
GET /users/:id - Returns single user
...
```

**Good**:
```markdown
## API
RESTful API in api/routes.py
See docs/api-reference.md for full spec
```

### ❌ Historical Context
Past decisions matter less than current state.

**Bad**:
```markdown
We used to use MySQL but switched to PostgreSQL in 2022 because...
```

**Good**:
```markdown
Database: PostgreSQL 15
```

### ❌ Tutorial Content
Claude doesn't need to learn your framework.

**Bad**:
```markdown
## FastAPI Introduction
FastAPI is a modern web framework...
```

**Skip entirely** - Claude knows FastAPI

## Structure Template

```markdown
# [Project Name]

## Overview
[1-2 sentences]

## Tech Stack
- [Key technologies]

## Project Structure
[Directory tree with brief descriptions]

## Code Standards
- Style: [linter/formatter]
- Testing: [framework and expectations]
- Documentation: [required docs]

## Development Workflow
[Your git/testing/deployment process]

## File Conventions
[Naming patterns]

## Architecture
[Key patterns or layers]

## Environment Setup
[Any non-standard setup steps]
```

## Real-World Example

```markdown
# TaskMaster API

## Overview
REST API for task management with user authentication and real-time notifications.

## Tech Stack
- Node.js 20 + Express
- PostgreSQL with Prisma ORM
- Redis for sessions
- Socket.io for real-time updates

## Project Structure
src/
  routes/      # Express route handlers
  services/    # Business logic
  models/      # Prisma schema
  middleware/  # Auth, validation, error handling
  websocket/   # Socket.io event handlers

## Code Standards
- Style: Airbnb + Prettier
- Testing: Jest, >80% coverage required
- All endpoints must have OpenAPI docs
- Use async/await, no callbacks

## Development Workflow
1. Branch from main: `feature/task-name`
2. Write code + tests
3. Run `npm test && npm run lint`
4. Open PR with ticket link

## File Conventions
- Routes: `{resource}.routes.js` (e.g., `tasks.routes.js`)
- Services: `{resource}.service.js`
- Tests: `{file}.test.js`

## Architecture
Layered: Route → Service → Database
- Routes handle HTTP, validation
- Services contain business logic
- Direct Prisma calls only in services

## Key Patterns
- All services throw AppError for errors
- Use ServiceResponse wrapper: {success, data, error}
- Middleware chain: auth → validate → rateLimit → route
```

## Maintenance

### Review Quarterly
- Remove outdated information
- Add new patterns that emerged
- Consolidate duplicate content

### Update on Major Changes
- New tech stack additions
- Architecture refactors
- Convention changes

### Keep Examples Current
If you include code examples, ensure they match your current codebase.

## Anti-Patterns

❌ **The Encyclopedia**: 1000+ lines covering everything
❌ **The Placeholder**: "TODO: Document this later"
❌ **The Time Capsule**: References to deleted code
❌ **The Copy-Paste**: Duplicates README.md verbatim

✅ **The Guide**: Concise, current, actionable

## Key Takeaway

CLAUDE.md is not comprehensive documentation - it's a quick reference guide for Claude to understand your project's patterns and conventions. Quality over quantity, patterns over procedures.
