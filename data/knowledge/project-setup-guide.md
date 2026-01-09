---
title: Project Setup Guide
category: project-setup
commands: []
keywords: setup initialization new-project getting-started configuration
related_topics: [claude-md-basics, gitignore-setup]
difficulty: beginner
---

# Project Setup Guide

## Summary

Setting up a Claude Code project correctly from the start ensures smooth collaboration with Claude. This guide walks through creating a well-structured project foundation.

## Quick Start (5 minutes)

1. **Create Project Directory**
```bash
mkdir my-project && cd my-project
git init
```

2. **Create CLAUDE.md**
```bash
touch CLAUDE.md
```

Add minimal content:
```markdown
# My Project

## Overview
[What this project does]

## Tech Stack
- [Language/Framework]
- [Key dependencies]

## Project Structure
[How files are organized]
```

3. **Configure .gitignore**
```bash
touch .gitignore
```

Essential patterns:
```gitignore
.claude/cache/
.claude/*.local.json
.DS_Store
node_modules/
venv/
```

4. **Create .claude Directory** (optional but recommended)
```bash
mkdir .claude
```

5. **Start Coding**
```bash
claude
```

## Detailed Setup

### Directory Structure

Recommended layout:
```
my-project/
├── .claude/                 # Claude Code configuration
│   ├── config.json         # Project settings
│   ├── skills/             # Custom skills
│   └── settings.local.json # Local overrides (ignored)
├── CLAUDE.md               # Project documentation
├── .gitignore             # Git ignore patterns
├── README.md              # Public documentation
└── src/                   # Your code
```

### CLAUDE.md Template

Complete starter template:

```markdown
# [Project Name]

## Overview
One-paragraph description of what this project does and why it exists.

## Tech Stack
- Language: [Python/JavaScript/etc]
- Framework: [Django/React/etc]
- Database: [PostgreSQL/MongoDB/etc]
- Key Libraries: [list 3-5 most important]

## Project Structure
```
src/
  core/       # Core business logic
  api/        # API endpoints
  models/     # Data models
tests/        # Test files
```

## Development Workflow
1. Create feature branch
2. Write code + tests
3. Run test suite
4. Create PR

## Code Standards
- Style: [PEP 8/Airbnb/etc]
- Testing: [pytest/jest/etc]
- Documentation: Docstrings for all public functions

## Conventions
- File naming: snake_case
- Class naming: PascalCase
- Function naming: snake_case
```

### Claude Config (Optional)

Create `.claude/config.json`:

```json
{
  "model": "sonnet",
  "shell": "bash",
  "features": {
    "autoSave": true
  }
}
```

### Skills Directory (Optional)

Create `.claude/skills/` for custom commands:

```bash
mkdir -p .claude/skills
```

Example skill (`.claude/skills/test.md`):
```markdown
---
description: Run test suite and report results
---

Run the full test suite and provide a summary of:
- Tests passed/failed
- Any errors or warnings
- Coverage percentage if available
```

## Post-Setup Checklist

- [ ] CLAUDE.md exists and has essential sections
- [ ] .gitignore includes Claude cache patterns
- [ ] Git repository initialized
- [ ] Project runs successfully
- [ ] First commit created

## First Commit

```bash
git add .
git commit -m "Initial project setup with Claude Code configuration"
```

## Next Steps

- Configure your development environment
- Set up CI/CD if needed
- Create your first feature with Claude
- Review best practices guide

## Common Issues

**Claude can't find CLAUDE.md**: Must be in project root
**Cache files committed**: Check .gitignore
**Skills not loading**: Check .claude/skills/ directory structure

## Key Takeaway

Fifteen minutes of setup saves hours of confusion later. A well-configured project lets Claude understand your codebase immediately.
