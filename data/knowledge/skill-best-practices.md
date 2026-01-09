---
title: Skill Best Practices
category: advanced-patterns
commands: ["/skill"]
keywords: skills custom-commands automation best-practices patterns
related_topics: [skills-vs-claude-md, skill-context-patterns]
difficulty: intermediate
---

# Skill Best Practices

## Summary

Skills are powerful automation tools in Claude Code. Well-designed skills are reusable, maintainable, and provide clear value. Learn how to create effective skills that enhance your workflow.

## Anatomy of a Good Skill

```markdown
# .claude/skills/test-and-commit.md
---
description: Run tests and commit if they pass
---

**Context**: This project requires all commits to pass tests first

**Steps**:
1. Run the test suite with `pytest`
2. If all tests pass:
   - Stage all changes with `git add .`
   - Create a descriptive commit message
   - Commit the changes
3. If tests fail:
   - Show the test output
   - Do NOT commit
   - Explain what needs to be fixed

**Success Criteria**:
- Tests passing AND changes committed
- OR tests failing AND clear explanation provided
```

## Skill Structure

### Required: Description

```yaml
---
description: Clear, concise description (shown in skill list)
---
```

**Good descriptions**:
- ✅ "Run tests before committing"
- ✅ "Deploy to staging environment"
- ✅ "Generate API documentation"

**Bad descriptions**:
- ❌ "Do stuff" (too vague)
- ❌ "Run tests, commit changes, push to remote, update docs, notify team" (too long)
- ❌ "test-commit" (not a description)

### Optional: Context Section

Provide relevant background:

```markdown
**Context**:
- This project uses pytest for testing
- All tests must pass before committing
- We follow conventional commit format
```

### Required: Clear Instructions

Be specific about what Claude should do:

```markdown
**Steps**:
1. Check if package.json exists
2. Run `npm test` to execute test suite
3. If exit code is 0 (success):
   - Ask user for commit message
   - Commit with that message
4. If exit code is not 0 (failure):
   - Show test output
   - Abort without committing
```

## Skill Categories

### 1. Workflow Automation

**Purpose**: Automate repeated processes

**Examples**:
- Test before commit
- Build and deploy
- Create pull request
- Run linters and formatters

```markdown
# format-and-check.md
---
description: Format code and run linters
---

1. Run code formatter (black for Python, prettier for JS)
2. Run linter (flake8 for Python, eslint for JS)
3. If any issues found, show them and stop
4. If all checks pass, confirm code is ready for commit
```

### 2. Code Generation

**Purpose**: Generate boilerplate following patterns

**Examples**:
- Create new API endpoint
- Add database model
- Generate test file

```markdown
# add-endpoint.md
---
description: Create a new REST API endpoint
---

Ask user for:
- Resource name (e.g., "products")
- HTTP method (GET, POST, PUT, DELETE)

Then create:
1. Route handler in `api/routes/{resource}_routes.py`
2. Service method in `services/{resource}_service.py`
3. Test file in `tests/api/test_{resource}_routes.py`

Follow existing patterns from user_routes.py
```

### 3. Analysis and Reports

**Purpose**: Generate insights about codebase

**Examples**:
- Code coverage report
- Dependency audit
- Performance analysis

```markdown
# coverage-report.md
---
description: Generate test coverage report with insights
---

1. Run `pytest --cov=src --cov-report=term-missing`
2. Analyze the output
3. Identify files with <80% coverage
4. Suggest which files need more tests
5. Provide example test cases for low-coverage functions
```

### 4. Project Setup

**Purpose**: Initialize common configurations

**Examples**:
- Set up pre-commit hooks
- Initialize CI/CD config
- Create project structure

```markdown
# setup-precommit.md
---
description: Configure pre-commit hooks for this project
---

1. Install pre-commit if not present
2. Create .pre-commit-config.yaml with:
   - black (Python formatter)
   - flake8 (linter)
   - pytest (run tests)
3. Run `pre-commit install`
4. Test by running `pre-commit run --all-files`
```

## Best Practices

### ✅ DO: Make Skills Focused

**Good** (single purpose):
```markdown
# test.md - Run test suite
# commit.md - Create commit
# deploy.md - Deploy to server
```

**Bad** (too broad):
```markdown
# do-everything.md - Test, commit, push, deploy, notify
```

### ✅ DO: Provide Context

```markdown
**Context**:
- We use pytest with pytest-cov for testing
- Minimum coverage requirement: 80%
- Fast tests in tests/unit/, slow tests in tests/integration/
```

### ✅ DO: Handle Errors

```markdown
3. If tests fail:
   - Show which tests failed
   - Display error messages
   - Suggest potential fixes
   - Do NOT proceed with commit
```

### ✅ DO: Make Skills Reusable

Write skills that work across similar projects:

```markdown
# generic-test-commit.md
1. Detect test framework (pytest, jest, go test)
2. Run appropriate test command
3. If pass, commit; if fail, show errors
```

### ❌ DON'T: Hard-Code Specifics

**Bad**:
```markdown
1. Test the login function in auth/login.py line 42
2. Commit with message "Fixed bug #123"
```

**Good**:
```markdown
1. Ask user which function to test
2. Run tests for that function
3. Ask user for commit message if tests pass
```

### ❌ DON'T: Duplicate CLAUDE.md

**Bad** (redundant):
```markdown
# commit.md
Context: We use git for version control. Git is a distributed system...
(300 lines of git documentation)
```

**Good** (reference):
```markdown
# commit.md
Context: Follow our git conventions defined in CLAUDE.md

Steps: ...
```

### ❌ DON'T: Make Overly Complex Skills

**Bad** (too complex):
```markdown
1. Run tests
2. If pass, analyze code quality
3. Generate performance report
4. Check security vulnerabilities
5. Update documentation
6. Create commit
7. Push to remote
8. Create PR
9. Notify team
10. Update project board
```

**Good** (focused):
```markdown
1. Run tests
2. If pass, commit changes
```

## Naming Conventions

### File Names

```
test-before-commit.md    # Descriptive, hyphenated
add-api-endpoint.md      # Action-oriented
review-pr.md             # Verb-noun pattern
```

### Avoid

```
test.md                  # Too generic
test_commit.md           # Use hyphens, not underscores
my-skill-v2-final.md     # No versions in filename
```

## Testing Skills

Before adding a skill to your repo:

1. **Test Manually**: Run the skill and verify behavior
2. **Test Edge Cases**: What if tests fail? What if files don't exist?
3. **Test on Fresh Clone**: Does it work without local setup?

## Documentation

### README for Skills

Create `.claude/skills/README.md`:

```markdown
# Custom Skills

## Available Skills

### /test-and-commit
Runs test suite and commits if passing

### /add-endpoint
Creates a new API endpoint following our patterns

### /coverage-report
Generates test coverage report with recommendations

## Creating New Skills

Follow patterns in existing skills:
- Clear description
- Numbered steps
- Error handling
- Success criteria
```

## Skill Organization

### Small Projects (< 5 skills)
```
.claude/
  skills/
    test-commit.md
    deploy.md
    coverage.md
```

### Large Projects (> 5 skills)
```
.claude/
  skills/
    README.md
    testing/
      test-commit.md
      coverage-report.md
    deployment/
      deploy-staging.md
      deploy-production.md
    code-gen/
      add-endpoint.md
      add-model.md
```

## Key Takeaway

Great skills are focused, well-documented, and handle errors gracefully. They automate repeated tasks without over-engineering. Keep them simple, test them thoroughly, and maintain them like code.
