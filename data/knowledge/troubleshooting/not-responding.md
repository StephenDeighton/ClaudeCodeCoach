---
slug: not-responding
title: Claude Not Responding
category: troubleshooting
difficulty: beginner
keywords: not responding frozen stuck hang timeout
commands: []
related: [slow-performance, context-bloated]
---

# Claude Not Responding

## Symptoms
- No response after prompt
- Spinning/waiting indicator
- Timeout errors
- Frozen interface

## Common Causes

### 1. Network Issues
```bash
# Check connection
ping api.anthropic.com
```

### 2. API Key Problems
```bash
# Verify API key
echo $ANTHROPIC_API_KEY
# Should show sk-ant-api03-...
```

### 3. Context Overload
```bash
/status
# If > 180k tokens, context may be causing timeout
```

### 4. Large Operation
```bash
# Reading massive file or running long command
# May just need time to complete
```

## Solutions

### Quick Fixes
1. Wait 30 seconds (may be processing)
2. Ctrl+C to cancel
3. Try again
4. Check /status for context issues

### Network Fixes
```bash
# Check internet
curl https://api.anthropic.com

# Restart session
/exit
claude
```

### Context Fixes
```bash
# Clear context
/clear

# Or fresh session
/exit
claude
```

### API Key Fixes
```bash
# Reset API key
export ANTHROPIC_API_KEY=sk-ant-api03-...

# Restart Claude
claude
```

## Prevention
- Monitor context usage
- Clear context regularly
- Keep operations reasonably sized
- Check network before long sessions

## Key Takeaway
Most "not responding" issues are network, API key, or context overload. Check /status, verify connectivity, and clear context if needed. Ctrl+C cancels hung operations.
