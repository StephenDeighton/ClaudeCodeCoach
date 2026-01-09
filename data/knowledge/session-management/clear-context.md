---
slug: clear-context
title: Clearing Context
category: session-management
difficulty: beginner
keywords: clear context reset refresh clean session
commands: ["/clear"]
related: [start-session, fresh-vs-clear]
---

# Clearing Context

## Summary

Use `/clear` to remove accumulated context and conversation history from the current session while staying in the same session. This refreshes Claude's "mental state" without losing your project setup or starting over.

## What /clear Does

When you run `/clear`:

✅ **Clears:**
- Previous conversation messages
- Accumulated context bloat
- Old file contents from memory
- Previous tool outputs
- Reasoning artifacts

✅ **Preserves:**
- Your CLAUDE.md project context
- Available skills
- Current working directory
- Project configuration
- Session identity (for resume)

## When to Clear

**Clear when:**
- Session feels sluggish or slow
- Claude seems confused about earlier context
- You're starting a new task in the same project
- Context has accumulated but project is the same
- Responses are getting worse/confused

**Don't clear when:**
- In the middle of implementing something
- Claude needs the previous context to continue
- About to reference prior conversation
- Just started the session (nothing to clear)

## Clear vs Start Fresh

Many users start new sessions when they should just clear:

### Clear (Within Session)
```bash
> /clear
Context cleared. CLAUDE.md still loaded.
> Let's build the user profile page
```
**Use for:** New task, same project

### Fresh Session
```bash
> /exit
$ claude
> Let's build the user profile page
```
**Use for:** Different project or complete restart

## Performance Impact

Clearing context dramatically improves performance:

**Before clear** (100,000 tokens context):
- Response time: 8-12 seconds
- Context bloated with old conversation
- Responses may be confused

**After clear** (5,000 tokens context):
- Response time: 2-4 seconds
- Fresh context, only essentials
- Responses focused and accurate

## How Context Accumulates

During a session, context grows from:
1. **Messages:** Every message you send
2. **Responses:** Every response Claude generates
3. **Files read:** Contents of files Claude examines
4. **Tool outputs:** Results from commands run
5. **Thinking:** Extended reasoning (if enabled)

Example accumulation:
```
Start:     5,000 tokens (CLAUDE.md + skills)
+10 messages: +20,000 tokens
+file reads:  +30,000 tokens
+tool outputs:+15,000 tokens
Total:    70,000 tokens in context
```

At this point, `/clear` brings you back to 5,000 tokens.

## Clear Strategies

### Strategic Clearing

Clear at natural breakpoints:

```bash
# Just finished implementing auth
> The authentication is working!
> /clear
> Now let's implement the payment flow
```

### Preventive Clearing

Clear before starting major work:

```bash
# About to start complex feature
> /clear
> Let's implement the entire checkout process.
  I want to start with fresh context.
```

### Recovery Clearing

Clear when session degrades:

```bash
# Claude seems confused
> /clear
> Let me restate what we're working on...
```

## What to Say After Clear

After clearing, provide fresh context about what you're doing:

**Good:**
```bash
> /clear
> We're building a user dashboard. I need tables
  for recent activity, profile summary, and settings.
```

**Bad:**
```bash
> /clear
> Continue what we were doing
# Claude doesn't remember "what we were doing"!
```

## Clear with Context Handoff

If you need to preserve key decisions:

```bash
# Before clear - save important points
> The decisions we made:
  - Use JWT for auth
  - PostgreSQL for user data
  - Redis for sessions
> /clear
> Now building the auth system with those choices
```

Or better, commit decisions to CLAUDE.md:

```markdown
## Decisions Made
- Auth: JWT tokens
- DB: PostgreSQL
- Cache: Redis
```

Then clear freely - CLAUDE.md persists.

## Clear Frequency

**Too frequent** (every 3-5 messages):
- Wastes time reestablishing context
- Claude can't build on previous work
- You repeat yourself constantly

**Too rare** (never clearing):
- Sessions become sluggish
- Context bloat degrades quality
- Eventually hit context limits

**Just right** (every 15-30 messages or at task boundaries):
- Good performance maintained
- Context stays relevant
- Natural workflow rhythm

## Signs You Need to Clear

Watch for these signals:

1. **Slowness:** Responses taking >10 seconds
2. **Confusion:** Claude references old, irrelevant context
3. **Repetition:** Claude repeating things already done
4. **Quality drop:** Responses becoming generic or confused
5. **Context errors:** "Based on our earlier discussion about X" when X was 50 messages ago

## Clear in Different Workflows

### During Feature Development

```bash
# Feature research phase
[30 messages exploring options]
> /clear
# Implementation phase with chosen approach
[20 messages implementing]
> /clear
# Testing phase
[15 messages testing and fixing]
```

### During Debugging

```bash
# Initial investigation
[25 messages examining logs, tracing code]
> /clear
# Focused fix attempt
> The issue is in payment_processor.py line 45.
  Let's fix it.
```

### During Refactoring

```bash
# Reading and understanding code
[20 messages exploring codebase]
> /clear
# Executing refactor plan
> Here's the refactor plan. Let's execute it.
```

## Clear vs Thinking

If you have extended thinking enabled:

```bash
# Extended thinking accumulates extra context
[thinking tokens: 20,000]
[conversation: 30,000]
Total: 50,000 tokens

> /clear
# Back to baseline
[thinking cleared too]
```

Clearing removes both conversation and thinking artifacts.

## Automatic Clear

Claude Code doesn't auto-clear, but you can create a skill for it:

```markdown
# .claude/skills/start-fresh.md
---
description: Clear context and start fresh on new task
---

1. Run /clear to remove accumulated context
2. Ask user what they want to work on
3. Begin with fresh context and clear focus
```

Then use `/start-fresh` when transitioning between tasks.

## Clear with Subagents

Clearing the main session doesn't affect running subagents:

```bash
# Main session
> /clear

# Subagents keep their context
# They're independent sessions
```

Each subagent has its own context and must be cleared separately if needed.

## Common Mistakes

### ❌ Clearing mid-implementation

```bash
> Let's refactor auth.py
[Claude starts refactoring]
> /clear  # DON'T!
> Uh, what were we doing?
```

Wait until the task completes.

### ❌ Never clearing

```bash
# 200 messages later...
> Why are responses so slow?
# Context is overloaded!
```

Clear periodically at task boundaries.

### ❌ Clearing without context handoff

```bash
> /clear
> Continue
# Claude has no idea what to continue!
```

Always re-explain what you're working on.

## Quick Reference

```bash
# Clear context
/clear

# Clear and check status
/clear
/status

# Clear and state new goal
/clear
> Building the email notification system

# Clear for fresh start on same project
/clear
> Fresh start. Let's tackle the API tests.
```

## Best Practices

1. **Clear at boundaries:** Between features, not mid-task
2. **Restate goals:** After clear, say what you're doing
3. **Watch performance:** If slow, consider clearing
4. **Don't overdo it:** Clearing every few messages wastes time
5. **Use CLAUDE.md:** Persistent decisions go there, not in context

## Key Takeaway

`/clear` is your tool for maintaining a healthy session. Clear when you feel context bloat or when transitioning between tasks, but always reestablish what you're working on after clearing. Think of it as a mental "palate cleanser" between courses of work.
