---
slug: git-worktrees
title: Git Worktrees with Claude
category: advanced-patterns
difficulty: advanced
keywords: git worktrees multiple branches parallel development
commands: []
related: [parallel-subagents]
---

# Git Worktrees with Claude

## Summary

Use git worktrees to work on multiple branches simultaneously with separate Claude sessions. Each worktree gets its own Claude agent, enabling true parallel development.

## Setup

```bash
# Main branch
cd ~/project
claude  # Work on main

# Create worktree for feature
git worktree add ../project-feature feature-branch
cd ../project-feature
claude  # Work on feature

# Both sessions run simultaneously
```

## Pattern

```
~/project/ (main branch)
  Claude Session 1: Bug fixes
  
~/project-feature/ (feature branch)
  Claude Session 2: New feature

~/project-refactor/ (refactor branch)
  Claude Session 3: Refactoring
```

## Use Cases

- Parallel feature development
- Testing different approaches
- Reviewing PR while developing
- Hotfix while working on feature

## Benefits

- No branch switching
- Separate contexts
- No conflicts
- True parallelism

## Workflow

```bash
# Setup worktrees
git worktree add ../project-auth auth-feature
git worktree add ../project-profiles profile-feature

# Spawn agents
cd ../project-auth && claude agent feature "Auth" &
cd ../project-profiles && claude agent feature "Profiles" &

# Agents work independently
# No git conflicts
# Merge when complete
```

## Key Takeaway

Git worktrees enable multiple Claude sessions on different branches simultaneously. Use for parallel feature development, testing approaches, or working on multiple tasks without branch switching overhead.
