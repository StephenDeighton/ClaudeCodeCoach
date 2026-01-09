---
slug: context-hygiene
title: Context Hygiene Practices
category: context-efficiency
difficulty: intermediate
keywords: hygiene practices context management discipline
commands: ["/clear", "/exit"]
related: [context-window-basics, reducing-bloat]
---

# Context Hygiene Practices

## Summary

Context hygiene means maintaining clean, focused, and efficient context through disciplined practices. Like code hygiene, good context hygiene improves performance and prevents issues.

## Core Principles

### 1. Context is Finite
Treat every token as valuable. Don't waste context on irrelevant data.

### 2. Context Degrades
Older context becomes less relevant. Refresh periodically.

### 3. Context is Shared
Everything competes for same 200k tokens. Prioritize wisely.

## Daily Hygiene Practices

### Morning: Fresh Start
```bash
# Don't resume yesterday's session
# Start fresh for new day
claude

# Clean slate: 0 tokens
# Yesterday's context: irrelevant
```

### Between Features: Clear
```bash
# Finish feature A
/commit
/clear

# Start feature B
# Fresh context, no baggage
```

### Afternoon: Check In
```bash
/status

# If > 100k tokens after lunch
# Consider /clear or fresh session
```

### Evening: Exit Clean
```bash
# Don't leave session running overnight
/exit

# Fresh tomorrow
```

## The 40/60 Rule

**40% of time: One session**
```
Work on related tasks
Context accumulates naturally
Clear when reaching 120k
```

**60% of time: Fresh sessions**
```
New feature = fresh session
Unrelated work = fresh session
After major milestone = fresh session
```

## Context Checkpoints

### Every Hour
```bash
/status

< 50k: ✓ Great
50-100k: ✓ Good
100-150k: ⚠️ Monitor
150k+: 🔴 Clear soon
```

### Every Major Task
```bash
# Before starting
/status
# Consider clearing if > 100k

# After completing
/status
# Clear if > 120k
```

## Context Cleaning Schedule

### Immediate Clean (do now)
- Context > 180k
- Performance noticeably slow
- Switching to unrelated task
- Session > 4 hours old

### Soon Clean (within 30 min)
- Context > 140k
- About to start major new task
- Completed major milestone
- Session > 2 hours old

### Consider Clean
- Context > 100k
- Between related tasks
- Natural break point

## Hygiene Anti-Patterns

### ❌ Never Clearing
```
8-hour session
Context: 195k
Performance: terrible
Should have cleared 3 times
```

### ❌ Hoarding Context
```
"I might need that file later"
[Keeps 50k of unused context]
[Uses 5k for actual work]
```

### ❌ Ignoring Warnings
```
Warning at 160k: ignored
Warning at 170k: ignored
Warning at 180k: ignored
Forced to clear at 200k
Lost flow state
```

## Clean Context Indicators

```
✓ Context < 50% of limit
✓ Only relevant files in context
✓ Recent conversation history
✓ Fast response times
✓ < 2 hour session age
```

## Dirty Context Indicators

```
✗ Context > 75% of limit
✗ Many irrelevant files
✗ Old conversation history
✗ Slow response times
✗ > 4 hour session age
```

## Context Hygiene Workflow

### Template: Feature Development

```
1. Fresh session (0k)
2. Load project context (5k)
3. Explore (+ 20k = 25k)
4. Plan (+ 15k = 40k)
5. Implement (+ 40k = 80k)
6. Test (+ 20k = 100k)
7. ✓ Check: 100k - still good
8. Refine (+ 30k = 130k)
9. ⚠️ Check: 130k - clear soon
10. /clear
11. Final polish (20k)
12. Done
```

## Hygiene Habits

### ✅ Good Habits
- Clear between unrelated tasks
- Exit session daily
- Monitor context regularly
- Read files once
- Use progressive disclosure
- Fresh session for new features

### ❌ Bad Habits
- Never clearing
- Multi-day sessions
- Ignore context warnings
- Re-read files repeatedly
- Read everything upfront
- Resume old sessions

## Emergency Hygiene

### Context Crisis (195k)
```
1. Stop immediately
2. Note current task
3. /clear
4. Load only essential files
5. Continue with focused context
```

### Performance Crisis
```
Symptoms: Very slow responses
Cause: Likely context bloat
Fix:
1. /status (check context)
2. If > 150k: /clear
3. Fresh start
```

## Context Hygiene Metrics

### Excellent Hygiene
```
Average session: 40k tokens
Max session: 80k tokens
Clears per day: 3-4
Session duration: 1-2 hours
```

### Poor Hygiene
```
Average session: 120k tokens
Max session: 195k tokens
Clears per day: 0-1
Session duration: 4-8 hours
```

## Key Takeaway

Practice context hygiene: start fresh daily, clear between major tasks, monitor context usage, exit sessions cleanly, and follow the 40/60 rule (40% work in one session, 60% fresh sessions). Good hygiene prevents performance issues and keeps Claude Code fast and effective. Think of context like RAM - it needs periodic cleanup to perform well.
