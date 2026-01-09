---
title: Skills vs CLAUDE.md
category: feature-selection
commands: ["/skill", "Shift+Tab"]
keywords: skills CLAUDE.md features comparison when-to-use
related_topics: [claude-md-basics, skill-best-practices]
difficulty: intermediate
---

# Skills vs CLAUDE.md: When to Use Each

## Summary

Skills and CLAUDE.md serve different purposes in Claude Code. CLAUDE.md provides persistent project context, while Skills are reusable commands for specific tasks. Understanding when to use each is key to efficient workflows.

## CLAUDE.md: Your Project Foundation

**Purpose**: Persistent project documentation and instructions

**Best For**:
- Project overview and architecture
- Tech stack and dependencies
- Coding standards and conventions
- File organization patterns
- Development workflow guidelines

**Example Content**:
```markdown
## Code Standards
- Use TypeScript strict mode
- All components must have prop types
- Follow atomic design pattern
```

## Skills: Reusable Task Automation

**Purpose**: Encapsulated, reusable commands for specific tasks

**Best For**:
- Custom commit workflows
- Project-specific testing procedures
- Deployment processes
- Code generation templates
- Complex multi-step operations

**Example Skill**:
```markdown
# .claude/skills/test-before-commit.md
---
description: Run tests before committing
---

1. Run full test suite with `npm test`
2. If tests pass, stage and commit changes
3. If tests fail, show errors and abort
```

## Decision Framework

**Use CLAUDE.md when**:
- Information applies to the entire project
- Context should always be available
- You're documenting "how things work here"

**Use Skills when**:
- Task is repeatable and specific
- You want to invoke it on-demand
- It requires a specific sequence of steps
- Different projects might need different variations

## Using Them Together

The most effective setup combines both:

1. **CLAUDE.md** defines your project's conventions
2. **Skills** automate tasks following those conventions

Example:
- CLAUDE.md says: "All commits must pass tests first"
- Skill implements: `/test-before-commit` command

## Common Anti-Patterns

❌ Putting step-by-step procedures in CLAUDE.md
✅ Use Skills for procedures

❌ Duplicating project info in multiple Skills
✅ Keep it in CLAUDE.md, reference from Skills

❌ Creating a Skill for project context
✅ That's what CLAUDE.md is for

## Key Takeaway

Think of CLAUDE.md as your project's constitution and Skills as its executable programs. One defines the rules, the other automates the work.
