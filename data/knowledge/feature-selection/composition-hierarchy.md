---
slug: composition-hierarchy
title: Feature Composition Hierarchy
category: feature-selection
difficulty: advanced
keywords: composition hierarchy features combine integrate
commands: []
related: [feature-decision-guide, progressive-path]
---

# Feature Composition Hierarchy

## Summary

Claude Code features compose hierarchically: commands provide data to skills, skills use MCP servers, agents spawn subagents and use skills. Understanding this hierarchy enables powerful workflow composition.

## Composition Hierarchy

```
MCP Servers (External Data)
     ↑
Commands (Quick Data) ←─┐
     ↑                   │
Skills (Workflows) ──────┤
     ↑                   │
Agents (Autonomous) ─────┘
```

## Level 1: Commands Use Nothing

Commands are atomic:

```bash
#!/bin/bash
# /test-count
find tests -name "*.test.ts" | wc -l
```

**Uses**: Bash, file system
**Doesn't use**: Skills, agents, MCP

## Level 2: Skills Use Commands

Skills can invoke commands:

```markdown
# /deploy skill

1. Check status: /git-status command
2. Check tests: /test-count command
3. If tests > 0 and status clean
4. Deploy
5. Check health: /api-health command
```

**Uses**: Commands, bash, tools
**Doesn't use**: Other skills (generally), agents

## Level 3: Skills Use MCP

Skills can query MCP servers:

```markdown
# /release skill

1. Get milestone from GitHub MCP
2. Build release
3. Run tests
4. Deploy
5. Close milestone via GitHub MCP
6. Notify team via Slack MCP
```

**Uses**: Commands, MCP servers, tools

## Level 4: Agents Use Skills

Agents can invoke skills:

```markdown
# Feature development agent

1. Explore codebase
2. Plan feature
3. Implement code
4. Use /test skill to run tests
5. Fix failures
6. Use /commit skill to commit
7. Use /deploy skill if needed
```

**Uses**: Skills, commands, MCP, tools

## Level 5: Agents Spawn Subagents

Agents can spawn other agents:

```markdown
# Release coordinator agent

1. Spawn test-agent (run full suite)
2. Spawn docs-agent (update docs)
3. Spawn build-agent (create bundles)
4. Wait for all to complete
5. Use /release skill
6. Verify deployment
```

**Uses**: Subagents, skills, commands, MCP, tools

## Composition Patterns

### Pattern 1: Skill + Commands

Skill orchestrates multiple commands:

```markdown
# /project-status skill

## Gather Data
- Git status: /git-status
- Test count: /test-count
- Coverage: /coverage
- Build status: /build-status

## Analyze & Report
Combine data into summary report
```

### Pattern 2: Skill + MCP

Skill uses external data:

```markdown
# /standup skill

## Gather from GitHub MCP
- PRs authored by me
- Issues assigned to me
- Commits since yesterday

## Format & Send
Post to Slack MCP #standup channel
```

### Pattern 3: Agent + Skills

Agent delegates workflows to skills:

```markdown
# Feature agent workflow

1. Explore & plan (agent)
2. Implement (agent)
3. /test skill (run & fix tests)
4. /lint skill (fix linting)
5. /docs skill (update docs)
6. /commit skill (create commit)
```

### Pattern 4: Agent + Subagents + Skills

Complex coordination:

```markdown
# Release agent

## Spawn parallel subagents
- test-subagent
  Uses /test skill internally
- docs-subagent
  Uses /docs skill internally
- build-subagent
  Runs builds

## Coordinate
Wait for subagents
Use /deploy skill
Use /notify skill (uses Slack MCP)
```

## Data Flow

### Bottom-Up

```
MCP Servers → External data
     ↓
Commands → Quick data
     ↓
Skills → Workflow results
     ↓
Agents → Feature implementation
```

### Example Flow

```
1. Agent spawns
2. Agent uses /test skill
3. Skill calls /test-count command
4. Command queries filesystem
5. Returns "42 tests"
6. Skill runs tests
7. Tests use GitHub MCP for fixtures
8. Results return to agent
9. Agent decides next action
```

## Composition Anti-Patterns

### ❌ Command Calls Skill
```bash
#!/bin/bash
# DON'T: Commands shouldn't call skills
/deploy  # Wrong
```

Commands should be atomic.

### ❌ Skill Spawns Agent
```markdown
# DON'T: Skills shouldn't spawn agents
1. Do thing
2. Spawn agent for next thing  # Wrong
```

Agents spawn themselves, not called by skills.

### ❌ Circular Dependencies
```markdown
# DON'T
Skill A uses Skill B
Skill B uses Skill A  # Circular
```

Keep dependency graph acyclic.

### ❌ Too Deep Nesting
```markdown
# DON'T
Agent → Subagent → Sub-subagent → ...
# Too complex to manage
```

Max 2-3 levels deep.

## Composition Benefits

### Code Reuse
```markdown
# /test skill used by
- User directly
- /deploy skill
- Feature agent
- CI/CD agent
- Release agent

# One implementation, many uses
```

### Maintainability
```bash
# Update /test skill once
# All users benefit automatically

# Before: 5 places with test logic
# After: 1 skill, 5 callers
```

### Flexibility
```markdown
# Mix and match as needed

Simple: Command only
Medium: Skill + Commands
Complex: Agent + Skills + MCP
Very Complex: Agent + Subagents + Skills + MCP + Commands
```

## Best Practices

### ✅ Do:
- Keep commands atomic
- Skills orchestrate commands
- Agents use skills when appropriate
- MCP servers provide external data
- Document composition relationships

### ❌ Don't:
- Create circular dependencies
- Over-nest (> 3 levels)
- Have commands call skills
- Mix concerns inappropriately
- Forget to handle errors at each level

## Real Example: Full Stack

```
Release Process
│
├─ Release Agent (coordinator)
│  ├─ Spawns test-subagent
│  │  └─ Uses /test skill
│  │     ├─ Calls /test-count command
│  │     └─ Uses database MCP for fixtures
│  │
│  ├─ Spawns docs-subagent
│  │  └─ Uses /docs skill
│  │     └─ Calls /api-endpoints command
│  │
│  └─ Main agent workflow
│     ├─ Uses /build skill
│     ├─ Uses /deploy skill
│     │  ├─ Calls /git-status command
│     │  └─ Uses GitHub MCP to create release
│     └─ Uses /notify skill
│        └─ Uses Slack MCP to announce
```

Each level handles its responsibility, composing upward for powerful workflows.

## Key Takeaway

Features compose hierarchically: commands provide data, skills orchestrate workflows, agents handle autonomous work. Higher levels use lower levels: skills use commands/MCP, agents use skills/subagents. This composition enables simple building blocks to create powerful, complex workflows while maintaining clarity and reusability.
