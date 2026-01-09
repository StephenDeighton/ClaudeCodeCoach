---
slug: feature-decision-guide
title: Feature Selection Decision Guide
category: feature-selection
difficulty: intermediate
keywords: decision guide choose feature skill command agent MCP
commands: []
related: [skills-vs-commands, when-use-subagents, when-use-mcp]
---

# Feature Selection Decision Guide

## Summary

Claude Code offers skills, commands, agents, and MCP servers for different needs. Use this guide to choose the right feature based on complexity, duration, and interaction requirements.

## Decision Flowchart

```
Task to accomplish
       │
       ▼
Is it < 2 seconds? ──Yes──→ COMMAND
       │                    (git-status, file-tree)
       No
       ▼
Is it single operation? ──Yes──→ COMMAND
       │                         (test-count, line-count)
       No
       ▼
Is it multi-step workflow? ──Yes──→ SKILL
       │                            (/commit, /deploy)
       No
       ▼
Does it need external data? ──Yes──→ MCP SERVER
       │                             (GitHub, Slack, DB)
       No
       ▼
Is it autonomous work? ──Yes──→ AGENT
                               (feature-dev, debug, refactor)
```

## Feature Comparison Matrix

| Feature | Duration | Complexity | Interactive | Context | Use Case |
|---------|----------|------------|-------------|---------|----------|
| **Command** | < 2s | Low | No | None | Quick data retrieval |
| **Skill** | 1-10min | Medium | Yes | Session | Multi-step workflow |
| **Agent** | 10min+ | High | Async | Own | Autonomous work |
| **MCP** | Varies | Varies | Yes | Session | External integration |

## Commands

### When to Use
- Need data immediately
- Single operation
- No conversation context needed
- < 2 second response time

### Examples
```bash
/git-status       # Show git status
/test-count       # Count test files
/file-tree        # Display directory tree
/line-count       # Count lines of code
```

### Create Command When:
- Returning simple data
- No multi-step logic
- Fast execution critical
- No conversation needed

### Don't Use Commands For:
- Multi-step workflows
- Long-running operations
- Complex decision-making
- Needing conversation context

## Skills

### When to Use
- Multi-step workflow
- Needs conversation context
- 1-10 minute execution
- User interaction needed

### Examples
```bash
/commit           # Create git commit (multi-step)
/deploy staging   # Deploy with checks
/review-pr 123    # Review PR with analysis
/refactor file.ts # Safe refactoring
```

### Create Skill When:
- Multiple related steps
- Needs to reference conversation
- Interactive with user
- Moderate complexity

### Don't Use Skills For:
- Instant data (use command)
- Hours of work (use agent)
- External data fetch (use MCP)
- Fire-and-forget tasks

## Agents

### When to Use
- Autonomous work (10min+)
- Complex problem-solving
- Can run in background
- Makes independent decisions

### Examples
```bash
claude agent feature "Add authentication"
claude agent debug "Performance issues"
claude agent test "Increase coverage to 90%"
claude agent refactor "Extract service layer"
```

### Create Agent When:
- Task takes > 10 minutes
- Requires exploration
- Can work independently
- Complex decision-making needed

### Don't Use Agents For:
- Quick questions
- Simple operations
- Needing frequent user input
- Instant results needed

## MCP Servers

### When to Use
- Need external data
- Third-party integration
- Real-time data
- External services

### Examples
```bash
# GitHub MCP
"Show open PRs for this repo"

# Slack MCP
"Send message to #dev channel"

# Database MCP
"Query user table for stats"
```

### Create MCP Server When:
- Integrating external service
- Need real-time data
- Multiple projects need it
- API access required

### Don't Use MCP For:
- Internal project logic
- One-time operations
- Simple file operations
- No external dependency

## Decision Examples

### Example 1: Git Status

**Task**: Show current git status

**Options**:
- ❌ Skill: Too simple for multi-step
- ❌ Agent: Way overkill
- ❌ MCP: No external service
- ✅ Command: Perfect - fast, simple, data return

**Choice**: Command `/git-status`

### Example 2: Deploy Application

**Task**: Deploy to staging with checks

**Options**:
- ❌ Command: Too complex, multi-step
- ✅ Skill: Perfect - workflow with checks
- ❌ Agent: Don't need autonomous work
- ❌ MCP: Deployment logic is internal

**Choice**: Skill `/deploy staging`

### Example 3: Build New Feature

**Task**: Implement user authentication

**Options**:
- ❌ Command: Way too complex
- ❌ Skill: Too long for single workflow
- ✅ Agent: Perfect - autonomous, complex
- ❌ MCP: Internal feature, not external

**Choice**: Agent `claude agent feature "Add auth"`

### Example 4: GitHub Integration

**Task**: List and review open PRs

**Options**:
- ❌ Command: Needs GitHub API
- ❌ Skill: Needs external data
- ❌ Agent: Not autonomous task
- ✅ MCP: Perfect - external service

**Choice**: MCP Server (GitHub)

### Example 5: Run Tests

**Task**: Run test suite

**Options**:
- ✅ Command: If just count/status
- ✅ Skill: If run + analyze + fix
- ✅ Agent: If improve coverage autonomously
- ❌ MCP: No external service needed

**Choice**: Depends on goal
- Just status: Command `/test-count`
- Run and analyze: Skill `/test`
- Improve coverage: Agent `claude agent test`

## Composition

Features can work together:

### Skill uses Commands
```markdown
# /deploy skill
1. Check status: /git-status command
2. Run tests: /test-count command
3. Deploy
4. Verify
```

### Agent uses Skills
```markdown
# Feature agent
1. Plan approach
2. Create structure
3. Build feature
4. Use /commit skill
5. Use /test skill
```

### MCP used by Skills
```markdown
# /release skill
1. Get milestone: GitHub MCP
2. Build
3. Deploy
4. Close milestone: GitHub MCP
5. Notify: Slack MCP
```

## Quick Reference

### I need to...

**Get simple data quickly**
→ Command

**Execute multi-step workflow**
→ Skill

**Build feature autonomously**
→ Agent

**Integrate external service**
→ MCP Server

**Commit changes**
→ Skill (`/commit`)

**Deploy application**
→ Skill (`/deploy`)

**Debug complex issue**
→ Agent (debug-agent)

**Show git log**
→ Command (`/git-log`)

**Interact with GitHub**
→ MCP Server (GitHub)

**Run parallel exploration**
→ Agent (explore-agent)

**Get test coverage**
→ Command (`/coverage`)

**Improve test coverage**
→ Agent (test-agent)

## Feature Hierarchy

```
Project Level
├── MCP Servers (external integrations)
│   ├── GitHub
│   ├── Slack
│   └── Database
│
├── Agents (autonomous work)
│   ├── Feature Development
│   ├── Debugging
│   └── Refactoring
│
├── Skills (workflows)
│   ├── /commit
│   ├── /deploy
│   └── /test
│
└── Commands (quick data)
    ├── /git-status
    ├── /test-count
    └── /file-tree
```

## Cost Considerations

**Commands**: Free/cheap
- Fast execution
- Minimal tokens

**Skills**: Moderate
- Uses conversation context
- Moderate tokens

**Agents**: Expensive
- Long-running
- High token usage

**MCP**: Varies
- Depends on API costs
- External service pricing

**Optimization**: Use cheapest feature that meets needs.

## Key Takeaway

Choose features based on task needs:
- Commands for instant data
- Skills for multi-step workflows
- Agents for autonomous work
- MCP for external services

Start simple (command/skill) and escalate to agents only when needed. Features can compose for powerful combinations.
