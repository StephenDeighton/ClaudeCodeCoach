---
slug: skills-vs-commands
title: Skills vs Commands
category: feature-selection
difficulty: beginner
keywords: skills commands difference comparison decision
commands: []
related: [feature-decision-guide, creating-skills, creating-commands]
---

# Skills vs Commands

## Summary

Skills and commands both extend Claude Code, but serve different purposes. Commands return quick data, while skills execute multi-step workflows with conversation context.

## Key Differences

| Aspect | Command | Skill |
|--------|---------|-------|
| **Duration** | < 2 seconds | 1-10 minutes |
| **Steps** | Single operation | Multiple steps |
| **Context** | No conversation context | Uses conversation |
| **Interactive** | No | Yes |
| **Implementation** | Script (bash/python/node) | Markdown with instructions |
| **Output** | Data/text | Results + actions |

## Commands

### Purpose
Return data or perform single operation instantly.

### Characteristics
```bash
# Fast execution
/git-status      # Returns in <1s

# Single purpose
/test-count      # Counts, returns number

# No conversation
# Doesn't remember previous messages

# No decisions
# Fixed logic, no branching
```

### Example Command
```bash
#!/bin/bash
# .claude/commands/test-count.sh

find tests -name "*.test.ts" | wc -l
```

Usage:
```bash
/test-count
# Output: 42
```

### When to Use Commands
- Getting status or counts
- Listing information
- Quick calculations
- Simple checks

## Skills

### Purpose
Execute multi-step workflows with user guidance.

### Characteristics
```markdown
# Multi-step process
/commit
1. Review changes
2. Analyze git diff
3. Suggest commit message
4. Create commit

# Uses conversation
# References what user said earlier

# Interactive
# Asks questions if unclear

# Makes decisions
# Adapts based on context
```

### Example Skill
```markdown
---
name: commit
description: Create smart git commits
tools: [bash, read, git]
---

# Smart Commit

## Process
1. Check git status
2. Review changed files
3. Analyze changes
4. Generate commit message following conventions
5. Confirm with user
6. Create commit
```

Usage:
```bash
User: I fixed the login bug
/commit

Claude: Reviewed changes in auth.ts
Suggested: "fix(auth): resolve token validation issue"
Proceed? (y/n)
```

## Comparison Examples

### Example: Git Status

**As Command** (Better):
```bash
#!/bin/bash
# Fast, simple
git status --short
```

**As Skill** (Overkill):
```markdown
# Unnecessary multi-step for simple operation
1. Check git status
2. Format output
3. Analyze status
...
```

**Winner**: Command ✓

### Example: Deployment

**As Command** (Too Simple):
```bash
#!/bin/bash
# Missing safety checks
npm run deploy
```

**As Skill** (Better):
```markdown
# Multi-step with checks
1. Check branch (must be main)
2. Check tests (must pass)
3. Check build (must succeed)
4. Confirm with user
5. Deploy
6. Verify deployment
7. Notify team
```

**Winner**: Skill ✓

### Example: Test Count

**As Command** (Better):
```bash
#!/bin/bash
find tests -name "*.test.ts" | wc -l
```

**As Skill** (Overkill):
```markdown
1. Find test files
2. Count them
3. Analyze coverage
...
```

**Winner**: Command ✓

### Example: Code Review

**As Command** (Too Limited):
```bash
#!/bin/bash
# Can't do analysis
git diff
```

**As Skill** (Better):
```markdown
1. Get changed files
2. Read each file
3. Analyze changes
4. Check for issues
5. Provide feedback
6. Suggest improvements
```

**Winner**: Skill ✓

## Decision Criteria

### Use Command When:
✅ Single operation
✅ < 2 second execution
✅ Pure data return
✅ No decisions needed
✅ No user input needed

### Use Skill When:
✅ Multiple steps
✅ Need conversation context
✅ Requires analysis
✅ Interactive workflow
✅ Conditional logic

## Converting Between

### Command → Skill
When command becomes too complex:

```bash
# Command getting complex
#!/bin/bash
if [ "$BRANCH" == "main" ]; then
    if [ "$(git status --porcelain)" == "" ]; then
        npm run deploy
        notify_team
    fi
fi
```

Convert to skill for clarity:
```markdown
# Skill with clear workflow
1. Check branch is main
2. Check working directory clean
3. Run deployment
4. Notify team
```

### Skill → Command
When skill is too simple:

```markdown
# Skill that's just one command
name: git-log
1. Run git log
2. Return output
```

Simplify to command:
```bash
#!/bin/bash
git log --oneline -n 10
```

## Practical Guidelines

### Start with Command
```bash
# Try as command first
#!/bin/bash
npm test
```

### Upgrade to Skill
```markdown
# If you need:
- Pre-checks
- Error handling
- User interaction
- Multi-step logic

Then make it a skill
```

### Real Example
```bash
# Started as command
/test

# Grew to skill
/test
1. Check for changed files
2. Run relevant tests only
3. If failures, analyze
4. Suggest fixes
5. Rerun after fixes
```

## Common Patterns

### Data Retrieval: Command
```bash
/test-count
/line-count
/git-log
/file-tree
```

### Workflows: Skill
```bash
/commit
/deploy
/review-pr
/refactor
```

### Status Checks: Command
```bash
/build-status
/coverage
/dependencies
```

### Complex Operations: Skill
```bash
/test (with analysis)
/docs (generation)
/release (full process)
```

## Key Takeaway

Commands are for quick data retrieval (< 2s, single operation). Skills are for multi-step workflows that use conversation context. Start with commands for simplicity, upgrade to skills when you need multiple steps, user interaction, or decision-making.
