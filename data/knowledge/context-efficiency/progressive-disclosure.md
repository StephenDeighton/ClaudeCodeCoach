---
slug: progressive-disclosure
title: Progressive Disclosure
category: context-efficiency
difficulty: intermediate
keywords: progressive disclosure exploration gradual context management
commands: []
related: [context-window-basics, reducing-bloat]
---

# Progressive Disclosure

## Summary

Progressive disclosure means loading code into context gradually - start with structure, then zoom into specifics. This keeps context clean and focused on what's relevant now.

## Traditional Approach (Inefficient)

```
1. Read all files (100k tokens)
2. Find what you need
3. Make changes
4. Context 90% wasted
```

## Progressive Disclosure (Efficient)

```
1. List directory structure (500 tokens)
2. Identify relevant area
3. Grep for keywords (1k tokens)
4. Read specific files (5k tokens)
5. Make changes
6. Context 100% relevant
```

## Step-by-Step Example

### Task: Add Authentication

**Level 1: Structure** (500 tokens)
```bash
tree src/ -L 2

src/
├── api/
├── auth/  ← Relevant
├── database/
└── utils/
```

**Level 2: Search** (1k tokens)
```bash
grep -r "auth" src/
# Shows auth-related files
```

**Level 3: Read Specific** (5k tokens)
```bash
Read src/auth/service.ts
Read src/auth/middleware.ts
```

**Level 4: Deep Dive** (10k tokens)
```bash
# Only if needed
Read related files
```

**Total: 16.5k tokens vs 100k**

## Disclosure Levels

### Level 0: Overview
```bash
ls -la
tree -L 1
# Just see what's there
```

### Level 1: Structure
```bash
tree -L 2
# See organization
```

### Level 2: Search
```bash
grep "keyword" -r src/
# Find relevant files
```

### Level 3: Sample
```bash
head -n 50 file.ts
# Preview file
```

### Level 4: Full Read
```bash
Read file.ts
# Full content
```

### Level 5: Deep Context
```bash
Read file.ts
Read dependencies
Read tests
# Complete picture
```

## Techniques

### Use Grep First
```bash
# Don't
Read all 50 files to find auth code

# Do
Grep for "auth"
Read the 3 files that match
```

### Use Tree/LS
```bash
# Don't
Read every file to understand structure

# Do
tree src/ -L 2
# See structure without reading
```

### Read Headers Only
```bash
# Don't
Read entire 2000-line file

# Do
head -n 100 file.ts
# See imports, types, main functions
```

### Use File Previews
```bash
# Don't
Read complete file immediately

# Do
"Show me the main functions in auth.ts"
# Claude can preview without full read
```

## When to Disclose More

```
Start minimal → Need more detail → Read more

Example:
1. "Where is auth code?" → tree + grep
2. "How does it work?" → Read auth files
3. "What about database?" → Read db files
4. "Need to modify X" → Read X and dependencies
```

## Lazy Loading Pattern

```markdown
## Phase 1: Discovery (minimal context)
- Understand requirements
- Find relevant areas
- Identify files to read

## Phase 2: Focused Reading
- Read only identified files
- Understand current implementation

## Phase 3: Implementation
- Read dependencies as needed
- Not before needed
```

## Anti-Patterns

### ❌ Read Everything Upfront
```
Read all 200 files
Use 150k tokens
Only needed 10 files
```

### ❌ Re-read Same Files
```
Read auth.ts (5k tokens)
...later...
Read auth.ts again (5k tokens)
...later...
Read auth.ts again (5k tokens)
# 15k tokens for one file!
```

### ❌ Read Without Purpose
```
"Let me understand the codebase"
[Reads 50 random files]
[Context bloat, no clear goal]
```

## Progressive Patterns

### Pattern: Breadth-First
```
1. See all top-level directories
2. Identify relevant directory
3. Explore that directory
4. Read specific files
```

### Pattern: Search-Driven
```
1. Search for keyword
2. Review search results
3. Read promising matches
4. Follow references as needed
```

### Pattern: Need-Based
```
1. Start with task requirements
2. Read only to answer questions
3. Stop when you have enough info
4. Read more only if blocked
```

## Tools for Progressive Disclosure

```bash
# Structure
tree, ls, find

# Search
grep, rg (ripgrep)

# Preview
head, tail, less

# Sample
Read with limit parameter
```

## Measuring Effectiveness

```
Good progressive disclosure:
- Context < 50k for medium task
- Read < 20 files
- 80%+ files read were useful

Poor progressive disclosure:
- Context > 100k for medium task
- Read > 50 files
- < 50% files read were useful
```

## Key Takeaway

Load code into context progressively: start with structure and search, read only files you need, add detail as required. Use tree/grep/head before full reads. This keeps context efficient and focused. A well-executed progressive disclosure uses 10-20% the tokens of reading everything upfront.
