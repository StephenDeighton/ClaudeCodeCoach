---
slug: toggle-modes
title: Toggling Permission Modes
category: permission-modes
difficulty: beginner
keywords: permission modes toggle shift+tab normal plan auto
commands: ["Shift+Tab"]
related: [plan-mode, auto-mode, permission-config]
---

# Toggling Permission Modes

## Summary

Press `Shift+Tab` to cycle through Claude Code's three permission modes: Normal, Plan, and Auto. Each mode controls how Claude requests permission for actions, balancing autonomy with safety.

## The Three Modes

### Normal Mode (Default)
**Permission:** Ask before each action

```
User: Add authentication to the app
Claude: I'll need to:
        - Create auth.py
        - Modify main.py
        - Install dependencies

        Proceed? (y/n)
```

**Visual indicator:** No special indicator (default state)

### Plan Mode
**Permission:** Read-only, no file modifications

```
User: Add authentication to the app
Claude: [Reads files, analyzes code]
        Here's the plan I recommend...
        [Cannot modify files in this mode]
```

**Visual indicator:** `[PLAN MODE]` in status line

### Auto Mode
**Permission:** Execute without asking

```
User: Add authentication to the app
Claude: [Creates auth.py]
        [Modifies main.py]
        [Installs dependencies]
        Done. I've added authentication.
```

**Visual indicator:** `[AUTO MODE]` in status line (often in red/warning color)

## Cycling Through Modes

Press `Shift+Tab` repeatedly to cycle:

```
Normal → Plan → Auto → Normal → ...
```

Each press shows the new mode:
```
Switched to Plan Mode
Switched to Auto Mode
Switched to Normal Mode
```

## When to Use Each Mode

### Use Normal Mode When:
- **Default choice** - balanced control
- Learning a new codebase
- Working on critical files
- Uncertain about changes
- Want to review each step

**Example scenario:**
```
Working on production database schema
Want to see each migration before it runs
Normal mode: review every change
```

### Use Plan Mode When:
- Exploring unfamiliar code
- Understanding architecture
- Getting recommendations
- Researching approaches
- Safety is paramount

**Example scenario:**
```
New to this codebase
Want Claude to analyze and suggest
Plan mode: read-only exploration
Then switch to Normal to implement
```

### Use Auto Mode When:
- Repetitive tasks
- Well-defined operations
- High trust in Claude's judgment
- Bulk operations
- Time-sensitive work

**Example scenario:**
```
Creating 20 CRUD endpoints
All following same pattern
Auto mode: batch creation
```

## Mode Persistence

Modes persist across:
✅ Multiple commands in same session
✅ File operations
✅ Tool executions

Modes reset:
❌ New session (back to Normal)
❌ After `/exit` and restart

## Visual Indicators

### In Prompt
```
# Normal mode
>

# Plan mode
[PLAN] >

# Auto mode
[AUTO] >
```

### In Status Bar
```
# Check current mode
/status

Mode: Normal
```

## Safety Guardrails

Even in Auto mode, Claude won't:
- Delete entire directories without confirmation
- Run destructive commands (rm -rf, drop database)
- Modify .git/ directory
- Overwrite critical system files

These require explicit confirmation regardless of mode.

## Mode Recommendations by Task

| Task | Recommended Mode | Why |
|------|------------------|-----|
| Exploring codebase | Plan | Read-only safety |
| Implementing feature | Normal | Review each change |
| Bulk file operations | Auto | Efficiency |
| Debugging critical bug | Normal | Careful control |
| Refactoring | Normal | Review structural changes |
| Adding tests | Auto | Repetitive, low risk |
| Database migrations | Normal | High impact changes |
| Documentation updates | Auto | Low risk |

## Changing Mid-Task

You can switch modes at any time:

```
User: Create user authentication
[Claude in Normal mode, asking permissions]

User: [Shift+Tab] switched to Auto
[Claude continues without asking]
```

Previously asked permissions are remembered - switching modes doesn't restart the task.

## Mode with Skills

Skills respect the current permission mode:

```
# In Auto mode
/deploy-staging

# Skill runs without asking
[Deploying to staging...]
```

```
# In Plan mode
/deploy-staging

# Skill only plans, doesn't execute
Here's what would happen:
1. Build application
2. Upload to staging
3. Run migrations
```

## Command Line Mode Selection

Set mode at start:

```bash
# Start in Plan mode
claude --permission-mode plan

# Start in Auto mode
claude --permission-mode auto

# Start in Normal mode (default)
claude
```

## Permission Mode Config

Set default in settings:

```json
// settings.json
{
  "defaultPermissionMode": "normal"
}
```

Options: `"normal"`, `"plan"`, `"auto"`

## Common Patterns

### Explore-Then-Build

```
1. Start in Plan mode
   [Shift+Tab] → Plan
   "Show me how the auth system works"
   [Claude reads and explains]

2. Switch to Normal mode
   [Shift+Tab] → Normal
   "Now implement password reset"
   [Claude asks permission for each step]
```

### Trusted-Task-Batch

```
1. Switch to Auto mode
   [Shift+Tab] → Auto
   "Create test files for all 15 API endpoints"
   [Claude generates all without asking]

2. Back to Normal
   [Shift+Tab] → Normal
   "Now let's review and refine them"
```

## Keyboard Shortcuts Summary

```
Shift+Tab       Cycle modes
Ctrl+C          Interrupt (any mode)
/status         Check current mode
/exit           Exit (any mode)
```

## Troubleshooting

### "Mode won't change"

**Cause:** In middle of operation
**Fix:** Wait for current operation to complete, then toggle

### "Auto mode not working"

**Cause:** Blocked by safety settings or enterprise policy
**Fix:** Check `/allowed-tools` and permission settings

### "Plan mode executing changes"

**Cause:** Not actually in Plan mode
**Fix:** Press `Shift+Tab` until you see `[PLAN MODE]` indicator

## Best Practices

1. **Default to Normal** - Safe, balanced choice
2. **Plan for exploration** - Learn before changing
3. **Auto for repetition** - Batch similar tasks
4. **Switch deliberately** - Know why you're changing modes
5. **Visual check** - Always verify mode indicator
6. **Reset after auto** - Return to Normal after auto mode tasks

## Key Takeaway

`Shift+Tab` is your mode toggle. Normal mode (ask each time) is the safe default. Plan mode (read-only) for exploration. Auto mode (no asking) for trusted batch operations. Always know which mode you're in by checking the indicator.
