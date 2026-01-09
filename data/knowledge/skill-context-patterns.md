---
title: Skill Context Patterns
category: advanced-patterns
commands: []
keywords: skills context patterns data-passing state-sharing
related_topics: [skill-best-practices, skills-vs-claude-md]
difficulty: advanced
---

# Skill Context Patterns

## Summary

Skills often need context from the current project state. Learn patterns for providing necessary context without duplicating CLAUDE.md or making skills brittle.

## The Context Problem

Skills run in specific project contexts but need to be somewhat portable. How do you balance project-specific information with reusability?

## Pattern 1: Reference, Don't Duplicate

### ❌ Anti-Pattern
```markdown
# commit.md

**Context**:
Our project uses Node.js with Express framework.
We use MongoDB for database storage.
Our coding standards require:
- ESLint with Airbnb config
- Prettier for formatting
- Jest for testing with >80% coverage
We follow agile methodology with 2-week sprints.
Our git workflow involves feature branches...
(300 more lines from CLAUDE.md)

**Steps**:
1. Create commit
```

### ✅ Better Pattern
```markdown
# commit.md

**Context**: Follow git conventions in CLAUDE.md

**Commit Format**: `type(scope): message`

**Steps**:
1. Verify changes follow our coding standards
2. Create commit with conventional format
3. Verify commit message is clear and descriptive
```

## Pattern 2: Contextual Discovery

Let Claude discover context as needed:

```markdown
# add-api-endpoint.md
---
description: Create a new REST API endpoint
---

**Discovery Phase**:
1. Find existing API endpoints by searching for route definitions
2. Identify the pattern used (Express, FastAPI, Django, etc.)
3. Locate where routes are registered

**Implementation**:
4. Create new endpoint following discovered pattern
5. Add corresponding service method if pattern uses service layer
6. Add basic tests matching existing test structure
```

**Why Effective**: Works across different frameworks without hard-coding

## Pattern 3: Ask for Specifics

```markdown
# deploy.md
---
description: Deploy application to specified environment
---

**Steps**:
1. Ask user: "Which environment? (staging/production)"
2. Ask user: "Which deployment method do you use?"
   - Options: Docker, SSH, CI/CD, Cloud platform, Other
3. Based on answer, proceed with appropriate deployment
4. Verify deployment succeeded
5. Provide rollback instructions if needed
```

**Why Effective**: Adapts to project-specific setup

## Pattern 4: Configuration Files

Reference external config instead of embedding:

```markdown
# run-quality-checks.md
---
description: Run code quality checks
---

**Configuration**: See `.claude/config/quality-checks.json`

**Steps**:
1. Read quality-checks.json for:
   - Linter command
   - Formatter command
   - Type checker command
   - Coverage threshold
2. Run each configured check
3. Report results
```

**quality-checks.json**:
```json
{
  "linter": "flake8 src/",
  "formatter": "black --check src/",
  "typeChecker": "mypy src/",
  "coverageThreshold": 80
}
```

**Why Effective**: Project-specific config separate from skill logic

## Pattern 5: Smart Defaults with Override

```markdown
# test-and-commit.md
---
description: Run tests and commit if passing
---

**Default Behavior**:
- Test command: Detect from project (pytest, jest, go test, etc.)
- Coverage threshold: 80%
- Commit format: Conventional Commits

**Override via .claude/config.json**:
```json
{
  "testCommand": "npm run test:ci",
  "coverageThreshold": 90,
  "commitFormat": "jira"
}
```

**Steps**:
1. Check for overrides in config.json
2. Use detected defaults if no override
3. Run tests with appropriate command
4. Check coverage meets threshold
5. Create commit in specified format
```

**Why Effective**: Works out of the box, customizable when needed

## Pattern 6: Project Type Detection

```markdown
# setup-ci.md
---
description: Set up CI/CD configuration
---

**Detection**:
1. Detect project type:
   - package.json → Node.js
   - requirements.txt → Python
   - go.mod → Go
   - Gemfile → Ruby

2. Detect test framework from:
   - package.json scripts
   - pytest.ini / tox.ini
   - Test file patterns

**Generation**:
3. Generate appropriate CI config:
   - GitHub Actions (.github/workflows/)
   - GitLab CI (.gitlab-ci.yml)
   - CircleCI (.circleci/config.yml)

4. Include detected test command
5. Set up quality checks for detected language
```

**Why Effective**: Truly portable across projects

## Pattern 7: Minimal Required Context

Only ask for what you absolutely need:

```markdown
# generate-migration.md
---
description: Generate database migration
---

**Required Context**:
- Database type (will detect or ask)
- Migration description (ask user)

**Steps**:
1. Detect database from imports/config:
   - SQLAlchemy → Alembic
   - Django ORM → Django migrations
   - Prisma → Prisma migrate
   - Other → Ask user

2. Ask user: "What does this migration do?"

3. Generate migration with appropriate tool

4. Show user the generated file location
```

**Why Effective**: Focused on essentials, discovers the rest

## Pattern 8: Context Inheritance

Skills can reference other skills:

```markdown
# full-deploy.md
---
description: Complete deployment workflow
---

**Steps**:
1. Run /test-and-commit skill
   (Inherits test configuration and commit conventions)

2. Build application:
   - Detect build tool
   - Run build command

3. Run /deploy skill with environment=production
   (Inherits deployment configuration)

4. Verify deployment succeeded
```

**Why Effective**: Reuses context from other skills

## Pattern 9: Convention Over Configuration

Assume common conventions, document exceptions:

```markdown
# add-model.md
---
description: Add a new database model
---

**Conventions Assumed**:
- Models in `models/` or `src/models/`
- One model per file
- File named `{model_name}_model.py` or `{model_name}.model.js`
- Tests in `tests/models/test_{model_name}.py`

**Override if Different**:
Specify in CLAUDE.md:
```markdown
## File Conventions
Models: `src/database/entities/{name}.entity.ts`
```

**Steps**:
1. Check CLAUDE.md for custom model location
2. If not found, use convention above
3. Create model file in appropriate location
4. Generate corresponding test file
```

**Why Effective**: Works immediately for standard setups, adaptable for custom

## Pattern 10: Progressive Context Building

Build context over multiple interactions:

```markdown
# optimize-performance.md
---
description: Analyze and optimize application performance
---

**Phase 1 - Discovery**:
1. What type of performance issue?
   - API response time
   - Database queries
   - Frontend rendering
   - Memory usage

**Phase 2 - Analysis** (based on Phase 1 answer):
- If API: Profile endpoint, identify slow queries
- If Database: Check indexes, query plans
- If Frontend: Check bundle size, rendering cycles
- If Memory: Profile heap, check for leaks

**Phase 3 - Optimization** (based on findings):
- Apply targeted fixes
- Measure improvement
- Document changes
```

**Why Effective**: Gathers context progressively, avoids overwhelming upfront

## Real-World Example

Combining multiple patterns:

```markdown
# prepare-release.md
---
description: Prepare a new release
---

**Pattern: Reference + Discovery + Ask**

**Context**: See CLAUDE.md for versioning scheme

**Discovery**:
1. Detect current version from:
   - package.json (Node)
   - pyproject.toml (Python)
   - git tags

**User Input**:
2. Ask: "Bump major, minor, or patch?"
3. Ask: "Any breaking changes?" (for changelog)

**Actions**:
4. Update version in appropriate file
5. Generate changelog from commits since last tag
6. Create git tag
7. Ask: "Push tag and create GitHub release?"
```

## Anti-Patterns

### ❌ The Context Novel
Embedding entire project history and philosophy

### ❌ The Context Void
No context, skill fails on every project

### ❌ The Hard-Coder
Hard-coding every project-specific detail

## Key Takeaway

Great skills balance portability with project specificity. Reference CLAUDE.md for stable context, discover project patterns dynamically, and ask users only for information that can't be detected.
