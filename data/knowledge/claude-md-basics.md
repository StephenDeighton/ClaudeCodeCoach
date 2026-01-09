---
title: CLAUDE.md Basics
category: project-setup
commands: []
keywords: CLAUDE.md setup configuration project instructions
related_topics: [project-setup-guide, claude-md-best-practices]
difficulty: beginner
---

# CLAUDE.md Basics

## Summary

CLAUDE.md is the primary configuration and instruction file for Claude Code projects. It provides persistent context about your project that Claude can reference throughout your session.

## What is CLAUDE.md?

CLAUDE.md is a markdown file that lives in the root of your project. Claude Code automatically reads this file at the start of each session, making its contents available as context without consuming tokens from your conversation.

## Basic Structure

A minimal CLAUDE.md file should include:

```markdown
# Project Name

## Overview
Brief description of what this project does

## Tech Stack
- Language/framework
- Key dependencies
- Tools used

## Project Structure
Description of how files are organized

## Conventions
- Coding standards
- Naming patterns
- File organization rules
```

## Why It Matters

- **Persistent Context**: Instructions stay available across sessions
- **Token Efficiency**: Content doesn't count against conversation limits
- **Consistency**: Ensures Claude follows your project conventions
- **Onboarding**: Makes it easy for Claude to understand your codebase

## Common Mistakes

1. **Too verbose**: Keep it concise and scannable
2. **Outdated info**: Update as your project evolves
3. **Missing conventions**: Be explicit about your standards
4. **No examples**: Show, don't just tell

## Next Steps

- Set up your first CLAUDE.md
- Review best practices for structuring content
- Learn about Skills and how they complement CLAUDE.md
