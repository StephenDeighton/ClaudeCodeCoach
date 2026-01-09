---
slug: resume-session
title: Resuming Sessions
category: session-management
difficulty: beginner
keywords: resume continue session restore context memory
commands: ["claude --resume", "/resume"]
related: [start-session, clear-context]
---

# Resuming Sessions

## Summary

Resume a previous Claude Code session to continue exactly where you left off, with full conversation history and context preserved. Use `claude --resume` or the `/resume` command to restore your last session.

## When to Resume

**Resume when:**
- You closed the terminal but want to continue the same work
- Session ended unexpectedly (crash, network issue)
- You took a break and want to pick up where you left off
- The previous conversation context is still relevant
- Working on the same feature across multiple work sessions

**Don't resume when:**
- Starting a completely different task or feature
- Context from previous session is no longer relevant
- Previous session was working on a different project
- You want fresh context for a new approach

## How to Resume

### From Terminal (Recommended)

```bash
# Resume most recent session
claude --resume

# Or use the /resume command once inside Claude
claude
> /resume
```

### What Gets Restored

When you resume a session:

✅ **Full conversation history**: Every message and response
✅ **File changes discussed**: Claude remembers what was modified
✅ **Context and decisions**: Prior reasoning and choices
✅ **Tool usage history**: What commands were run
✅ **Project state**: Current working directory and files

❌ **Not restored:**
- Uncommitted file changes (use git)
- Terminal state outside Claude
- Environment variables set during session

## Resume Limitations

### Time Decay
- Sessions older than 24 hours may have degraded context
- Very old sessions (>1 week) may not resume reliably
- Recent sessions (<1 hour) resume perfectly

### Context Window
If the previous session filled the context window, resuming adds to it. You may need to `/clear` early in the resumed session to make room for new work.

### File Changes
Claude remembers discussing changes but doesn't track actual file state. If you manually edited files between sessions, mention it:

```
Me: I resumed the session. FYI, I manually fixed the
    bug in auth.py while you were offline.

Claude: Thanks for the update. I see you fixed the
        authentication issue. Let's continue with...
```

## Resume Best Practices

### Start with a Status Update

When you resume, briefly remind Claude what's next:

```
Good: "Resuming. Let's continue implementing the
       payment webhook handler."

Better: "Resuming. I tested the auth changes and they
        work. Now let's add the payment webhook."
```

### Check Context Quality

If resumed session feels confused:

```bash
# Clear to make room for new work
/clear

# Or start fresh if too much accumulated context
/exit
claude  # Start new session
```

### Don't Resume Across Projects

If you switched projects, start fresh:

```bash
# Wrong - resuming in different directory
cd ~/other-project
claude --resume  # Still has old project context!

# Right - fresh start in new project
cd ~/other-project
claude  # Clean start with new project
```

## Resume vs Clear vs Fresh

**Resume**: Continue exact same conversation
- Use when: Picking up where you left off
- Pros: No need to re-explain context
- Cons: Accumulated context bloat

**Clear** (`/clear`): Same session, lighter context
- Use when: Same session but need fresh thinking
- Pros: Clears clutter, keeps current work
- Cons: Loses detailed history

**Fresh** (`claude`): Brand new session
- Use when: Different task or project
- Pros: Cleanest context, fastest performance
- Cons: No memory of previous work

## Common Scenarios

### Scenario 1: Terminal Crashed

```bash
# Terminal died mid-implementation
# Just resume - everything preserved
claude --resume
> Continuing the user registration feature...
```

### Scenario 2: Took a Break

```bash
# Worked for 2 hours, took lunch, coming back
claude --resume
> Let's finish the API tests we were writing
```

### Scenario 3: Session Got Confused

```bash
# Session feels lost or sluggish
claude --resume
> /clear  # Clean up context but stay in session
> Now let's refocus on the checkout flow...
```

### Scenario 4: Next Day, Different Feature

```bash
# Don't resume - too much context, different task
claude  # Fresh start
> Today let's work on the email notifications
```

## Troubleshooting Resume

### "No session to resume"

This means:
- No previous session exists
- Session history was cleared
- Running from different directory

**Fix**: Start a fresh session with `claude`

### Resumed session is slow

The previous session filled the context window.

**Fix**:
```bash
/clear  # Clear some context
# Or exit and start fresh
```

### Resumed session seems confused

Context from old session is interfering.

**Fix**:
```bash
# Give explicit context
> FYI, I'm resuming but we're switching to a
  different feature now. Ignore the previous
  discussion about X.

# Or start fresh
/exit
claude
```

## Session Persistence

Sessions are stored locally:
- Location: `~/.claude/sessions/`
- Format: JSONL (JSON Lines)
- Retention: Automatic cleanup of old sessions

You don't need to manage session files manually.

## Advanced: Multiple Sessions

If you have multiple projects:

```bash
# Project A
cd ~/project-a
claude
# ... work work ...
/exit

# Project B (different session)
cd ~/project-b
claude
# Fresh session, no memory of Project A

# Resume Project A later
cd ~/project-a
claude --resume  # Back to Project A context
```

Each directory can have its own session history.

## Quick Reference

```bash
# Resume from CLI
claude --resume

# Resume from within Claude
/resume

# Check if session exists
claude --list-sessions

# Clear old sessions
claude --clear-sessions
```

## Key Takeaway

Resume is powerful for continuing work, but don't abuse it. If the resumed session feels confused or slow, start fresh. A clean session is often more productive than fighting with accumulated context.
