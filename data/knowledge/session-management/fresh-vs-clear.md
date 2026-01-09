---
slug: fresh-vs-clear
title: Fresh Session vs Clear Context
category: session-management
difficulty: intermediate
keywords: fresh clear session decide choice comparison
commands: ["claude", "/clear"]
related: [start-session, clear-context, session-best-practices]
---

# Fresh Session vs Clear Context

## Summary

Understand when to start a fresh session (`claude`) versus clearing context within the current session (`/clear`). This decision affects performance, context preservation, and workflow efficiency.

## Quick Decision Guide

```
Different project/codebase → Fresh session
Same project, new task → /clear
Same project, continue work → Neither (keep going)
Context feels bloated → /clear first, fresh if still bad
Quality degrading → /clear
Switching directories → Fresh session
```

## Fresh Session: Starting Over

### When to Start Fresh

**Start a new session when:**

1. **Different Project**
   ```bash
   cd ~/project-a
   claude  # Working on Project A
   /exit

   cd ~/project-b
   claude  # Fresh start for Project B
   ```

2. **Fundamentally Different Work**
   ```bash
   # Was: Backend API development
   # Now: Frontend React components
   # Context doesn't transfer → Fresh start
   ```

3. **Clean Slate Needed**
   ```bash
   # Previous session went off track
   # Need to approach differently
   # Fresh perspective needed
   ```

4. **Next Day/Work Session**
   ```bash
   # Yesterday: Implemented feature X
   # Today: Implementing feature Y (unrelated)
   # Fresh start with clear mind
   ```

5. **Context is Irretrievably Confused**
   ```bash
   # Session completely lost track
   # Clearing won't help
   # Need full reset
   ```

### What Fresh Gives You

✅ **Benefits:**
- Fastest possible performance (minimal context)
- No accumulated confusion
- Clean mental model
- CLAUDE.md reloaded (picks up any updates)
- Skills reloaded (picks up new/modified skills)

❌ **Costs:**
- Lose all conversation history
- Must re-explain context
- Can't reference previous work
- Can't resume if you made progress

## Clear Context: Refresh Within Session

### When to Clear

**Clear context when:**

1. **New Task, Same Project**
   ```bash
   > Finished implementing auth
   > /clear
   > Now let's build the payment system
   ```

2. **Performance Degrading**
   ```bash
   # Responses getting slow
   # But want to stay in same project
   > /clear
   ```

3. **Context Bloated**
   ```bash
   # 80+ messages in
   # Context full of old exploration
   > /clear
   > Let's focus on just the checkout flow
   ```

4. **Fresh Perspective, Same Work**
   ```bash
   # Stuck on approach
   # Want different angle
   > /clear
   > Let me describe the problem differently...
   ```

5. **Between Phases**
   ```bash
   # Research phase done
   > /clear
   # Now implementation phase with clear plan
   ```

### What Clear Gives You

✅ **Benefits:**
- Stays in same session (can still resume)
- Keeps CLAUDE.md context
- Keeps skills loaded
- Keeps working directory
- Much faster than fresh (less reload)

❌ **Costs:**
- Loses conversation history
- Must restate current goal
- May need to re-explain recent context

## The Spectrum

```
Keep Going  →  /clear  →  Fresh Session
↓              ↓         ↓
0% reset     70% reset  100% reset
Fastest      Fast       Slowest
Most context Some       No history
              context
```

## Decision Matrix

| Situation | Keep Going | /clear | Fresh |
|-----------|------------|--------|-------|
| Continuing same implementation | ✅ | ❌ | ❌ |
| New feature, same project | ❌ | ✅ | ❌ |
| Different project | ❌ | ❌ | ✅ |
| Session feels slow | ❌ | ✅ | ⚠️ |
| Context confused | ❌ | ✅ | ⚠️ |
| Next day, same feature | ⚠️ | ✅ | ❌ |
| Next day, different feature | ❌ | ❌ | ✅ |
| CLAUDE.md was updated | ❌ | ❌ | ✅ |
| Skills were modified | ❌ | ❌ | ✅ |

## Practical Examples

### Example 1: Feature Development Day

```bash
# Morning
claude  # Fresh start for the day
> Implementing user authentication

[2 hours, 40 messages]
> Authentication complete!

> /clear  # Clear for next feature
> Now implementing password reset

[1 hour, 25 messages]
> Password reset done!

> /clear  # Clear for next feature
> Building email notifications

[continues...]
```

**Why:** Same project, moving between features. Clear between features, fresh at start of day.

### Example 2: Deep Dive Same Feature

```bash
claude
> Debugging the payment processing issue

[3 hours, 120 messages, lots of exploration]
# Context is bloated but still relevant

# DON'T clear - you need that context
# Keep going or take break and resume

# Only clear if quality really degrades
```

**Why:** All context is relevant to current problem. Clearing would lose valuable debugging context.

### Example 3: Project Switching

```bash
# Project A
cd ~/project-a
claude
> Working on Project A feature

/exit  # Done for now

# Project B - DIFFERENT codebase
cd ~/project-b
claude  # Fresh start, not resume!
> Working on Project B feature
```

**Why:** Different projects need clean separation. Fresh session for each.

### Example 4: Updated CLAUDE.md

```bash
# In session
> [working away]

# Meanwhile, you edited CLAUDE.md
# Added new conventions

> /exit  # Exit to reload
claude  # Fresh start picks up new CLAUDE.md
```

**Why:** CLAUDE.md only loads at session start. Must start fresh to see updates.

## Performance Comparison

### Fresh Session
```
Token count: ~5,000 (CLAUDE.md + skills)
Response time: 2-3 seconds
Quality: Excellent (no context pollution)
```

### After Clear
```
Token count: ~8,000 (CLAUDE.md + skills + last exchange)
Response time: 2-4 seconds
Quality: Excellent (context refreshed)
```

### Long Session (No Clear)
```
Token count: ~80,000 (accumulated context)
Response time: 8-15 seconds
Quality: Degrading (context overload)
```

## Context Budget Analogy

Think of context like a budget:

**Fresh Session:**
- $5,000 to spend
- Invested in essential project info

**Cleared Session:**
- $5,000 to spend
- Invested in essential project info
- Plus ~$3,000 from last few exchanges

**Long Session:**
- $5,000 for essentials
- $75,000 for accumulated conversation
- Running out of "budget"

## Common Patterns

### The Daily Fresh
```bash
# Every morning
claude  # Fresh start

# Throughout day
/clear  # Between tasks

# End of day
/exit
```

### The Feature Fresh
```bash
# Big feature
claude
[intensive work]
/exit

# Next feature
claude  # Fresh for new feature context
```

### The Continuous Clear
```bash
# Long session on one project
claude
[work work work /clear work work /clear work work]
/exit
```

## Mistakes to Avoid

### ❌ Fresh When Clear Would Do

```bash
# Same project, just new task
/exit
claude
# Wasted time - /clear was enough
```

### ❌ Clear When Should Continue

```bash
# In middle of implementation
[making progress]
> /clear  # WHY?!
# Lost all context about what you were doing
```

### ❌ Never Clearing

```bash
# 6 hours later, 300 messages
# Response time: 30 seconds per message
# Quality: terrible
# Should have cleared 4 hours ago!
```

### ❌ Resume Different Project

```bash
cd ~/project-b
claude --resume
# Resumes Project A context!
# Should have done fresh start
```

## Advanced Strategies

### Hybrid Approach

```bash
# Keep important context before clear
> Key decisions we made:
  - Using JWT
  - PostgreSQL for storage
  - Redis for cache
> /clear
> Implementing auth with those decisions...
```

### Skill-Based Clear

Create a skill:

```markdown
# .claude/skills/new-task.md
Clear context and start fresh on a new task

Steps:
1. /clear
2. Ask user what task they want to tackle
3. Start with fresh focus
```

### Document-Then-Clear

```bash
# Before clearing, update CLAUDE.md
> Update CLAUDE.md with:
  ## Recent Decisions
  - Auth: JWT tokens
  - DB: PostgreSQL schema v2

> /clear  # Now safe to clear
```

## Quick Reference

```bash
# Fresh session
claude

# Clear context
/clear

# Resume (use with caution)
claude --resume

# Check context size
/status  # Shows token usage

# Exit to start fresh
/exit
claude
```

## Key Takeaway

Default to `/clear` for transitions within the same project, and use fresh sessions when switching projects or when you need a complete reset. Most users fresh-start too often - clearing is usually enough and faster. Save fresh starts for actual new beginnings.
