---
title: Writing Clear Instructions
category: best-practices
commands: []
keywords: instructions prompts communication clarity requests
related_topics: [task-breakdown-strategies, providing-examples]
difficulty: beginner
---

# Writing Clear Instructions

## Summary

The quality of Claude's output directly correlates with the clarity of your instructions. Well-written prompts save time, reduce back-and-forth, and produce better code.

## Core Principles

### 1. Be Specific

**Vague**: "Fix the login"
**Clear**: "Fix the login form to display validation errors below each input field instead of in an alert"

### 2. Provide Context

**Missing Context**: "Add pagination"
**With Context**: "Add pagination to the user list table. We're currently loading all 10,000 users at once, causing slow page loads."

### 3. State the Goal

**Implementation-Focused**: "Use useState for the counter"
**Goal-Focused**: "Add a counter that persists between page refreshes"

(Claude might suggest localStorage instead of useState)

### 4. Include Constraints

**No Constraints**: "Add authentication"
**With Constraints**: "Add JWT authentication. Must work with our existing Express middleware and PostgreSQL database."

## Effective Request Structure

```markdown
**What**: [Brief description]
**Why**: [The problem you're solving]
**Context**: [Relevant information]
**Constraints**: [Limitations or requirements]
**Success Criteria**: [How to know it's done]
```

Example:
```markdown
**What**: Add rate limiting to the API
**Why**: We're seeing abuse from automated scrapers
**Context**: Express + Redis backend, REST API
**Constraints**: Must exempt authenticated admin users
**Success Criteria**: Block more than 100 requests/minute per IP, return 429 status
```

## Anti-Patterns

### ❌ The Novel

```
"So I've been thinking about how we might want to potentially
consider adding some kind of system that would allow users to,
you know, sort of manage their preferences, maybe with some
kind of settings page or something, and I was wondering if
perhaps we could..."
```

**Problem**: Too much hedging, no clear request

✅ **Better**: "Add a user preferences page with email notification settings"

### ❌ The Assumption

```
"Update the config"
```

**Problem**: Which config? Update how?

✅ **Better**: "Update config.json to set API timeout to 30 seconds"

### ❌ The XY Problem

```
"How do I parse this JSON string manually?"
```

**Problem**: Asked about solution (parsing manually) instead of goal

✅ **Better**: "I'm getting an error when trying to load user data from the API. The response looks like [example]. How should I handle this?"

### ❌ The Laundry List

```
"Fix the navbar, update dependencies, refactor the auth system,
add tests, improve performance, update docs, and clean up the
database queries"
```

**Problem**: Too many tasks at once

✅ **Better**: Break into separate, focused requests

## Power Phrases

**For Refactoring**:
- "Extract [X] into a separate [function/module/component]"
- "Refactor [X] to follow [pattern/principle]"

**For Debugging**:
- "This error occurs when [scenario]. Here's the error message: [error]"
- "Expected [X], got [Y]. Here's the relevant code: [code]"

**For Features**:
- "Add [feature] that allows users to [action]"
- "Implement [feature] similar to how [example] works"

**For Exploration**:
- "Explain how [X] works in this codebase"
- "What's the best way to [accomplish goal] given our stack?"

## Using Examples

**Without Example**:
"Style the button nicely"

**With Example**:
"Style the button like Material UI's primary button: blue background, white text, subtle shadow, hover effect"

Or even better:
"Style the button like this: [paste example code or screenshot]"

## Providing Code Context

When asking about specific code:

```
❌ "Fix the bug in processPayment"

✅ "Fix the bug in processPayment (src/payment/processor.py:45).
    It's throwing a KeyError on 'amount' when processing refunds.
    Here's the error: [paste traceback]"
```

## Follow-Up Clarity

If Claude asks for clarification:

**Vague**: "Whatever you think is best"
**Clear**: "Use JWT. Our frontend is React and we're already using axios."

## Testing Instructions

**Vague**: "Add tests"
**Clear**: "Add unit tests for the payment processing logic. Focus on edge cases: negative amounts, invalid currencies, network failures."

## Key Takeaway

Think of your instruction as a specification. The more precisely you describe what success looks like, the more likely Claude is to achieve it on the first try.
