---
slug: reducing-bloat
title: Reducing Context Bloat
category: context-efficiency
difficulty: intermediate
keywords: bloat reduce optimize cleanup efficiency
commands: ["/clear"]
related: [context-window-basics, context-hygiene]
---

# Reducing Context Bloat

## Summary

Context bloat happens when unnecessary data accumulates. Common causes: re-reading files, verbose outputs, long conversations, and inefficient exploration. Regular cleanup and mindful practices keep context lean.

## Common Bloat Sources

### 1. Re-reading Files (30-50% of bloat)
```
Read auth.ts (10k)
...work...
Read auth.ts again (10k)
...work...
Read auth.ts again (10k)
Total: 30k for one file!
```

### 2. Large File Dumps (20-30%)
```
Read 5000-line file (100k tokens)
Only needed 50 lines
Wasted: 98k tokens
```

### 3. Verbose Command Output (10-20%)
```
npm install (full output): 50k tokens
Test run (all output): 30k tokens
Build logs: 40k tokens
```

### 4. Circular Conversations (10-15%)
```
"How does X work?"
[Explanation]
"Wait, how does X work again?"
[Same explanation]
Repeated 3 times: 15k wasted tokens
```

## Bloat Detection

### Check Context Efficiency

```bash
/status

Context: 120k / 200k (60%)
Files read: 8
Average per file: 15k tokens

# If average > 10k per file, likely bloat
```

### Signs of Bloat
- Context filling faster than progress
- Reading same files multiple times
- Large command outputs accumulating
- Circular discussions
- Context > 100k for simple task

## Reduction Techniques

### Technique 1: Read Once
```
# Before reading
"I'll need to reference auth.ts"
Read auth.ts once
Reference it in conversation
Don't re-read unless changed
```

### Technique 2: Targeted Reading
```
# Instead of full file
Read lines 50-100 of large-file.ts

# Or
"Show me just the UserAuth class"
```

### Technique 3: Suppress Verbose Output
```bash
# Verbose
npm install
# Output: 50k tokens

# Quiet
npm install --silent
# Output: 500 tokens
```

### Technique 4: Summarize Instead
```
# Don't dump full output
"Run tests and show results"
[40k tokens of output]

# Summarize
"Run tests and summarize failures"
[5k tokens summary]
```

## Preventive Practices

### Before Large Operations

```
Check: /status (50k tokens)
Action: Safe to proceed

Check: /status (140k tokens)
Action: /clear first, then proceed
```

### During Exploration

```
# Progressive, not exhaustive
tree -L 2 (500 tokens)
grep keywords (1k tokens)
Read 3 specific files (15k tokens)
Total: 16.5k tokens

vs.

Read all 50 files (500k - exceeds limit!)
```

### After Major Milestones

```
Complete feature planning ✓
/clear
Start implementation

Complete implementation ✓
/clear
Start testing
```

## Emergency Debloating

### Context at 180k+

```
1. /clear immediately
2. Summarize what you've learned
3. Note files that matter
4. Start fresh with just those files
```

### Context Recovery

```
Before clear:
"Summarize current state and key findings"

After clear:
"Based on summary, continue with X"
```

## Bloat Budget

### Acceptable Bloat
```
10-20% overhead: Normal
Example: 50k productive + 10k overhead = 60k total
```

### Excessive Bloat
```
50%+ overhead: Problem
Example: 50k productive + 50k bloat = 100k total
Action: Clean up practices
```

## Tools for Reduction

### .claudeignore
```
# Exclude bloat-prone files
node_modules/
dist/
*.log
*.min.js
```

### Selective Grep
```bash
# Exclude noise
grep "auth" src/ --exclude="*.test.ts" --exclude="*.spec.ts"
```

### Head/Tail
```bash
# Preview instead of full read
head -n 50 large-file.ts
tail -n 50 large-file.ts
```

## Key Takeaway

Context bloat comes from re-reading files, verbose outputs, and inefficient exploration. Read files once, suppress verbose command output, use progressive disclosure, and /clear between major tasks. Keep context focused on what's actively needed. Aim for < 20% overhead.
