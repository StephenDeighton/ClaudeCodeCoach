---
slug: commands-overview
title: Commands Overview
category: project-setup
difficulty: intermediate
keywords: commands scripts tools utilities quick data
commands: []
related: [creating-commands, skills-overview, agents-overview]
---

# Commands Overview

## Summary

Commands are lightweight scripts that provide quick data or perform single operations. Unlike skills (multi-step workflows), commands return results immediately without conversation context.

## Commands vs Skills

### Commands
- **Single operation**: One specific task
- **Returns data**: Quick results
- **No context**: Doesn't need conversation history
- **Fast**: Executes immediately
- **Examples**: `/git-status`, `/test-count`, `/file-tree`

### Skills
- **Multiple steps**: Full workflow
- **Uses context**: Can reference conversation
- **Tool access**: Can read/write files, run commands
- **Examples**: `/commit`, `/deploy`, `/review-pr`

## Built-in Commands

```bash
# System info
/status              # Claude Code status
/config              # View configuration
/allowed-tools       # Show allowed tools

# Git commands
/git-status          # Git status
/git-log             # Recent commits
/git-diff            # Show diff

# Project info
/file-tree           # Show directory structure
/test-count          # Count tests
/line-count          # Count lines of code
/dependencies        # List dependencies
```

List all commands:
```bash
/commands

Available commands:
  /git-status      Show git status
  /file-tree       Display directory tree
  /test-count      Count test files
  ...
```

## Using Commands

### Basic Usage

```bash
# Just the command
/git-status

# Output returned immediately
On branch main
Your branch is up to date with 'origin/main'.
```

### With Arguments

```bash
/file-tree src/
/line-count --include-tests
/git-log --since="1 week ago"
```

## Command Types

### 1. Information Commands

Return data about project:

```bash
/git-status          # Git state
/file-tree           # Directory structure
/dependencies        # Installed packages
/env-check           # Environment variables
```

### 2. Analysis Commands

Analyze code or project:

```bash
/test-count          # Count tests
/coverage            # Test coverage
/complexity          # Code complexity
/todo-list           # Find TODOs
/unused-exports      # Find unused exports
```

### 3. Quick Actions

Perform simple operations:

```bash
/clean-branches      # Delete merged branches
/format-staged       # Format staged files
/update-deps         # Update dependencies
/clear-cache         # Clear build cache
```

## Custom Commands

### Project Commands

Located in `.claude/commands/`:

```bash
your-project/
└── .claude/
    └── commands/
        ├── api-health.sh        # /api-health
        ├── db-status.py         # /db-status
        └── bundle-size.js       # /bundle-size
```

### User Commands

Located in `~/.claude/commands/`:

```bash
~/.claude/
└── commands/
    ├── todos.sh         # /todos (all projects)
    ├── uptime.sh        # /uptime (all projects)
    └── weather.py       # /weather (all projects)
```

## Command Structure

### Shell Script Command

```bash
#!/bin/bash
# File: .claude/commands/test-summary.sh
# Returns summary of test results

pytest --collect-only -q | tail -n 1
```

Usage:
```bash
/test-summary
# Output: 142 tests collected
```

### Python Command

```python
#!/usr/bin/env python3
# File: .claude/commands/line-stats.py
# Returns line count statistics

import os
import sys

def count_lines(directory):
    total = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file)) as f:
                    total += len(f.readlines())
    return total

if __name__ == '__main__':
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    print(f"Total lines: {count_lines(directory)}")
```

Usage:
```bash
/line-stats src/
# Output: Total lines: 3,482
```

### Node.js Command

```javascript
#!/usr/bin/env node
// File: .claude/commands/bundle-size.js
// Returns bundle size information

const fs = require('fs');
const path = require('path');

const distDir = 'dist';
let totalSize = 0;

fs.readdirSync(distDir).forEach(file => {
  const stats = fs.statSync(path.join(distDir, file));
  totalSize += stats.size;
  console.log(`${file}: ${(stats.size / 1024).toFixed(2)} KB`);
});

console.log(`\nTotal: ${(totalSize / 1024).toFixed(2)} KB`);
```

Usage:
```bash
/bundle-size
# Output:
# main.js: 245.32 KB
# vendor.js: 512.45 KB
# Total: 757.77 KB
```

## Command Arguments

### Positional Arguments

```bash
#!/bin/bash
# File: .claude/commands/git-commits-since.sh

since=${1:-"1 week ago"}
git log --oneline --since="$since"
```

Usage:
```bash
/git-commits-since "2 days ago"
```

### Flag Arguments

```bash
#!/bin/bash
# File: .claude/commands/test-count.sh

INCLUDE_TESTS=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --include-integration)
      INCLUDE_TESTS=true
      shift
      ;;
    *)
      shift
      ;;
  esac
done

find tests/ -name "test_*.py" | wc -l
```

Usage:
```bash
/test-count --include-integration
```

## Command Discovery

Claude loads commands from:
1. Built-in commands (always available)
2. `~/.claude/commands/` (user global)
3. `.claude/commands/` (project-specific)

```bash
# See where a command comes from
/commands --info git-status

Command: git-status
Source: built-in
Type: shell
Description: Show git status
```

## Making Commands Executable

```bash
# Create command
cat > .claude/commands/my-command.sh << 'EOF'
#!/bin/bash
echo "Hello from custom command"
EOF

# Make executable
chmod +x .claude/commands/my-command.sh

# Use it
/my-command
```

## Output Formatting

### Simple Text

```bash
#!/bin/bash
echo "Test Results:"
echo "  Passed: 142"
echo "  Failed: 3"
echo "  Skipped: 5"
```

### JSON Output

```bash
#!/bin/bash
cat << EOF
{
  "passed": 142,
  "failed": 3,
  "skipped": 5,
  "total": 150
}
EOF
```

### Markdown Table

```bash
#!/bin/bash
echo "| File | Lines | Tests |"
echo "|------|-------|-------|"
echo "| auth.py | 245 | 12 |"
echo "| api.py | 532 | 28 |"
```

## Error Handling

```bash
#!/bin/bash
# Check if directory exists
if [ ! -d "tests" ]; then
  echo "Error: tests/ directory not found" >&2
  exit 1
fi

# Run command
test_count=$(find tests -name "*.py" | wc -l)
echo "Found $test_count test files"
```

## Command Best Practices

### ✅ Do:
- Return results quickly (< 2 seconds)
- Handle missing inputs gracefully
- Provide clear output format
- Exit with appropriate status codes
- Make scripts executable

### ❌ Don't:
- Modify files (use skills for that)
- Require user input
- Take > 10 seconds to run
- Assume specific environment
- Print excessive debug info

## Common Command Patterns

### Git Information

```bash
#!/bin/bash
# .claude/commands/git-summary.sh

branch=$(git branch --show-current)
commits=$(git log --oneline origin/main..HEAD | wc -l)
modified=$(git status --short | wc -l)

echo "Branch: $branch"
echo "Commits ahead: $commits"
echo "Modified files: $modified"
```

### Project Statistics

```bash
#!/bin/bash
# .claude/commands/project-stats.sh

echo "Project Statistics"
echo "===================="
echo "Files: $(find src -name "*.py" | wc -l)"
echo "Lines: $(find src -name "*.py" -exec wc -l {} + | tail -1 | awk '{print $1}')"
echo "Tests: $(find tests -name "*.py" | wc -l)"
echo "TODOs: $(grep -r "TODO" src | wc -l)"
```

### Dependency Check

```bash
#!/bin/bash
# .claude/commands/deps-outdated.sh

npm outdated --json | jq -r 'to_entries[] | "\(.key): \(.value.current) → \(.value.latest)"'
```

## Combining with Claude

Commands provide data that Claude can use:

```bash
User: How many tests do we have?
Claude: Let me check
/test-count
# Output: 142 tests

Claude: You have 142 test files in your project.
```

## Key Takeaway

Commands are fast, single-purpose scripts that return data quickly. Use them for information gathering and quick operations. Keep commands simple, fast, and focused on returning useful data rather than complex workflows.
