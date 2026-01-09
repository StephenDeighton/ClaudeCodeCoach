---
title: Git Ignore Setup for Claude Code
category: project-setup
commands: []
keywords: gitignore git ignore cache artifacts venv node_modules
related_topics: [project-setup-guide]
difficulty: beginner
---

# Git Ignore Setup for Claude Code

## Summary

Properly configuring .gitignore prevents caching artifacts, build outputs, and environment-specific files from being committed. Claude Code projects have specific ignore patterns you should include.

## Essential Claude Code Patterns

Add these to your `.gitignore`:

```gitignore
# Claude Code cache and artifacts
.claude/cache/
.claude/*.local.json
.claude/sessions/

# Operating system files
.DS_Store
Thumbs.db

# Editor directories
.vscode/
.idea/
*.swp
*.swo
*~
```

## Language-Specific Additions

### Python Projects
```gitignore
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv
pip-log.txt
```

### Node.js Projects
```gitignore
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.eslintcache
dist/
build/
```

### General Build Outputs
```gitignore
*.log
*.tmp
*.bak
dist/
build/
target/
out/
*.o
*.exe
```

## Why This Matters

**Cache Files**: `.claude/cache/` can grow large with embeddings and temporary data
**Local Settings**: `*.local.json` contains machine-specific paths
**Session Data**: Session transcripts may contain sensitive information
**Build Artifacts**: Prevent bloat and merge conflicts

## Common Mistakes

❌ Committing `.claude/cache/` (can be hundreds of MB)
❌ Forgetting OS-specific files (`.DS_Store`)
❌ Including editor config (`.vscode/`, `.idea/`)
❌ Tracking build outputs (`dist/`, `build/`)

## Checking Your Setup

Verify nothing unwanted is tracked:

```bash
git status
```

See what's ignored:

```bash
git status --ignored
```

## Retroactive Cleanup

If you already committed ignored files:

```bash
# Remove from git but keep local copy
git rm --cached .claude/cache/ -r
git commit -m "Remove cached files from git"
```

## Template .gitignore

Quick start template:

```gitignore
# Claude Code
.claude/cache/
.claude/*.local.json
.claude/sessions/

# Environment
.env
.env.local
*.local

# OS
.DS_Store

# Editors
.vscode/
.idea/

# Dependencies (add your language)
node_modules/    # Node
venv/           # Python
vendor/         # Go, PHP

# Build outputs
dist/
build/
*.log
```

## Key Takeaway

A well-configured .gitignore keeps your repository clean, speeds up operations, and prevents sensitive data leaks. Set it up before your first commit.
