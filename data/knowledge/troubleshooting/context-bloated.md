---
slug: context-bloated
title: Context Bloated / Full
category: troubleshooting
difficulty: beginner
keywords: context full bloated limit exceeded
commands: ["/clear", "/status"]
related: [context-window-basics, reducing-bloat]
---

# Context Bloated / Full

## Symptoms
- "Context approaching limit" warnings
- Slow responses
- Forced to clear context
- Can't proceed without clearing

## Diagnosis

```bash
/status

Context: 185,000 / 200,000 (93%)
# Context nearly full!
```

## Causes
- Reading too many files
- Long conversation history
- Verbose command outputs
- Re-reading same files
- Never clearing context

## Immediate Fix

```bash
# Clear context
/clear

# Or start fresh
/exit
claude
```

## Recovery Steps

1. Note current task
2. /clear
3. Load only essential files
4. Continue with focused context

## Prevention

### Monitor Context
```bash
# Check hourly
/status

# Watch for warnings
⚠️ Context at 80%
```

### Clear Proactively
```bash
# Between major tasks
Complete feature A
/clear
Start feature B
```

### Use Progressive Disclosure
```bash
# Don't read everything
tree -L 2  # Structure first
grep "keyword"  # Search
Read specific files  # Only what's needed
```

### Limit Output
```bash
# Suppress verbose output
npm install --silent
npm test --quiet
```

## Quick Context Diet

```bash
1. /clear immediately
2. Load CLAUDE.md only
3. Read 3-5 key files max
4. Proceed with focused work
```

## Key Takeaway
Context bloat is preventable. Monitor with /status, clear between tasks, use progressive disclosure, and start fresh sessions regularly. When bloated, /clear immediately and reload only essentials.
