---
slug: git-issues
title: Git Operation Issues
category: troubleshooting
difficulty: intermediate
keywords: git errors commit push pull issues
commands: []
related: []
---

# Git Operation Issues

## Common Git Problems

### Commit Blocked by Hook

```bash
# Pre-commit hook failing
⛔ Tests failed - commit blocked

# Solutions
1. Fix failing tests
2. Temporarily skip (if appropriate)
   git commit --no-verify
```

### Push Rejected

```bash
# Remote has changes
! [rejected] main -> main (fetch first)

# Solution
git pull --rebase
git push
```

### Merge Conflicts

```bash
# After agent work
<<<<<<< HEAD
your changes
=======
agent changes
>>>>>>> agent-branch

# Resolve manually
# Then
git add .
git commit
```

### Detached HEAD

```bash
# Not on branch
HEAD detached at abc123

# Solution
git checkout main
# Or create branch
git checkout -b new-branch
```

### Authentication Failed

```bash
# Git credentials issue
remote: Invalid username or password

# Solution
# Use SSH or update credentials
git remote set-url origin git@github.com:user/repo.git
```

## Claude-Specific Issues

### Auto-Commit Failing

```bash
# Claude tries to commit but fails
# Check git config
git config user.name
git config user.email

# Set if missing
git config user.name "Your Name"
git config user.email "you@example.com"
```

### Hook Blocking Claude

```bash
# Pre-commit hook too strict
# Temporarily disable
mv .claude/hooks/pre-commit.sh .claude/hooks/pre-commit.sh.disabled

# Or fix hook to be less strict
```

## Key Takeaway
Git issues with Claude usually involve hooks, authentication, or merge conflicts. Fix hooks if blocking commits, ensure git credentials configured, and resolve conflicts manually when agents create them.
