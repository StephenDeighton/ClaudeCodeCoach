---
slug: mcp-connection
title: MCP Connection Issues
category: troubleshooting
difficulty: advanced
keywords: MCP connection failed server error
commands: []
related: [when-use-mcp]
---

# MCP Connection Issues

## Symptoms
- "MCP server not responding"
- "Connection failed"
- MCP queries timeout
- Server won't start

## Common Causes

### 1. Server Not Installed
```bash
# Check if MCP server installed
npx @modelcontextprotocol/server-github --version

# Install if missing
npm install -g @modelcontextprotocol/server-github
```

### 2. Missing Environment Variables
```bash
# GitHub MCP needs token
echo $GITHUB_TOKEN
# Should show ghp_...

# Set if missing
export GITHUB_TOKEN=ghp_your_token_here
```

### 3. Wrong Configuration
```json
// .claude/config.json
{
  "mcp": {
    "servers": {
      "github": {
        "command": "npx",  // Correct
        "args": ["-y", "@modelcontextprotocol/server-github"]
      }
    }
  }
}
```

### 4. Port Conflict
```bash
# Another process using port
lsof -i :3000

# Kill conflicting process or change port
```

### 5. Network Issues
```bash
# MCP server can't reach external API
ping api.github.com

# Check firewall
```

## Solutions

### Restart MCP Server
```bash
# Stop Claude
/exit

# Restart
claude

# MCP servers restart automatically
```

### Check MCP Status
```bash
# List MCP servers
claude --list-mcp

Available MCP servers:
✓ github (connected)
✗ slack (disconnected)
```

### Test MCP Manually
```bash
# Test GitHub MCP
export GITHUB_TOKEN=ghp_...
npx -y @modelcontextprotocol/server-github

# Should start without errors
```

### Debug Mode
```bash
export CLAUDE_MCP_DEBUG=1
claude

# Shows MCP connection details
```

### Disable Problematic MCP
```json
{
  "mcp": {
    "servers": {
      "github": {
        "enabled": false
      }
    }
  }
}
```

## Verification

```bash
# Test MCP query
User: "What GitHub repos do I have?"

# Should work if connected
# If error, MCP issue
```

## Key Takeaway
MCP connection issues stem from missing environment variables, incorrect configuration, or uninstalled servers. Verify tokens set, check config syntax, ensure servers installed, and test with --list-mcp.
