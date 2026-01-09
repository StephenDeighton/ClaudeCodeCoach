---
slug: slow-performance  
title: Slow Performance
category: troubleshooting
difficulty: intermediate
keywords: slow performance lag latency sluggish
commands: ["/status"]
related: [context-bloated, reducing-bloat]
---

# Slow Performance

## Symptoms
- Slow responses (> 10s)
- Lag between prompt and response
- Thinking time excessive
- Operations timing out

## Diagnosis

```bash
/status

Context: 175,000 / 200,000 (88%)
# Context near limit → Slow performance
```

## Causes

### 1. Context Bloat (Most Common)
```
High context (> 150k) = Slow responses
```

### 2. Network Issues
```bash
# Test latency
ping api.anthropic.com
```

### 3. Large Operations
```
Reading huge file = Slow
Running extensive tests = Slow
```

### 4. Thinking Mode On
```
Extended thinking enabled = Slower but deeper
```

## Solutions

### Clear Context
```bash
# If > 100k tokens
/clear

# Or fresh session
/exit
claude
```

### Disable Thinking
```bash
# If Tab key enabled thinking
Tab  # Toggle off
```

### Optimize Network
```bash
# Check connection
speedtest-cli

# Switch network if slow
```

### Break Up Operations
```bash
# Instead of
"Read all 50 files and analyze"

# Do
"Read files 1-10"
"Read files 11-20"
...
```

## Prevention

### Monitor Context
```bash
# Check regularly
/status

# Clear before reaching 120k
```

### Use Haiku for Speed
```bash
/model haiku
# 3-5x faster for simple tasks
```

### Progressive Disclosure
```bash
# Don't read everything
grep → Read specific files
```

## Performance Benchmarks

```
Context < 50k: ⚡ < 2s response
Context 50-100k: ⚡ 2-5s response
Context 100-150k: ⚙️ 5-10s response
Context 150-180k: ⚠️ 10-20s response
Context > 180k: 🐌 20s+ response
```

## Key Takeaway
Slow performance is usually context bloat. Check /status, clear if > 100k tokens, use progressive disclosure, and start fresh sessions regularly. For simple tasks, switch to Haiku model for 3-5x speed improvement.
