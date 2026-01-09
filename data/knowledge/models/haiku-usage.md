---
slug: haiku-usage
title: Haiku for Speed and Volume
category: models
difficulty: beginner
keywords: haiku fast speed batch volume cheap
related: [change-model, sonnet-usage]
---

# Haiku for Speed and Volume

## Summary

Claude Haiku 4.0 is the fastest, most cost-effective model. Use it for simple tasks, batch operations, and when speed matters more than sophisticated reasoning.

## Haiku's Strengths

**Speed**: 3-5x faster than Sonnet
**Cost**: ~1/3 price of Sonnet
**Volume**: Perfect for batch operations

## Ideal Use Cases

### 1. Batch Operations
- Creating 20+ similar files
- Bulk formatting
- Mass updates

### 2. Simple Tasks
- Adding comments
- Fixing typos
- Updating documentation
- Running tests

### 3. Repetitive Work
- CRUD generation
- Boilerplate code
- Test file creation

### 4. Fast Iteration
- Quick fixes
- Rapid prototyping
- Exploratory coding

## What Haiku Can't Do Well

❌ Complex architectural decisions
❌ Difficult debugging
❌ Novel problem-solving
❌ Large refactors
❌ Unfamiliar frameworks

For these, use Sonnet or Opus.

## Subagent Use

Haiku excels as subagent model:
```bash
# Main session: Sonnet
# Subagents: Haiku for parallel exploration
```

Cost-effective parallel work.

## Pattern: Haiku for Polish

```bash
# Core work with Sonnet
/model sonnet
"Implement payment system"

# Polish with Haiku
/model haiku
"Add JSDoc comments to all functions"
"Format all files with prettier"
"Generate test data"
```

## Performance

- Response time: 1-2 seconds
- Good for interactive work
- Not noticeably "dumber" for simple tasks

## Key Takeaway

Haiku is perfect for simple, fast, high-volume work. Don't underestimate it for straightforward tasks. Save Sonnet/Opus for when you actually need the extra capability.
