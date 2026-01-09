---
slug: hooks-not-running
title: Hooks Not Running
category: troubleshooting
difficulty: intermediate
keywords: hooks not running executing failing
commands: []
related: [hooks-overview]
---

# Hooks Not Running

## Symptoms
- Hooks don't execute
- No hook output
- Expected automation missing

## Common Causes

### 1. Not Executable
```bash
# Check permissions
ls -la .claude/hooks/
# Should show -rwxr-xr-x

# Fix
chmod +x .claude/hooks/*.sh
```

### 2. Wrong Location
```bash
# Should be
.claude/hooks/post-write.sh ✓

# Not
.claude/post-write.sh ✗
hooks/post-write.sh ✗
```

### 3. Hooks Disabled
```bash
# Check if disabled
claude --show-config

# Enable
claude  # (not --no-hooks)
```

### 4. Wrong Event Name
```bash
# Correct
post-write.sh ✓
pre-commit.sh ✓

# Incorrect
after-write.sh ✗
before-commit.sh ✗
```

### 5. Syntax Error
```bash
# Test hook manually
./.claude/hooks/post-write.sh test.txt

# Check for errors
```

### 6. Shebang Missing
```bash
# Must have shebang
#!/bin/bash  ✓

# Without shebang
# Won't execute ✗
```

## Debugging

### Test Manually
```bash
# Run hook directly
./.claude/hooks/session-start.sh

# Should execute without errors
```

### Enable Debug
```bash
export CLAUDE_HOOKS_DEBUG=1
claude

# Shows hook execution details
```

### Check Logs
```bash
# If logging enabled
tail -f ~/.claude/hooks.log
```

## Solutions

### Fix Permissions
```bash
find .claude/hooks -name "*.sh" -exec chmod +x {} \;
```

### Verify Shebang
```bash
head -1 .claude/hooks/*.sh
# Each should show #!/bin/bash or #!/usr/bin/env python3
```

### Test Hook
```bash
# Minimal test hook
cat > .claude/hooks/test.sh << 'EOFHOOK'
#!/bin/bash
echo "Hook works!"
EOFHOOK

chmod +x .claude/hooks/test.sh
```

## Key Takeaway
Hooks not running is usually permissions (chmod +x), wrong location (.claude/hooks/), or missing shebang (#!/bin/bash). Test hooks manually to verify they execute correctly.
