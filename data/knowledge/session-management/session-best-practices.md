---
slug: session-best-practices
title: Session Best Practices
category: session-management
difficulty: intermediate
keywords: session best practices workflow tips optimal
commands: []
related: [start-session, clear-context, fresh-vs-clear]
---

# Session Best Practices

## Summary

Optimize your Claude Code workflow with proven session management practices. Learn optimal session length, when to clear or restart, and how to maintain high-quality interactions throughout your workday.

## The 40/60 Rule

**40% of context should be your project (CLAUDE.md + skills)**
**60% left for active conversation**

When conversation context exceeds 60%, quality degrades. This is your signal to clear.

Check with `/status` to see token usage.

## Optimal Session Length

### By Time

**Sweet spot:** 1-3 hours per session

- **< 1 hour:** Not enough to hit stride, fresh too often
- **1-3 hours:** Optimal - enough time to build context, not too bloated
- **> 3 hours:** Context accumulation likely, quality may degrade

### By Message Count

**Sweet spot:** 30-60 messages per session

- **< 30:** Fresh too often, interrupts flow
- **30-60:** Good work gets done, context manageable
- **> 60:** Consider clearing, context likely bloated

### By Task

**Sweet spot:** 1-3 features per session

```bash
# Good session arc
claude
> Feature 1: User authentication [25 messages]
> /clear
> Feature 2: Password reset [20 messages]
> /clear
> Feature 3: Email verification [18 messages]
> /exit
```

## Daily Workflow Patterns

### Pattern 1: Fresh Daily

```bash
# Monday morning
claude
[work all day, clearing between tasks]
/exit

# Tuesday morning
claude  # Fresh start
[work all day]
/exit

# Repeat
```

**Pros:** Clean start each day, CLAUDE.md updates loaded
**Cons:** None really, this is the default pattern

### Pattern 2: Resume Daily (Same Feature)

```bash
# Monday
claude
> Starting major refactor
[make progress]
/exit

# Tuesday
claude --resume
> Continuing the refactor
[continue work]
/exit
```

**Pros:** Continuity on multi-day features
**Cons:** Context accumulates across days

### Pattern 3: Fresh Per Feature

```bash
# Feature A
claude
[complete Feature A]
/exit

# Feature B - even if 5 minutes later
claude
[complete Feature B]
/exit
```

**Pros:** Clean context per feature
**Cons:** Overhead of restarting frequently

## Task Transition Patterns

### Minor Transition (Same Domain)

```bash
> Finished the login endpoint
> Now building the logout endpoint
# No clear needed - related work
```

### Major Transition (Different Domain)

```bash
> Finished all authentication
> /clear
> Now building the payment system
```

### Project Transition

```bash
> Done with Project A
> /exit
$ cd ~/project-b
$ claude
> Working on Project B
```

## Context Hygiene

### Regular Clearing

Clear at natural boundaries:

```bash
# After exploration phase
[30 messages exploring options]
> /clear
> We'll use approach B. Let's implement it.

# After implementation phase
[implementation complete]
> /clear
> Now let's write tests

# After debugging phase
[bug fixed]
> /clear
> Moving to next feature
```

### Preventive Clearing

Don't wait for performance to degrade:

```bash
# Check context regularly
> /status
Context: 45,000 tokens

# Clear before it's a problem
> /clear
Context: 8,000 tokens
```

### Strategic Preservation

Before clearing, save important context:

**Option 1: To CLAUDE.md**
```markdown
## Current Work
- Implementing JWT auth
- Using bcrypt for passwords
- Token expiry: 7 days
```

Then clear freely.

**Option 2: Explicit Handoff**
```bash
> Key facts before I clear:
  - Database schema uses UUID primary keys
  - All passwords hashed with bcrypt
  - JWT secret is in .env
> /clear
> Continuing with JWT implementation...
```

## Performance Monitoring

### Signs of Degradation

Watch for:
1. **Response time** > 8 seconds consistently
2. **Confusion** - Claude references wrong context
3. **Quality drop** - Generic or confused responses
4. **Repetition** - Saying same things repeatedly
5. **Token warnings** - Approaching context limit

### Recovery Strategies

**Level 1: Keep Going**
```bash
# Mild slowness, still accurate
# Just finish current task
```

**Level 2: Clear**
```bash
# Noticeable degradation
> /clear
> Restating goal: [explain what you're doing]
```

**Level 3: Fresh Start**
```bash
# Severe degradation, clearing didn't help
> /exit
$ claude
> Fresh start on [project]
```

## Session Types

### Exploration Session

**Goal:** Learn about codebase, research options

```bash
claude
> Help me understand the architecture
[ask lots of questions, read many files]
# Don't clear - building understanding
# May take 50-80 messages
/exit when done exploring
```

### Implementation Session

**Goal:** Build specific feature

```bash
claude
> Implementing user profile page
[focused work, fewer files]
# Clear if switching to different feature
# 20-40 messages typical
```

### Debugging Session

**Goal:** Find and fix specific bug

```bash
claude
> Debugging: Users can't login
[trace through code, test, fix]
# Keep context - all relevant to bug
# 15-30 messages typical
```

### Refactoring Session

**Goal:** Improve existing code

```bash
claude
> Refactoring payment processor
[read code, plan, execute]
# Clear after reading, before implementing
# Phases: understand [clear] refactor [clear] test
```

## Multi-Session Workflows

### Feature Development Over Days

**Day 1:** Plan and setup
```bash
claude
> Planning the notification system
[design decisions, architecture]
> Document these decisions in CLAUDE.md
/exit
```

**Day 2:** Core implementation
```bash
claude  # Fresh start with documented plan
> Implementing notification system per plan
[build core features]
/exit
```

**Day 3:** Tests and polish
```bash
claude
> Adding tests for notification system
[tests and refinements]
/exit
```

### Parallel Features

**Feature A** (worktree 1)
```bash
cd ~/project/.trees/feature-a
claude
[work on Feature A]
```

**Feature B** (worktree 2)
```bash
cd ~/project/.trees/feature-b
claude
[work on Feature B in separate session]
```

Each worktree = independent session.

## Context Budgeting

Think of each session as having a context "budget":

**Total budget:** ~200,000 tokens (varies by model)

**Allocation:**
- CLAUDE.md: 5,000 tokens (2.5%)
- Skills: 3,000 tokens (1.5%)
- Active work: 120,000 tokens (60%)
- Buffer: 72,000 tokens (36%)

When active work exceeds 60%, clear or restart.

## Error Recovery

### Session Crashes

```bash
# Session died unexpectedly
$ claude --resume
> Let me verify where we were...
> [reorient and continue]
```

### Accidental Clear

```bash
# Cleared by mistake
# Can't undo, but can quickly reestablish context
> I accidentally cleared. We were implementing
  the payment webhook handler. Let me restate...
```

### Wrong Direction

```bash
# Session went down wrong path
> /clear
> Let me restart with the correct approach
```

## Team Collaboration

### Handoff to Team Member

```bash
# Before handoff
> Document current state in CLAUDE.md
> Commit all work
> Write clear commit message
# They start fresh session with updated docs
```

### Resuming After Team Work

```bash
# Don't resume your old session
# Others changed code while you were away
claude  # Fresh start
> I see the team made changes. Let me review...
```

## Advanced: Session Scripts

Create shell functions for common patterns:

```bash
# ~/.bashrc or ~/.zshrc

# Fresh start with status check
alias cs='claude && claude --status'

# Clear and continue
alias cc='echo "/clear" | claude'

# Exit and fresh
alias cf='claude --exit && claude'
```

## Common Mistakes

### ❌ Never Clearing
```bash
# 6 hour session, 250 messages
# Response time crawling
# Quality terrible
# Should have cleared hours ago
```

### ❌ Clearing Too Often
```bash
# Every 5 messages: /clear
# Constant re-explanation
# Never builds useful context
# Wastes time
```

### ❌ Resuming Everything
```bash
# Next day, different feature
claude --resume  # Wrong!
# Old context not relevant
# Should start fresh
```

### ❌ Ignoring Performance Signs
```bash
# Responses take 15 seconds
# Claude seems confused
# "I'll just push through"
# Clear or restart!
```

## Quick Checklist

**Start of day:**
- [ ] Start fresh session
- [ ] In correct project directory
- [ ] CLAUDE.md is up to date

**During work:**
- [ ] Clear between major task transitions
- [ ] Monitor response time and quality
- [ ] Keep session under 60 messages if possible

**End of day:**
- [ ] Commit work in progress
- [ ] Update CLAUDE.md with decisions
- [ ] Exit cleanly

**Between sessions:**
- [ ] Decide: resume or fresh?
- [ ] If resuming, same project?
- [ ] If fresh, load new context

## Key Takeaways

1. **Fresh daily** - Start each day with `claude`, not resume
2. **Clear between features** - `/clear` when switching tasks
3. **Monitor quality** - Watch for degradation signals
4. **Budget context** - Keep active conversation < 60% of total
5. **Exit cleanly** - Always use `/exit`, never force-quit
6. **Document decisions** - Put important context in CLAUDE.md
7. **Trust your instincts** - If it feels slow or confused, clear or restart

## Session Management is an Art

There's no single "right" way. Adjust based on:
- Your working style
- Project complexity
- Task type (explore vs implement)
- Context sensitivity

Start with these practices, then adapt to what works for you.
