---
slug: config-menu
title: Configuration Menu
category: configuration
difficulty: beginner
keywords: settings menu preferences UI configure options
commands: ["/config"]
related: [cli-config, theme-settings, settings-files]
---

# Configuration Menu

## Summary

Access Claude Code's configuration through the `/config` command to adjust settings via an interactive menu interface.

## Opening Configuration

```bash
# In any session
/config

# Opens interactive menu
┌─ Configuration ─────────────┐
│ 1. Model Settings          │
│ 2. Permission Mode         │
│ 3. Theme                   │
│ 4. Context Settings        │
│ 5. Git Settings            │
│ 6. Advanced                │
│ 0. Exit                    │
└────────────────────────────┘
```

## Model Settings

```bash
Current model: sonnet
Available models:
  1. opus    (most capable)
  2. sonnet  (balanced) ←
  3. haiku   (fastest)

Select: 2
```

Changes apply immediately to session.

## Permission Mode

```bash
Current mode: Normal
Available modes:
  1. Normal (ask each time)     ←
  2. Plan   (read-only)
  3. Auto   (autonomous)

Select: 1
```

Can also toggle with Shift+Tab.

## Theme Settings

```bash
Current theme: dark
Available themes:
  1. Light
  2. Dark     ←
  3. System

Color scheme:
  Primary: #007ACC
  Accent: #4CAF50

Customize? (y/n): n
```

## Context Settings

```bash
Context management:
  Max context: 200,000 tokens
  Warning threshold: 160,000 tokens (80%)
  Auto-clear: disabled

Clear context on: never
Show token usage: true
```

## Git Settings

```bash
Git configuration:
  Auto-commit: false
  Commit style: conventional
  Default branch: main
  Push after commit: ask

Author:
  Name: Steve Deighton
  Email: steve@example.com
```

## Navigation

- **Arrow keys**: Move between options
- **Enter**: Select option
- **Escape/0**: Exit menu
- **?**: Help for current section

## Saving Changes

Changes save automatically:
```bash
✓ Settings saved to ~/.claude/settings.json
✓ Project config updated: .claude/config.json
```

## Quick Access

```bash
# Jump to specific section
/config model
/config theme
/config git
```

## Key Takeaway

Use `/config` for a guided settings experience. Changes apply immediately and save automatically. For programmatic configuration, use settings files or CLI flags instead.
