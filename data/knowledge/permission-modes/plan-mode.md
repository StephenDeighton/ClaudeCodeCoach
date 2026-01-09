---
slug: plan-mode
title: Plan Mode - Read-Only Exploration
category: permission-modes
difficulty: beginner
keywords: plan mode read-only explore safe analysis
commands: ["--permission-mode plan", "Shift+Tab"]
related: [toggle-modes, auto-mode]
---

# Plan Mode - Read-Only Exploration

## Summary

Plan mode is Claude Code's read-only safety mode where Claude can analyze your codebase and make recommendations without modifying any files. Perfect for exploration, learning unfamiliar code, and getting architectural advice.

## What Plan Mode Does

In Plan mode, Claude can:
✅ Read any file
✅ Analyze code structure
✅ Search codebase
✅ Explain architecture
✅ Suggest approaches
✅ Create implementation plans
✅ Answer questions
✅ Run read-only commands (ls, find, grep, git log)

In Plan mode, Claude cannot:
❌ Modify files
❌ Create files
❌ Delete files
❌ Run write operations
❌ Install packages
❌ Commit changes
❌ Execute potentially destructive commands

## Entering Plan Mode

### Via Keyboard

```bash
# In session, press Shift+Tab until Plan mode
[Shift+Tab]
Switched to Plan Mode
```

### Via Command Line

```bash
# Start session in Plan mode
claude --permission-mode plan
```

### Via Command

```bash
# Switch to Plan mode
/mode plan
```

## When to Use Plan Mode

### 1. Exploring Unknown Codebases

```
User: I'm new to this project. Help me understand the architecture.
[In Plan mode]
Claude: [Reads files, analyzes structure]
        This is a three-tier architecture:
        - Frontend: React in src/components/
        - API: FastAPI in src/api/
        - Database: PostgreSQL with SQLAlchemy models

        Entry point is main.py...
```

### 2. Getting Recommendations

```
User: How should I implement user authentication?
[In Plan mode]
Claude: [Analyzes existing code]
        Based on your stack, I recommend:

        1. Use JWT tokens (matches your REST API)
        2. Store in PostgreSQL user table
        3. Hash passwords with bcrypt

        Here's the implementation plan: ...
```

### 3. Code Review

```
User: Review the payment processing code for issues
[In Plan mode]
Claude: [Reads payment code]
        I found 3 potential issues:

        1. Missing error handling on line 45
        2. SQL injection vulnerability in query
        3. No rate limiting on payment endpoint

        Recommendations: ...
```

### 4. Before Major Changes

```
User: Before I refactor the auth system, analyze what would be affected
[In Plan mode]
Claude: [Scans for dependencies]
        The auth system is used by:
        - 12 API endpoints
        - 3 middleware functions
        - 2 frontend components

        Impact analysis: ...
```

## Plan Mode Workflow

### Typical Pattern

```
1. Enter Plan mode
   [Shift+Tab] → Plan

2. Explore and plan
   "Analyze the database schema"
   "Suggest improvements"
   [Claude provides detailed analysis]

3. Switch to Normal mode
   [Shift+Tab] → Normal

4. Implement the plan
   "Implement the improvements you suggested"
   [Claude makes changes with your approval]
```

## Visual Indicators

When in Plan mode, you'll see:

```
[PLAN MODE] >
```

Status check confirms:
```bash
/status

Mode: Plan
Can read: ✅
Can write: ❌
```

## Benefits of Plan Mode

### Safety

No risk of accidental changes:
- Can't break working code
- Can't delete files
- Can't introduce bugs
- Perfect for learning

### Clarity

Read-only focus produces better analysis:
- Not distracted by "how to implement"
- Focus on "what exists" and "what should be"
- Clearer recommendations

### Learning

Great for understanding codebases:
- Ask questions freely
- No pressure to change things
- Explore without consequences

## Example Sessions

### Example 1: New to Project

```
claude --permission-mode plan

User: This is my first time with this codebase.
      Walk me through it.

Claude: [In Plan mode]
        Let me explore the structure...

        [Reads package.json, main files]

        This is a Node.js project with:
        - Express backend
        - MongoDB database
        - JWT authentication

        Main entry: server.js
        Routes defined in: routes/
        Models in: models/

        Would you like me to explain any specific area?

User: Yes, explain the authentication flow

Claude: [Reads auth files]
        Here's how authentication works:
        ...
```

### Example 2: Before Refactoring

```
[Shift+Tab] → Plan Mode

User: I want to refactor the user service. What would break?

Claude: [Analyzes dependencies]
        The user service is imported by:
        - auth_controller.js (4 places)
        - admin_routes.js (2 places)
        - profile_controller.js (6 places)

        If you change the interface, you'll need to update
        these 12 call sites.

        I recommend:
        1. Keep the existing interface
        2. Refactor internal implementation
        3. Add new methods without removing old ones
```

### Example 3: Security Audit

```
[Shift+Tab] → Plan Mode

User: Check for security vulnerabilities

Claude: [Scans codebase]
        Found 4 security concerns:

        1. SQL injection in user_search.py line 23
           Risk: High
           Fix: Use parameterized queries

        2. Missing rate limiting on /api/login
           Risk: Medium
           Fix: Add express-rate-limit

        ...
```

## Plan Mode with Skills

Skills in Plan mode behave differently:

```markdown
# .claude/skills/test.md
Run test suite and report results
```

**Normal mode:** Runs tests
**Plan mode:** Shows what tests would be run

```
[PLAN MODE]
User: /test

Claude: In Plan mode - showing test plan:
        Would execute: npm test
        Test files found:
        - tests/auth.test.js (12 tests)
        - tests/api.test.js (8 tests)
        - tests/database.test.js (15 tests)

        Total: 35 tests
```

## Limitations

### Can't Execute Plans

Plans are just recommendations:

```
[PLAN MODE]
Claude: Here's the implementation plan for authentication:
        1. Create models/user.js
        2. Add routes/auth.js
        3. Install bcrypt and jsonwebtoken

User: Do it
Claude: I'm in Plan mode - I can't modify files.
        Press Shift+Tab to switch to Normal mode.
```

### Can't Run Generators

Code generators won't work:

```
[PLAN MODE]
User: Generate boilerplate for a REST API

Claude: I can describe what should be generated,
        but can't create files in Plan mode.

        Switch to Normal mode to generate files.
```

## Exiting Plan Mode

Three ways out:

### 1. Toggle to Normal
```
[Shift+Tab]
Switched to Normal Mode
```

### 2. Toggle to Auto
```
[Shift+Tab] [Shift+Tab]
Switched to Auto Mode
```

### 3. Command
```
/mode normal
```

## Plan Mode Anti-Patterns

### ❌ Staying in Plan Mode Too Long

```
# Been in Plan mode for 30 minutes
# Asked 50 questions
# Switch to Normal and implement!
```

Plan mode is for planning, not doing. After 10-15 minutes of exploration, switch to Normal and implement.

### ❌ Using Plan Mode for Implementation

```
[PLAN MODE]
User: Add authentication

Claude: I can't add files in Plan mode.

User: Just tell me the code

Claude: [Provides code]

User: Paste it into files

# Better: Switch to Normal mode!
```

### ❌ Expecting Execution

```
[PLAN MODE]
User: /deploy

Claude: Can't deploy in Plan mode - read-only.

# Plan mode doesn't execute, only explains
```

## Configuration

### Default to Plan Mode

```json
// settings.json
{
  "defaultPermissionMode": "plan"
}
```

Now `claude` starts in Plan mode by default.

### Allowed Tools in Plan

```json
// settings.json
{
  "planModeTools": [
    "read",
    "grep",
    "list",
    "analyze"
  ]
}
```

## Pro Tips

1. **Start sessions in Plan** - Explore before building
2. **Use for code review** - Read-only is perfect for review
3. **Safe experimentation** - Ask "what if" questions without risk
4. **Understand before changing** - Always plan first for unfamiliar code
5. **Pair with Normal** - Plan in Plan mode, execute in Normal mode

## Quick Reference

```bash
# Enter Plan mode
claude --permission-mode plan
[Shift+Tab]  # Toggle to Plan
/mode plan

# Check if in Plan mode
/status

# Exit Plan mode
[Shift+Tab]  # Toggle to Normal
/mode normal

# What Plan mode can do
Read files: ✅
Analyze code: ✅
Make plans: ✅
Modify files: ❌
Execute commands: ❌
```

## Key Takeaway

Plan mode is your safety net for exploration and analysis. Use it when you want to understand code, get recommendations, or review changes without any risk of modification. Perfect for "thinking before doing." Always switch to Normal or Auto mode when you're ready to actually make changes.
