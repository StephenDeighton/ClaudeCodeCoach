---
slug: hooks-patterns
title: Advanced Hook Patterns
category: advanced-patterns
difficulty: advanced
keywords: hooks patterns automation workflows advanced
commands: []
related: [hooks-overview]
---

# Advanced Hook Patterns

## Summary

Advanced hook patterns automate complex workflows through hook composition, conditional execution, and integration with external services.

## Pattern: Hook Chain

```bash
# post-write.sh triggers formatting
# which triggers linting
# which triggers tests

post-write → format → lint → test
```

## Pattern: Conditional Hooks

```bash
#!/bin/bash
# pre-commit.sh

if [ "$BRANCH" == "main" ]; then
  # Strict checks on main
  npm run lint --max-warnings 0
  npm test --coverage --min 80%
else
  # Relaxed on feature branches
  npm run lint
  npm test
fi
```

## Pattern: Notification Hooks

```bash
#!/bin/bash
# post-commit.sh

COMMIT_MSG=$(git log -1 --pretty=%B)
BRANCH=$(git branch --show-current)

# Notify team
curl -X POST $SLACK_WEBHOOK \
  -d "{\"text\": \"📝 $COMMIT_MSG on $BRANCH\"}"
```

## Pattern: Context-Aware Hooks

```bash
#!/bin/bash
# post-write.sh

FILE=$1

case "$FILE" in
  *.ts|*.js)
    prettier --write "$FILE"
    eslint --fix "$FILE"
    ;;
  *.py)
    black "$FILE"
    ruff check "$FILE"
    ;;
  *.go)
    gofmt -w "$FILE"
    ;;
esac
```

## Pattern: Rollback Hook

```bash
#!/bin/bash
# pre-deploy.sh

# Backup before deploy
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL > backups/pre_deploy_$TIMESTAMP.sql

# Store rollback info
echo "$TIMESTAMP" > .last-deploy
```

## Key Takeaway

Advanced hook patterns enable sophisticated automation through chaining, conditional logic, notifications, and context-aware behavior. Build complex workflows by composing simple hooks.
