---
title: Skill Anti-Patterns
category: troubleshooting
commands: []
keywords: skills anti-patterns mistakes errors common-problems debugging
related_topics: [skill-best-practices, skills-vs-claude-md]
difficulty: intermediate
---

# Skill Anti-Patterns

## Summary

Learn common mistakes when creating Skills and how to avoid them. Understanding these anti-patterns helps you design more effective, maintainable skills.

## The God Skill

### ❌ Anti-Pattern

Creating one massive skill that does everything:

```markdown
# do-everything.md
---
description: Complete development workflow
---

1. Check code style with linter
2. Run all tests
3. Generate coverage report
4. Analyze code quality
5. Check for security issues
6. Update documentation
7. Build project
8. Create git commit
9. Push to remote
10. Create pull request
11. Notify team on Slack
12. Update project board
13. Generate release notes
```

### ✅ Better Approach

Break into focused skills:

```markdown
# test-and-commit.md
1. Run tests
2. If pass, commit changes

# deploy.md
1. Build project
2. Deploy to staging

# code-quality.md
1. Run linter
2. Generate coverage report
3. Show recommendations
```

**Why Better**: Each skill has single purpose, easier to maintain and debug

## The Duplicate

### ❌ Anti-Pattern

Multiple skills doing nearly the same thing:

```markdown
# test-then-commit.md
1. Run tests
2. Commit if passing

# test-and-commit.md
1. Run tests
2. Commit if passing

# commit-after-test.md
1. Run tests
2. Commit if passing
```

### ✅ Better Approach

One well-named skill:

```markdown
# test-before-commit.md
---
description: Run tests and commit if they pass
---
```

**Why Better**: Reduces confusion, easier to maintain

## The Vague Instruction

### ❌ Anti-Pattern

Instructions too vague to execute:

```markdown
# improve-code.md
---
description: Make the code better
---

1. Look at the code
2. Find issues
3. Fix them
4. Make it better
```

### ✅ Better Approach

Specific, actionable steps:

```markdown
# refactor-long-functions.md
---
description: Refactor functions over 50 lines
---

1. Find functions longer than 50 lines
2. For each function:
   - Identify logical sub-tasks
   - Extract sub-tasks into helper functions
   - Maintain test coverage
3. Verify all tests still pass
```

**Why Better**: Clear expectations, measurable outcomes

## The Context Dumper

### ❌ Anti-Pattern

Duplicating all of CLAUDE.md in every skill:

```markdown
# commit.md
---
description: Create a commit
---

**Context**:
Our project is a web application built with React and Node.js.
We use MongoDB for database. Our team follows agile methodology.
We have daily standups at 9am. Our coding standards require...
(500 more lines)

**Steps**:
1. Create commit
```

### ✅ Better Approach

Reference CLAUDE.md, add only skill-specific context:

```markdown
# commit.md
---
description: Create a commit following our conventions
---

**Context**: See CLAUDE.md for full git workflow

**Commit Format**: `type(scope): message`
- type: feat, fix, docs, refactor, test
- scope: affected module
- message: imperative tense, no period

**Steps**:
1. Stage changes with `git add`
2. Create commit with conventional format
3. Verify commit message follows format
```

**Why Better**: Avoids duplication, stays focused

## The Assumption Monster

### ❌ Anti-Pattern

Assuming tools or files exist:

```markdown
# deploy.md
1. Run `./deploy.sh production`
2. Check logs at `/var/log/app.log`
3. Notify #deployments Slack channel
```

### ✅ Better Approach

Check prerequisites, provide fallbacks:

```markdown
# deploy.md
1. Check if deploy.sh exists:
   - If yes: Run `./deploy.sh production`
   - If no: Ask user for deployment command
2. Check deployment status:
   - Look for logs in common locations
   - If not found, ask user where logs are
3. Confirm deployment succeeded
```

**Why Better**: Handles different project setups gracefully

## The Hard-Coder

### ❌ Anti-Pattern

Hard-coding specific values:

```markdown
# test-feature.md
1. Test the login function in src/auth/login.js line 42
2. Commit with message "Fixed bug #123 in sprint 5"
3. Assign PR to john@example.com
```

### ✅ Better Approach

Make it parameterized or interactive:

```markdown
# test-feature.md
1. Ask user: "Which feature should I test?"
2. Run tests for that feature
3. If passing, ask user for commit message
4. Create commit with provided message
```

**Why Better**: Reusable across different situations

## The Silent Failer

### ❌ Anti-Pattern

Not handling errors:

```markdown
# build-and-deploy.md
1. Build the project
2. Deploy to production
3. Done!
```

### ✅ Better Approach

Explicit error handling:

```markdown
# build-and-deploy.md
1. Run build command
   - If build fails:
     - Show build errors
     - STOP - do not deploy
     - Suggest common fixes
2. If build succeeds, deploy:
   - Confirm with user before deploying
   - If deployment fails:
     - Show error message
     - Suggest rollback if needed
3. If successful, confirm deployment
```

**Why Better**: Clear what happens when things go wrong

## The Recursive Loop

### ❌ Anti-Pattern

Skill that calls itself or creates infinite loops:

```markdown
# auto-fix.md
1. Run tests
2. If tests fail:
   - Try to fix automatically
   - Run /auto-fix again
```

### ✅ Better Approach

Clear termination conditions:

```markdown
# auto-fix.md
1. Run tests (max 3 attempts)
2. If tests fail:
   - Analyze failure
   - Apply fix
   - Re-run tests
3. If still failing after 3 attempts:
   - Report what was tried
   - Ask user for guidance
```

**Why Better**: Prevents infinite loops, clear limits

## The Overstepper

### ❌ Anti-Pattern

Skill doing more than described:

```markdown
# run-tests.md
---
description: Run test suite
---

1. Run tests
2. If tests fail, automatically fix the code
3. Refactor test files for better coverage
4. Update all documentation
5. Create performance benchmarks
6. Deploy to staging
```

### ✅ Better Approach

Do what the description says:

```markdown
# run-tests.md
---
description: Run test suite and report results
---

1. Execute test command (pytest, jest, etc.)
2. Show test results:
   - Number passed/failed
   - Failed test names
   - Error messages if any
3. If tests pass, confirm ready to commit
4. If tests fail, suggest next steps
```

**Why Better**: Predictable behavior, no surprises

## The Dependency Hell

### ❌ Anti-Pattern

Skill requires specific, undocumented setup:

```markdown
# deploy.md
1. Run `deploy-tool push --config ~/.deploy.secret.json`
```

*Skill fails because deploy-tool isn't installed*

### ✅ Better Approach

Check and document dependencies:

```markdown
# deploy.md
---
description: Deploy to production
---

**Prerequisites**:
- deploy-tool installed (`npm install -g deploy-tool`)
- Config file at ~/.deploy.json
- Production credentials configured

**Steps**:
1. Check if deploy-tool is available
   - If not: Show installation instructions
2. Check if config exists
   - If not: Ask user for config location
3. Run deployment command
```

**Why Better**: Self-documenting, handles missing deps

## Quick Diagnosis

| Symptom | Likely Anti-Pattern |
|---------|-------------------|
| Skill does too many things | God Skill |
| Multiple similar skills | The Duplicate |
| "Nothing happened" | The Vague Instruction |
| Skill has 100+ lines of context | The Context Dumper |
| Works on my machine only | The Assumption Monster |
| Only works in specific scenario | The Hard-Coder |
| Fails silently | The Silent Failer |
| Never stops running | The Recursive Loop |
| Does unexpected things | The Overstepper |
| "Command not found" errors | The Dependency Hell |

## Key Takeaway

Good skills are focused, explicit, and handle errors gracefully. If your skill is hard to name concisely, does more than expected, or fails mysteriously, you've likely hit one of these anti-patterns.
