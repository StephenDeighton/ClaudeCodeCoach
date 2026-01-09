---
slug: creating-skills
title: Creating Custom Skills
category: project-setup
difficulty: advanced
keywords: custom skills create build workflow automation
commands: []
related: [skills-overview, commands-overview, hooks-overview]
---

# Creating Custom Skills

## Summary

Create custom skills to encapsulate project-specific workflows into reusable slash commands. Skills are markdown files with YAML frontmatter that define multi-step processes Claude can execute.

## Quick Start

```bash
# Create skills directory
mkdir -p .claude/skills

# Create your first skill
cat > .claude/skills/build-test.md << 'EOF'
---
name: build-test
description: Build and test the project
tools: [bash, read]
---

# Build and Test

Run the full build and test suite.

## Process
1. Clean previous build
2. Run build command
3. Run test suite
4. Report results

```bash
npm run clean
npm run build
npm test
```

If tests fail, analyze failures and suggest fixes.
EOF

# Use it
claude
/build-test
```

## Skill File Structure

### Frontmatter (Required)

```markdown
---
name: skill-name
description: Short description of what this skill does
tools: [bash, read, write]
permissions: []
model: sonnet
args: []
---
```

### Frontmatter Fields

**name** (required): Slash command name
```yaml
name: deploy-staging
# Used as: /deploy-staging
```

**description** (required): One-line description
```yaml
description: Deploy application to staging environment
```

**tools** (optional): Required tools
```yaml
tools: [bash, read, write, git]
# Claude requests permission for these tools
```

**permissions** (optional): Special permissions
```yaml
permissions: [git_push, remote_exec, database]
```

**model** (optional): Preferred model
```yaml
model: opus  # Use Opus for this skill
```

**args** (optional): Argument definitions
```yaml
args:
  - name: environment
    type: string
    required: true
  - name: dry-run
    type: boolean
    default: false
```

## Skill Body (Markdown Content)

The body contains instructions for Claude:

```markdown
# Skill Title

Brief overview of what this skill accomplishes.

## Process
Step-by-step breakdown of the workflow.

## Code/Commands
Actual commands or code snippets to execute.

## Error Handling
How to handle common failures.

## Output
What to report back to the user.
```

## Complete Example: Database Migration Skill

```markdown
---
name: migrate
description: Run database migrations safely
tools: [bash, read, write]
permissions: [database]
model: sonnet
args:
  - name: direction
    type: string
    default: up
    choices: [up, down, redo]
  - name: steps
    type: integer
    default: 1
---

# Database Migration

Run database migrations with safety checks.

## Pre-flight Checks
1. Check current migration status
2. Verify database connection
3. Check for pending migrations
4. If production, confirm with user

## Backup (Production Only)
If database is production:
```bash
timestamp=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL > backups/db_$timestamp.sql
```

## Run Migration
```bash
# Check status
npm run migrate:status

# Run migrations
npm run migrate:${direction}
```

## Verification
1. Check migration completed successfully
2. Run basic health check queries
3. Verify app still starts

## Rollback Plan
If migration fails:
1. Stop immediately
2. Restore from backup (if production)
3. Report error details
4. Suggest fix

## Report Results
Provide summary:
- Migrations applied
- Time taken
- Any warnings
- Database state
```

## Example: Code Review Skill

```markdown
---
name: review-code
description: Comprehensive code review with security checks
tools: [read, bash]
model: opus
args:
  - name: path
    type: string
    description: File or directory to review
---

# Code Review

Perform thorough code review.

## Areas to Check

### 1. Code Quality
- Readability and maintainability
- DRY violations
- Magic numbers/strings
- Naming conventions

### 2. Best Practices
- Error handling
- Resource cleanup
- Async/await usage
- Type safety

### 3. Security
- SQL injection risks
- XSS vulnerabilities
- Authentication/authorization
- Sensitive data exposure
- Input validation

### 4. Performance
- N+1 queries
- Unnecessary loops
- Memory leaks
- Caching opportunities

### 5. Testing
- Test coverage gaps
- Edge cases
- Error conditions

## Output Format
For each issue found:
```
📍 file.py:42
🔴 Critical / 🟡 Warning / 🔵 Info
Description of issue
Suggested fix:
```code
fixed version
```
\```

## Prioritization
List issues by severity:
1. Critical (security, data loss)
2. High (bugs, major issues)
3. Medium (code quality)
4. Low (style, minor improvements)
```

## Argument Handling

### Simple Arguments

```markdown
---
name: deploy
args:
  - name: environment
    type: string
    required: true
---

Usage: /deploy staging
Access in skill: ${environment}
```

### Optional Arguments with Defaults

```markdown
---
name: test
args:
  - name: type
    type: string
    default: all
    choices: [unit, integration, e2e, all]
  - name: verbose
    type: boolean
    default: false
---

Usage: /test integration --verbose
```

### Multiple Arguments

```bash
/deploy staging --dry-run --notify-slack
```

## Using Variables in Skills

Skills can reference:

### Argument Variables
```markdown
Environment: ${environment}
Dry run: ${dry-run}
```

### Environment Variables
```markdown
Database: ${DATABASE_URL}
API Key: ${API_KEY}
```

### Dynamic Values
```bash
# Current date
today=$(date +%Y-%m-%d)

# Git branch
branch=$(git branch --show-current)
```

## Error Handling Patterns

### Graceful Failures

```markdown
## Error Handling

If build fails:
1. Show build error
2. Identify likely cause
3. Suggest fixes
4. Don't proceed to tests

If tests fail:
1. List failing tests
2. Show failure messages
3. Analyze common cause
4. Suggest fixes
5. Ask if should continue deployment
```

### Conditional Logic

```markdown
## Conditional Deployment

If environment is production:
- Require confirmation
- Run full test suite
- Backup database
- Use blue-green deployment

If environment is staging:
- Auto-deploy
- Run smoke tests
- Notify team channel
```

## Skill Best Practices

### ✅ Do:
- Keep skills focused on one workflow
- Document each step clearly
- Handle errors gracefully
- Provide clear output
- Test skills thoroughly

### ❌ Don't:
- Create overly complex skills
- Skip error handling
- Assume environment details
- Ignore security implications
- Forget user confirmation for dangerous operations

## Testing Skills

```bash
# Test in safe environment
claude --permission-mode plan
/your-skill --dry-run

# Test with actual execution
claude
/your-skill --verbose

# Check error handling
# (simulate failures)
```

## Skill Organization

```bash
.claude/skills/
├── build/
│   ├── build.md
│   ├── build-test.md
│   └── build-prod.md
├── database/
│   ├── migrate.md
│   ├── seed.md
│   └── backup.md
├── deploy/
│   ├── deploy-staging.md
│   └── deploy-prod.md
└── utils/
    ├── clean.md
    └── doctor.md
```

## Sharing Skills

### Team Repository

```bash
# Create shared skills repo
git init claude-skills
cd claude-skills

# Add skills
mkdir skills
cp ~/.claude/skills/*.md skills/

# Team members install
git clone team/claude-skills
ln -s $(pwd)/skills ~/.claude/skills/team
```

### Skill Packages

```bash
# Package structure
my-skill-pack/
├── package.json
├── README.md
└── skills/
    ├── skill1.md
    ├── skill2.md
    └── skill3.md

# Install
claude install-skills ./my-skill-pack
```

## Debugging Skills

### Enable Verbose Mode

```markdown
---
name: debug-example
---

# Debug Example

Set CLAUDE_DEBUG for detailed output:
```bash
export CLAUDE_DEBUG=1
/debug-example
```
\```
```

### Add Logging

```markdown
## Execution

```bash
echo "Starting deployment..."
npm run deploy
echo "Deployment complete"
```
\```
```

## Key Takeaway

Create custom skills by writing markdown files with YAML frontmatter in `.claude/skills/`. Keep skills focused, handle errors gracefully, and document steps clearly. Skills make complex workflows repeatable and shareable with your team.
