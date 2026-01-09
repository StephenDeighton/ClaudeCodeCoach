---
slug: claude-md-guide
title: CLAUDE.md - Project Instructions
category: project-setup
difficulty: beginner
keywords: CLAUDE.md instructions project context onboarding
commands: []
related: [skills-overview, hooks-overview]
---

# CLAUDE.md - Project Instructions

## Summary

CLAUDE.md is a markdown file in your project root that provides persistent instructions and context to Claude Code. It's automatically loaded at session start and helps Claude understand your project's conventions, architecture, and workflow.

## Location

```bash
# Project root
your-project/
├── .claude/
│   └── config.json
├── CLAUDE.md          ← Project instructions
├── README.md
└── src/
```

## Basic Structure

```markdown
# Project Name

## Overview
Brief description of what this project does.

## Architecture
Key architectural patterns and decisions.

## Code Standards
- Language: Python 3.12+
- Style: PEP 8
- Testing: pytest
- Linting: ruff

## Common Tasks
How to run tests, build, deploy, etc.

## Important Context
Anything Claude should know when working on this project.
```

## What to Include

### 1. Project Overview

```markdown
## Project Overview
A Flet-based Mac app for health checking Claude Code projects.
Three-tier architecture: pages (UI) → services (logic) → database (SQLite).
```

### 2. Technology Stack

```markdown
## Technology Stack
- Python 3.12+
- Flet 0.28.3 for UI
- SQLite with FTS5 for search
- Git for version control
```

### 3. Code Conventions

```markdown
## Code Conventions
- All UI components use theme.py
- Services are singletons via get_* functions
- No business logic in page classes
- Type hints required
```

### 4. File Organization

```markdown
## File Organization
- `pages/`: UI components (class with build() method)
- `services/`: Business logic (singleton pattern)
- `database/`: Data layer
- `data/knowledge/`: Knowledge base topics
```

### 5. Common Commands

```markdown
## Common Commands
```bash
# Run app
python main.py

# Run tests
pytest

# Lint
ruff check .

# Format
ruff format .
```
\```
```

### 6. Workflow Preferences

```markdown
## Workflow
- Commit after each working feature
- Update status.md with dated entries
- Run tests before committing
- Keep commits atomic
```

### 7. Important Notes

```markdown
## Important Notes
- Never modify the database schema directly
- Always use theme components for consistency
- Health checks are in `detectors/` directory
- Knowledge base uses YAML frontmatter
```

## Real Examples

### Web Application

```markdown
# MyApp Web Application

## Overview
Full-stack web app with React frontend and Node.js backend.

## Architecture
- Frontend: React 18 + TypeScript
- Backend: Express.js + PostgreSQL
- API: RESTful, documented in `/docs/api.md`

## Code Standards
- TypeScript strict mode
- ESLint + Prettier
- Tests with Jest + React Testing Library

## Database
- Migrations in `migrations/`
- Run with `npm run migrate`
- Seeds in `seeds/`

## Environment
- `.env.example` shows required variables
- Use `.env.local` for local development
- Never commit `.env` files

## Deployment
- Staging: `npm run deploy:staging`
- Production: Requires manual approval
```

### Python Library

```markdown
# DataProcessor Library

## Overview
Python library for processing large datasets efficiently.

## Code Standards
- Python 3.11+
- Type hints everywhere
- Docstrings: Google style
- Tests: pytest with 80%+ coverage

## Architecture
- `core/`: Main processing logic
- `utils/`: Helper functions
- `models/`: Data models (Pydantic)

## Testing
```bash
# Run all tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific file
pytest tests/test_processor.py
```
\```

## Release Process
1. Update version in `__version__.py`
2. Update CHANGELOG.md
3. Create git tag
4. Build: `python -m build`
5. Publish: `twine upload dist/*`
```

## Tips for Effective CLAUDE.md

### ✅ Do:
- Keep it concise (1-2 pages max)
- Update when conventions change
- Include actual commands that work
- List gotchas and special cases
- Reference key files and their purposes

### ❌ Don't:
- Duplicate README content
- Include API documentation (link to it instead)
- Write a novel (Claude can explore code)
- Add personal notes (use comments instead)
- Include sensitive information

## Dynamic Content

CLAUDE.md supports environment variables:

```markdown
## Database
Connection: ${DATABASE_URL}
User: ${DB_USER}
```

## Multiple Profiles

For different contexts:

```bash
your-project/
├── CLAUDE.md              # Default
├── CLAUDE.backend.md      # Backend work
├── CLAUDE.frontend.md     # Frontend work
└── CLAUDE.devops.md       # DevOps tasks
```

Load specific profile:
```bash
claude --instructions CLAUDE.backend.md
```

## Integration with Other Files

CLAUDE.md works with:

- `.claude/config.json` - Technical settings
- `README.md` - User-facing documentation
- `CONTRIBUTING.md` - Contributor guidelines
- `.claudeignore` - Files to exclude

```markdown
## Related Documentation
- Architecture: See `docs/architecture.md`
- API: See `docs/api.md`
- Contributing: See `CONTRIBUTING.md`
```

## Updating CLAUDE.md

When project evolves:

```bash
# Review and update
claude "Review CLAUDE.md and suggest updates based on recent changes"

# Or manually edit
code CLAUDE.md
```

## Checking Claude's Understanding

```bash
# Ask Claude to summarize
claude "What are the key conventions for this project?"

# Should reference CLAUDE.md content
```

## Key Takeaway

CLAUDE.md is Claude's onboarding document for your project. Keep it concise, focused on conventions and workflow, and update it as your project evolves. Think of it as the "what I'd tell a new team member" document.
