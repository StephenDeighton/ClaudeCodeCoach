---
slug: exit-session
title: Exiting Sessions Cleanly
category: session-management
difficulty: beginner
keywords: exit quit close end session Ctrl+D
commands: ["/exit", "Ctrl+D"]
related: [start-session, resume-session]
---

# Exiting Sessions Cleanly

## Summary

Exit Claude Code sessions cleanly using `/exit` or `Ctrl+D` to ensure proper cleanup and session saving. Clean exits allow you to resume later and prevent corruption of session history.

## How to Exit

### Method 1: /exit Command (Recommended)

```bash
> /exit
Saving session...
Session saved. You can resume with 'claude --resume'
Goodbye!
```

This is the cleanest way to exit:
- Saves session state properly
- Flushes any pending operations
- Ensures session can be resumed

### Method 2: Ctrl+D (Unix Standard)

Press `Ctrl+D` to send EOF (End of File):
- Works like `/exit`
- Standard terminal exit pattern
- Triggers cleanup handlers

### Method 3: Ctrl+C (Emergency Only)

Press `Ctrl+C` to interrupt:
- Use only if Claude is stuck
- May not save session properly
- Forces immediate termination

**When to use Ctrl+C:**
- Claude stopped responding
- Caught in infinite loop
- Need emergency exit

**Avoid using Ctrl+C when:**
- Normal exit with `/exit` works
- Just want to pause (use `/clear` instead)
- In middle of file operations

## Clean Exit vs Dirty Exit

### Clean Exit (Good)
```bash
> /exit
✓ Session saved
✓ History preserved
✓ Can resume later
```

### Dirty Exit (Bad)
```bash
> [closes terminal window]
✗ Session may not save
✗ History incomplete
✗ Resume may fail
```

## When to Exit

**Exit when:**
- Done working for now
- Switching to different project
- Session is complete
- Context is no longer relevant

**Don't exit when:**
- Just want to clear context (use `/clear`)
- Want to pause briefly (close terminal, resume later)
- In middle of multi-step operation (finish first)

## Exit vs Clear

Many users exit when they should clear:

**Clear** (`/clear`): Stay in session, remove clutter
```bash
> /clear
Context cleared. Session continues.
> Let's start the next feature...
```

**Exit** (`/exit`): End session completely
```bash
> /exit
Session ended. Must restart or resume.
```

**Decision guide:**
- Same project, different task → `/clear`
- Different project → `/exit`
- Done for the day → `/exit`
- Just need focus → `/clear`

## What Happens on Exit

When you exit cleanly:

1. **Session Save**: Conversation written to disk
2. **Cleanup**: Temporary files removed
3. **State Preservation**: Context and history stored
4. **Resource Release**: Connections closed properly
5. **Resume Ready**: Session marked for potential resume

Location: `~/.claude/sessions/{session-id}.jsonl`

## After Exit

You can:

**Resume the session:**
```bash
claude --resume
```

**Start fresh:**
```bash
claude
```

**Check session history:**
```bash
claude --list-sessions
```

## Exit with Uncommitted Work

If you have uncommitted changes, Claude may remind you:

```bash
> /exit
⚠️  You have uncommitted changes:
    - modified: src/auth.py
    - modified: tests/test_auth.py

Exit anyway? (yes/no)
```

Options:
- Commit the changes first
- Type `yes` to exit anyway
- Type `no` to stay and commit

## Common Mistakes

### ❌ Closing Terminal Instead of Exiting

Don't close the terminal window directly. Use `/exit` first.

**Why it matters:**
- Session may not save
- Cleanup may not run
- Resume might fail

**Fix:**
```bash
# Always exit properly
> /exit
# Then close terminal
```

### ❌ Exiting During Operations

Don't exit while Claude is:
- Writing files
- Running commands
- Processing large operations

**Wait for completion:**
```bash
> [Claude is writing multiple files...]
# DON'T exit yet - let it finish
> [Operation complete]
> /exit
```

### ❌ Using Exit as Clear

If you just want fresh thinking, use `/clear` not `/exit`:

```bash
# Wrong
> /exit
$ claude
> Let's continue with the API...
# Lost all context!

# Right
> /clear
> Let's continue with the API...
# Same session, fresh context
```

## Force Exit (Emergency)

If Claude is truly stuck:

1. Try `/exit` first (wait 5 seconds)
2. If no response, try `Ctrl+C` once
3. If still stuck, `Ctrl+C` twice rapidly
4. Last resort: Close terminal (session may not save)

```bash
# Stuck session
> /exit
[no response after 5 seconds]

# Force interrupt
^C  # Press Ctrl+C
Interrupted. Cleaning up...
Session saved.
```

## Session Cleanup

Old sessions auto-cleanup after:
- 30 days of inactivity
- Manual cleanup with `--clear-sessions`
- Disk space threshold reached

You don't need to manually delete session files.

## Exit in Different Modes

### Auto Mode
```bash
# Exit works same in auto mode
> /exit
Saving session...
```

### Plan Mode
```bash
# Plan mode can exit normally
> /exit
Exiting plan mode and session...
```

### With Active Subagents
```bash
> /exit
⚠️  Active subagents will be terminated.
Continue? (yes/no)
> yes
Stopping subagents...
Session saved.
```

## Quick Reference

```bash
# Clean exit
/exit
Ctrl+D

# Emergency exit
Ctrl+C

# Exit and clear history
/exit --no-save

# Check what would be saved
/exit --dry-run

# Force exit without prompts
/exit --force
```

## Exit Shortcuts by Shell

Different shells may have different shortcuts:

**Bash/Zsh:**
- `Ctrl+D` - Exit
- `Ctrl+C` - Interrupt
- `Ctrl+Z` - Suspend (don't use)

**Fish:**
- Same as Bash/Zsh

**PowerShell (Windows):**
- `Ctrl+D` - Exit
- `Ctrl+C` - Interrupt

## Best Practices

1. **Always exit cleanly** - Use `/exit` or `Ctrl+D`
2. **Commit before exit** - Don't leave uncommitted work
3. **Clear not exit** - Use `/clear` for fresh thinking in same session
4. **Check status** - Review what you're leaving before exit
5. **Resume awareness** - Know if you'll want to resume or not

## Exit Checklist

Before exiting:
- [ ] Work is committed or saved
- [ ] No operations in progress
- [ ] Decided: resume later or start fresh?
- [ ] Used `/exit` or `Ctrl+D`
- [ ] Waited for "Session saved" message

## Key Takeaway

Exit cleanly with `/exit` or `Ctrl+D` to preserve your session and enable resuming. Don't confuse exiting with clearing - exit ends the session, clear just refreshes context within the same session.
