---
title: Context Efficiency Strategies
category: context-efficiency
commands: []
keywords: context tokens efficiency optimization memory performance
related_topics: [managing-large-files, claude-md-best-practices]
difficulty: intermediate
---

# Context Efficiency Strategies

## Summary

Maximizing context efficiency means getting the most value from Claude Code's context window. Smart organization and selective inclusion help Claude understand your project without wasting tokens.

## Understanding Context

Claude Code has a limited context window (tokens). Everything Claude reads consumes this budget:
- Your messages
- File contents
- CLAUDE.md
- Skills
- Tool outputs

## Efficiency Principles

### 1. Be Concise in CLAUDE.md

**Bad**: 500 lines of detailed documentation
**Good**: 50 lines of essential patterns and conventions

Example:
```markdown
❌ "Our API uses RESTful principles with GET, POST, PUT, DELETE..."
✅ "REST API - see /api/README.md for details"
```

### 2. Use Progressive Disclosure

Don't front-load everything. Let Claude ask for details:

```markdown
## Architecture
Three-tier: pages → services → database

## File Patterns
- Pages: class with build() → ft.Control
- Services: singleton via get_*() functions
```

Claude can request specifics when needed.

### 3. Leverage File Structure

Well-organized code is self-documenting:

```
services/
  auth_service.py      # Clear naming
  payment_service.py   # No explanation needed
  notification_service.py
```

### 4. Extract Large Reference Data

Don't put API documentation in CLAUDE.md:

**Instead of**:
```markdown
## API Endpoints
POST /users - Creates a user...
GET /users/:id - Fetches a user...
(500 more lines)
```

**Do this**:
```markdown
## API
See docs/api-reference.md for endpoints
```

### 5. Use Comments Strategically

Put context in code comments for complex logic:

```python
# Health score: (100 - severity_penalties)
# Critical: -20, Warning: -5, Info: -1
score = 100 - sum(penalties)
```

Now Claude understands without reading CLAUDE.md.

## Anti-Patterns

❌ **Duplicating Info**: Same conventions in multiple files
❌ **Over-Explaining**: Teaching Claude basics it already knows
❌ **Premature Context**: Providing info before it's needed
❌ **Historical Documentation**: Past decisions that don't affect current code

## Measuring Efficiency

Good indicators:
- ✅ CLAUDE.md under 200 lines
- ✅ Claude rarely asks "where is X?"
- ✅ Clear separation of concerns in code
- ✅ Descriptive names reducing need for comments

## Advanced: Context Compaction

For mature projects:
1. Use `.claudeignore` to exclude irrelevant files
2. Break large features into isolated modules
3. Use facade patterns to hide complexity
4. Document patterns once, apply everywhere

## Key Takeaway

Think of context as precious real estate. Every token should earn its place by guiding Claude's understanding or decision-making.
