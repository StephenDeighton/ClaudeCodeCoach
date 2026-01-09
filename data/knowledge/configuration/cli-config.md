---
slug: cli-config
title: CLI Configuration Flags
category: configuration
difficulty: intermediate
keywords: CLI flags command-line arguments options startup
commands: ["claude --help"]
related: [config-menu, settings-files, environment-variables]
---

# CLI Configuration Flags

## Summary

Configure Claude Code behavior at startup using command-line flags for model selection, permission modes, project paths, and more.

## Basic Flags

```bash
# Model selection
claude --model opus
claude --model sonnet
claude --model haiku

# Permission mode
claude --permission-mode normal
claude --permission-mode plan
claude --permission-mode auto

# Resume session
claude --resume
claude --resume <session-id>
```

## Project Flags

```bash
# Specify project directory
claude --project /path/to/project

# Load specific config
claude --config /path/to/config.json

# Ignore project config
claude --no-project-config
```

## Context Flags

```bash
# Set context limit
claude --max-context 150000

# Disable thinking
claude --no-thinking

# Set thinking token limit
claude --thinking-tokens 2000
```

## Output Flags

```bash
# Quiet mode (minimal output)
claude --quiet

# Verbose mode (detailed logging)
claude --verbose

# Debug mode
claude --debug

# JSON output format
claude --format json
```

## Git Flags

```bash
# Skip git checks
claude --no-git

# Auto-commit changes
claude --auto-commit

# Specify git author
claude --git-author "Name <email@example.com>"
```

## MCP Server Flags

```bash
# Disable MCP servers
claude --no-mcp

# Specify MCP config
claude --mcp-config /path/to/mcp.json

# List available MCP servers
claude --list-mcp
```

## Flag Combinations

```bash
# Planning session with Opus
claude --model opus --permission-mode plan

# Fast execution with Haiku in auto mode
claude --model haiku --permission-mode auto --quiet

# Fresh project exploration
claude --project ./myproject --model sonnet --no-thinking
```

## Environment Variable Fallbacks

Flags override environment variables:

```bash
# Environment
export ANTHROPIC_MODEL=haiku

# Override with flag
claude --model opus  # Uses opus, not haiku
```

## Listing All Options

```bash
claude --help

Usage: claude [OPTIONS]

Options:
  --model TEXT              Model to use (opus, sonnet, haiku)
  --permission-mode TEXT    Permission mode (normal, plan, auto)
  --project PATH            Project directory
  --config PATH             Config file path
  --resume [ID]             Resume previous session
  --max-context INTEGER     Maximum context tokens
  --thinking-tokens INTEGER Maximum thinking tokens
  --no-thinking             Disable extended thinking
  --quiet                   Minimal output
  --verbose                 Detailed logging
  --debug                   Debug mode
  --help                    Show this message and exit
```

## Config File Override

CLI flags override config files in this order:
1. CLI flags (highest priority)
2. Project config (.claude/config.json)
3. Global config (~/.claude/settings.json)
4. Environment variables
5. Defaults (lowest priority)

## Key Takeaway

Use CLI flags for one-off configuration changes or scripting. For persistent settings, use config files. Flags always take precedence over other configuration methods.
