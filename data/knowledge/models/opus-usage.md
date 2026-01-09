---
slug: opus-usage
title: When to Use Opus
category: models
difficulty: intermediate
keywords: opus complex reasoning architecture planning
related: [change-model, sonnet-usage]
---

# When to Use Opus

## Summary

Use Claude Opus 4.5 for complex reasoning, architectural decisions, large refactors, and challenging debugging where quality matters more than speed or cost.

## Opus Strengths

- **Deep reasoning**: Complex logic and trade-off analysis
- **Large context**: Better handling of extensive codebases
- **Architectural thinking**: System design and patterns
- **Debugging**: Traces through complex issues
- **Quality**: Highest quality output

## Ideal Use Cases

### 1. System Architecture
Planning multi-component systems, microservices, database schemas.

### 2. Complex Refactoring
Restructuring large codebases while maintaining functionality.

### 3. Difficult Bugs
Issues requiring deep analysis across multiple files.

### 4. Learning Codebases
Understanding unfamiliar, complex architectures.

### 5. Critical Code
Authentication, payments, security-sensitive features.

## Cost Consideration

Opus is ~15x more expensive than Haiku, ~5x more than Sonnet.

**Use when**: Quality justifies cost
**Avoid when**: Simple, repetitive tasks

## Performance

- Slower than Sonnet/Haiku
- Worth it for complex tasks
- Not ideal for rapid iteration

## Pattern: Opus for Planning

```bash
/model opus
"Design the architecture for this feature"
[Get detailed plan]

/model sonnet  
"Implement this plan"
[Faster execution]
```

## Key Takeaway

Opus is your heavy-duty tool for complex problems. Don't use it for everything, but don't hesitate when you need its capabilities.
