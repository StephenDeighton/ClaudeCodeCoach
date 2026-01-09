---
slug: progressive-path
title: Progressive Enhancement Path
category: feature-selection
difficulty: beginner
keywords: progressive enhancement start simple upgrade path
commands: []
related: [feature-decision-guide, composition-hierarchy]
---

# Progressive Enhancement Path

## Summary

Start simple with built-in features, then progressively enhance with commands, skills, agents, and MCP servers as needs grow. This approach minimizes complexity while maximizing capability.

## Enhancement Levels

```
Level 1: Built-in Tools → Basic usage
Level 2: Commands → Quick data
Level 3: Skills → Workflows
Level 4: Agents → Autonomous work
Level 5: MCP Servers → External integration
```

## Level 1: Built-in Tools (Day 1)

### Start Here
```bash
# Just use Claude Code directly
claude

User: "Show me the auth code"
Claude: [reads files, shows code]

User: "Add error handling"
Claude: [edits files]

User: "Run the tests"
Claude: [runs bash commands]
```

### When This Works
✅ Learning the tool
✅ Small projects
✅ Simple tasks
✅ No workflow automation needed

### Limitations
❌ Repetitive commands
❌ No custom workflows
❌ Manual every time

## Level 2: Add Commands (Week 1)

### Enhance with Quick Data
```bash
# Create first command
cat > .claude/commands/status.sh << 'EOF'
#!/bin/bash
echo "Tests: $(find tests -name "*.test.ts" | wc -l)"
echo "Coverage: $(npm run coverage --silent | tail -1)"
echo "Build: $(npm run build 2>&1 | tail -1)"
EOF

chmod +x .claude/commands/status.sh

# Now use it
/status
```

### When to Add Commands
- Repeating same data requests
- Need quick status checks
- Simple operations

### Progressive Addition
```bash
# Start
/git-status

# Add more as needed
/test-count
/coverage
/file-tree
/line-count
```

## Level 3: Add Skills (Month 1)

### Enhance with Workflows
```bash
# Noticed you're manually doing multi-step commit process
# Create skill to automate

cat > .claude/skills/commit.md << 'EOF'
---
name: commit
description: Smart git commits
tools: [bash, read, git]
---

# Smart Commit
1. Check git status
2. Review changes
3. Generate conventional commit message
4. Confirm with user
5. Commit
EOF

# Now use it
/commit
```

### When to Add Skills
- Repeating multi-step workflows
- Need conversation context
- Want consistency

### Progressive Addition
```bash
# Start
/commit

# Add more workflows
/deploy staging
/test
/release
```

## Level 4: Add Agents (Month 2+)

### Enhance with Autonomy
```bash
# Complex features taking hours
# Start using agents

# Before
User: "Add authentication"
[Hours of back-and-forth]

# After
claude agent feature "Add JWT authentication"
[Agent works autonomously]
```

### When to Add Agents
- Features taking > 1 hour
- Complex exploration needed
- Can work independently
- Want parallel work

### Progressive Addition
```bash
# Start simple
claude agent explore "How does caching work?"

# Add feature agents
claude agent feature "Add dark mode"

# Add specialized
claude agent debug "Performance issues"
claude agent test "Increase coverage"
```

## Level 5: Add MCP (Month 3+)

### Enhance with External Services
```bash
# Need external data frequently
# Add MCP servers

# Before
User: "What PRs are open?"
Claude: "Let me check via gh CLI"
[Manual command every time]

# After (with GitHub MCP)
User: "What PRs are open?"
Claude: [Queries GitHub MCP directly]
"3 open PRs: #42, #43, #44"
```

### When to Add MCP
- Frequent external API use
- Team integrations needed
- Real-time data required

### Progressive Addition
```bash
# Start with common ones
- GitHub MCP
- Slack MCP

# Add as needed
- Database MCP
- Company API MCP
- Analytics MCP
```

## Real-World Progression

### Project: E-commerce Site

**Week 1-2: Built-in Only**
```bash
# Just chatting with Claude
"Show me the cart logic"
"Add validation"
"Run tests"
```

**Week 3: Add Commands**
```bash
# Getting tired of repeating
/test-count
/coverage
/build-status
```

**Month 2: Add Skills**
```bash
# Workflows emerging
/commit
/deploy staging
/test
```

**Month 3: Add Agents**
```bash
# Complex features
claude agent feature "Add payment system"
claude agent test "Improve coverage"
```

**Month 4: Add MCP**
```bash
# External integrations
GitHub MCP for PR management
Stripe MCP for payment testing
Slack MCP for deployment notifications
```

## Decision Points

### From Built-in → Commands
**Trigger**: "I keep asking for the same data"
**Solution**: Create command

### From Commands → Skills
**Trigger**: "I'm doing the same multi-step workflow repeatedly"
**Solution**: Create skill

### From Skills → Agents
**Trigger**: "This task takes hours and could run independently"
**Solution**: Use agent

### From Agents → MCP
**Trigger**: "We need external service data frequently"
**Solution**: Add MCP server

## Anti-Pattern: Jumping Ahead

### ❌ Don't Start with Agents
```bash
# Day 1
User: "How do I create an agent for my project?"
# Too complex, learn basics first
```

### ✅ Start Simple
```bash
# Day 1
User: "Help me understand this code"
Claude: [Uses built-in read tool]

# Week 2
"I keep checking test count"
→ Create /test-count command

# Month 2
"I keep doing commit process"
→ Create /commit skill

# Month 3
"I need to build large feature"
→ Use feature agent
```

## Optimization Path

```
Start: Do everything manually
  ↓
Automate: Repetitive data → Commands
  ↓
Streamline: Workflows → Skills
  ↓
Delegate: Complex work → Agents
  ↓
Integrate: External services → MCP
```

## Key Takeaway

Start simple with built-in Claude Code features. Add commands for repeated data requests, skills for common workflows, agents for autonomous work, and MCP servers for external integration. Let complexity emerge from actual needs rather than premature optimization. Most users never need agents or custom MCP servers - commands and skills cover 80% of use cases.
