---
slug: agents-overview
title: Agents Overview
category: project-setup
difficulty: advanced
keywords: agents subagents autonomous background tasks parallel
commands: []
related: [creating-agents, skills-overview]
---

# Agents Overview

## Summary

Agents are autonomous Claude instances that run in parallel to handle complex, multi-step tasks independently. They can explore codebases, run tests, debug issues, and complete entire features while you work on other things.

## What are Agents?

Agents are specialized Claude instances that:
- Run autonomously with specific goals
- Work in parallel with your main session
- Have their own tool access and permissions
- Can spawn sub-agents for parallel work
- Report back when complete

## Agent vs Skill vs Command

### Agent (autonomous)
- Long-running (minutes to hours)
- Makes independent decisions
- Can explore and iterate
- Works in background
- Example: "Implement user authentication"

### Skill (workflow)
- Medium complexity (seconds to minutes)
- Follows defined steps
- Interactive with user
- Example: `/deploy`, `/commit`

### Command (instant)
- Quick operation (< 2 seconds)
- Returns data immediately
- No decision making
- Example: `/git-status`, `/test-count`

## Built-in Agents

Claude Code includes specialized agents:

### Explore Agent
```bash
# Explore codebase
claude explore "How does authentication work?"

# Scans code, traces execution, explains architecture
```

### Feature Development Agent
```bash
# Build complete feature
claude feature "Add password reset flow"

# Plans, implements, tests, documents
```

### Debug Agent
```bash
# Debug complex issue
claude debug "Users can't login on mobile"

# Investigates, finds root cause, suggests fix
```

### Refactor Agent
```bash
# Safe refactoring
claude refactor "Extract auth logic to service layer"

# Analyzes impact, performs refactor, maintains tests
```

### Test Agent
```bash
# Improve test coverage
claude test "Increase auth module coverage to 90%"

# Analyzes gaps, writes tests, verifies coverage
```

## Starting Agents

### From Command Line

```bash
# Start agent
claude agent feature "Add dark mode toggle"

# Agent runs autonomously
Agent started: feature-dark-mode-a3b2
Working on: Add dark mode toggle
Progress updates will appear here...
```

### From Within Session

```bash
# In active session
User: Can you work on adding dark mode in the background?

Claude: I'll spawn a feature agent to handle this
[Spawns agent]

Agent spawned: feature-dark-mode
You can continue working while it runs.
Check status: /agent status feature-dark-mode
```

## Agent Lifecycle

### 1. Planning Phase
- Agent receives goal
- Explores relevant code
- Creates implementation plan
- Identifies dependencies

### 2. Execution Phase
- Implements changes
- Runs tests
- Fixes issues iteratively
- Documents work

### 3. Completion Phase
- Verifies success
- Reports results
- Commits changes (if configured)
- Returns control

## Monitoring Agents

### Check Status

```bash
# List active agents
/agents

Active agents:
  feature-dark-mode (running, 5m)
  debug-login-issue (completed, 12m ago)
  refactor-auth (running, 2m)

# Check specific agent
/agent status feature-dark-mode

Agent: feature-dark-mode
Status: Running
Progress: 60% (3/5 tasks complete)
Current: Adding theme toggle component
Time: 5m 23s
```

### View Agent Output

```bash
# Stream agent output
/agent logs feature-dark-mode

[14:23:15] Created theme context
[14:24:32] Added toggle component
[14:25:41] Updating existing components...
[14:26:18] Running tests...
```

### Agent Communication

```bash
# Send message to agent
/agent message feature-dark-mode "Use local storage for theme preference"

# Agent acknowledges
Agent feature-dark-mode: Acknowledged. Will use localStorage.
```

## Parallel Agents

### Running Multiple Agents

```bash
# Start multiple agents for parallel work
claude agent feature "Add user profiles" &
claude agent feature "Add notification system" &
claude agent test "Increase coverage to 90%" &

# All run in parallel
3 agents started:
  feature-profiles-x9z1
  feature-notifications-k2m4
  test-coverage-w5n7
```

### Agent Coordination

Agents can coordinate:

```bash
# Agent 1: Frontend work
# Agent 2: Backend work
# Agent 3: Tests

# They communicate through shared context
# Resolve conflicts automatically
# Report integration issues
```

## Agent Specialization

### Code Exploration Agent

```bash
claude explore "How is caching implemented?"

Agent will:
- Find cache-related code
- Trace data flow
- Document cache strategy
- Identify improvement opportunities
```

### Security Audit Agent

```bash
claude security "Audit authentication system"

Agent will:
- Check for vulnerabilities
- Review auth flows
- Test edge cases
- Report findings with severity
```

### Performance Agent

```bash
claude performance "Optimize API response times"

Agent will:
- Profile current performance
- Identify bottlenecks
- Implement optimizations
- Measure improvements
```

## Agent Configuration

### Agent Permissions

Configure in `.claude/config.json`:

```json
{
  "agents": {
    "defaultModel": "sonnet",
    "defaultPermissionMode": "auto",
    "maxConcurrent": 3,
    "allowedAgents": ["feature", "test", "debug"],
    "permissions": {
      "feature": {
        "tools": ["read", "write", "bash", "git"],
        "autoCommit": false
      },
      "test": {
        "tools": ["read", "write", "bash"],
        "autoCommit": true
      }
    }
  }
}
```

### Agent Limits

```json
{
  "agents": {
    "maxConcurrent": 3,
    "maxDuration": 3600,
    "maxTokens": 100000,
    "requireApproval": ["deploy", "database"]
  }
}
```

## Agent Best Practices

### ✅ When to Use Agents:
- Long-running tasks (> 5 minutes)
- Independent work that can run in parallel
- Exploration of unfamiliar code
- Automated testing or documentation
- Complex refactoring

### ❌ When Not to Use Agents:
- Quick questions or simple tasks
- Work requiring frequent user input
- Critical changes needing oversight
- Tasks with unclear requirements

## Agent Output

### Success Report

```
Agent feature-dark-mode completed successfully

Summary:
✓ Added theme context provider
✓ Created theme toggle component
✓ Updated 15 components to use theme
✓ Added theme persistence
✓ All tests passing (142/142)

Files changed: 17
Lines added: 342
Lines removed: 89

Next steps:
- Review changes in src/theme/
- Test theme switching in browser
- Commit changes
```

### Failure Report

```
Agent feature-notifications failed

Error: Test failures in notification service

Details:
- 3 tests failing in tests/notifications/
- Issue with WebSocket connection handling
- Suggested fix: Add connection retry logic

Files changed: 8 (partial)
Time spent: 15m

Recommendations:
1. Fix test failures
2. Add retry logic to WebSocket client
3. Rerun agent after fixes
```

## Stopping Agents

```bash
# Stop specific agent
/agent stop feature-dark-mode

# Stop all agents
/agent stop-all

# Cancel and rollback changes
/agent cancel feature-dark-mode --rollback
```

## Agent Communication

### Agent to User

Agents can ask for clarification:

```
Agent feature-profiles:
Question: Should profile images be stored in S3 or database?
Options:
  1. S3 (recommended for scalability)
  2. Database (simpler setup)
  3. Let me decide

/agent reply feature-profiles 1
```

### User to Agent

```bash
# Provide guidance
/agent message feature-profiles "Use PostgreSQL for user data"

# Change direction
/agent message feature-profiles "Actually, prioritize mobile view first"
```

## Creating Custom Agents

See [Creating Agents](creating-agents.md) for detailed guide.

Quick example:

```markdown
---
name: documentation-agent
description: Generate comprehensive documentation
type: feature
model: opus
tools: [read, write]
---

# Documentation Agent

Generate complete documentation for the project.

## Tasks
1. Analyze codebase structure
2. Generate API documentation
3. Create usage examples
4. Write tutorials
5. Update README
```

## Key Takeaway

Agents are autonomous Claude instances for complex, long-running tasks. Use them for feature development, debugging, testing, and exploration that can run independently. Monitor with `/agents`, communicate with `/agent message`, and let them work in parallel while you focus on other tasks.
