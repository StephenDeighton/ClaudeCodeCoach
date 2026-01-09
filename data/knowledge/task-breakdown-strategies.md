---
title: Task Breakdown Strategies
category: psb-workflow
commands: []
keywords: planning task-breakdown workflow PSB plan-scan-build decomposition
related_topics: [writing-clear-instructions]
difficulty: intermediate
---

# Task Breakdown Strategies

## Summary

Breaking complex tasks into manageable steps helps Claude work more effectively and produces better results. Learn proven strategies for decomposing large features into actionable subtasks.

## Why Break Down Tasks?

**Benefits**:
- Claude can focus on one thing at a time
- Easier to track progress
- Better error recovery
- Clearer communication
- Incremental commits

**Without Breakdown**: "Build a user authentication system"
**With Breakdown**: 5 clear steps Claude can execute sequentially

## The PSB Pattern

**Plan → Scan → Build**

1. **Plan**: Break down the work
2. **Scan**: Explore relevant code
3. **Build**: Implement incrementally

Example:
```
Task: Add password reset feature

Plan:
- Design email template
- Create reset token generation
- Build reset endpoint
- Add frontend form
- Write tests

Scan:
- Review existing auth code
- Check email service
- Find token utilities

Build:
- Implement each planned step
- Test as you go
```

## Decomposition Techniques

### 1. Layer-Based Breakdown

Split by architectural layers:
```
Task: User profile editing

Subtasks:
1. Database: Add profile fields to schema
2. Backend: Create PUT /profile endpoint
3. Frontend: Build profile edit form
4. Validation: Add input validation
5. Tests: Unit + integration tests
```

### 2. Dependency-Driven Breakdown

Start with dependencies:
```
Task: Payment processing

Subtasks:
1. Set up Stripe SDK (needed by all)
2. Create payment model (needed by processing)
3. Implement payment processing
4. Add webhook handlers
5. Build UI components
```

### 3. Risk-Based Breakdown

Tackle unknowns first:
```
Task: Integrate third-party API

Subtasks:
1. Research API authentication (unknown)
2. Prototype API call (test it works)
3. Implement error handling
4. Add to main codebase
5. Write documentation
```

### 4. User Flow Breakdown

Follow the user journey:
```
Task: Checkout flow

Subtasks:
1. Cart summary page
2. Shipping information form
3. Payment method selection
4. Order confirmation
5. Email receipt
```

## Practical Example

**Bad Request**:
> "Add comments to blog posts"

**Good Request**:
> "Add comment system to blog posts:
> 1. Create comments table with: post_id, user_id, content, created_at
> 2. Add POST /posts/:id/comments endpoint
> 3. Display comments under each post
> 4. Add comment form for logged-in users
> 5. Show comment count in post list"

## How Small Is Too Small?

**Too Large** (won't fit in one response):
- "Refactor entire authentication system"

**Just Right** (clear deliverable):
- "Extract token generation into utils/auth_tokens.py"

**Too Small** (micro-management):
- "Add a newline after function definition"

## Claude's Built-In Task Tracking

Claude can use TodoWrite tool to track subtasks:

```
Request: "Add dark mode. Use the TodoWrite tool to track your progress."

Claude creates:
☐ Add theme toggle to settings
☐ Create dark theme styles
☐ Store preference in localStorage
☐ Apply theme on page load
```

## Anti-Patterns

❌ **Waterfall**: "Plan everything before building anything"
✅ **Iterative**: Plan next 2-3 steps, adjust as you learn

❌ **Over-Specification**: "Put the button at x:120, y:340"
✅ **Goal-Oriented**: "Add a prominent save button to the form"

❌ **Vague Handwaving**: "Make it better"
✅ **Specific Outcomes**: "Reduce load time by caching API responses"

## Adaptive Breakdown

Sometimes you learn during implementation:

```
Initial Plan:
1. Add email validation
2. Implement password reset
3. Send reset email

After Step 1 (discovery):
1. ✅ Add email validation
2a. Generate secure reset tokens
2b. Store tokens with expiry
2c. Create reset endpoint
3. Send reset email
```

Be ready to adjust!

## Key Takeaway

Great task breakdown is like good directions: specific enough to be actionable, flexible enough to adapt, and organized to build on previous steps.
