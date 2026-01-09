---
slug: permission-config
title: Permission Configuration
category: permission-modes
difficulty: advanced
keywords: permissions settings config allow deny tools restrictions
commands: ["/allowed-tools"]
related: [toggle-modes, auto-mode]
---

# Permission Configuration

## Summary

Configure fine-grained permissions for Claude Code through settings files and runtime commands. Control which tools and operations are allowed, set restrictions by mode, and enforce organizational policies.

## Permission Hierarchy

Permissions are checked in this order:

```
1. System safety rules (always enforced)
   ↓
2. Enterprise/organization policy
   ↓
3. User global settings (~/.claude/settings.json)
   ↓
4. Project settings (.claude/config.json)
   ↓
5. Current permission mode (Normal/Plan/Auto)
```

Lower levels can restrict but not expand upper levels.

## Configuration Files

### Global Settings

Location: `~/.claude/settings.json`

```json
{
  "permissions": {
    "defaultMode": "normal",
    "allowedTools": ["read", "write", "bash", "edit"],
    "deniedTools": ["docker", "kubectl"],
    "requireConfirm": ["git_push", "deploy"]
  }
}
```

### Project Settings

Location: `.claude/config.json`

```json
{
  "permissions": {
    "allowedTools": ["read", "write", "bash"],
    "deniedTools": ["docker"],
    "autoModeAllowed": false
  }
}
```

## Available Tools

Claude Code uses various tools for operations:

### File Operations
- `read` - Read file contents
- `write` - Create new files
- `edit` - Modify existing files
- `delete` - Remove files

### Code Operations
- `bash` - Execute shell commands
- `python` - Run Python scripts
- `node` - Run Node.js scripts

### Version Control
- `git_status` - Check git status
- `git_commit` - Create commits
- `git_push` - Push to remote
- `git_branch` - Branch operations

### External Tools
- `docker` - Docker operations
- `kubectl` - Kubernetes operations
- `npm` - NPM package management
- `pip` - Python package management

### System Operations
- `file_system` - Directory operations
- `process` - Process management
- `network` - Network operations

## Checking Current Permissions

### Command

```bash
/allowed-tools
```

Output:
```
Allowed tools in current mode:
✅ read
✅ write
✅ bash
✅ git_status
✅ git_commit
❌ git_push (requires confirmation)
❌ docker (denied)
❌ kubectl (denied)

Current mode: Normal
```

### Status Check

```bash
/status
```

Shows:
```
Mode: Normal
Allowed tools: 15
Denied tools: 3
Confirmations required: 2
```

## Mode-Specific Permissions

### Plan Mode Default Permissions

```json
{
  "planMode": {
    "allowedTools": [
      "read",
      "grep",
      "list",
      "git_log",
      "git_status"
    ],
    "deniedTools": [
      "write",
      "edit",
      "delete",
      "bash",
      "git_commit"
    ]
  }
}
```

### Auto Mode Restrictions

```json
{
  "autoMode": {
    "maxFilesPerOperation": 50,
    "requireConfirmFor": [
      "git_push",
      "deploy",
      "database_migration"
    ],
    "deniedPatterns": [
      "**/node_modules/**",
      "**/.git/**"
    ]
  }
}
```

## Allow/Deny Patterns

### Tool Patterns

```json
{
  "permissions": {
    "allowedTools": [
      "read",
      "write",
      "bash:ls",      // Allow only specific bash commands
      "bash:git",
      "bash:npm test"
    ],
    "deniedTools": [
      "bash:rm",      // Deny specific bash commands
      "bash:curl",
      "docker:*"      // Deny all docker
    ]
  }
}
```

### File Patterns

```json
{
  "permissions": {
    "allowedPaths": [
      "src/**",
      "tests/**"
    ],
    "deniedPaths": [
      "**/.env",
      "**/secrets/**",
      "node_modules/**"
    ]
  }
}
```

## Confirmation Requirements

Force confirmations for specific operations:

```json
{
  "permissions": {
    "requireConfirm": [
      {
        "tool": "git_push",
        "condition": "branch == 'main'"
      },
      {
        "tool": "delete",
        "condition": "fileCount > 10"
      },
      {
        "tool": "bash",
        "condition": "command.includes('rm')"
      }
    ]
  }
}
```

## Enterprise Policies

Organizations can enforce policies:

### Policy File

Location: Managed centrally, distributed to users

```json
{
  "enterprisePolicy": {
    "version": "1.0",
    "enforced": true,
    "permissions": {
      "deniedTools": [
        "docker",
        "kubectl",
        "ssh"
      ],
      "requireConfirm": [
        "git_push",
        "deploy",
        "database"
      ],
      "autoModeDisabled": true
    }
  }
}
```

### Checking Policy

```bash
/policy
```

Shows:
```
Enterprise Policy: Enabled
Version: 1.0

Restrictions:
- Auto mode: Disabled
- Docker: Not allowed
- Kubernetes: Not allowed
- SSH: Not allowed

Required confirmations:
- Git push
- Deployments
- Database operations
```

## Runtime Permission Changes

### Temporary Tool Allow

```bash
# Allow docker for this session only
/allow-tool docker

Docker temporarily allowed for this session.
```

### Temporary Tool Deny

```bash
# Deny git push for safety
/deny-tool git_push

Git push denied for this session.
```

Changes revert when session ends.

## Safety Rules (Cannot Override)

These are always enforced regardless of configuration:

❌ **Blocked:**
- `rm -rf /` or system directories
- Modifying Claude Code itself
- Accessing system passwords
- Network scanning/attacks
- Cryptomining operations

⚠️ **Always Confirm:**
- Deleting >100 files
- Force push to protected branches
- Database drops
- Production deployments

## Permission Debugging

### Why was operation blocked?

```bash
# Try operation
User: Delete all test files

Claude: Operation denied: batch delete not allowed

# Check why
/allowed-tools delete

# Shows
delete: ❌ Denied by project config
Reason: Batch operations restricted
Override: Use /allow-tool delete --temporary
```

### Permission Trace

```bash
/permission-trace git_push
```

Output:
```
Tool: git_push
Decision: Requires confirmation

Evaluated rules:
1. System safety: ✅ Pass
2. Enterprise policy: ⚠️  Requires confirm
3. Global settings: ✅ Allowed
4. Project settings: ✅ Allowed
5. Current mode: Normal - ✅ Allowed

Final: Allowed with confirmation required
```

## Common Configurations

### Restrictive (High Security)

```json
{
  "permissions": {
    "defaultMode": "plan",
    "autoModeAllowed": false,
    "allowedTools": ["read", "grep", "list"],
    "requireConfirm": ["write", "edit", "bash"]
  }
}
```

### Permissive (Trusted Environment)

```json
{
  "permissions": {
    "defaultMode": "auto",
    "allowedTools": ["*"],
    "deniedTools": ["docker:rm", "kubectl:delete"],
    "requireConfirm": []
  }
}
```

### Balanced (Recommended)

```json
{
  "permissions": {
    "defaultMode": "normal",
    "allowedTools": ["read", "write", "edit", "bash", "git"],
    "deniedTools": ["docker", "kubectl"],
    "requireConfirm": ["git_push", "delete_batch"]
  }
}
```

## Testing Permissions

```bash
# Test what would be allowed
/test-permission write src/test.js

Result: ✅ Allowed
Mode: Normal
Rules: Global settings allow file write

# Test auto mode operation
/test-permission bash:deploy --mode auto

Result: ⚠️  Requires confirmation
Mode: Auto
Rules: Enterprise policy requires confirm for deploy
```

## Best Practices

1. **Start Restrictive** - Begin with limited permissions, expand as needed
2. **Project-Specific** - Use `.claude/config.json` for project rules
3. **Document Policies** - Comment your permission configs
4. **Test Before Enforce** - Use `/test-permission` to verify rules
5. **Review Regularly** - Audit permissions quarterly
6. **Principle of Least Privilege** - Only allow what's necessary

## Troubleshooting

### "Permission denied" unexpectedly

```bash
# Check which rule blocked it
/permission-trace <operation>

# Check current permissions
/allowed-tools

# Check for enterprise policy
/policy
```

### "Can't enable Auto mode"

```bash
# Check if auto mode allowed
/status

# Check policy
/policy

# Override if permitted
/mode auto --force
```

### "Operation requires confirmation" in Auto mode

This is intentional for dangerous operations. Either:
1. Switch to Normal mode and confirm manually
2. Configure permission to not require confirmation (if appropriate)

## Key Takeaway

Permission configuration gives you fine-grained control over what Claude can do. Use project-level `.claude/config.json` for project-specific rules, check permissions with `/allowed-tools`, and follow the principle of least privilege. Enterprise policies can enforce organizational standards that can't be overridden at the project level.
