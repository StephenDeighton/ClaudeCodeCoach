---
slug: psb-overview
title: PSB Workflow Overview
category: psb-workflow
difficulty: intermediate
keywords: PSB workflow methodology plan setup build execution
commands: []
related: [planning-phase, setup-phase, execution-phase]
---

# PSB Workflow Overview

## Summary

PSB (Plan-Setup-Build) is Claude Code's recommended methodology for feature development. It breaks work into three phases: planning the approach, setting up infrastructure, and building the feature with testing.

## What is PSB?

PSB is a structured workflow:

1. **Plan**: Explore, analyze, design approach
2. **Setup**: Configure tools, create structure
3. **Build**: Implement, test, document

## Why PSB?

### Traditional Approach Problems

❌ Jump straight to coding
❌ Miss architectural issues
❌ Incomplete requirements
❌ Rework and technical debt
❌ Poor test coverage

### PSB Benefits

✅ Clear requirements before coding
✅ Optimal architecture decisions
✅ Reduced rework
✅ Better test coverage
✅ Documentation as you go

## PSB Phases

### Phase 1: Plan (Explore & Design)

**Purpose**: Understand problem, explore codebase, design solution

**Activities**:
- Explore relevant code
- Understand existing patterns
- Identify dependencies
- Design approach
- Get user approval

**Permission Mode**: Plan mode (read-only)

**Duration**: 10-30% of total time

**Output**: Implementation plan

### Phase 2: Setup (Infrastructure)

**Purpose**: Prepare environment and structure

**Activities**:
- Create files and directories
- Set up configuration
- Install dependencies
- Create scaffolding
- Write tests (TDD)

**Permission Mode**: Normal mode

**Duration**: 10-20% of total time

**Output**: Project structure ready for implementation

### Phase 3: Build (Implementation)

**Purpose**: Implement feature with testing

**Activities**:
- Write implementation code
- Run and fix tests
- Handle edge cases
- Add error handling
- Document changes

**Permission Mode**: Normal or Auto mode

**Duration**: 50-70% of total time

**Output**: Working, tested feature

## PSB in Action

### Example: Add User Authentication

#### Plan Phase
```bash
# Enter plan mode
Shift+Tab → Plan Mode

User: "Add JWT-based authentication"

Claude: Let me explore the codebase
- Reads existing auth patterns
- Checks database schema
- Reviews API structure
- Identifies where auth fits

Claude: Here's my plan:
1. Add JWT library
2. Create auth middleware
3. Add login/register endpoints
4. Update protected routes
5. Add tests

User: Approved ✓
```

#### Setup Phase
```bash
# Switch to normal mode
Shift+Tab → Normal Mode

Claude: Setting up structure
- npm install jsonwebtoken bcrypt
- Create src/auth/middleware.ts
- Create src/auth/service.ts
- Create tests/auth.test.ts
- Update tsconfig paths
```

#### Build Phase
```bash
# Implement with testing
Claude: Implementing authentication
- Write auth service ✓
- Write middleware ✓
- Add endpoints ✓
- Write tests ✓
- Run tests → Fix issues ✓
- Update documentation ✓

Feature complete!
```

## PSB Decision Tree

```
Start
  │
  ├─ Requirements clear? ───No──→ Plan Phase
  │                          │
  │                         Yes
  │                          │
  ├─ Structure exists? ─────No──→ Setup Phase
  │                          │
  │                         Yes
  │                          │
  └─ Ready to code? ────────Yes─→ Build Phase
```

## When to Use Each Phase

### Use Planning When:
- New feature with unclear approach
- Unfamiliar codebase area
- Multiple implementation options
- Complex architectural decisions
- Need to understand existing code

### Skip Planning When:
- Tiny change (typo, comment)
- Clear, simple requirement
- Well-understood area
- Similar to previous work

### Use Setup When:
- New files/directories needed
- Dependencies to install
- Configuration required
- Test structure needed
- Scaffolding helpful

### Skip Setup When:
- Modifying existing files only
- No new dependencies
- Simple changes

## PSB with Different Scales

### Small Task (< 30 min)
```
Plan:  5 min  (Quick review)
Setup: 2 min  (If needed)
Build: 23 min (Implementation)
```

### Medium Task (1-3 hours)
```
Plan:  20 min (Thorough exploration)
Setup: 15 min (Structure creation)
Build: 2 hr   (Implementation & testing)
```

### Large Task (1+ days)
```
Plan:  1-2 hr (Deep analysis, design)
Setup: 1 hr   (Complete infrastructure)
Build: 6+ hr  (Iterative implementation)
```

## PSB with Permission Modes

### Plan Mode → Plan Phase
```bash
Shift+Tab until: [Plan Mode]
# Read-only exploration
# Design and document
# No code changes
```

### Normal Mode → Setup & Build
```bash
Shift+Tab until: [Normal Mode]
# Create structure
# Implement features
# Confirm each operation
```

### Auto Mode → Build Phase (Optional)
```bash
Shift+Tab until: [Auto Mode]
# Rapid implementation
# Batch operations
# For trusted, repetitive work
```

## PSB with Models

### Planning: Use Opus or Sonnet
```bash
/model opus
# Complex architectural decisions
# Novel problem-solving
# Pattern analysis
```

### Setup: Use Sonnet or Haiku
```bash
/model sonnet
# Create files and structure
# Standard patterns
# Fast execution
```

### Build: Use Sonnet
```bash
/model sonnet
# Implementation
# Testing
# Documentation
```

## Iterative PSB

PSB can be nested:

```
Main Feature PSB
├─ Sub-feature 1
│  ├─ Mini Plan
│  ├─ Mini Setup
│  └─ Mini Build
├─ Sub-feature 2
│  ├─ Mini Plan
│  └─ Mini Build (no setup needed)
└─ Sub-feature 3
   └─ Mini Build (trivial)
```

## PSB Anti-Patterns

### ❌ Skipping Planning
```
User: Add authentication
Claude: *immediately starts coding*
# Misses existing patterns, suboptimal design
```

### ❌ Over-Planning
```
Claude: *writes 10-page design doc for simple feature*
# Analysis paralysis, wastes time
```

### ❌ Setup During Planning
```
# In Plan Mode
Claude: "Let me create these files..."
# Should stay read-only in Plan
```

### ❌ Planning During Build
```
# Already coding
Claude: "Wait, I should explore how this works..."
# Should have done in Plan phase
```

## PSB Success Metrics

Good PSB execution shows:
- ✅ Minimal rework
- ✅ Consistent with codebase patterns
- ✅ Comprehensive test coverage
- ✅ Clear documentation
- ✅ User approved plan before building
- ✅ ~80% time in Build phase

## PSB Workflow Commands

```bash
# Start planning
Shift+Tab → Plan Mode
"Explore authentication in the codebase"

# Review plan
"Show me your implementation plan"

# Approve plan
"Looks good, proceed"

# Setup
Shift+Tab → Normal Mode
"Set up the structure"

# Build
"Implement the feature"

# Test
"Run tests and fix any issues"

# Complete
"Document the changes"
```

## Key Takeaway

PSB (Plan-Setup-Build) is a structured methodology for feature development. Use Plan mode to explore and design, Normal mode to setup structure, then implement and test in Build phase. Spend 10-30% of time planning to save 50%+ on rework. Always get user approval on plan before building.
