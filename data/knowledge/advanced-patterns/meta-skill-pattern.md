---
slug: meta-skill-pattern
title: Meta-Skill Pattern
category: advanced-patterns
difficulty: advanced
keywords: meta-skill composition orchestration skills
commands: []
related: [skills-overview, composition-hierarchy]
---

# Meta-Skill Pattern

## Summary

Meta-skills are skills that orchestrate other skills, creating powerful workflow compositions. Use meta-skills to build complex, reusable workflows from simple building blocks.

## Pattern

```markdown
# /release meta-skill

1. /test (run test suite)
2. /lint (check code quality)
3. /build (create production build)
4. /docs (update documentation)
5. /deploy production (deploy to prod)
6. /notify (send notifications)
```

## Example: Release Workflow

```markdown
---
name: release
description: Complete release workflow
tools: [bash]
---

# Release Workflow

## Execute Skills in Order

1. Run Tests
   /test
   If failures, stop and report

2. Check Linting
   /lint
   If errors, stop and report

3. Build Production
   /build production
   Verify build succeeds

4. Update Documentation
   /docs
   Generate API docs, update README

5. Deploy
   /deploy production
   With safety checks

6. Notify Team
   /notify "Release v{version} deployed"
   Via Slack and email

## Rollback Plan
If any step fails after deploy:
/rollback
/notify "Release failed, rolled back"
```

## Pattern: Conditional Meta-Skill

```markdown
# /smart-deploy meta-skill

If staging:
  /test
  /deploy staging
  
If production:
  /test
  /lint
  /build
  /security-scan
  Confirm with user
  /deploy production
  /notify
```

## Benefits

- Compose workflows from skills
- Reusable at higher level
- Clear step-by-step logic
- Easy to modify
- Self-documenting

## Best Practices

✅ Build from tested skills
✅ Handle failures gracefully
✅ Add rollback steps
✅ Clear error messages
✅ Document prerequisites

## Key Takeaway

Meta-skills orchestrate other skills into powerful workflows. Build complex release, deployment, and maintenance workflows by composing simple, tested skills. Meta-skills are maintainable and reusable across projects.
