---
slug: auto-mode
title: Auto Mode - Autonomous Execution
category: permission-modes
difficulty: intermediate
keywords: auto mode autonomous execute batch automate
commands: ["--permission-mode auto", "Shift+Tab"]
related: [toggle-modes, plan-mode, permission-config]
---

# Auto Mode - Autonomous Execution

## Summary

Auto mode allows Claude to execute operations autonomously without asking permission for each action. Use it for well-defined, repetitive, or batch operations where you trust Claude's judgment and want maximum efficiency.

## What Auto Mode Does

In Auto mode, Claude executes immediately:
✅ Creates files
✅ Modifies files
✅ Deletes files (with safety limits)
✅ Runs commands
✅ Installs packages
✅ Commits changes
✅ Batch operations

Auto mode still has safety guards:
⚠️ Confirms truly destructive operations
⚠️ Won't delete entire directories
⚠️ Won't run `rm -rf /`
⚠️ Won't modify .git/ internals
⚠️ Respects permission-config rules

## Entering Auto Mode

### Via Keyboard

```bash
# Press Shift+Tab twice from Normal
[Shift+Tab] → Plan Mode
[Shift+Tab] → Auto Mode
```

### Via Command Line

```bash
# Start in Auto mode
claude --permission-mode auto
```

### Via Command

```bash
/mode auto
```

## Visual Indicators

Auto mode shows clear warnings:

```
[AUTO MODE] >
```

Often displayed in red or warning color to remind you of the autonomous behavior.

## When to Use Auto Mode

### 1. Repetitive Tasks

```
User: Create CRUD endpoints for User, Product, Order, and Invoice

[AUTO MODE]
Claude: [Creates user_routes.js]
        [Creates product_routes.js]
        [Creates order_routes.js]
        [Creates invoice_routes.js]
        [Creates corresponding controllers]
        [Creates test files]

        Done. Created 12 files for CRUD endpoints.
```

### 2. Batch Operations

```
User: Add TypeScript types to all 30 JavaScript files in src/

[AUTO MODE]
Claude: [Converts file1.js → file1.ts]
        [Converts file2.js → file2.ts]
        ...
        [Updates 30 files]

        Conversion complete. All files now TypeScript.
```

### 3. Well-Defined Processes

```
User: Set up a new React component with tests, styles, and stories

[AUTO MODE]
Claude: [Creates Button.jsx]
        [Creates Button.test.jsx]
        [Creates Button.module.css]
        [Creates Button.stories.jsx]

        Component ready.
```

### 4. Time-Critical Work

```
User: Fix the critical production bug - payment processor failing

[AUTO MODE]
Claude: [Analyzes issue]
        [Patches payment_processor.py]
        [Runs tests]
        [All tests pass]

        Bug fixed. Patch ready for deployment.
```

## Auto Mode Workflow

### Typical Pattern

```
1. Define clear task
   "Create test files for all API endpoints"

2. Switch to Auto mode
   [Shift+Tab] [Shift+Tab] → Auto

3. Execute
   [Claude creates all files without asking]

4. Review results
   Check that everything looks correct

5. Switch back to Normal
   [Shift+Tab] → Normal
```

## Benefits of Auto Mode

### Speed

No permission interruptions:
```
Normal mode: 20 files = 20 confirmations
Auto mode: 20 files = 0 confirmations
```

### Flow

Maintain focus on goals:
```
User: Implement the entire auth system
[AUTO MODE]
# Claude handles all details
# You stay focused on architecture
```

### Batch Efficiency

Perfect for bulk operations:
```
User: Migrate all 50 components to new pattern
[AUTO MODE]
# Completes in one go
# No 50 individual approvals
```

## Risks of Auto Mode

### Unintended Changes

Claude might:
- Misunderstand requirements
- Make assumptions
- Change the wrong files
- Introduce bugs

**Mitigation:** Use Auto mode only when:
- Task is well-defined
- You trust the operation
- Changes are reviewable
- Easy to undo (git)

### Cascade Errors

One mistake can propagate:
```
[AUTO MODE]
# Wrong assumption about API structure
# Updates 20 files with wrong pattern
# Now 20 files need fixing
```

**Mitigation:**
- Start with smaller batch
- Review before large operations
- Have git safety net

### Loss of Control

Can't intervene mid-process:
```
[AUTO MODE]
Claude: [Creating file 1/30]
        [Creating file 2/30]
        [Creating file 3/30 - WRONG APPROACH!]
        [Creating file 4/30]
        ...

User: Stop! Wrong approach!
# But files 1-15 already created
```

**Mitigation:**
- Use Ctrl+C to interrupt
- Switch to Normal for uncertain tasks

## Auto Mode with Skills

Skills become fully autonomous:

```markdown
# .claude/skills/deploy.md
Build, test, and deploy to staging
```

```
[AUTO MODE]
User: /deploy

# No confirmation - executes entire deployment
Claude: [Runs build]
        [Runs tests]
        [Deploys to staging]
        [Verifies deployment]

        Deployment complete.
```

## Safety Guardrails

Even in Auto mode, destructive operations confirm:

```
[AUTO MODE]
User: Delete the database

Claude: ⚠️  This would delete production database.
        Confirm? (yes/no)

# Still asks for truly dangerous operations
```

Protected operations:
- Database drops
- Directory deletion (>100 files)
- Force push to main
- rm -rf on large paths

## Configuration

### Global Auto Mode

```json
// settings.json
{
  "defaultPermissionMode": "auto"
}
```

⚠️ Not recommended - too risky as default

### Per-Project Auto Mode

```json
// .claude/config.json
{
  "permissionMode": "auto",
  "autoModeFor": [
    "file_creation",
    "testing"
  ]
}
```

### Allowed Tools in Auto

```json
// settings.json
{
  "autoModeRestrictions": {
    "noDelete": true,
    "noInstall": false,
    "requireConfirm": ["deploy", "database"]
  }
}
```

## Auto Mode Best Practices

### 1. Clear Instructions

```
Good: "Create React component with test,
       styles, and story file for UserCard"

Bad: "Make the UserCard better"
```

### 2. Review After Execution

```
[AUTO MODE]
User: Create 10 API endpoints
Claude: [Creates all endpoints]

User: [Switch to Normal]
      [Review git diff]
      [Test the endpoints]
```

### 3. Use with Git Safety Net

```bash
# Before Auto mode batch operation
git commit -m "Before batch changes"

[AUTO MODE]
# Make changes

# Review
git diff
# If bad:
git reset --hard HEAD
```

### 4. Start Small

```
# Don't jump straight to:
User: Refactor entire application to new pattern

# Start with:
User: Refactor one module to new pattern
[Review results]
# Then scale up
```

### 5. Interrupt When Needed

```
[AUTO MODE]
Claude: [Starting batch operation]

User: [Notices wrong approach]
      [Ctrl+C to interrupt]
      [Shift+Tab to switch to Normal]
```

## Common Scenarios

### Scenario 1: Test File Generation

```
[Shift+Tab][Shift+Tab] → Auto Mode

User: Generate test files for all 15 API routes

Claude: [Creates test_user_routes.js]
        [Creates test_product_routes.js]
        ...
        [15 test files created]

        All test files created with base cases.
```

### Scenario 2: Code Style Migration

```
[AUTO MODE]

User: Convert all var declarations to const/let in src/

Claude: [Scans for var usage]
        [Updates 45 files]
        [Fixes 237 var declarations]

        Migration complete.
```

### Scenario 3: Documentation Generation

```
[AUTO MODE]

User: Add JSDoc comments to all public functions

Claude: [Analyzes functions]
        [Adds documentation]
        [Updates 23 files]

        Documentation added.
```

## When NOT to Use Auto Mode

❌ **Unfamiliar codebases** - Too risky without understanding
❌ **Complex logic changes** - Need to review each step
❌ **Database migrations** - Too critical for automation
❌ **Production deployments** - Need manual verification
❌ **Security-sensitive code** - Review is essential
❌ **Unclear requirements** - Will make wrong assumptions

## Recovering from Auto Mode Mistakes

### If caught early:

```
[AUTO MODE]
Claude: [Created file 1]
        [Created file 2 - WRONG]

User: Ctrl+C [interrupt]
      git checkout file1 file2
```

### If completed:

```
# Check what changed
git diff

# If acceptable:
git add .
git commit

# If unacceptable:
git reset --hard HEAD
```

### If partially acceptable:

```
# Keep some changes
git add goodfile1.js goodfile2.js
git checkout badfile3.js badfile4.js
```

## Monitoring Auto Mode

### Watch for:
- Files being created/modified
- Commands being executed
- Unexpected behavior
- Error messages

### Intervene if:
- Wrong approach detected
- Errors occurring
- Scope creeping beyond intent
- Performance degrading

## Auto Mode + Subagents

Auto mode with subagents is powerful but risky:

```
[AUTO MODE]
User: Run parallel refactoring with subagents

# Multiple autonomous agents making changes
# Very fast but hard to monitor
# Use with caution
```

## Quick Reference

```bash
# Enter Auto mode
claude --permission-mode auto
[Shift+Tab] [Shift+Tab]
/mode auto

# Visual indicator
[AUTO MODE] >

# Interrupt
Ctrl+C

# Exit Auto mode
[Shift+Tab] → Normal
/mode normal

# Check status
/status
```

## Key Takeaway

Auto mode is powerful for well-defined, repetitive tasks where you trust Claude's execution. Always have a git safety net, start with small batches, and be ready to interrupt if things go wrong. Default to Normal mode - use Auto mode deliberately and temporarily for specific batch operations.
