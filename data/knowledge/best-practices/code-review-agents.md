---
slug: code-review-agents
title: Code Review with Agents
category: best-practices
difficulty: advanced
keywords: code review agent automated review quality
commands: []
related: [agents-overview]
---

# Code Review with Agents

## Summary

Use specialized review agents to automatically check code for bugs, security issues, style problems, and best practice violations before committing or opening PRs.

## Review Agent Pattern

```bash
# Before committing
claude agent review "Review auth changes"

Agent checks:
- Logic errors
- Security vulnerabilities
- Code quality
- Test coverage
- Documentation
- Best practices
```

## Review Agent Configuration

```markdown
---
name: code-review
description: Comprehensive code review
type: review
model: opus
tools: [read, bash]
---

# Code Review Agent

## Review Areas

### 1. Correctness
- Logic errors
- Off-by-one errors
- Null/undefined handling
- Type mismatches

### 2. Security
- SQL injection
- XSS vulnerabilities
- Authentication issues
- Authorization bypass
- Data exposure

### 3. Performance
- N+1 queries
- Inefficient algorithms
- Memory leaks
- Unnecessary operations

### 4. Code Quality
- DRY violations
- Complex functions
- Magic numbers
- Unclear naming
- Missing comments

### 5. Testing
- Coverage gaps
- Missing edge cases
- Missing error cases

### 6. Best Practices
- Framework conventions
- Project patterns
- Style guide compliance
```

## Automated Review Workflow

```bash
# 1. Make changes
git add .

# 2. Pre-commit review
claude agent review --scope staged

# 3. Review reports issues
Agent found:
🔴 Critical: SQL injection risk in query
🟡 Warning: Function too complex (45 lines)
🔵 Info: Consider extracting helper

# 4. Fix issues
[Fix critical issues]

# 5. Re-review
claude agent review --scope staged

# 6. All clear, commit
git commit
```

## Review Skill

```markdown
---
name: review
description: Quick code review
tools: [read]
---

# Quick Review

Review changed files for:
1. Obvious bugs
2. Security issues
3. Style violations
4. Missing tests

Report findings by severity.
```

## Usage

```bash
# Before PR
/review

# Specific files
/review src/auth/

# With focus
/review security
/review performance
```

## Review Output Format

```markdown
## Code Review Results

### Critical Issues (2)
📍 src/auth/service.ts:45
🔴 SQL Injection Risk
Raw SQL with string concatenation
Fix: Use parameterized queries

📍 src/api/users.ts:23
🔴 Authentication Bypass
Missing auth check on sensitive endpoint
Fix: Add authMiddleware

### Warnings (3)
📍 src/db/queries.ts:67
🟡 N+1 Query
Loading users in loop
Fix: Use batch query

...

### Info (5)
...

## Summary
Critical: 2 (must fix)
Warnings: 3 (should fix)
Info: 5 (consider)

Overall: ⚠️ Address critical issues before merging
```

## Review Checklist

```
□ No critical security issues
□ No obvious bugs
□ Tests passing
□ Coverage adequate
□ Code quality acceptable
□ Documentation updated
□ Follows project conventions
```

## Integration

### Git Hook
```bash
#!/bin/bash
# .claude/hooks/pre-push.sh

# Review before push
claude agent review --scope changes

if [ $? -ne 0 ]; then
  echo "Review found critical issues"
  exit 1
fi
```

### CI/CD
```yaml
# .github/workflows/review.yml
- name: Claude Review
  run: |
    claude agent review --format json > review.json
    # Fail if critical issues
    jq '.critical | length' review.json | grep '^0$'
```

## Key Takeaway

Automated code review with agents catches bugs, security issues, and quality problems before they reach production. Use review agents before commits and PRs. Focus on critical/security issues first, address warnings as time permits.
