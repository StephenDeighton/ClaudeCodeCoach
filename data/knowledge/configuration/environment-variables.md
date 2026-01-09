---
slug: environment-variables
title: Environment Variables
category: configuration
difficulty: intermediate
keywords: environment variables env ANTHROPIC CLAUDE configuration
commands: []
related: [settings-files, cli-config]
---

# Environment Variables

## Summary

Configure Claude Code using environment variables for API keys, model selection, and behavior settings. Useful for CI/CD, scripts, and per-shell configuration.

## Core Variables

### ANTHROPIC_API_KEY

Required for Claude Code to function:

```bash
export ANTHROPIC_API_KEY=sk-ant-api03-...

# Or in .env file
echo "ANTHROPIC_API_KEY=sk-ant-api03-..." >> ~/.env
```

### ANTHROPIC_MODEL

Set default model:

```bash
export ANTHROPIC_MODEL=opus      # Use Opus
export ANTHROPIC_MODEL=sonnet    # Use Sonnet (default)
export ANTHROPIC_MODEL=haiku     # Use Haiku
```

### ANTHROPIC_BASE_URL

Custom API endpoint (for enterprise):

```bash
export ANTHROPIC_BASE_URL=https://api.anthropic.com
```

## Claude Code Variables

### CLAUDE_CONFIG_DIR

Override config directory:

```bash
export CLAUDE_CONFIG_DIR=~/my-claude-config
# Uses ~/my-claude-config/settings.json
```

### CLAUDE_PERMISSION_MODE

Set default permission mode:

```bash
export CLAUDE_PERMISSION_MODE=normal  # Ask each time (default)
export CLAUDE_PERMISSION_MODE=plan    # Read-only
export CLAUDE_PERMISSION_MODE=auto    # Autonomous
```

### CLAUDE_MAX_CONTEXT

Set context token limit:

```bash
export CLAUDE_MAX_CONTEXT=150000
```

### CLAUDE_THINKING_DEFAULT

Enable thinking by default:

```bash
export CLAUDE_THINKING_DEFAULT=true
```

### CLAUDE_NO_COLOR

Disable colored output:

```bash
export CLAUDE_NO_COLOR=1
```

## Git Configuration

### GIT_AUTHOR_NAME / GIT_AUTHOR_EMAIL

Used for commits:

```bash
export GIT_AUTHOR_NAME="Your Name"
export GIT_AUTHOR_EMAIL="you@example.com"
```

### CLAUDE_GIT_AUTO_COMMIT

Auto-commit changes:

```bash
export CLAUDE_GIT_AUTO_COMMIT=true
```

## Setting Up Environment

### Shell Configuration

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Claude Code Configuration
export ANTHROPIC_API_KEY=sk-ant-api03-...
export ANTHROPIC_MODEL=sonnet
export CLAUDE_PERMISSION_MODE=normal
export CLAUDE_MAX_CONTEXT=200000

# Git settings
export GIT_AUTHOR_NAME="Your Name"
export GIT_AUTHOR_EMAIL="you@example.com"
```

### .env File

Create `.env` in project:

```bash
# API Configuration
ANTHROPIC_API_KEY=sk-ant-api03-...
ANTHROPIC_MODEL=opus

# Claude Settings
CLAUDE_PERMISSION_MODE=plan
CLAUDE_MAX_CONTEXT=150000
CLAUDE_THINKING_DEFAULT=true
```

Load with:
```bash
source .env
claude
```

Or use `direnv`:
```bash
# Install direnv
brew install direnv

# Allow directory
direnv allow .

# Auto-loads .env when entering directory
```

## Variable Precedence

Settings are applied in this order (later overrides earlier):

```
1. Built-in defaults
2. ~/.claude/settings.json
3. .claude/config.json
4. Environment variables
5. CLI flags (highest priority)
```

Example:
```bash
# In settings.json
{"model": "sonnet"}

# Environment variable
export ANTHROPIC_MODEL=opus

# CLI flag
claude --model haiku

# Result: Uses haiku (CLI flag wins)
```

## Checking Current Environment

```bash
# Show all Claude-related variables
env | grep -E '(ANTHROPIC|CLAUDE)'

# Check specific variable
echo $ANTHROPIC_MODEL

# View effective settings in Claude
claude --show-config
```

## Security Best Practices

### Never Commit API Keys

```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo "*.local.env" >> .gitignore

# Check what's committed
git ls-files | grep env
```

### Use Key Management

```bash
# macOS Keychain
security add-generic-password -a claude -s anthropic-api-key -w

# Retrieve in script
export ANTHROPIC_API_KEY=$(security find-generic-password -a claude -s anthropic-api-key -w)
```

## CI/CD Configuration

### GitHub Actions

```yaml
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  ANTHROPIC_MODEL: opus
  CLAUDE_PERMISSION_MODE: auto
```

### Docker

```dockerfile
ENV ANTHROPIC_API_KEY=""
ENV ANTHROPIC_MODEL=sonnet
ENV CLAUDE_PERMISSION_MODE=normal
```

```bash
docker run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY my-image
```

## Troubleshooting

### "API key not found"

```bash
# Check if set
echo $ANTHROPIC_API_KEY

# If empty, set it
export ANTHROPIC_API_KEY=sk-ant-api03-...

# Make permanent
echo 'export ANTHROPIC_API_KEY=sk-ant-api03-...' >> ~/.zshrc
source ~/.zshrc
```

### "Invalid model"

```bash
# Check current
echo $ANTHROPIC_MODEL

# Valid values: opus, sonnet, haiku
export ANTHROPIC_MODEL=sonnet
```

### Variables Not Loading

```bash
# Reload shell config
source ~/.zshrc

# Or restart terminal
```

## Key Takeaway

Environment variables provide flexible configuration for Claude Code, especially useful for API keys, CI/CD, and per-project settings. Set ANTHROPIC_API_KEY for authentication and use other CLAUDE_* variables to customize behavior. Always use .gitignore to protect API keys.
