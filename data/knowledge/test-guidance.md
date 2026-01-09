---
title: Test Guidance for Claude
category: models
commands: []
keywords: testing test-driven tdd pytest jest guidance practices
related_topics: [code-style-guide, writing-clear-instructions]
difficulty: intermediate
---

# Test Guidance for Claude

## Summary

Clear testing guidelines help Claude write appropriate tests for your codebase. Define your testing philosophy, frameworks, and expectations in CLAUDE.md to ensure consistent test quality.

## Why Document Testing Approach

**Benefits**:
- Claude writes tests matching your style
- Consistent test structure across codebase
- Appropriate level of test coverage
- Tests that actually add value

**Without Guidance**: Inconsistent tests, wrong framework, over/under-testing
**With Guidance**: Tests that fit your project perfectly

## Essential Testing Info

### In CLAUDE.md

```markdown
## Testing

### Framework
- Python: pytest with pytest-cov
- JavaScript: Jest with React Testing Library

### Coverage Requirements
- Minimum: 80% overall
- Critical paths (auth, payments): 95%+
- Utility functions: 90%+

### Test Organization
```
tests/
  unit/           # Fast, isolated tests
  integration/    # Tests with database
  e2e/            # Full user flows
```

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific file
pytest tests/unit/test_auth.py
```

### Test Naming
Format: `test_{function}_{scenario}_{expected}`
Example: `test_create_user_with_duplicate_email_raises_error`
```

## Test Types to Guide

### 1. Unit Tests

**What to Test**:
```markdown
## Unit Test Guidelines

Test individual functions/methods in isolation:
- ✅ Business logic
- ✅ Data transformations
- ✅ Calculations
- ✅ Validation functions

Example:
```python
def test_calculate_discount_with_valid_percentage():
    result = calculate_discount(100, 0.1)
    assert result == 90.0

def test_calculate_discount_with_negative_percentage_raises_error():
    with pytest.raises(ValueError):
        calculate_discount(100, -0.1)
```
```

### 2. Integration Tests

**What to Test**:
```markdown
## Integration Test Guidelines

Test interactions between components:
- ✅ Database operations
- ✅ API endpoint with service layer
- ✅ External service integrations

Example:
```python
def test_create_user_saves_to_database(db_session):
    user_service = UserService(db_session)
    user = user_service.create_user("test@example.com", "password")

    retrieved = db_session.query(User).filter_by(id=user.id).first()
    assert retrieved.email == "test@example.com"
```
```

### 3. End-to-End Tests

**What to Test**:
```markdown
## E2E Test Guidelines

Test complete user workflows:
- ✅ Critical user journeys
- ✅ Authentication flows
- ✅ Payment processes

Keep E2E tests minimal (slow and brittle):
- Focus on happy paths
- Test critical business flows only
```

## What NOT to Test

Be explicit about what to skip:

```markdown
## Testing: What to Skip

Don't waste time testing:
- ❌ Framework/library internals
- ❌ Simple getters/setters
- ❌ Generated code
- ❌ Third-party APIs (use mocks)
- ❌ Obvious language features

Example (don't test):
```python
# Don't test this - it's too simple
def get_name(self):
    return self.name
```
```

## Test Patterns

### Arrange-Act-Assert

```markdown
## Test Structure: AAA Pattern

All tests follow Arrange-Act-Assert:

```python
def test_user_creation():
    # Arrange: Set up test data
    email = "test@example.com"
    password = "secure123"

    # Act: Perform the action
    user = User.create(email, password)

    # Assert: Verify the results
    assert user.email == email
    assert user.password != password  # Should be hashed
    assert user.id is not None
```
```

### Fixtures and Mocks

```markdown
## Test Fixtures

Use pytest fixtures for common setup:

```python
@pytest.fixture
def db_session():
    \"\"\"Provide a database session for testing.\"\"\"
    session = create_test_session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def sample_user(db_session):
    \"\"\"Create a sample user for testing.\"\"\"
    user = User(email="test@example.com")
    db_session.add(user)
    db_session.commit()
    return user
```

## Mocking External Services

Mock HTTP requests, don't hit real APIs:

```python
from unittest.mock import patch

@patch('requests.post')
def test_send_email(mock_post):
    mock_post.return_value.status_code = 200

    result = EmailService.send("test@example.com", "Subject", "Body")

    assert result is True
    mock_post.assert_called_once()
```
```

## Coverage Guidelines

```markdown
## Code Coverage

Target coverage levels:
- **Critical code** (auth, payments, core business logic): 95%+
- **Standard features**: 80%+
- **Utilities and helpers**: 90%+
- **UI components**: 70%+ (focus on logic, not rendering)

How to achieve:
1. Write tests for new features (TDD when possible)
2. Add tests when fixing bugs
3. Don't chase 100% - focus on value

Exceptions:
- Configuration files: No tests needed
- Simple data models: Minimal tests
- Scripts run manually: Optional tests
```

## Test-Driven Development

If you practice TDD:

```markdown
## Test-Driven Development

We follow TDD for new features:

1. **Red**: Write failing test first
```python
def test_calculate_tax():
    result = calculate_tax(100, 0.08)
    assert result == 8.0
```

2. **Green**: Write minimal code to pass
```python
def calculate_tax(amount, rate):
    return amount * rate
```

3. **Refactor**: Clean up while keeping tests green

Request tests first by saying:
"Add tax calculation feature. Start with tests."
```

## Framework-Specific Guidance

### Python + pytest

```markdown
## pytest Configuration

```python
# conftest.py - shared fixtures
import pytest

@pytest.fixture(scope="session")
def app():
    \"\"\"Create application for testing.\"\"\"
    return create_app(testing=True)

@pytest.fixture
def client(app):
    \"\"\"Provide test client.\"\"\"
    return app.test_client()
```

Run tests:
- `pytest` - All tests
- `pytest -v` - Verbose output
- `pytest -k "auth"` - Tests matching "auth"
- `pytest --cov` - With coverage
```

### JavaScript + Jest

```markdown
## Jest Configuration

```javascript
// Setup file: jest.setup.js
import '@testing-library/jest-dom';

// Test example
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Button from './Button';

test('button click calls onClick handler', async () => {
  const handleClick = jest.fn();
  render(<Button onClick={handleClick}>Click me</Button>);

  await userEvent.click(screen.getByText('Click me'));

  expect(handleClick).toHaveBeenCalledTimes(1);
});
```

Run tests:
- `npm test` - All tests
- `npm test -- --coverage` - With coverage
- `npm test -- --watch` - Watch mode
```

## Anti-Patterns

```markdown
## Testing Anti-Patterns to Avoid

❌ **Testing Implementation Details**
```python
# Bad: Tests internal method
def test_user_validate_internal():
    user._validate_email()  # Private method

# Good: Tests public interface
def test_user_creation_with_invalid_email_fails():
    with pytest.raises(ValueError):
        User.create("invalid-email")
```

❌ **Brittle Tests**
```python
# Bad: Assumes specific order
def test_get_users():
    users = get_users()
    assert users[0].name == "Alice"

# Good: Tests properties, not order
def test_get_users():
    users = get_users()
    assert any(u.name == "Alice" for u in users)
```

❌ **Testing Multiple Things**
```python
# Bad: Tests creation AND deletion
def test_user_lifecycle():
    user = create_user()
    assert user.id
    delete_user(user)
    assert get_user(user.id) is None

# Good: Separate tests
def test_user_creation():
    user = create_user()
    assert user.id

def test_user_deletion():
    user = create_user()
    delete_user(user)
    assert get_user(user.id) is None
```
```

## Requesting Tests from Claude

**Vague**:
> "Add tests"

**Clear**:
> "Add pytest unit tests for the calculate_shipping_cost function. Test these scenarios:
> 1. Standard shipping (under 1kg)
> 2. Heavy items (over 5kg)
> 3. Invalid weight (negative)
> 4. Zero weight
> Follow our AAA pattern and use the test_shipping fixture."

## Key Takeaway

Well-documented testing guidelines ensure Claude writes valuable tests that integrate seamlessly with your test suite. Be specific about frameworks, coverage expectations, and what to test (and skip).
