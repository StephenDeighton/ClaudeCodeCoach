---
slug: mcp-context-warning
title: MCP Context Impact
category: context-efficiency
difficulty: intermediate
keywords: MCP context tokens cost impact server
commands: []
related: [context-window-basics, when-use-mcp]
---

# MCP Context Impact

## Summary

MCP servers can significantly impact context usage. Each MCP query returns data that fills context, and excessive MCP use can bloat context quickly. Use MCP strategically and cache results when possible.

## MCP Token Costs

### Typical MCP Query Costs

```
GitHub PR list: 2k-5k tokens
Database query results: 1k-10k tokens
Slack message history: 3k-15k tokens
File search results: 2k-20k tokens
```

### Cumulative Impact

```
Session start: 1k tokens
GitHub query (PRs): +4k = 5k
Database query: +3k = 8k
Slack history: +8k = 16k
GitHub issues: +5k = 21k
Database stats: +4k = 25k

25k tokens from just 5 MCP queries!
```

## MCP Context Patterns

### Inefficient Pattern

```bash
# Query same data repeatedly
"What PRs are open?" (4k tokens)
...later...
"Check PR #42 status" (queries again, +4k = 8k)
...later...
"Any new PRs?" (queries again, +4k = 12k)

# 12k tokens for essentially same data
```

### Efficient Pattern

```bash
# Query once, reference results
"What PRs are open?" (4k tokens)
"Tell me about PR #42" (uses existing context)
"Focus on PR #43" (uses existing context)

# 4k tokens total
```

## When MCP Bloats Context

### ❌ Large Result Sets

```
"Show all database records" → 50k tokens
"List all Slack messages" → 80k tokens
"Get entire file tree" → 30k tokens
```

### ❌ Repeated Queries

```
Query every 5 minutes
Each query: 5k tokens
Hour of work: 60k tokens
Just from MCP!
```

### ❌ Unnecessary Detail

```
"Get user data"
Returns: All fields, all relationships, full history
Needed: Just name and email

Token waste: 90%
```

## MCP Optimization Strategies

### Strategy 1: Query Once

```
# Start of session
"Get current PRs and issues"

# Use throughout session
"Work on PR #42"
"Check issue #123"
# No additional MCP queries needed
```

### Strategy 2: Limit Results

```
# Bad
"Get all database users"

# Good
"Get database user count"
"Get 10 most recent users"
```

### Strategy 3: Selective Fields

```
# Bad: Full objects
SELECT * FROM users

# Good: Just what's needed
SELECT id, name, email FROM users
```

### Strategy 4: Summary Over Detail

```
# Bad
"Show all Slack messages"

# Good
"Summarize Slack activity"
"Show last 5 messages only"
```

## MCP Configuration for Efficiency

### Limit Result Sizes

```json
{
  "mcp": {
    "servers": {
      "database": {
        "maxResults": 100,
        "defaultLimit": 10
      },
      "slack": {
        "maxMessages": 50,
        "defaultCount": 10
      }
    }
  }
}
```

### Cache Duration

```json
{
  "mcp": {
    "cache": {
      "enabled": true,
      "ttl": 300
    }
  }
}
```

## Monitoring MCP Impact

```bash
/status

Context: 85k / 200k (43%)
MCP queries: 12
MCP tokens: ~35k (41% of context)

# MCP is major context consumer
```

## When to Clear After MCP

```
Scenario 1: Large query result
Query: 40k tokens
Action: Use data, then /clear

Scenario 2: Multiple queries
5 queries × 8k = 40k tokens
Action: Clear before next major task

Scenario 3: Stale data
Queried 2 hours ago
Action: Clear and re-query
```

## MCP Best Practices

### ✅ Do
- Query once, reuse results
- Limit result sizes
- Request summaries over raw data
- Clear context after large queries
- Cache when appropriate

### ❌ Don't
- Query same data repeatedly
- Request unlimited results
- Fetch data you won't use
- Ignore MCP token costs
- Keep stale data in context

## MCP vs Manual

Sometimes manual is more efficient:

### MCP Query: 5k tokens
```
GitHub MCP: "Get PR #42 details"
Returns: Full PR object, comments, reviews, commits
```

### Manual: 500 tokens
```
gh pr view 42 --json title,state,author
Returns: Just what's needed
```

## Key Takeaway

MCP servers can bloat context quickly. Query once and reuse results, limit result sizes, prefer summaries over full data dumps, and clear context after large MCP operations. Monitor MCP token usage with /status and optimize queries to request only necessary data.
