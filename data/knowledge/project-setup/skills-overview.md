---
slug: skills-overview
title: Skills Overview
category: project-setup
difficulty: intermediate
keywords: skills slash commands custom tools workflows
commands: ["/skills"]
related: [creating-skills, commands-overview, agents-overview]
---

# Skills Overview

## Summary

Skills are reusable workflows accessible via slash commands (like `/commit` or `/review-pr`). They extend Claude Code with project-specific or domain-specific capabilities, combining prompts, tools, and logic into convenient commands.

## What are Skills?

Skills are custom commands that:
- Execute complex workflows with single command
- Encapsulate domain knowledge
- Can be shared across projects
- Run with specialized prompts and tool access

## Built-in Skills

```bash
# Common skills included with Claude Code
/commit           # Create git commits
/review-pr        # Review pull requests
/test             # Run and fix tests
/docs             # Generate documentation
/refactor         # Refactor code safely
```

List all available:
```bash
/skills

Available skills:
  /commit        Create git commits
  /review-pr     Review pull requests
  /test          Run and fix tests
  /docs          Generate documentation
  ...
```

## Using Skills

### Basic Usage

```bash
# Just the command
/commit

# With arguments
/commit -m "Fix authentication bug"

# With context from conversation
User: I just fixed the login issue
/commit
# Claude uses conversation context for commit message
```

### Skill Invocation

Skills can:
1. **Read context** - Access conversation history
2. **Take arguments** - Accept flags and parameters
3. **Use tools** - Read/write files, run commands
4. **Provide output** - Return results to conversation

## Skill Categories

### 1. Git Workflows

```bash
/commit              # Smart commits
/review-pr 123       # Review PR #123
/branch feature-x    # Create feature branch
/merge --squash      # Merge with squash
```

### 2. Testing

```bash
/test                # Run all tests
/test unit           # Run unit tests
/test --fix          # Fix failing tests
/coverage            # Generate coverage report
```

### 3. Documentation

```bash
/docs                # Generate/update docs
/readme              # Update README
/changelog           # Update CHANGELOG
/api-docs            # Generate API docs
```

### 4. Code Quality

```bash
/lint                # Run linter
/format              # Format code
/refactor            # Safe refactoring
/security            # Security scan
```

### 5. Deployment

```bash
/deploy staging      # Deploy to staging
/deploy production   # Deploy to production
/rollback            # Rollback deployment
/status              # Check deployment status
```

## Custom Skills

### Project Skills

Located in `.claude/skills/`:

```bash
your-project/
└── .claude/
    └── skills/
        ├── migrate.md       # /migrate
        ├── seed-db.md       # /seed-db
        └── gen-types.md     # /gen-types
```

### User Skills

Located in `~/.claude/skills/`:

```bash
~/.claude/
└── skills/
    ├── journal.md       # /journal (all projects)
    ├── standup.md       # /standup (all projects)
    └── snippet.md       # /snippet (all projects)
```

## Skill Structure

Basic skill file:

```markdown
---
name: migrate
description: Run database migrations
tools: [bash, read, write]
---

# Migration Skill

Check for pending migrations and run them safely.

## Steps
1. Check migration status
2. Backup database if production
3. Run migrations
4. Verify success
5. Report results

## Important
- Always backup production DB first
- Check for migration conflicts
- Verify app still works after
```

## Skill Discovery

Claude loads skills from:
1. Built-in skills (always available)
2. `~/.claude/skills/` (user global)
3. `.claude/skills/` (project-specific)
4. Skill packs (installable collections)

```bash
# See where a skill comes from
/skills --info commit

Skill: commit
Source: built-in
Description: Create git commits
Tools: bash, read, git
```

## Skill Arguments

Skills can accept:

### Flags
```bash
/deploy --dry-run
/test --verbose
/commit --amend
```

### Positional Args
```bash
/review-pr 123
/branch feature-name
/deploy staging
```

### Multiple Args
```bash
/refactor src/auth.py --safe --test
```

## Skill Composition

Skills can call other skills:

```markdown
---
name: release
description: Full release workflow
---

# Release Workflow

1. Run tests: /test
2. Update version
3. Update changelog: /changelog
4. Commit: /commit -m "Release v1.0.0"
5. Tag release
6. Deploy: /deploy production
```

## Skill vs Command vs Agent

### Skill (workflow)
- Multi-step workflow
- Can use tools and agents
- Markdown format
- Example: /commit, /deploy

### Command (single operation)
- Single specific task
- Returns data quickly
- Python/shell script
- Example: /git-status, /test-count

### Agent (autonomous)
- Long-running task
- Makes decisions
- Can spawn subagents
- Example: Feature development, refactoring

Use skills when:
- Multiple related steps
- Need conversation context
- Workflow should be reusable
- Mid-level complexity

## Skill Permissions

Skills declare required tools:

```markdown
---
name: deploy
tools: [bash, read]
permissions: [git_push, remote_exec]
---
```

Claude requests permission before using restricted tools.

## Skill Packs

Install skill collections:

```bash
# Install pack
claude install-skills web-dev

# List packs
claude list-skill-packs

Available packs:
  web-dev         Web development workflows
  data-science    Data analysis and ML
  devops          Deployment and ops
  testing         Testing and QA
```

## Creating Skills

See [Creating Skills](creating-skills.md) for detailed guide.

Quick start:

```bash
# Create new skill
mkdir -p .claude/skills
cat > .claude/skills/build.md << 'EOF'
---
name: build
description: Build the project
tools: [bash]
---

# Build Project

Run the build process and report results.

```bash
npm run build
```

Check for errors and report build time.
EOF

# Use it
/build
```

## Key Takeaway

Skills are reusable workflows triggered by slash commands. Use built-in skills for common tasks, create custom skills for project-specific workflows. Skills live in `.claude/skills/` and provide a powerful way to extend Claude Code with domain knowledge.
