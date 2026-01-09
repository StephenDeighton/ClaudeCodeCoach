---
title: Providing Examples
category: best-practices
commands: []
keywords: examples samples patterns demonstrations show-dont-tell
related_topics: [writing-clear-instructions, code-style-guide]
difficulty: beginner
---

# Providing Examples

## Summary

Examples are one of the most powerful tools for communicating with Claude. A single well-chosen example can replace paragraphs of explanation and ensure Claude matches your exact expectations.

## Why Examples Work

**Psychology**: Humans and AI both learn better from concrete examples than abstract descriptions.

**Precision**: Examples eliminate ambiguity:
- "Use consistent naming" → vague
- "Like `user_service.py`, `auth_service.py`" → crystal clear

## Types of Examples

### 1. Code Examples

**For Patterns**:
```markdown
Create a new service following this pattern:

```python
# Example: services/auth_service.py
class AuthService:
    def __init__(self, db):
        self.db = db

    def authenticate(self, credentials):
        # implementation
        pass

def get_auth_service():
    return AuthService(get_db())
```

Apply this pattern to create UserService.
```

### 2. Style Examples

**For Formatting**:
```markdown
Format the component like this existing one:

```jsx
// Example: components/Button.jsx
export const Button = ({
  label,
  onClick,
  variant = 'primary'
}) => {
  return (
    <button className={`btn btn-${variant}`} onClick={onClick}>
      {label}
    </button>
  );
};
```

Create a new Input component following the same style.
```

### 3. API Examples

**For Integration**:
```markdown
Call the API like this:

```python
# Example from existing code
response = requests.post(
    f"{API_BASE_URL}/users",
    headers={"Authorization": f"Bearer {token}"},
    json={"name": name, "email": email}
)
```

Add a similar function for creating organizations.
```

### 4. Output Examples

**For Format**:
```markdown
Generate output in this format:

Example:
```
✅ Tests passed: 45
❌ Tests failed: 3
⏭️  Tests skipped: 2

Failed tests:
  - test_authentication_flow
  - test_password_reset
  - test_email_validation
```
```

## Example Placement Strategies

### In CLAUDE.md

```markdown
## Code Style

Example service:
```python
class PaymentService:
    """Handle payment processing.

    Usage:
        service = get_payment_service()
        result = service.process_payment(amount, card_token)
    """
```

### In Skills

```markdown
# .claude/skills/add-endpoint.md
---
description: Add a new REST endpoint
---

Follow this pattern from existing code:

```python
@app.route('/users', methods=['POST'])
@require_auth
def create_user():
    data = request.get_json()
    user = User.create(data)
    return jsonify(user.to_dict()), 201
```

Create a new endpoint: [describe what you need]
```

### In Request

```markdown
Request: "Add error handling like we do in fetch_user_data():

```python
try:
    data = fetch_external_api()
except requests.Timeout:
    logger.error("API timeout")
    return None
except requests.RequestException as e:
    logger.error(f"API error: {e}")
    return None
```

Apply this pattern to fetch_organization_data()."
```

## Examples vs Descriptions

### Scenario: Button Styling

**❌ Description Only**:
"Make the button look modern and professional with good visual feedback"

**✅ Example**:
"Style like the GitHub 'Star' button: green background (#2ea44f), white text, rounded corners, slightly darker on hover, small icon"

### Scenario: Function Structure

**❌ Description Only**:
"Write a clean function with proper error handling"

**✅ Example**:
```python
def process_order(order_id: str) -> Optional[Order]:
    """Process an order and return the result.

    Args:
        order_id: Unique order identifier

    Returns:
        Processed Order object or None if failed
    """
    try:
        order = Order.find(order_id)
        order.process()
        return order
    except OrderNotFoundError:
        logger.warning(f"Order {order_id} not found")
        return None
```

## Multiple Examples Show Patterns

**One Example**: Shows what to do
**Multiple Examples**: Shows the pattern

```markdown
Create a validator following our pattern:

Example 1:
```python
def validate_email(email: str) -> tuple[bool, str]:
    if '@' not in email:
        return False, "Email must contain @"
    return True, ""
```

Example 2:
```python
def validate_password(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    return True, ""
```

Pattern: All validators return (bool, error_message) tuple
```

## Example Sources

1. **Your codebase**: Best because it matches your style exactly
2. **Popular libraries**: "Like how Express.js does middleware"
3. **Well-known apps**: "Like Twitter's notification bell"
4. **Previous work**: "Like the user dashboard we built last week"

## When Examples Aren't Enough

Sometimes you need **examples + explanation**:

```markdown
Format errors like this:

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Invalid input data",
    "details": [
      {"field": "email", "issue": "Invalid format"}
    ]
  }
}
```

Note:
- Always include `code` (machine-readable)
- `message` is human-readable
- `details` is optional array for multiple issues
```

## Anti-Patterns

❌ **Too Specific**: Example is for exact same thing you're building
✅ **Analogous**: Example shows pattern to apply

❌ **Complex**: 500-line example
✅ **Minimal**: Just enough to show the pattern

❌ **Outdated**: Example from deprecated code
✅ **Current**: Example from active codebase

## Quick Wins

**Before asking Claude to**:
- Add a feature → Show similar feature
- Fix a bug → Show similar fix
- Refactor code → Show target structure
- Style something → Show desired style
- Format output → Show example output

## Key Takeaway

"Show, don't tell" applies to AI collaboration too. One good example beats ten sentences of description.
