---
slug: context-window-basics
title: Context Window Basics
category: context-efficiency
difficulty: beginner
keywords: context window tokens limit budget memory
commands: ["/status"]
related: [context-hygiene, progressive-disclosure, reducing-bloat]
---

# Context Window Basics

## Summary

Claude Code has a 200,000 token context window that holds conversation history, file contents, and tool outputs. Understanding and managing this context is critical for performance and effectiveness.

## What is Context?

Context is everything Claude "remembers":

```
Context Window (200,000 tokens)
├─ Conversation history
├─ Files you've read
├─ Command outputs
├─ Tool results
├─ CLAUDE.md content
├─ Skill instructions
└─ Agent communications
```

## Token Basics

### What's a Token?

Roughly:
- 1 token ≈ 4 characters
- 1 token ≈ 0.75 words
- 100 tokens ≈ 75 words
- 1,000 tokens ≈ 750 words

### File Size Examples

```
Small file (100 lines): ~2,000 tokens
Medium file (500 lines): ~10,000 tokens
Large file (2,000 lines): ~40,000 tokens
Very large file (10,000 lines): ~200,000 tokens (entire context!)
```

## Context Limit

Claude Code: **200,000 tokens**

```
Empty session: 0 tokens
After CLAUDE.md: 1,000 tokens
After exploring code: 20,000 tokens
After building feature: 80,000 tokens
Near limit: 160,000 tokens (warning)
At limit: 200,000 tokens (must clear)
```

## Checking Context Usage

### Status Command

```bash
/status

Context: 45,234 / 200,000 tokens (23%)
Model: Claude Sonnet 4.5
Mode: Normal
Session: 2h 15m
```

### During Session

Claude warns when reaching 80%:

```
⚠️  Context Warning
Current: 165,000 / 200,000 tokens (83%)

Recommendation: Consider /clear or start fresh session
```

## What Uses Context?

### High Usage

```
Reading large files: 10k-50k tokens
Full codebase exploration: 50k-100k tokens
Long conversations: 20k-50k tokens
Agent work: 30k-80k tokens
```

### Low Usage

```
Small file edits: 1k-5k tokens
Commands: 100-500 tokens
Short questions: 500-2k tokens
```

## Context Lifecycle

```
Session Start
0 tokens
  ↓
Load CLAUDE.md
1k tokens
  ↓
Read a few files
10k tokens
  ↓
Conversation and work
50k tokens
  ↓
Build feature
120k tokens
  ↓
More work
160k tokens → Warning!
  ↓
Clear or exit
Back to low usage
```

## When Context Fills Up

### Symptoms

```
- Slower responses
- "Context full" warnings
- Suggestions to clear
- Performance degradation
```

### Options

1. **/clear** - Clear context, stay in session
2. **/exit** then `claude` - Fresh session
3. **Continue** - Risk hitting limit

## Context Efficiency

### Efficient

```bash
# Read specific files only
Read src/auth/service.ts

# Use grep to find, then read
Grep for "auth"
Read matching file

# Clear between major tasks
Build feature A
/clear
Build feature B
```

### Inefficient

```bash
# Reading everything
Read all 500 files

# Never clearing
Work for 8 hours straight
Context: 195k tokens

# Reading same files repeatedly
Read file.ts (10 times)
```

## Context vs Performance

```
0-50k tokens: ⚡ Fast
50k-100k tokens: ⚡ Still good
100k-150k tokens: ⚙️  Slowing down
150k-180k tokens: ⚠️  Noticeably slower
180k-200k tokens: 🐌 Very slow
200k tokens: ❌ Must clear
```

## Best Practices

### ✅ Do

- Check context with /status
- Clear between unrelated tasks
- Read only files you need
- Use grep before reading
- Exit and restart periodically

### ❌ Don't

- Read entire codebase at once
- Ignore context warnings
- Work for hours without clearing
- Re-read same files repeatedly
- Keep irrelevant conversation

## Context Budgeting

### Small Task (< 30 min)

```
Budget: 20k-40k tokens
- Read 3-5 files
- Short conversation
- Make changes
- Test
```

### Medium Task (1-3 hours)

```
Budget: 60k-100k tokens
- Read 10-20 files
- Exploration
- Implementation
- Testing

Consider: Clear after planning phase
```

### Large Task (Half day+)

```
Budget: Multiple sessions
Session 1 (0-80k): Plan
/clear or /exit
Session 2 (0-80k): Implement
/clear or /exit
Session 3 (0-40k): Test & refine
```

## Monitoring Context

```bash
# Check frequently
/status

# When to check
- Before starting large task
- After major file reads
- When responses slow down
- Every hour of work
```

## Context Strategies

### Strategy 1: Clear Between Features

```
Feature A planning → implement → test
/clear
Feature B planning → implement → test
```

### Strategy 2: Fresh Sessions

```
Morning: Authentication (fresh session)
Afternoon: User profiles (fresh session)
```

### Strategy 3: Agent Partitioning

```
Main session: Coordination (low context)
Agent 1: Auth (own context)
Agent 2: Profiles (own context)
```

## Key Takeaway

Claude Code has 200,000 token context limit. Monitor usage with /status, clear context between major tasks with /clear, and start fresh sessions for new features. Context is valuable but finite - use it efficiently by reading only necessary files and clearing proactively before hitting limits.
