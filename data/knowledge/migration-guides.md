---
title: Migration and Deprecated Features
category: troubleshooting
commands: []
keywords: migration deprecated upgrade breaking-changes updates versions
related_topics: [claude-md-best-practices]
difficulty: intermediate
---

# Migration and Deprecated Features

## Summary

Claude Code evolves over time with new features and occasional deprecations. Learn how to identify deprecated patterns and migrate to current best practices.

## Common Deprecation Patterns

### 1. Old Config Locations

**Deprecated**:
```
project-root/
  claude_config.json    # Old location
```

**Current**:
```
project-root/
  .claude/
    config.json         # New location
```

**Migration**:
```bash
# Move config to new location
mkdir -p .claude
mv claude_config.json .claude/config.json
```

### 2. Legacy Instruction Files

**Deprecated**:
```
ANTHROPIC.md          # Old name
Claude_Instructions.md
```

**Current**:
```
CLAUDE.md             # Standard name
```

**Migration**:
```bash
# Rename to standard
mv ANTHROPIC.md CLAUDE.md
```

### 3. Old Skill Format

**Deprecated** (plain text):
```markdown
# my-skill.md
This skill does X.
Do step 1.
Do step 2.
```

**Current** (with frontmatter):
```markdown
# my-skill.md
---
description: Short description for skill list
---

**Steps**:
1. Step 1
2. Step 2
```

**Migration**:
1. Add YAML frontmatter with description
2. Structure content with headers
3. Use numbered steps for clarity

### 4. Inline Config in CLAUDE.md

**Deprecated**:
```markdown
# CLAUDE.md
```json
{
  "model": "opus",
  "features": {...}
}
```
```

**Current**:
```markdown
# CLAUDE.md (instructions only)
Project overview and conventions...
```

```json
// .claude/config.json (configuration)
{
  "model": "opus"
}
```

**Migration**: Separate config from instructions

## Breaking Changes to Watch

### Model Name Changes

**Deprecated**:
```json
{
  "model": "claude-2"
}
```

**Current**:
```json
{
  "model": "sonnet"  // or "opus", "haiku"
}
```

### Command Syntax Evolution

**Deprecated**:
```
:model opus         # Old prefix
```

**Current**:
```
/model opus        # Slash prefix
```

## Detecting Deprecated Patterns

### Health Check Indicators

The Health Scan feature detects:
- ✅ CLAUDE.md missing
- ✅ Config in wrong location
- ✅ Deprecated feature usage
- ✅ Old skill format

### Self-Audit

Run these checks periodically:

```bash
# Check for old config files
find . -maxdepth 1 -name "*claude*.json" -o -name "*anthropic*.md"

# Check for non-standard instruction files
ls -la | grep -i "claude\|anthropic"

# Check skill format
find .claude/skills -name "*.md" -exec grep -L "^---" {} \;
```

## Migration Strategy

### 1. Assess Impact

```markdown
**Before Migrating**:
- [ ] Read release notes for breaking changes
- [ ] Check which features you use
- [ ] Review CLAUDE.md and skills
- [ ] Backup current configuration
```

### 2. Test in Branch

```bash
# Create migration branch
git checkout -b migrate-claude-config

# Make changes
# Test thoroughly

# Commit if successful
git commit -m "chore: migrate to new Claude Code configuration format"
```

### 3. Update Gradually

Don't change everything at once:

**Week 1**: Update config location
**Week 2**: Migrate skill format
**Week 3**: Update CLAUDE.md patterns
**Week 4**: Remove deprecated features

### 4. Document Changes

Update CLAUDE.md:

```markdown
## Recent Changes

### 2024-01-15: Config Migration
- Moved config from root to .claude/config.json
- Separated configuration from CLAUDE.md
- Updated all skills to use frontmatter format

### Breaking Changes
- Old config location no longer supported
- Skills require description in frontmatter
```

## Common Migration Scenarios

### Scenario 1: Moving to .claude Directory

**Current State**:
```
project/
  claude_config.json
  my_skill.md
  CLAUDE.md
```

**Target State**:
```
project/
  .claude/
    config.json
    skills/
      my-skill.md
  CLAUDE.md
```

**Steps**:
```bash
# 1. Create structure
mkdir -p .claude/skills

# 2. Move config
mv claude_config.json .claude/config.json

# 3. Move skills
mv *_skill.md .claude/skills/

# 4. Rename skills to kebab-case
cd .claude/skills
for file in *_skill.md; do
    mv "$file" "${file//_/-}"
done

# 5. Test
claude  # Verify everything works

# 6. Clean up
cd ../..
rm -f old_config.json
```

### Scenario 2: Updating Skill Format

**Old Format**:
```markdown
# deploy.md
This skill deploys the app.

First, run tests.
Then, build the app.
Finally, deploy to server.
```

**New Format**:
```markdown
# deploy.md
---
description: Deploy application to production
---

**Prerequisites**:
- Tests passing
- Production credentials configured

**Steps**:
1. Verify tests pass: `npm test`
2. Build application: `npm run build`
3. Deploy to server: `./deploy.sh production`
4. Verify deployment succeeded

**Success Criteria**:
- Application accessible at production URL
- Health check returns 200 OK
```

### Scenario 3: Separating Config from Instructions

**Old CLAUDE.md**:
```markdown
# My Project

## Configuration
```json
{"model": "opus", "features": {...}}
```

## Instructions
Use Python 3.11...
```

**New Structure**:

**CLAUDE.md**:
```markdown
# My Project

## Overview
Python 3.11 web application...

## Instructions
Follow PEP 8...
```

**.claude/config.json**:
```json
{
  "model": "opus",
  "features": {
    "autoSave": true
  }
}
```

## Staying Current

### Subscribe to Updates

- Watch Claude Code release notes
- Check GitHub releases
- Follow deprecation warnings

### Periodic Review

Quarterly review:
```markdown
## Quarterly Claude Code Review Checklist

- [ ] Check for deprecation warnings in logs
- [ ] Review release notes since last check
- [ ] Run health scan on project
- [ ] Update skills to current format
- [ ] Review and update CLAUDE.md
- [ ] Test new features
- [ ] Remove deprecated patterns
```

### Version Pinning

If you need stability:

```json
// .claude/config.json
{
  "version": "0.5.0",  // Pin to specific version
  "allowUpdates": false
}
```

## When to Migrate

### Immediate (Security/Critical)
- Security vulnerabilities fixed
- Critical bug fixes
- Blocking issues

### Soon (Deprecation Announced)
- Feature marked as deprecated
- Migration guide available
- New approach clearly better

### Eventually (Nice to Have)
- Minor improvements
- New convenience features
- Better patterns emerge

### Never (Working Fine)
- No deprecation warning
- Current approach works well
- No clear benefit to change

## Getting Help

If migration is unclear:

1. **Check Health Scan**: Run health check for specific issues
2. **Read Release Notes**: Look for migration guides
3. **Ask Claude**: "How do I migrate from X to Y?"
4. **Check Examples**: Look at updated example projects
5. **Report Issues**: File GitHub issue if stuck

## Key Takeaway

Technology evolves, and so do best practices. Stay informed about deprecations, migrate proactively when possible, but don't fix what isn't broken. Use health scans to catch deprecated patterns early.
