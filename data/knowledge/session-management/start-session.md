---
slug: start-session
title: Starting a New Session
category: session-management
difficulty: beginner
keywords: claude start new session fresh begin terminal
commands: ["claude"]
related: [resume-session, clear-context]
---

# Starting a New Session

## Summary

Run `claude` in your terminal to start a fresh interactive session in the current directory. Each new session starts with clean context and loads your project's CLAUDE.md and active skills.

## When to Start Fresh

**Start a new session when:**
- Beginning work on a different project or feature
- Previous session ended or was closed
- You want completely clean context
- Switching between unrelated tasks
- After making changes to CLAUDE.md or skills

**Don't start fresh when:**
- Continuing the same conversation (use `/resume` instead)
- Context is still relevant (use `/clear` for cleanup)
- Building on previous work in the same session

## What Happens on Start

When you run `claude`:

1. **Directory Detection**: Claude checks your current working directory
2. **Project Loading**: Looks for `.claude/` directory and `CLAUDE.md`
3. **Context Initialization**: Loads project instructions into context
4. **Skills Discovery**: Scans `.claude/skills/` for available skills
5. **Ready State**: Shows prompt and awaits your first message

## Starting in Different Directories

```bash
# Start in current directory
claude

# Start in specific directory
cd /path/to/project && claude

# Or use absolute path navigation after starting
claude
> cd /path/to/project
> [Claude now has that project context]
```

## First Message Best Practices

Your first message sets the tone for the session:

**Good first messages:**
- "Let's implement the user authentication feature"
- "I need to debug the payment processing bug"
- "Create a new API endpoint for user profiles"

**Avoid vague starts:**
- "Help me code" (too vague)
- "Fix everything" (no specific goal)
- Starting with unrelated questions

## Project Context Loading

If you have a `CLAUDE.md` file:

```markdown
# My Project

## Tech Stack
- Python 3.11 + FastAPI
- PostgreSQL database

## Code Standards
- PEP 8
- Type hints required
```

Claude loads this automatically and will follow these conventions without you repeating them each session.

## Skills Auto-Loading

Available skills appear in autocomplete and are ready to use:

```bash
# Skills are immediately available
/test-before-commit
/deploy-staging
/code-review
```

You don't need to "activate" skills - they're always ready.

## Session Isolation

Each session is isolated:
- No memory of previous sessions (unless you `/resume`)
- Independent context window
- Separate conversation history
- Fresh start with project files

This isolation prevents:
- Context contamination between unrelated tasks
- Accumulated confusion from long sessions
- Mixing concerns between different features

## Common Mistakes

**❌ Starting fresh mid-task**
If you're in the middle of implementing something, don't start a new session. Use `/clear` to clean up context while preserving the current work.

**❌ Not being in the project directory**
Always `cd` to your project before running `claude`, otherwise you won't get your CLAUDE.md context.

**❌ Expecting memory of previous sessions**
Each fresh start has no memory. Document important decisions in CLAUDE.md or commit your work.

## Performance Note

Fresh sessions are fastest - they start with minimal context. As the session progresses and context accumulates, responses may slow down. This is normal and expected.

## Quick Reference

```bash
# Start new session
claude

# Start with specific model
ANTHROPIC_MODEL=opus claude

# Start with extended thinking
MAX_THINKING_TOKENS=10000 claude

# Check Claude Code version
claude --version
```

## Next Steps

- Learn about [resuming sessions](/knowledge/resume-session) to continue work
- Understand [when to clear context](/knowledge/clear-context) vs starting fresh
- Review [session best practices](/knowledge/session-best-practices) for optimal workflow
