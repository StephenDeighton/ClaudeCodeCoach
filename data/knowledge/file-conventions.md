---
title: File Naming Conventions
category: best-practices
commands: []
keywords: naming conventions files structure organization patterns
related_topics: [code-style-guide, project-setup-guide]
difficulty: beginner
---

# File Naming Conventions

## Summary

Consistent file naming helps Claude locate code quickly and place new files correctly. Establishing clear conventions in your CLAUDE.md prevents confusion and maintains organization.

## Why Conventions Matter

**Benefits**:
- Claude knows where to put new code
- Reduces "Where should this go?" questions
- Makes codebase navigable
- Easier to find related files

**Without**: `helper.py`, `util.py`, `stuff.js`, `new_feature_v2_final.py`
**With**: `user_service.py`, `auth_middleware.js`, `payment_processor.py`

## Common Patterns by Language

### Python

**Standard Patterns**:
```
models/user_model.py          # snake_case
services/payment_service.py
utils/string_helpers.py
tests/test_auth_service.py
```

**Descriptive suffixes**:
- `_model.py` - Data models
- `_service.py` - Business logic
- `_handler.py` - Request handlers
- `_helper.py` / `_utils.py` - Utilities
- `test_*.py` - Tests

### JavaScript/TypeScript

**Standard Patterns**:
```
components/UserProfile.jsx      # PascalCase for components
services/paymentService.js      # camelCase for services
utils/stringHelpers.js
hooks/useAuth.js                # use prefix for hooks
pages/dashboard.tsx
```

**React Conventions**:
- `ComponentName.jsx` - React components
- `useHookName.js` - Custom hooks
- `ServiceName.js` - Service classes
- `*.test.js` - Tests

### Go

**Standard Patterns**:
```
user.go                    # Package name in directory
user_service.go           # snake_case
user_service_test.go      # Tests adjacent
```

## Directory Organization

### Flat vs Nested

**Flat** (< 20 files):
```
services/
  auth_service.py
  user_service.py
  payment_service.py
```

**Nested** (> 20 files):
```
services/
  auth/
    auth_service.py
    token_manager.py
  user/
    user_service.py
    profile_service.py
```

### Feature-Based

```
features/
  auth/
    auth_service.py
    auth_routes.py
    auth_model.py
  payments/
    payment_service.py
    payment_routes.py
    payment_model.py
```

## Documenting Conventions

### In CLAUDE.md

```markdown
## File Conventions

### Models
`{entity}_model.py` in `models/`
Example: `user_model.py`, `order_model.py`

### Services
`{entity}_service.py` in `services/`
Singleton pattern via `get_{entity}_service()`

### API Routes
`{resource}_routes.py` in `api/routes/`
Example: `user_routes.py`, `product_routes.py`

### Tests
`test_{module_name}.py` in same directory as module
Example: `services/test_user_service.py`

### Utilities
`{purpose}_utils.py` in `utils/`
Example: `date_utils.py`, `string_utils.py`
```

## Anti-Patterns

### ❌ Vague Names
```
helper.py           # Helper for what?
utils.py           # What utilities?
manager.py         # Manages what?
handler.py         # Handles what?
```

### ❌ Version Numbers
```
api_v2.py          # Use folders: api/v2/
user_service_new.py # Just update user_service.py
payment_final.py    # Use git for versions
```

### ❌ Abbreviations
```
usr_svc.py         # Is the 5 characters saved worth it?
pmnt_proc.py       # Just spell it out
auth_ctrl.py       # controller or control?
```

### ❌ Redundant Context
```
services/user_service_service.py  # Double service
models/user_model_class.py        # Obvious it's a class
utils/utilities_helper.py         # Redundant
```

## Language-Specific Tips

### Python
- `__init__.py` for packages
- `_private_module.py` for internal use
- Test files: `test_*.py` or `*_test.py`

### JavaScript
- `index.js` for default exports
- `*.config.js` for configuration
- `*.spec.js` or `*.test.js` for tests

### TypeScript
- `*.types.ts` for type definitions
- `*.interface.ts` for interfaces
- `*.d.ts` for declaration files

## Special Files

### Configuration
```
.env.example       # Environment template
config.json        # App configuration
.eslintrc.js      # Tool configuration
```

### Documentation
```
README.md          # Project overview
CONTRIBUTING.md    # Contribution guide
CHANGELOG.md       # Version history
```

### Claude Code
```
CLAUDE.md          # Claude instructions
.claude/
  config.json      # Claude configuration
  skills/          # Custom skills
```

## Naming Checklist

✅ **Is it descriptive?** Name clearly indicates purpose
✅ **Is it consistent?** Follows established patterns
✅ **Is it discoverable?** Easy to find via search
✅ **Is it future-proof?** Won't need renaming soon

## Examples by Project Type

### Django Project
```
myapp/
  models/
    user.py           # Model per file
    order.py
  views/
    user_views.py     # Views for entity
    order_views.py
  serializers/
    user_serializer.py
  tests/
    test_user_views.py
```

### Express API
```
src/
  routes/
    users.routes.js
    products.routes.js
  controllers/
    users.controller.js
    products.controller.js
  services/
    users.service.js
  models/
    User.model.js     # PascalCase for classes
```

### React App
```
src/
  components/
    Button.jsx         # PascalCase components
    UserCard.jsx
  pages/
    Dashboard.jsx      # Page components
    Login.jsx
  hooks/
    useAuth.js         # use prefix
    useApi.js
  utils/
    formatters.js      # camelCase utils
```

## Key Takeaway

File names are signposts in your codebase. Clear, consistent naming helps both humans and Claude navigate efficiently. Document your patterns in CLAUDE.md and follow them religiously.
