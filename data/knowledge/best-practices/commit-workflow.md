---
slug: commit-workflow
title: Commit Workflow Best Practices
category: best-practices
difficulty: beginner
keywords: commit workflow git best practices conventions
commands: ["/commit"]
related: [incremental-sprints]
---

# Commit Workflow Best Practices

## Summary

Commit early and often with clear, conventional messages. Each commit should represent working, tested code that can be deployed or rolled back independently.

## When to Commit

### Commit After:
- Feature complete and tested
- Bug fixed and verified
- Refactor complete with tests passing
- Documentation updated
- Any working state worth saving

### Don't Commit:
- Broken code
- Failing tests
- Work in progress (unless WIP branch)
- Commented-out code
- Debug statements

## Commit Frequency

```
Too Infrequent:
Day's work in 1 commit ✗

Too Frequent:
Commit every line ✗

Just Right:
1-3 commits per hour ✓
Each commit is complete feature/fix ✓
```

## Conventional Commits

```bash
# Format
type(scope): description

# Types
feat: New feature
fix: Bug fix
docs: Documentation
style: Formatting
refactor: Code restructure
test: Add tests
chore: Maintenance
```

### Examples

```bash
feat(auth): add JWT authentication
fix(api): resolve CORS issue
docs(readme): update installation steps
test(auth): add integration tests
refactor(db): extract query helpers
```

## Using /commit Skill

```bash
# Let Claude analyze and suggest
/commit

Claude analyzes changes:
- 3 files modified
- Added auth service
- Updated API routes
- Added tests

Suggested message:
"feat(auth): implement JWT authentication

- Add auth service with token generation
- Create auth middleware
- Add login/register endpoints
- Include integration tests"

Confirm? (y/n)
```

## Commit Size

### Good Commits
```
- 1-10 files changed
- Single logical change
- All tests passing
- Clear purpose
```

### Too Large
```
- 50+ files changed
- Multiple unrelated changes
- Mixed concerns
- Hard to review
```

### Too Small
```
- Typo fix (unless critical)
- Single line change
- Incomplete work
```

## Commit Message Quality

### Good Messages
```
feat(auth): add password reset flow
fix(api): handle null user IDs
docs(api): document rate limiting
test(checkout): add payment failure scenarios
```

### Bad Messages
```
fixed stuff
wip
updates
asdf
final version
```

## Commit Workflow

```
1. Make changes
2. Run tests
3. Review changes (git diff)
4. Stage files (git add)
5. Write message
6. Commit
7. Verify (git log)
```

## With Claude

```bash
# Work session
User: "Add authentication"
[Claude implements]
[Tests pass]

# Commit
/commit

# Claude creates conventional commit
# With Co-Authored-By tag
```

## Atomic Commits

Each commit should:
- Build successfully
- Pass all tests
- Work independently
- Be revertable

## Key Takeaway

Commit working code frequently (1-3/hour) with conventional commit messages. Use /commit skill for smart commit messages. Each commit should be atomic, tested, and represent complete logical change. Early commits create safety nets for experimentation.
