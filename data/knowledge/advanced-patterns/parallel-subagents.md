---
slug: parallel-subagents
title: Parallel Subagents Pattern
category: advanced-patterns
difficulty: advanced
keywords: parallel subagents concurrent agents coordination
commands: []
related: [when-use-subagents, scaling-phase]
---

# Parallel Subagents Pattern

## Summary

Run multiple subagents concurrently to parallelize independent work. Coordinate integration points and manage dependencies between agents for maximum efficiency.

## Pattern

```bash
# Spawn multiple agents in parallel
claude agent feature "Backend API" &
claude agent feature "Frontend UI" &
claude agent test "Test suite" &

# Work proceeds concurrently
# 3x faster than sequential
```

## When to Use

- Independent features (no shared files)
- Large features (> 2 hours each)
- Clear boundaries
- Integration points well-defined

## Coordination

```
Main Session: Coordinator
├─ Agent 1: Backend (src/api/)
├─ Agent 2: Frontend (src/ui/)
└─ Agent 3: Tests (tests/)

Integration: Main session combines results
```

## Best Practices

✅ Max 3-5 concurrent agents
✅ Clear domain separation
✅ Define integration contract upfront
✅ Monitor progress regularly
✅ Test integration thoroughly

## Key Takeaway

Parallel subagents provide massive speed improvements for independent work. Spawn 2-5 agents for separate features, coordinate integration points, and test thoroughly when combining results.
