---
slug: automated-docs
title: Automated Documentation Pattern
category: advanced-patterns
difficulty: intermediate
keywords: documentation automation generation docs
commands: []
related: [hooks-patterns]
---

# Automated Documentation Pattern

## Summary

Automatically generate and maintain documentation through hooks, skills, and agents. Keep docs synchronized with code changes without manual effort.

## Pattern 1: Post-Commit Hook

```bash
#!/bin/bash
# .claude/hooks/post-commit.sh

# Auto-update docs after commit
if git diff --name-only HEAD~1 | grep -q "src/"; then
  npm run docs:generate
  
  # If docs changed, amend commit
  if [ -n "$(git status --porcelain docs/)" ]; then
    git add docs/
    git commit --amend --no-edit
  fi
fi
```

## Pattern 2: Doc Generation Skill

```markdown
---
name: docs
description: Generate comprehensive documentation
tools: [read, write, bash]
---

# Documentation Generator

## Process
1. Scan all source files
2. Extract JSDoc/docstrings
3. Generate API documentation
4. Update README examples
5. Create usage guides
6. Build doc site
```

## Pattern 3: Doc Agent

```bash
# Spawn doc agent for large projects
claude agent docs "Update all documentation"

# Agent:
# - Analyzes code changes
# - Updates API docs
# - Refreshes examples
# - Fixes outdated references
# - Generates new guides
```

## Pattern 4: Real-time Sync

```bash
# Watch mode for docs
npm run docs:watch

# On file change:
# 1. Regenerate affected docs
# 2. Reload preview
# 3. Show diff
```

## Documentation Types

### API Documentation
```
Extract from code:
- Function signatures
- Parameter types
- Return values
- Examples
```

### Usage Guides
```
Generate from:
- README examples
- Test cases
- Common patterns
```

### Architecture Docs
```
Auto-generate:
- Directory structure
- Module dependencies
- Data flow diagrams
```

## Best Practices

✅ Generate from code (single source of truth)
✅ Automate via hooks
✅ Version with code
✅ Include examples
✅ Keep simple and clear

❌ Don't write docs manually
❌ Don't let docs drift
❌ Don't duplicate information

## Key Takeaway

Automate documentation generation through hooks, skills, and agents. Extract docs from code, sync with changes automatically, and maintain single source of truth. Well-automated docs stay current with zero manual maintenance.
