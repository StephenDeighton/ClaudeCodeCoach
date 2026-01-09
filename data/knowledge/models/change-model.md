---
slug: change-model
title: Changing Models
category: models
difficulty: beginner
keywords: model switch change opus sonnet haiku
commands: ["/model"]
related: [opus-usage, sonnet-usage]
---

# Changing Models

## Summary

Switch between Claude models using `/model opus`, `/model sonnet`, or `/model haiku` based on task complexity and speed requirements.

## Quick Switch

```bash
/model opus     # Most capable
/model sonnet   # Balanced (default)
/model haiku    # Fastest
```

## Setting Defaults

Environment variable:
```bash
export ANTHROPIC_MODEL=opus
```

Config file:
```json
{"model": "opus"}
```

## When to Switch

**Opus**: Complex architecture, difficult bugs, large refactors
**Sonnet**: General development (default)
**Haiku**: Simple tasks, batch operations, speed priority

## Mid-Session Changes

Models switch immediately with context preserved:
```bash
/model opus  # Upgrade for complex task
[work]
/model sonnet  # Back to normal
```

## Key Takeaway

Start with Sonnet. Escalate to Opus when stuck. Use Haiku for simple, fast operations.
