---
slug: creating-commands
title: Creating Custom Commands
category: project-setup
difficulty: intermediate
keywords: commands create custom scripts tools utilities
commands: []
related: [commands-overview, creating-skills]
---

# Creating Custom Commands

## Summary

Create custom commands as executable scripts in `.claude/commands/` to provide quick data or perform single operations. Commands are simpler than skills and return results immediately.

## Quick Start

```bash
# Create commands directory
mkdir -p .claude/commands

# Create your first command
cat > .claude/commands/hello.sh << 'EOF'
#!/bin/bash
echo "Hello from custom command!"
EOF

# Make executable
chmod +x .claude/commands/hello.sh

# Use it
claude
/hello
# Output: Hello from custom command!
```

## Command File Naming

```bash
.claude/commands/
├── git-summary.sh       # /git-summary
├── test-stats.py        # /test-stats
├── bundle-size.js       # /bundle-size
└── db-check.sh          # /db-check
```

File name = command name (without extension).

## Shell Script Commands

### Basic Template

```bash
#!/bin/bash
# Description: Brief description of what this command does
# Usage: /command-name [args]

# Your command logic here
echo "Command output"
```

### Example: Git Statistics

```bash
#!/bin/bash
# File: .claude/commands/git-stats.sh
# Description: Show git repository statistics
# Usage: /git-stats

branch=$(git branch --show-current)
commit_count=$(git rev-list --count HEAD)
author_count=$(git log --format='%an' | sort -u | wc -l)
file_count=$(git ls-files | wc -l)

cat << EOF
Git Repository Statistics
=========================
Branch: $branch
Total commits: $commit_count
Contributors: $author_count
Tracked files: $file_count
EOF
```

### Example: Test Summary

```bash
#!/bin/bash
# File: .claude/commands/test-summary.sh
# Description: Show test suite summary
# Usage: /test-summary

# Run tests and capture output
output=$(pytest --collect-only -q 2>&1)

# Parse results
total=$(echo "$output" | grep -oP '\d+(?= test)' | head -1)
unit=$(find tests/unit -name "test_*.py" | wc -l)
integration=$(find tests/integration -name "test_*.py" | wc -l)

cat << EOF
Test Suite Summary
==================
Total tests: $total
  Unit tests: $unit
  Integration tests: $integration
EOF
```

## Python Commands

### Basic Template

```python
#!/usr/bin/env python3
"""
Description: Brief description
Usage: /command-name [args]
"""

def main():
    # Your command logic here
    print("Command output")

if __name__ == '__main__':
    main()
```

### Example: Line Counter

```python
#!/usr/bin/env python3
# File: .claude/commands/line-count.py
"""Count lines of code by file type"""

import os
import sys
from collections import defaultdict

def count_lines(directory='.', extensions=None):
    if extensions is None:
        extensions = ['.py', '.js', '.ts', '.jsx', '.tsx']

    counts = defaultdict(int)

    for root, dirs, files in os.walk(directory):
        # Skip common directories
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'venv', '__pycache__']]

        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in extensions:
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        counts[ext] += len(f.readlines())
                except:
                    pass

    return counts

def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    counts = count_lines(directory)

    print("Lines of Code by Type")
    print("=====================")
    total = 0
    for ext, count in sorted(counts.items()):
        print(f"{ext:8s}: {count:6,d}")
        total += count
    print(f"{'Total':8s}: {total:6,d}")

if __name__ == '__main__':
    main()
```

### Example: Dependency Checker

```python
#!/usr/bin/env python3
# File: .claude/commands/check-deps.py
"""Check for outdated dependencies"""

import json
import subprocess
import sys

def check_npm_deps():
    try:
        result = subprocess.run(
            ['npm', 'outdated', '--json'],
            capture_output=True,
            text=True
        )
        if result.stdout:
            outdated = json.loads(result.stdout)
            return outdated
    except:
        return {}

def main():
    outdated = check_npm_deps()

    if not outdated:
        print("✓ All dependencies are up to date")
        return

    print(f"Outdated Dependencies ({len(outdated)})")
    print("=" * 50)

    for pkg, info in outdated.items():
        current = info.get('current', 'N/A')
        latest = info.get('latest', 'N/A')
        print(f"{pkg:20s}: {current:10s} → {latest}")

if __name__ == '__main__':
    main()
```

## Node.js Commands

### Basic Template

```javascript
#!/usr/bin/env node
/**
 * Description: Brief description
 * Usage: /command-name [args]
 */

function main() {
  // Your command logic here
  console.log("Command output");
}

main();
```

### Example: Bundle Analyzer

```javascript
#!/usr/bin/env node
// File: .claude/commands/analyze-bundle.js
/**
 * Analyze bundle size
 */

const fs = require('fs');
const path = require('path');

function formatBytes(bytes) {
  return (bytes / 1024).toFixed(2) + ' KB';
}

function analyzeBundles(distDir = 'dist') {
  if (!fs.existsSync(distDir)) {
    console.error(`Error: ${distDir} directory not found`);
    process.exit(1);
  }

  const files = fs.readdirSync(distDir)
    .filter(f => f.endsWith('.js'))
    .map(file => ({
      name: file,
      size: fs.statSync(path.join(distDir, file)).size
    }))
    .sort((a, b) => b.size - a.size);

  console.log('Bundle Analysis');
  console.log('===============');

  let total = 0;
  files.forEach(file => {
    console.log(`${file.name.padEnd(30)} ${formatBytes(file.size)}`);
    total += file.size;
  });

  console.log('-'.repeat(40));
  console.log(`${'Total'.padEnd(30)} ${formatBytes(total)}`);
}

analyzeBundles(process.argv[2]);
```

## Handling Arguments

### Positional Arguments

```bash
#!/bin/bash
# Usage: /command arg1 arg2

ARG1=${1:-"default_value"}
ARG2=${2:-"default_value"}

echo "Argument 1: $ARG1"
echo "Argument 2: $ARG2"
```

### Named Flags

```bash
#!/bin/bash
# Usage: /command --flag1 --flag2=value

FLAG1=false
FLAG2=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --flag1)
      FLAG1=true
      shift
      ;;
    --flag2)
      FLAG2="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

echo "Flag 1: $FLAG1"
echo "Flag 2: $FLAG2"
```

### Python argparse

```python
#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(description='Command description')
    parser.add_argument('path', nargs='?', default='.', help='Path to analyze')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--format', choices=['text', 'json'], default='text')

    args = parser.parse_args()

    # Use args.path, args.verbose, args.format
    print(f"Analyzing: {args.path}")

if __name__ == '__main__':
    main()
```

## Output Formats

### Plain Text

```bash
#!/bin/bash
echo "Test Results"
echo "============"
echo "Passed: 145"
echo "Failed: 2"
```

### JSON

```python
#!/usr/bin/env python3
import json

data = {
    "passed": 145,
    "failed": 2,
    "duration": "3.2s"
}

print(json.dumps(data, indent=2))
```

### Markdown Table

```bash
#!/bin/bash
cat << 'EOF'
| File | Lines | Coverage |
|------|-------|----------|
| auth.py | 245 | 92% |
| api.py | 532 | 85% |
| db.py | 189 | 78% |
EOF
```

### Colored Output

```python
#!/usr/bin/env python3

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

def print_colored(text, color):
    print(f"{color}{text}{Colors.RESET}")

print_colored("✓ Tests passed", Colors.GREEN)
print_colored("⚠ 3 warnings", Colors.YELLOW)
print_colored("✗ 2 failed", Colors.RED)
```

## Error Handling

### Shell Script

```bash
#!/bin/bash
set -e  # Exit on error

# Check prerequisites
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed" >&2
    exit 1
fi

if [ ! -d ".git" ]; then
    echo "Error: Not a git repository" >&2
    exit 1
fi

# Run command
git status
```

### Python

```python
#!/usr/bin/env python3
import sys
import os

def main():
    # Check prerequisites
    if not os.path.exists('package.json'):
        print("Error: package.json not found", file=sys.stderr)
        sys.exit(1)

    try:
        # Your command logic
        result = do_something()
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

## Testing Commands

```bash
# Test command directly
./.claude/commands/my-command.sh

# Test with arguments
./.claude/commands/my-command.sh arg1 arg2

# Test error handling
./.claude/commands/my-command.sh --invalid-flag

# Test in Claude
claude
/my-command
```

## Command Best Practices

### ✅ Do:
- Make scripts executable (`chmod +x`)
- Add shebang line (`#!/bin/bash` or `#!/usr/bin/env python3`)
- Handle missing arguments gracefully
- Exit with proper status codes (0 = success, 1+ = error)
- Keep output concise and readable
- Add usage comments at the top

### ❌ Don't:
- Modify files (use skills instead)
- Require user interaction
- Take more than a few seconds
- Print debug info to stdout (use stderr)
- Assume specific paths without checking

## Common Command Templates

### Git Command

```bash
#!/bin/bash
# Show commits since last tag

last_tag=$(git describe --tags --abbrev=0 2>/dev/null)
if [ -z "$last_tag" ]; then
    echo "No tags found"
    exit 0
fi

echo "Commits since $last_tag:"
git log "$last_tag..HEAD" --oneline
```

### File Analysis Command

```python
#!/usr/bin/env python3
# Find large files

import os
import sys

def find_large_files(directory, size_mb=1):
    large_files = []
    size_bytes = size_mb * 1024 * 1024

    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            try:
                size = os.path.getsize(path)
                if size > size_bytes:
                    large_files.append((path, size))
            except:
                pass

    return sorted(large_files, key=lambda x: x[1], reverse=True)

def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    files = find_large_files(directory)

    for path, size in files[:10]:
        size_mb = size / (1024 * 1024)
        print(f"{size_mb:6.2f} MB  {path}")

if __name__ == '__main__':
    main()
```

## Key Takeaway

Create commands as executable scripts in `.claude/commands/` for quick data retrieval. Keep them simple, fast, and focused on returning useful information. Use shell scripts for simple operations, Python for data processing, and Node.js for JavaScript projects.
