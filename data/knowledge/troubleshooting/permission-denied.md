---
slug: permission-denied
title: Permission Denied Errors
category: troubleshooting
difficulty: intermediate
keywords: permission denied blocked restricted access
commands: ["/allowed-tools"]
related: [permission-config, toggle-modes]
---

# Permission Denied Errors

## Symptoms
- "Permission denied" messages
- "Tool not allowed" errors
- Operations blocked
- Can't write/execute

## Common Causes

### 1. Permission Mode
```bash
# In Plan mode (read-only)
Shift+Tab
# Check mode indicator
# Switch to Normal if needed
```

### 2. Tool Restrictions
```bash
# Check allowed tools
/allowed-tools

# May show git_push denied
```

### 3. File Permissions
```bash
# File not executable
ls -la script.sh
# Fix
chmod +x script.sh
```

### 4. Project Config
```json
// .claude/config.json may restrict tools
{
  "permissions": {
    "deniedTools": ["docker", "kubectl"]
  }
}
```

## Solutions

### Switch Permission Mode
```bash
# If in Plan mode
Shift+Tab → Normal Mode

# If in Normal mode already
# Check tool restrictions
```

### Check Configuration
```bash
# View effective settings
claude --show-config

# Check project restrictions
cat .claude/config.json
```

### Temporary Override
```bash
# Allow tool for session
/allow-tool docker

# Disable restrictions
claude --no-restrictions
```

### Fix File Permissions
```bash
# Make executable
chmod +x .claude/hooks/post-commit.sh
chmod +x .claude/commands/status.sh
```

## Enterprise Policies

```bash
# Check if policy blocks operation
/policy

Enterprise Policy: Enabled
Restrictions:
- Docker: Not allowed
- Kubernetes: Not allowed
```

Can't override enterprise policies. Work within constraints or contact admin.

## Key Takeaway
Permission denied usually means wrong mode (Plan vs Normal) or tool restrictions. Check mode with Shift+Tab, verify allowed tools with /allowed-tools, and check .claude/config.json for project restrictions.
