---
title: Model Selection Guide
category: models
commands: ["/model"]
keywords: models sonnet opus haiku performance cost speed
related_topics: [context-efficiency]
difficulty: beginner
---

# Model Selection Guide

## Summary

Claude Code offers three models with different trade-offs: Opus (most capable), Sonnet (balanced), and Haiku (fastest). Choosing the right model for each task optimizes both performance and cost.

## Available Models

### Claude Opus
**Best For**: Complex reasoning, large refactors, architectural decisions

**Characteristics**:
- Highest capability
- Best at multi-step reasoning
- Most expensive
- Slower responses

**Use When**:
- Designing system architecture
- Complex debugging
- Large-scale refactoring
- Critical decision-making

### Claude Sonnet (Default)
**Best For**: General development work, most tasks

**Characteristics**:
- Excellent balance
- Fast enough for interactive work
- Good reasoning ability
- Cost-effective

**Use When**:
- Writing features
- Code reviews
- Bug fixes
- General development

### Claude Haiku
**Best For**: Simple, repetitive tasks

**Characteristics**:
- Fastest responses
- Lowest cost
- Good for straightforward work
- Limited reasoning

**Use When**:
- Formatting code
- Simple fixes
- Documentation updates
- Quick questions

## Decision Framework

```
Is it complex or critical? → Opus
Is it routine development? → Sonnet
Is it simple and quick? → Haiku
```

## Cost vs Speed vs Quality

```
Opus:   ████████████ Quality | ████░░░░ Speed | ████████████ Cost
Sonnet: ████████░░░░ Quality | ████████ Speed | ████████░░░░ Cost
Haiku:  ████░░░░░░░░ Quality | ████████████ Speed | ████░░░░ Cost
```

## Switching Models

Use `/model` command to switch during conversation:
- `/model opus` - Switch to Opus
- `/model sonnet` - Switch to Sonnet (default)
- `/model haiku` - Switch to Haiku

## Configuration

Set default model in `.claude/config.json`:

```json
{
  "model": "sonnet"
}
```

## Pro Tips

1. **Start with Sonnet**: It handles 90% of tasks well
2. **Escalate to Opus**: When Sonnet struggles with complexity
3. **Batch Simple Tasks**: Use Haiku for multiple simple operations
4. **Monitor Cost**: Check your usage if doing heavy development

## Common Patterns

**Architecture Phase**: Opus
↓
**Implementation Phase**: Sonnet
↓
**Polish Phase**: Haiku for simple cleanups

## When Model Choice Matters Most

- **Large codebases**: Opus better at tracking context
- **Time-sensitive**: Haiku for quick turnaround
- **Learning**: Sonnet provides good explanations
- **Production code**: Opus for critical business logic

## Key Takeaway

Model selection is a dial, not a binary choice. Adjust based on task complexity, time constraints, and quality requirements.
