---
title: Code Style Guide
category: best-practices
commands: []
keywords: style formatting linting prettier eslint black conventions
related_topics: [file-conventions, claude-md-best-practices]
difficulty: beginner
---

# Code Style Guide

## Summary

Consistent code style makes your codebase easier to read and helps Claude write code that fits naturally. Define your style preferences in CLAUDE.md and use automated tools to enforce them.

## Why Style Matters

**Benefits**:
- Claude matches your existing code style
- Reduces style inconsistencies in reviews
- Makes code more readable
- Easier to spot actual changes in diffs

**Without Style Guide**: Every file looks different
**With Style Guide**: Consistent, professional codebase

## Documenting Style

### In CLAUDE.md

```markdown
## Code Standards

### Style
- Python: PEP 8, enforced with black + flake8
- Line length: 88 characters (black default)
- Imports: sorted with isort
- Type hints: required for public functions

### Testing
- Framework: pytest
- Coverage: >80% required
- Naming: test_{function_name}_{scenario}

### Documentation
- Docstrings: Google style
- Comments: Explain why, not what
- TODOs: Include ticket number
```

## Language-Specific Guides

### Python

**Formatting**:
```python
# Good: PEP 8 style
def calculate_total_price(
    items: list[Item],
    discount: float = 0.0,
    tax_rate: float = 0.08
) -> float:
    """Calculate total price with discount and tax.

    Args:
        items: List of items to price
        discount: Discount percentage (0.0 to 1.0)
        tax_rate: Tax rate to apply

    Returns:
        Final price after discount and tax
    """
    subtotal = sum(item.price for item in items)
    discounted = subtotal * (1 - discount)
    total = discounted * (1 + tax_rate)
    return round(total, 2)
```

**Tools**:
- `black` - Automatic formatting
- `flake8` - Linting
- `mypy` - Type checking
- `isort` - Import sorting

### JavaScript/TypeScript

**Formatting**:
```javascript
// Good: Airbnb style
const calculateTotalPrice = (items, discount = 0, taxRate = 0.08) => {
  const subtotal = items.reduce((sum, item) => sum + item.price, 0);
  const discounted = subtotal * (1 - discount);
  const total = discounted * (1 + taxRate);

  return Number(total.toFixed(2));
};

export default calculateTotalPrice;
```

**Tools**:
- `prettier` - Automatic formatting
- `eslint` - Linting
- `typescript` - Type checking

### Go

**Formatting**:
```go
// Good: gofmt style
func CalculateTotalPrice(items []Item, discount float64, taxRate float64) float64 {
    subtotal := 0.0
    for _, item := range items {
        subtotal += item.Price
    }

    discounted := subtotal * (1 - discount)
    total := discounted * (1 + taxRate)

    return math.Round(total*100) / 100
}
```

**Tools**:
- `gofmt` - Standard formatting
- `golint` - Linting
- `go vet` - Code analysis

## Key Style Decisions

### Indentation
```markdown
## Style: Indentation
- Python: 4 spaces
- JavaScript: 2 spaces
- Go: tabs (gofmt default)
```

### Line Length
```markdown
## Style: Line Length
- Max: 88 characters (black default)
- Exception: Long URLs in comments
```

### Quotes
```markdown
## Style: Quotes
- Python: Double quotes for strings
- JavaScript: Single quotes (Airbnb)
- SQL: Single quotes
```

### Naming Conventions
```markdown
## Naming Conventions
- Variables: snake_case (Python) / camelCase (JS)
- Functions: snake_case (Python) / camelCase (JS)
- Classes: PascalCase
- Constants: UPPER_SNAKE_CASE
- Private: _leading_underscore (Python)
```

### Import Organization
```markdown
## Import Order
1. Standard library imports
2. Third-party imports
3. Local application imports

Sorted alphabetically within each group.
```

## Comments and Documentation

### Good Comments

```python
# Good: Explains WHY
# Use exponential backoff to avoid overwhelming the API
retry_delay = 2 ** attempt

# Good: Clarifies business logic
# Discount applies only to orders over $100
if order.total > 100:
    apply_discount(order)

# Good: Warns about gotchas
# Note: This modifies the array in place
items.sort(key=lambda x: x.priority)
```

### Bad Comments

```python
# Bad: Explains WHAT (obvious from code)
# Increment counter by 1
counter += 1

# Bad: Outdated
# TODO: Fix this before launch (launched 2 years ago)

# Bad: Vague
# Handle edge case
if x == 0:
    return None
```

### Docstring Style

**Google Style** (Recommended for Python):
```python
def process_payment(amount: float, currency: str = "USD") -> Payment:
    """Process a payment transaction.

    Args:
        amount: Payment amount in specified currency
        currency: Three-letter currency code (default: USD)

    Returns:
        Payment object with transaction details

    Raises:
        ValueError: If amount is negative
        PaymentError: If transaction fails
    """
```

**JSDoc** (JavaScript/TypeScript):
```javascript
/**
 * Process a payment transaction
 *
 * @param {number} amount - Payment amount
 * @param {string} currency - Three-letter currency code
 * @returns {Promise<Payment>} Payment object with transaction details
 * @throws {PaymentError} If transaction fails
 */
async function processPayment(amount, currency = 'USD') {
  // implementation
}
```

## Automation Setup

### Python
```bash
# Install tools
pip install black flake8 mypy isort

# Format code
black .
isort .

# Check style
flake8 .
mypy .

# Pre-commit hook (pyproject.toml)
[tool.black]
line-length = 88
target-version = ['py311']
```

### JavaScript
```bash
# Install tools
npm install --save-dev prettier eslint

# Format code
npx prettier --write .

# Check style
npx eslint .

# Configuration (.prettierrc)
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

## Claude-Specific Tips

### Show Examples

Instead of just listing rules, show Claude examples:

```markdown
## Error Handling Pattern

Example:
```python
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    return None
except Exception as e:
    logger.critical(f"Unexpected error: {e}")
    raise
```

Follow this pattern for all error handling.
```

### Be Opinionated

Don't say "you can use either X or Y." Pick one:

```markdown
❌ "Use either single or double quotes"
✅ "Always use double quotes for strings"
```

## Quick Reference Template

```markdown
## Code Standards

### Formatting
- Tool: black (Python) / prettier (JS)
- Line length: 88 characters
- Indentation: 4 spaces (Python) / 2 spaces (JS)

### Naming
- Functions: snake_case
- Classes: PascalCase
- Constants: UPPER_SNAKE_CASE
- Private: _leading_underscore

### Imports
1. Standard library
2. Third-party
3. Local
Sorted alphabetically

### Documentation
- Docstrings: Google style
- Public functions must have docstrings
- Explain WHY in comments, not WHAT

### Testing
- Framework: pytest
- Coverage: >80%
- Test files: test_*.py
- Naming: test_{function}_{scenario}
```

## Key Takeaway

Style guides aren't about personal preference - they're about consistency. Define your style once in CLAUDE.md, enforce it with tools, and Claude will naturally match your codebase.
