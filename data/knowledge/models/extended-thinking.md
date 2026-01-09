---
slug: extended-thinking
title: Extended Thinking Mode
category: models
difficulty: intermediate
keywords: thinking deeply reasoning tokens extended cognitive
commands: ["Tab", "MAX_THINKING_TOKENS"]
related: [change-model, opus-usage, sonnet-usage]
---

# Extended Thinking Mode

## Summary

Toggle Claude's extended thinking mode to enable deeper reasoning on complex problems. Use Tab key to activate, configure MAX_THINKING_TOKENS to control depth, and monitor for performance impact.

## What is Extended Thinking?

Extended thinking allows Claude to "think out loud" before responding, showing its reasoning process. This leads to:

- Better problem analysis
- More thorough solutions
- Visible reasoning steps
- Improved debugging

## Toggling Extended Thinking

### Quick Toggle

Press **Tab** during a session to toggle thinking mode:

```bash
# Start session
claude

# Press Tab to enable thinking
[Tab]
Extended thinking: ON

# Press Tab again to disable
[Tab]
Extended thinking: OFF
```

### Visual Indicators

When enabled, you'll see:
```
🧠 Thinking...
[Claude's internal reasoning visible here]

[Final response follows]
```

## Configuration

### Token Limit

Set maximum thinking tokens:

```bash
# In environment
export MAX_THINKING_TOKENS=2000

# In config
{
  "thinking": {
    "enabled": true,
    "maxTokens": 2000
  }
}
```

**Default**: 1000 tokens
**Range**: 100-4000 tokens

### Auto-Enable

Enable thinking by default:

```bash
# Environment
export CLAUDE_THINKING_DEFAULT=true

# Config
{
  "thinking": {
    "defaultEnabled": true
  }
}
```

## When to Use Extended Thinking

### ✅ Use For:

**Complex Debugging**
- Multi-layer issues
- Race conditions
- Performance problems

**Architectural Decisions**
- Trade-off analysis
- Pattern selection
- System design

**Algorithm Design**
- Optimization problems
- Data structure selection
- Complex logic

**Large Refactors**
- Planning multi-file changes
- Dependency analysis
- Migration strategies

### ❌ Disable For:

**Simple Tasks**
- Typo fixes
- Comment additions
- Simple formatting

**Fast Iteration**
- Rapid prototyping
- Quick experiments
- Batch operations

**Well-Defined Problems**
- Straightforward implementations
- Known patterns
- Standard operations

## Performance Impact

### Speed
- Adds 2-10 seconds per response
- Depends on problem complexity
- Token budget consumed by thinking

### Quality
- 20-40% improvement on complex tasks
- Minimal benefit on simple tasks
- Most effective with Opus

## Thinking Keywords

Trigger extended thinking with keywords in your prompts:

```bash
# These trigger deeper thinking automatically
"analyze thoroughly"
"think step by step"
"consider all options"
"debug carefully"
"plan in detail"
```

## Model Differences

### Opus + Thinking
Best combination for:
- Novel problems
- Complex reasoning
- Critical decisions

### Sonnet + Thinking
Good for:
- Moderate complexity
- Balanced speed/quality
- General debugging

### Haiku + Thinking
Limited benefit:
- Simple problems only
- Minimal quality gain
- Not recommended

## Monitoring Thinking Usage

### Check Token Usage

```bash
/stats

Thinking tokens: 1,847 / 2,000
Response tokens: 523
Total: 2,370
```

### Performance Comparison

```bash
# Without thinking
Task: Debug authentication issue
Time: 3 seconds
Quality: Missed edge case

# With thinking
Task: Debug authentication issue
Time: 8 seconds
Quality: Found edge case + root cause
```

## Common Patterns

### Pattern 1: Think Then Execute

```bash
# Enable thinking for planning
Tab (enable thinking)
"Plan the architecture for user authentication"
[Get detailed, well-reasoned plan]

# Disable for execution
Tab (disable thinking)
"Implement this plan"
[Fast implementation]
```

### Pattern 2: Thinking for Stuck Problems

```bash
# Problem not solving
"Why isn't this working?"
[Generic answer]

# Enable thinking and retry
Tab
"Analyze why this authentication flow fails"
[Detailed step-by-step analysis]
```

### Pattern 3: Selective Thinking

```bash
# Enable only for specific prompts
"think carefully: What could cause this race condition?"

# Regular prompt without thinking
"Add a comment explaining this function"
```

## Troubleshooting

### "Thinking takes too long"

```bash
# Reduce token limit
export MAX_THINKING_TOKENS=500

# Or disable
Tab (toggle off)
```

### "Not seeing thinking output"

```bash
# Check if enabled
/status

# Enable explicitly
Tab

# Try thinking keyword
"analyze step by step: [your question]"
```

### "Thinking doesn't help"

Thinking has minimal benefit when:
- Problem is too simple
- Using Haiku model
- Question is well-defined

Switch to Sonnet/Opus or disable thinking.

## Best Practices

1. **Default Off** - Enable when needed, not always
2. **Use with Opus** - Best model for thinking mode
3. **Complex Problems Only** - Save time on simple tasks
4. **Monitor Tokens** - Watch token usage with `/stats`
5. **Combine with Planning** - Great for Plan mode exploration

## Key Takeaway

Extended thinking is a powerful tool for complex problems but adds latency. Use Tab to toggle it on when you need deeper reasoning, keep it off for routine work. Most effective with Opus model on novel or difficult problems.
