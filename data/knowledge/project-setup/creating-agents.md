---
slug: creating-agents
title: Creating Custom Agents
category: project-setup
difficulty: advanced
keywords: custom agents create build autonomous specialized
commands: []
related: [agents-overview, creating-skills]
---

# Creating Custom Agents

## Summary

Create custom agents as specialized Claude instances for domain-specific autonomous work. Agents are defined in markdown files that specify their capabilities, permissions, and workflows.

## Quick Start

```bash
# Create agents directory
mkdir -p .claude/agents

# Create your first agent
cat > .claude/agents/security-audit.md << 'EOF'
---
name: security-audit
description: Perform security audit of codebase
type: audit
model: opus
tools: [read, bash]
permissions: [read-only]
---

# Security Audit Agent

Comprehensive security audit of the codebase.

## Objectives
1. Identify security vulnerabilities
2. Check for common attack vectors
3. Review authentication/authorization
4. Analyze data handling
5. Report findings with severity levels

## Methodology
- Static code analysis
- Dependency vulnerability scan
- Security pattern analysis
- Best practice compliance check
EOF

# Use it
claude agent security-audit
```

## Agent File Structure

### Frontmatter (Required)

```markdown
---
name: agent-name
description: Brief description of agent purpose
type: feature|debug|test|audit|refactor
model: opus|sonnet|haiku
tools: [read, write, bash, git]
permissions: [read-only, git_commit, deploy]
maxDuration: 3600
maxTokens: 100000
autoCommit: false
---
```

### Frontmatter Fields

**name** (required): Agent identifier
```yaml
name: feature-auth
# Invoked as: claude agent feature-auth
```

**description** (required): What this agent does
```yaml
description: Implement authentication features
```

**type** (required): Agent category
```yaml
type: feature  # feature, debug, test, audit, refactor, custom
```

**model** (optional): Preferred model
```yaml
model: opus  # opus for complex work, sonnet for balance, haiku for speed
```

**tools** (required): Tools agent can use
```yaml
tools: [read, write, bash, git]
```

**permissions** (optional): Special permissions
```yaml
permissions: [git_commit, git_push, database]
```

**maxDuration** (optional): Max runtime in seconds
```yaml
maxDuration: 3600  # 1 hour
```

**maxTokens** (optional): Context limit
```yaml
maxTokens: 150000
```

**autoCommit** (optional): Auto-commit changes
```yaml
autoCommit: true
```

## Agent Body (Instructions)

The body contains the agent's behavior:

```markdown
# Agent Title

Overview of what this agent accomplishes.

## Objectives
Clear list of goals to achieve.

## Methodology
How the agent should approach the task.

## Success Criteria
What defines successful completion.

## Error Handling
How to handle failures and edge cases.

## Deliverables
What should be produced/reported.
```

## Complete Examples

### Feature Development Agent

```markdown
---
name: feature-api
description: Build REST API endpoints
type: feature
model: sonnet
tools: [read, write, bash, git]
autoCommit: false
maxDuration: 7200
---

# API Feature Development Agent

Build production-ready REST API endpoints.

## Objectives
1. Design API endpoint structure
2. Implement handlers with validation
3. Add comprehensive error handling
4. Write integration tests
5. Generate API documentation
6. Update OpenAPI spec

## Methodology

### Phase 1: Planning
- Analyze existing API structure
- Review database schema
- Identify required endpoints
- Design request/response formats

### Phase 2: Implementation
- Create route definitions
- Implement request validation
- Add business logic in services
- Implement error handling
- Add logging and monitoring

### Phase 3: Testing
- Write unit tests for handlers
- Write integration tests
- Test error scenarios
- Verify OpenAPI compliance

### Phase 4: Documentation
- Add inline code comments
- Update API documentation
- Generate example requests
- Update CHANGELOG

## Success Criteria
- All endpoints functional
- 100% test coverage for new code
- OpenAPI spec updated
- Documentation complete
- All tests passing

## Error Handling
- Database errors: Log and return 500
- Validation errors: Return 400 with details
- Auth errors: Return 401/403
- Not found: Return 404

## Code Standards
- Follow existing patterns in `/api`
- Use async/await consistently
- Type annotations required
- Validate all inputs
- Return consistent response format

## Deliverables
1. Functional API endpoints
2. Test suite with full coverage
3. Updated OpenAPI spec
4. API documentation
5. Example requests
```

### Debug Agent

```markdown
---
name: debug-performance
description: Debug and fix performance issues
type: debug
model: opus
tools: [read, write, bash]
maxDuration: 5400
---

# Performance Debug Agent

Identify and fix performance bottlenecks.

## Objectives
1. Profile application performance
2. Identify bottlenecks
3. Implement optimizations
4. Measure improvements
5. Document changes

## Investigation Process

### 1. Baseline Measurement
```bash
# Measure current performance
npm run benchmark
```

Save baseline metrics for comparison.

### 2. Profiling
- CPU profiling
- Memory profiling
- Database query analysis
- Network request timing

### 3. Identify Issues
Common bottlenecks:
- N+1 database queries
- Inefficient algorithms
- Missing indexes
- Large payloads
- Memory leaks
- Blocking operations

### 4. Prioritization
Focus on issues with highest impact:
- Critical path operations
- High-frequency operations
- User-facing features

### 5. Implementation
For each issue:
1. Create test to reproduce
2. Implement fix
3. Verify improvement
4. Document change

### 6. Verification
```bash
# Re-run benchmarks
npm run benchmark

# Compare results
# Ensure 20%+ improvement
```

## Optimization Strategies

### Database
- Add indexes for frequent queries
- Use connection pooling
- Implement query caching
- Batch operations

### Code
- Use memoization
- Lazy loading
- Efficient data structures
- Async operations

### Frontend
- Code splitting
- Image optimization
- Bundle size reduction
- Caching strategies

## Success Criteria
- 20%+ performance improvement
- No regressions
- All tests passing
- Changes documented

## Deliverables
1. Performance analysis report
2. Implemented optimizations
3. Before/after benchmarks
4. Documentation updates
```

### Test Coverage Agent

```markdown
---
name: test-coverage
description: Improve test coverage to target %
type: test
model: sonnet
tools: [read, write, bash]
autoCommit: true
maxDuration: 3600
---

# Test Coverage Improvement Agent

Systematically improve test coverage.

## Objectives
1. Analyze current coverage
2. Identify uncovered code
3. Write comprehensive tests
4. Reach target coverage %
5. Ensure test quality

## Process

### 1. Coverage Analysis
```bash
# Generate coverage report
npm run test:coverage

# Identify gaps
npm run coverage:report
```

### 2. Prioritization
Focus on:
1. Critical paths (auth, payments)
2. Business logic
3. Error handling
4. Edge cases
5. Integration points

### 3. Test Writing
For each uncovered code path:

#### Unit Tests
- Test function behavior
- Test edge cases
- Test error conditions
- Mock dependencies

#### Integration Tests
- Test component interactions
- Test API endpoints
- Test database operations

### 4. Quality Checks
Ensure tests are:
- Independent (no interdependencies)
- Deterministic (consistent results)
- Fast (< 1s each)
- Clear (good descriptions)
- Maintainable (not brittle)

### 5. Documentation
- Add test descriptions
- Document test data
- Explain complex assertions

## Test Patterns

### Arrange-Act-Assert
```python
def test_user_login():
    # Arrange
    user = create_test_user()

    # Act
    result = login(user.email, "password")

    # Assert
    assert result.success is True
    assert result.user_id == user.id
```

### Given-When-Then
```python
def test_order_processing():
    # Given
    order = create_order()

    # When
    process_order(order.id)

    # Then
    assert order.status == "processed"
    assert payment.status == "captured"
```

## Success Criteria
- Target coverage % reached
- All new tests passing
- No flaky tests
- Test runtime acceptable (< 5min total)

## Deliverables
1. New test files
2. Coverage report showing improvement
3. Test documentation
4. CI/CD integration updated
```

### Refactor Agent

```markdown
---
name: refactor-extract-service
description: Extract logic into service layer
type: refactor
model: opus
tools: [read, write, bash, git]
maxDuration: 5400
---

# Service Layer Refactor Agent

Extract business logic into service layer.

## Objectives
1. Identify business logic in controllers
2. Design service layer architecture
3. Extract logic safely
4. Maintain test coverage
5. Update tests and documentation

## Process

### 1. Analysis
- Map current code structure
- Identify business logic patterns
- Find duplicated code
- List dependencies

### 2. Design
Service layer structure:
```
services/
├── auth_service.py
├── user_service.py
├── order_service.py
└── __init__.py
```

### 3. Extraction Pattern
For each service:

**Before** (controller):
```python
@app.route('/api/users', methods=['POST'])
def create_user():
    # Validation logic
    # Business logic
    # Database logic
    # Response formatting
```

**After** (service + controller):
```python
# services/user_service.py
class UserService:
    def create_user(self, data):
        # Validation
        # Business logic
        # Database operations
        return user

# api/users.py
@app.route('/api/users', methods=['POST'])
def create_user():
    user = user_service.create_user(request.json)
    return jsonify(user)
```

### 4. Migration Steps
For each piece of logic:
1. Create corresponding service method
2. Write tests for service method
3. Update controller to use service
4. Update controller tests
5. Remove old code
6. Verify all tests pass

### 5. Safety Checks
- Run full test suite after each migration
- No test coverage decrease
- No behavior changes
- All edge cases handled

## Service Design Principles
- Single responsibility
- Dependency injection
- Testable (mockable dependencies)
- Stateless when possible
- Clear interfaces

## Success Criteria
- All business logic in services
- Controllers thin (routing only)
- Test coverage maintained/improved
- No breaking changes
- Documentation updated

## Deliverables
1. New service modules
2. Updated controllers
3. Updated tests
4. Architecture documentation
```

## Agent Communication

### Asking Questions

```markdown
## Questions for User

Before proceeding, I need to know:

<question>
Should I use JWT or session-based authentication?
</question>

<question>
What database should I use for sessions? (Redis/PostgreSQL)
</question>
```

### Progress Updates

```markdown
## Progress Reporting

Report progress every 10 minutes:

```
Progress Update - [timestamp]
Completed:
- Task 1
- Task 2

In progress:
- Task 3 (60% complete)

Blocked:
- Task 4 (waiting for database schema)

ETA: 15 minutes
```
\```
```

## Agent Best Practices

### ✅ Do:
- Define clear objectives
- Specify success criteria
- Include error handling instructions
- Set reasonable time limits
- Document methodology
- Provide examples

### ❌ Don't:
- Make agents too broad
- Skip error handling
- Forget about testing
- Ignore existing patterns
- Make destructive changes without backup

## Testing Agents

```bash
# Dry run
claude agent my-agent --dry-run

# Limited scope test
claude agent my-agent --limit "src/auth only"

# Verbose output
claude agent my-agent --verbose
```

## Agent Templates

### Minimal Template

```markdown
---
name: my-agent
description: Brief description
type: custom
model: sonnet
tools: [read, write]
---

# Agent Title

## Objectives
1. Goal 1
2. Goal 2

## Process
Steps to achieve objectives.

## Success Criteria
How to know when done.
```

### Full Template

```markdown
---
name: my-agent
description: Detailed description
type: feature
model: opus
tools: [read, write, bash, git]
permissions: [git_commit]
maxDuration: 3600
maxTokens: 150000
autoCommit: false
---

# Agent Title

Detailed overview.

## Objectives
Clear numbered list.

## Methodology
Detailed approach.

## Phase 1: Name
Steps for phase 1.

## Phase 2: Name
Steps for phase 2.

## Error Handling
How to handle failures.

## Success Criteria
Definition of done.

## Code Standards
Standards to follow.

## Testing Requirements
Required test coverage.

## Documentation
What docs to update.

## Deliverables
What to produce.
```

## Key Takeaway

Create agents in `.claude/agents/` as markdown files with clear objectives, methodology, and success criteria. Specify tools, permissions, and time limits. Use opus for complex work, sonnet for balance. Test agents in limited scope before full deployment.
