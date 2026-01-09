---
slug: when-use-mcp
title: When to Use MCP Servers
category: feature-selection
difficulty: advanced
keywords: MCP servers external integration API third-party
commands: []
related: [feature-decision-guide, when-use-subagents]
---

# When to Use MCP Servers

## Summary

Use MCP (Model Context Protocol) servers to integrate external services like GitHub, Slack, databases, or APIs into Claude Code. MCP servers provide Claude with access to external data and actions beyond the local filesystem.

## What are MCP Servers?

MCP servers are bridges between Claude and external services:

```
Claude Code
    ↓
MCP Server (GitHub)
    ↓
GitHub API
    ↓
Your Repositories
```

## When to Use MCP

### External Data Access
```bash
# Without MCP
User: "What PRs are open?"
Claude: "I can't access GitHub from here"

# With GitHub MCP
User: "What PRs are open?"
Claude: [queries GitHub via MCP]
"You have 3 open PRs:
- #42: Add authentication
- #43: Fix bug in parser
- #44: Update documentation"
```

### Third-Party Integrations
```bash
# Slack MCP
"Send deploy notification to #dev"

# Database MCP
"Show user count from production DB"

# Jira MCP
"List my assigned tickets"
```

### Real-Time Data
```bash
# Weather MCP
"What's the weather for deployment?"

# Stock MCP
"Check if market is open"

# Status MCP
"Is the API healthy?"
```

## Built-in MCP Servers

Common MCP servers:

### GitHub MCP
```bash
# Access repositories
"List open issues"
"Show PR #123"
"Create issue"
"Merge PR"
```

### Filesystem MCP
```bash
# Advanced file operations
"Search all Python files"
"Find large files"
"Compare directories"
```

### Database MCP
```bash
# Query databases
"Show user table schema"
"Count active users"
"Find recent orders"
```

### Slack MCP
```bash
# Team communication
"Send message to #channel"
"Get recent messages"
"Update status"
```

## When NOT to Use MCP

### Local File Operations
```bash
# Don't need MCP
# Use built-in tools instead
Read, Write, Edit files

# Only use Filesystem MCP for advanced operations
```

### Internal Project Logic
```bash
# Don't need MCP
# Use skills or commands
/test
/build
/commit
```

### Simple External Calls
```bash
# Don't need full MCP server
# Use bash command
curl https://api.example.com/status
```

## MCP vs Other Features

### MCP vs Command
```bash
# Command: Local operation
/git-status

# MCP: External service
GitHub: "Show open PRs"
```

### MCP vs Skill
```bash
# Skill: Internal workflow
/deploy

# MCP + Skill: Workflow with external data
/deploy (uses MCP to notify Slack)
```

### MCP vs Agent
```bash
# Agent: Autonomous local work
claude agent feature "Add auth"

# MCP: Data source for agent
Agent uses GitHub MCP to check existing auth patterns in other repos
```

## Creating Custom MCP Servers

### When to Create MCP Server:
- ✅ Integrating external API
- ✅ Multiple projects need it
- ✅ Real-time data required
- ✅ Third-party service

### Don't Create MCP Server:
- ❌ One-off operation
- ❌ Local files only
- ❌ Simple bash command works
- ❌ No external service

### Example: Custom API MCP

```typescript
// mcp-servers/company-api/index.ts
import { MCPServer } from '@modelcontextprotocol/sdk';

const server = new MCPServer({
  name: 'company-api',
  version: '1.0.0'
});

// Define tools
server.addTool({
  name: 'get-employee',
  description: 'Get employee information',
  inputSchema: {
    type: 'object',
    properties: {
      id: { type: 'string' }
    }
  },
  handler: async ({ id }) => {
    const response = await fetch(`https://api.company.com/employees/${id}`);
    return await response.json();
  }
});

server.start();
```

Configure in `.claude/config.json`:
```json
{
  "mcp": {
    "servers": {
      "company-api": {
        "command": "node",
        "args": ["mcp-servers/company-api/index.js"],
        "env": {
          "API_KEY": "${COMPANY_API_KEY}"
        }
      }
    }
  }
}
```

## MCP Use Cases

### Development Workflow

```bash
# Check GitHub issues
"Show high-priority bugs"

# Check CI/CD status
"Is the build passing?"

# Deploy notification
/deploy staging
# Skill uses Slack MCP to notify team
```

### Data Analysis

```bash
# Query production DB
"How many users signed up this week?"

# Check analytics
"What's our API error rate?"

# Monitor performance
"Show slow queries from last hour"
```

### Team Coordination

```bash
# Slack integration
"Send standup update"
"Check team availability"

# Calendar integration
"Am I free for deployment?"

# Jira integration
"Update ticket status"
```

## MCP Best Practices

### ✅ Do:
- Use for external services
- Cache responses when possible
- Handle API errors gracefully
- Document MCP capabilities
- Secure API keys properly

### ❌ Don't:
- Use for local file operations
- Store credentials in code
- Make excessive API calls
- Ignore rate limits
- Skip error handling

## MCP Configuration

### Enable MCP Servers

```json
{
  "mcp": {
    "enabled": true,
    "servers": {
      "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {
          "GITHUB_TOKEN": "${GITHUB_TOKEN}"
        }
      },
      "slack": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-slack"],
        "env": {
          "SLACK_TOKEN": "${SLACK_TOKEN}"
        }
      }
    }
  }
}
```

### Verify MCP Servers

```bash
# List available MCP servers
claude --list-mcp

Available MCP servers:
✓ github (connected)
✓ slack (connected)
✓ company-api (connected)
```

## MCP Security

### API Key Management

```bash
# Store in environment
export GITHUB_TOKEN=ghp_...
export SLACK_TOKEN=xoxb-...

# Never commit to repo
# Add to .gitignore
echo ".env" >> .gitignore
```

### Permission Scopes

```json
{
  "mcp": {
    "servers": {
      "github": {
        "permissions": ["read:repo", "read:issues"],
        "denyActions": ["delete:repo"]
      }
    }
  }
}
```

## Key Takeaway

Use MCP servers to integrate external services (GitHub, Slack, databases, APIs) with Claude Code. Create custom MCP servers for company APIs or services used across multiple projects. MCP servers provide Claude with access to real-time external data and actions, making workflows more powerful and connected.
