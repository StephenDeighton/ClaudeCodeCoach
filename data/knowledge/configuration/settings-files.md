---
slug: settings-files
title: Settings Files
category: configuration
difficulty: intermediate
keywords: settings config json files configuration global project
commands: []
related: [config-menu, cli-config, environment-variables]
---

# Settings Files

## Summary

Claude Code uses JSON configuration files at global and project levels. Global settings in `~/.claude/settings.json` apply everywhere, while project settings in `.claude/config.json` override for specific projects.

## File Hierarchy

Settings are loaded in this order (later overrides earlier):

```
1. Default settings (built-in)
2. ~/.claude/settings.json (global)
3. .claude/config.json (project)
4. Environment variables
5. CLI flags
```

## Global Settings

Location: `~/.claude/settings.json`

```json
{
  "model": "sonnet",
  "permissionMode": "normal",
  "theme": {
    "mode": "dark"
  },
  "context": {
    "maxTokens": 200000,
    "warningThreshold": 160000,
    "autoClear": false
  },
  "thinking": {
    "defaultEnabled": false,
    "maxTokens": 1000
  },
  "git": {
    "autoCommit": false,
    "commitStyle": "conventional"
  }
}
```

Applies to all Claude Code sessions unless overridden.

## Project Settings

Location: `.claude/config.json` (in project root)

```json
{
  "model": "opus",
  "permissionMode": "plan",
  "context": {
    "maxTokens": 150000
  },
  "git": {
    "autoCommit": true,
    "branch": "development"
  },
  "customSettings": {
    "testCommand": "npm test",
    "buildCommand": "npm run build"
  }
}
```

Overrides global settings for this project only.

## Complete Settings Reference

### Model Configuration

```json
{
  "model": "sonnet",
  "modelSettings": {
    "opus": {
      "temperature": 0.7,
      "maxTokens": 4096
    },
    "sonnet": {
      "temperature": 0.7,
      "maxTokens": 4096
    },
    "haiku": {
      "temperature": 0.5,
      "maxTokens": 2048
    }
  }
}
```

### Permission Settings

```json
{
  "permissionMode": "normal",
  "permissions": {
    "allowedTools": ["read", "write", "bash", "git"],
    "deniedTools": ["docker", "kubectl"],
    "requireConfirm": ["git_push", "delete"]
  }
}
```

### Context Management

```json
{
  "context": {
    "maxTokens": 200000,
    "warningThreshold": 160000,
    "autoClear": false,
    "clearOnExit": false,
    "showUsage": true
  }
}
```

### Git Settings

```json
{
  "git": {
    "autoCommit": false,
    "commitStyle": "conventional",
    "defaultBranch": "main",
    "pushAfterCommit": "ask",
    "author": {
      "name": "Your Name",
      "email": "you@example.com"
    }
  }
}
```

## Creating Settings Files

### First Time Setup

```bash
# Global settings
mkdir -p ~/.claude
cat > ~/.claude/settings.json << 'EOF'
{
  "model": "sonnet",
  "permissionMode": "normal",
  "theme": {
    "mode": "dark"
  }
}
EOF

# Project settings
mkdir -p .claude
cat > .claude/config.json << 'EOF'
{
  "model": "opus",
  "git": {
    "autoCommit": true
  }
}
EOF
```

## Validating Settings

```bash
# Check settings
claude --validate-config

# View effective settings
claude --show-config

Output:
Effective configuration:
  Model: opus (from .claude/config.json)
  Permission mode: normal (from ~/.claude/settings.json)
  Theme: dark (from ~/.claude/settings.json)
  Git auto-commit: true (from .claude/config.json)
```

## Settings Inheritance

Project settings extend (not replace) global settings:

```json
// ~/.claude/settings.json
{
  "model": "sonnet",
  "thinking": {
    "defaultEnabled": false,
    "maxTokens": 1000
  }
}

// .claude/config.json
{
  "model": "opus",
  "thinking": {
    "defaultEnabled": true
    // maxTokens: 1000 inherited from global
  }
}
```

## Environment Variable Integration

Reference environment variables in settings:

```json
{
  "git": {
    "author": {
      "name": "${GIT_AUTHOR_NAME}",
      "email": "${GIT_AUTHOR_EMAIL}"
    }
  }
}
```

## Key Takeaway

Use `~/.claude/settings.json` for global preferences and `.claude/config.json` for project-specific overrides. Settings cascade with later sources overriding earlier ones. Validate configuration with `claude --validate-config`.
