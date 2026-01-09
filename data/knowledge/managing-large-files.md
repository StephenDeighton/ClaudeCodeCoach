---
title: Managing Large Files
category: context-efficiency
commands: []
keywords: large-files refactoring splitting modules organization LOC
related_topics: [context-efficiency, file-conventions]
difficulty: intermediate
---

# Managing Large Files

## Summary

Large files (>400 lines) slow down Claude's performance and make code harder to maintain. Learn strategies for identifying, splitting, and organizing code to keep files manageable.

## Why Size Matters

**Problems with Large Files**:
- Harder for Claude to process
- More context tokens consumed
- Difficult to navigate
- Higher chance of merge conflicts
- Violates single responsibility principle

**Sweet Spot**: 100-300 lines per file

## Identifying Candidates

### Size Thresholds
- **< 200 lines**: Usually fine
- **200-400 lines**: Consider refactoring
- **> 400 lines**: Definitely refactor

### Check File Sizes
```bash
# List files by line count
find . -name "*.py" -exec wc -l {} + | sort -rn | head -20
```

## Refactoring Strategies

### 1. Extract by Responsibility

**Before** (600 lines):
```python
# user_manager.py
class UserManager:
    def authenticate(self): ...
    def create_user(self): ...
    def update_user(self): ...
    def delete_user(self): ...
    def send_email(self): ...
    def validate_password(self): ...
    def hash_password(self): ...
    def format_user_data(self): ...
```

**After** (4 files × ~150 lines):
```python
# services/auth_service.py
class AuthService:
    def authenticate(self): ...
    def validate_password(self): ...
    def hash_password(self): ...

# services/user_service.py
class UserService:
    def create_user(self): ...
    def update_user(self): ...
    def delete_user(self): ...

# services/email_service.py
class EmailService:
    def send_welcome_email(self): ...
    def send_reset_email(self): ...

# utils/user_formatters.py
def format_user_data(user): ...
def format_user_response(user): ...
```

### 2. Extract Utilities

**Before**:
```python
# api_handler.py (500 lines)
def process_request(request):
    # 50 lines of validation
    # 100 lines of processing
    # 50 lines of formatting
    pass
```

**After**:
```python
# api_handler.py (200 lines)
from utils.validators import validate_request
from utils.formatters import format_response

def process_request(request):
    validate_request(request)
    result = do_processing(request)
    return format_response(result)

# utils/validators.py (100 lines)
def validate_request(request): ...

# utils/formatters.py (100 lines)
def format_response(data): ...
```

### 3. Extract Constants and Config

**Before**:
```python
# app.py (700 lines)
# 200 lines of constants
API_KEY = "..."
DATABASE_URL = "..."
EMAIL_TEMPLATES = {...}
# 500 lines of code
```

**After**:
```python
# config/settings.py (200 lines)
API_KEY = "..."
DATABASE_URL = "..."

# config/templates.py (150 lines)
EMAIL_TEMPLATES = {...}

# app.py (350 lines)
from config.settings import API_KEY, DATABASE_URL
from config.templates import EMAIL_TEMPLATES
```

### 4. Split by Feature

**Before**:
```python
# views.py (800 lines)
def user_list_view(): ...
def user_detail_view(): ...
def product_list_view(): ...
def product_detail_view(): ...
def order_list_view(): ...
def order_detail_view(): ...
```

**After**:
```python
# views/user_views.py (200 lines)
def user_list_view(): ...
def user_detail_view(): ...

# views/product_views.py (200 lines)
def product_list_view(): ...
def product_detail_view(): ...

# views/order_views.py (200 lines)
def order_list_view(): ...
def order_detail_view(): ...
```

## Practical Example: Health Scan Page

**Original**: 714 lines (too large)

**Refactored**:
- `health_scan.py` → 256 lines (page orchestration)
- `utils/platform_specific.py` → 172 lines (OS dialogs)
- `utils/report_formatter.py` → 77 lines (formatting)
- `components/issue_card.py` → 137 lines (UI component)
- `components/scan_results.py` → 228 lines (results display)

**Result**: Max file reduced from 714 → 256 lines (64% reduction)

## Organization Patterns

### Flat Structure
```
services/
  auth_service.py (200 lines)
  user_service.py (180 lines)
  payment_service.py (220 lines)
```
**Use when**: < 10 related files

### Nested Structure
```
services/
  auth/
    auth_service.py (150 lines)
    token_manager.py (120 lines)
    password_hasher.py (80 lines)
  user/
    user_service.py (180 lines)
    profile_service.py (140 lines)
```
**Use when**: Related files group naturally

### Feature-Based
```
features/
  auth/
    service.py
    models.py
    views.py
  payments/
    service.py
    models.py
    views.py
```
**Use when**: Strong feature boundaries

## Refactoring Process

1. **Analyze**: Identify large files
2. **Group**: Find related functions/classes
3. **Extract**: Move related code to new files
4. **Test**: Ensure functionality unchanged
5. **Update**: Fix imports
6. **Commit**: Small, atomic commits

## Maintaining Small Files

### Code Review Checklist
- [ ] No file over 400 lines
- [ ] Each file has single clear purpose
- [ ] Related code is grouped
- [ ] Clear file naming

### Prevent Growth
```markdown
## Code Standards (in CLAUDE.md)
- Max file size: 300 lines (exceptions require justification)
- Split files by responsibility, not size alone
- Extract utilities and constants early
```

## Anti-Patterns

❌ **Random Splitting**: Breaking file arbitrarily at line 400
✅ **Logical Splitting**: Extracting cohesive modules

❌ **Over-Splitting**: 50 files with 10 lines each
✅ **Balanced**: Meaningful modules of 100-300 lines

❌ **Split and Forget**: Never updating after initial split
✅ **Continuous**: Refactor as code evolves

## Tools

### Python
```bash
# Count lines in files
find . -name "*.py" -exec wc -l {} + | sort -rn

# Find files over 400 lines
find . -name "*.py" -exec wc -l {} + | awk '$1 > 400'
```

### JavaScript
```bash
# Count lines
find . -name "*.js" -exec wc -l {} + | sort -rn

# Files over 400 lines
find . -name "*.js" -exec wc -l {} + | awk '$1 > 400'
```

## Key Takeaway

Large files are a code smell. Keep files focused, cohesive, and under 400 lines. Your codebase (and Claude) will thank you.
