---
slug: incremental-sprints
title: Incremental Development Sprints
category: best-practices
difficulty: intermediate
keywords: incremental iterative sprints agile development
commands: []
related: [psb-overview, twenty-eighty-rule]
---

# Incremental Development Sprints

## Summary

Break work into small sprints (30-90 min) with clear goals and deliverables. Complete, test, and commit each sprint before starting the next.

## Sprint Structure

```
Sprint (30-90 min)
├─ Goal: Clear, specific objective
├─ Plan: Quick approach (5 min)
├─ Execute: Implementation (20-70 min)
├─ Test: Verification (5 min)
└─ Commit: Save progress (5 min)
```

## Sprint Sizing

### Small Sprint (30 min)
```
- Single small feature
- Bug fix
- Simple refactor
- Documentation update
```

### Medium Sprint (60 min)
```
- Complete feature
- Multiple related changes
- Integration work
- Test coverage
```

### Large Sprint (90 min)
```
- Complex feature
- Significant refactor
- Multiple components
```

**Never**: > 2 hours without commit

## Example: Auth Feature

### Sprint 1 (45 min) - Backend
```
Goal: Auth service with JWT
- Create auth service
- Add generateToken()
- Add verifyToken()
- Unit tests
✓ Commit: "feat: add auth service"
```

### Sprint 2 (60 min) - Middleware
```
Goal: Auth middleware
- Create middleware
- Protect routes
- Integration tests
✓ Commit: "feat: add auth middleware"
```

### Sprint 3 (30 min) - Endpoints
```
Goal: Login/Register endpoints
- POST /auth/login
- POST /auth/register
- Integration tests
✓ Commit: "feat: add auth endpoints"
```

## Benefits

✅ Regular progress commits
✅ Easy to rollback
✅ Clear stopping points
✅ Reduced context bloat
✅ Better focus

## Sprint Best Practices

### Start Sprint
```
1. Clear goal
2. Fresh or cleared context
3. 30-90 min time box
4. Single focus area
```

### During Sprint
```
- Stay focused on goal
- Resist scope creep
- Note future tasks
- Don't start new features
```

### End Sprint
```
1. Test thoroughly
2. Commit working code
3. Clear context
4. Take 5 min break
```

## Sprint Checklist

```
□ Goal is clear and achievable
□ Time estimate reasonable (30-90 min)
□ Can be tested independently
□ Has clear completion criteria
□ Can be committed atomically
```

## Key Takeaway

Work in focused 30-90 minute sprints with clear goals. Complete, test, and commit each sprint before starting next. Regular commits create save points and prevent work loss. Clear context between sprints for fresh start.
