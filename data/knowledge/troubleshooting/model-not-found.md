---
slug: model-not-found
title: Model Not Found
category: troubleshooting
difficulty: beginner
keywords: model not found error invalid
commands: ["/model"]
related: [change-model]
---

# Model Not Found

## Symptoms
- "Model not found" error
- "Invalid model" message
- Claude won't start

## Causes
- Typo in model name
- Wrong model specified
- Model not available
- Config error

## Solutions

### Check Model Name
```bash
# Valid models
claude --model opus     ✓
claude --model sonnet   ✓
claude --model haiku    ✓

# Invalid
claude --model gpt-4    ✗
claude --model claude-3 ✗
```

### Fix Config
```json
// .claude/config.json
{
  "model": "sonnet"  // Not "claude-sonnet-3.5"
}
```

### Reset to Default
```bash
# Remove model setting
claude
# Uses default (sonnet)
```

### Check Environment
```bash
# Remove conflicting env var
unset ANTHROPIC_MODEL

# Or set correctly
export ANTHROPIC_MODEL=sonnet
```

## Valid Model Names
- `opus` - Claude Opus 4.5
- `sonnet` - Claude Sonnet 4.5 (default)
- `haiku` - Claude Haiku 4.0

## Key Takeaway
Use exact model names: opus, sonnet, or haiku. Check config files and environment variables for typos. When in doubt, use `claude` without model flag for default.
