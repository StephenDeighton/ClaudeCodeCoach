---
slug: hooks-overview
title: Hooks Overview
category: project-setup
difficulty: advanced
keywords: hooks automation triggers events lifecycle scripts
commands: []
related: [claude-md-guide, skills-overview]
---

# Hooks Overview

## Summary

Hooks are scripts that run automatically at specific points in Claude Code's lifecycle. Use them to automate checks, transformations, notifications, or integrations when events occur.

## What are Hooks?

Hooks are executable scripts that trigger on events like:
- Session start/end
- Before/after file write
- Before/after command execution
- Git operations
- Context changes
- Tool usage

## Hook Types

### Lifecycle Hooks

```bash
session-start        # When session begins
session-end          # When session ends
context-clear        # After context cleared
context-warning      # When context reaches threshold
```

### File Operation Hooks

```bash
pre-write            # Before file write
post-write           # After file write
pre-edit             # Before file edit
post-edit            # After file edit
pre-delete           # Before file delete
```

### Git Hooks

```bash
pre-commit           # Before git commit
post-commit          # After git commit
pre-push             # Before git push
post-checkout        # After branch checkout
```

### Tool Hooks

```bash
pre-bash             # Before bash execution
post-bash            # After bash execution
pre-tool-use         # Before any tool use
post-tool-use        # After any tool use
```

## Hook Location

```bash
your-project/
└── .claude/
    └── hooks/
        ├── session-start.sh
        ├── post-write.py
        ├── pre-commit.sh
        └── post-bash.js
```

## Creating Hooks

### Basic Hook

```bash
# .claude/hooks/session-start.sh
#!/bin/bash

echo "Welcome to $(basename $PWD)!"
echo "Branch: $(git branch --show-current)"
echo "Last commit: $(git log -1 --oneline)"
```

Make executable:
```bash
chmod +x .claude/hooks/session-start.sh
```

### Hook with Arguments

Hooks receive context via arguments and environment variables:

```bash
#!/bin/bash
# .claude/hooks/post-write.sh

FILE_PATH=$1
echo "File written: $FILE_PATH"

# Run linter on Python files
if [[ $FILE_PATH == *.py ]]; then
    ruff check "$FILE_PATH"
fi
```

## Hook Environment Variables

Hooks receive these environment variables:

```bash
CLAUDE_SESSION_ID     # Current session ID
CLAUDE_PROJECT_ROOT   # Project root directory
CLAUDE_MODEL          # Current model (opus/sonnet/haiku)
CLAUDE_PERMISSION     # Permission mode (normal/plan/auto)
```

Event-specific variables:

```bash
# File hooks
CLAUDE_FILE_PATH      # File being operated on
CLAUDE_FILE_ACTION    # Action (write/edit/delete)

# Git hooks
CLAUDE_GIT_BRANCH     # Current branch
CLAUDE_GIT_COMMIT     # Commit hash (post-commit)

# Tool hooks
CLAUDE_TOOL_NAME      # Tool being used
CLAUDE_TOOL_ARGS      # Tool arguments
```

## Hook Examples

### Session Start: Project Status

```bash
#!/bin/bash
# .claude/hooks/session-start.sh

cat << EOF
╭──────────────────────────────────╮
│  Project: $(basename $PWD)
│  Branch: $(git branch --show-current)
│  Status: $(git status --short | wc -l) files modified
│  Tests: $(find tests -name "*.py" | wc -l) test files
╰──────────────────────────────────╯
EOF
```

### Post-Write: Auto-Format

```bash
#!/bin/bash
# .claude/hooks/post-write.sh

FILE_PATH=$1

# Format based on file type
case "$FILE_PATH" in
    *.py)
        ruff format "$FILE_PATH"
        ;;
    *.js|*.ts)
        prettier --write "$FILE_PATH"
        ;;
    *.go)
        gofmt -w "$FILE_PATH"
        ;;
esac
```

### Pre-Commit: Run Tests

```bash
#!/bin/bash
# .claude/hooks/pre-commit.sh

echo "Running tests before commit..."

if pytest tests/; then
    echo "✓ Tests passed"
    exit 0
else
    echo "✗ Tests failed - commit blocked"
    exit 1
fi
```

### Post-Commit: Notify Team

```bash
#!/bin/bash
# .claude/hooks/post-commit.sh

COMMIT_MSG=$(git log -1 --pretty=%B)
COMMIT_HASH=$(git log -1 --pretty=%h)
BRANCH=$(git branch --show-current)

# Send Slack notification
curl -X POST $SLACK_WEBHOOK_URL \
  -H 'Content-Type: application/json' \
  -d "{
    \"text\": \"New commit on $BRANCH\",
    \"blocks\": [{
      \"type\": \"section\",
      \"text\": {
        \"type\": \"mrkdwn\",
        \"text\": \"*$COMMIT_HASH*: $COMMIT_MSG\"
      }
    }]
  }"
```

### Pre-Bash: Security Check

```bash
#!/bin/bash
# .claude/hooks/pre-bash.sh

COMMAND=$1

# Block dangerous commands
DANGEROUS_PATTERNS=(
    "rm -rf /"
    "dd if="
    "mkfs"
    "> /dev/sda"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if [[ $COMMAND == *"$pattern"* ]]; then
        echo "⛔ Blocked dangerous command: $COMMAND"
        exit 1
    fi
done

exit 0
```

### Context Warning: Cleanup Suggestion

```python
#!/usr/bin/env python3
# .claude/hooks/context-warning.py

import os

context_usage = int(os.environ.get('CLAUDE_CONTEXT_USAGE', 0))
context_limit = int(os.environ.get('CLAUDE_CONTEXT_LIMIT', 200000))
percent = (context_usage / context_limit) * 100

print(f"⚠️  Context at {percent:.0f}%")

if percent > 90:
    print("Suggestion: Use /clear to refresh context")
    print("Or start fresh session with: /exit && claude")
```

## Hook Return Codes

Hooks can control flow with exit codes:

```bash
exit 0    # Success, continue
exit 1    # Failure, block operation
exit 2    # Warning, continue but notify
```

### Blocking Example

```bash
#!/bin/bash
# .claude/hooks/pre-commit.sh

# Block commits with "WIP" in message
if git log -1 --pretty=%B | grep -q "WIP"; then
    echo "⛔ Cannot commit with WIP message"
    exit 1
fi

exit 0
```

## Python Hooks

```python
#!/usr/bin/env python3
# .claude/hooks/post-write.py

import sys
import subprocess

def main():
    file_path = sys.argv[1]

    # Only process Python files
    if not file_path.endswith('.py'):
        return 0

    # Run type checker
    result = subprocess.run(
        ['mypy', file_path],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"⚠️  Type check warnings:")
        print(result.stdout)
        return 2  # Warning, don't block

    return 0

if __name__ == '__main__':
    sys.exit(main())
```

## Hook Configuration

Configure hooks in `.claude/config.json`:

```json
{
  "hooks": {
    "enabled": true,
    "timeout": 30,
    "allowedHooks": [
      "session-start",
      "post-write",
      "pre-commit"
    ],
    "deniedHooks": [
      "pre-bash"
    ],
    "exitOnFailure": true
  }
}
```

## Disabling Hooks

### Temporarily

```bash
# Disable for one session
claude --no-hooks

# Disable specific hook
claude --disable-hook pre-commit
```

### Permanently

```json
{
  "hooks": {
    "enabled": false
  }
}
```

## Hook Best Practices

### ✅ Do:
- Keep hooks fast (< 2 seconds)
- Make hooks idempotent (safe to run multiple times)
- Handle errors gracefully (don't crash)
- Log important actions
- Test hooks thoroughly
- Document hook behavior
- Version control hooks (commit to repo)

### ❌ Don't:
- Execute untrusted code
- Modify system files
- Store credentials in hooks
- Make network calls to untrusted servers
- Run hooks as root

## Key Takeaway

Hooks automate actions at key points in Claude Code lifecycle. Create executable scripts in `.claude/hooks/` named after the event they handle. Use hooks for formatting, linting, testing, notifications, and workflow automation. Keep hooks fast, safe, and well-documented.
