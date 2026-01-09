---
slug: when-use-subagents
title: When to Use Subagents
category: feature-selection
difficulty: advanced
keywords: subagents agents parallel autonomous delegation
commands: []
related: [agents-overview, feature-decision-guide, scaling-phase]
---

# When to Use Subagents

## Summary

Use subagents (spawned agents) for parallel autonomous work, complex exploration, or delegating independent subtasks. Subagents run concurrently with your main session, each handling specific goals independently.

## What are Subagents?

Subagents are Claude instances spawned from your session:

```
Main Session (You + Claude)
├─→ Subagent 1: Build feature A
├─→ Subagent 2: Build feature B
└─→ Subagent 3: Run tests
```

## When to Use Subagents

### Parallel Work
```bash
# Without subagents (sequential, 3 hours)
1. Build authentication (1 hour)
2. Build user profiles (1 hour)
3. Write tests (1 hour)

# With subagents (parallel, 1 hour)
Subagent 1: Build authentication (1 hour) &
Subagent 2: Build user profiles (1 hour) &
Subagent 3: Write tests (1 hour) &

# All complete simultaneously
```

### Complex Exploration
```bash
# Explore large codebase in parallel
claude "How does the system handle authentication?"

# Spawns subagents
Subagent 1: Explore backend auth
Subagent 2: Explore frontend auth
Subagent 3: Explore database schema

# Combines findings
```

### Independent Subtasks
```bash
# Main task: Release v2.0
# Delegate subtasks to subagents

Subagent 1: Update documentation
Subagent 2: Run full test suite
Subagent 3: Build production bundles
Subagent 4: Generate changelog

# Main session: Coordinate and integrate
```

## Subagent vs Main Session

### Main Session
```bash
# Interactive
# You're actively working
# Back-and-forth conversation
# High priority tasks
```

### Subagent
```bash
# Autonomous
# Works independently
# Reports back when done
# Can run in background
```

## Common Subagent Patterns

### Pattern 1: Parallel Features

```bash
# Spawn multiple feature subagents
User: "Build auth, profiles, and settings"

Claude: I'll spawn 3 subagents for parallel work:

claude agent feature "Authentication" &
claude agent feature "User Profiles" &
claude agent feature "Settings Page" &

# Work proceeds in parallel
# 3x faster than sequential
```

### Pattern 2: Explore + Build

```bash
# Spawn explorer while you plan
User: "I need to add caching"

Claude: Let me explore existing caching patterns
[Spawns explore subagent]

# You continue planning
# Subagent explores codebase
# Reports findings when done
```

### Pattern 3: Test + Fix

```bash
# Spawn test runner
claude agent test "Run full test suite" &

# Continue working
# Subagent reports failures
# You fix issues
# Subagent reruns tests
```

### Pattern 4: Feature + Documentation

```bash
# Build feature in main session
# Spawn doc subagent
claude agent docs "Document authentication" &

# You continue coding
# Subagent writes docs
# Both complete together
```

## When NOT to Use Subagents

### ❌ Simple Questions
```bash
# Don't spawn subagent
User: "What's in this file?"
# Just read the file directly
```

### ❌ Quick Operations
```bash
# Don't spawn subagent
User: "Fix this typo"
# Just fix it immediately
```

### ❌ Sequential Dependencies
```bash
# Don't parallelize if B depends on A
Subagent 1: Build auth &
Subagent 2: Build protected routes &  # Needs auth first!

# Instead: Build sequentially
```

### ❌ Need Frequent Input
```bash
# Don't spawn if you'll interrupt often
User: "Add feature but I need to approve each step"
# Keep in main session
```

## Subagent Management

### Spawning Subagents
```bash
# From main session
User: "Can you explore auth patterns in the background?"

Claude: I'll spawn an explorer subagent
Agent spawned: explore-auth-a3b2

# Continue working
# Check progress: /agent status explore-auth-a3b2
```

### Monitoring Subagents
```bash
# List active subagents
/agents

Active agents:
  explore-auth-a3b2 (running, 3m)
  feature-profiles-k4m2 (running, 8m)
  test-runner-w9x1 (completed)

# Check specific subagent
/agent status feature-profiles-k4m2

Status: Running
Progress: 60% (3/5 tasks complete)
ETA: 5 minutes
```

### Subagent Communication
```bash
# Send message to subagent
/agent message feature-profiles-k4m2 "Use PostgreSQL, not MongoDB"

# Subagent acknowledges
Agent: Acknowledged, switching to PostgreSQL
```

## Subagent Coordination

### Independent Subagents
```bash
# No coordination needed
Subagent A: Frontend
Subagent B: Backend
Subagent C: Tests

# No conflicts
# Each has own domain
```

### Coordinated Subagents
```bash
# Share integration points
Main: Coordinate overall system
Subagent 1: Auth API (produces tokens)
Subagent 2: Protected routes (consumes tokens)

# Subagent 2 waits for Subagent 1 API contract
# Main session coordinates
```

## Subagent Best Practices

### ✅ Do:
- Use for independent work
- Run parallel when possible
- Monitor progress
- Set clear goals
- Coordinate integration

### ❌ Don't:
- Spawn too many (max 3-5)
- Create circular dependencies
- Forget to monitor
- Assume no conflicts
- Skip integration testing

## Subagent Limits

### Practical Limits
```bash
# Good
3 subagents (manageable)

# Okay
5 subagents (getting complex)

# Too many
10+ subagents (coordination nightmare)
```

### Resource Limits
```json
{
  "agents": {
    "maxConcurrent": 3,
    "maxDuration": 3600,
    "maxTokens": 100000
  }
}
```

## Cost Considerations

Subagents consume tokens:

```bash
# Main session: 10k tokens
# Subagent 1: 50k tokens
# Subagent 2: 50k tokens
# Subagent 3: 30k tokens
# Total: 140k tokens

# Worth it for 3x speed improvement
# Not worth it for trivial tasks
```

## Integration After Completion

```bash
# Subagents complete
Subagent 1: Auth complete ✓
Subagent 2: Profiles complete ✓
Subagent 3: Settings complete ✓

# Main session: Integration
1. Review each feature
2. Test integration points
3. Fix conflicts
4. Run full test suite
5. Commit everything
```

## Key Takeaway

Use subagents for parallel autonomous work on independent tasks. Spawn 2-5 subagents for features that can develop concurrently. Monitor progress and coordinate integration. Subagents provide massive speed improvements for large features but add complexity - use wisely for tasks > 30 minutes that can truly run in parallel.
