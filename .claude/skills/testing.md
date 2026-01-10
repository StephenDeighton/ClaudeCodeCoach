---
name: testing
description: Testing philosophy and mandatory checklist for C3 development
---

# C3 Testing Philosophy

## Critical Rule: Always Test Before Committing

**MANDATORY**: Before any commit that adds/modifies UI pages or services, you MUST complete this checklist:

## Pre-Commit Testing Checklist

### 1. Import Testing
```bash
python3 -c "
import sys
sys.path.insert(0, '.')
from pages.setup_wizard import SetupWizardPage
from pages.health_scan import HealthScanPage
from pages.fix_page import FixPage
from pages.knowledge_page import KnowledgePage
from pages.settings import SettingsPage
print('✅ All pages import successfully')
"
```

### 2. App Launch Test (CRITICAL)
```bash
# Launch app and verify no startup errors
# Let it run for 5-10 seconds to ensure initialization completes
python3 main.py
```

**What to verify:**
- [ ] App window opens
- [ ] No AttributeError or ImportError in console
- [ ] Database initializes successfully
- [ ] Default page (Scan) loads without errors

### 3. Navigation Test
Manually navigate to EACH tab:
- [ ] Scan tab - loads without errors
- [ ] Fix tab - loads without errors
- [ ] Knowledge tab - loads without errors
- [ ] Settings tab - loads without errors
- [ ] Wizard tab - loads without errors (if applicable)

### 4. Key User Flow Test
For the feature you just built:
- [ ] Test the happy path end-to-end
- [ ] Test one error case (e.g., invalid input)
- [ ] Verify status.md gets updated (if applicable)

### 5. Service Testing
For new services:
```bash
python3 -c "
from services.your_service import get_your_service
service = get_your_service()
# Test critical methods
result = service.your_method(test_input)
assert result is not None
print('✅ Service works')
"
```

## Common Gotchas

### Typography Constants
❌ **WRONG**: `Typography.BODY`
✅ **CORRECT**: `Typography.BODY_MD`, `Typography.BODY_SM`, `Typography.BODY_LG`

Typography class attributes:
- `DISPLAY_LG`, `DISPLAY_MD`, `DISPLAY_SM` (32, 28, 24)
- `H1`, `H2`, `H3` (22, 18, 16)
- `BODY_LG`, `BODY_MD`, `BODY_SM` (15, 14, 13)
- `CAPTION`, `TINY` (12, 11)

### Colors Constants
❌ **WRONG**: `Colors.BORDER_LIGHT`, `Colors.BORDER_DARK`
✅ **CORRECT**: `Colors.LIGHT_BORDER`, `Colors.PRIMARY_700`

For borders in light/dark mode:
```python
# CORRECT
border=ft.border.all(1, Colors.LIGHT_BORDER if not is_dark else Colors.PRIMARY_700)

# WRONG
border=ft.border.all(1, Colors.BORDER_LIGHT if not is_dark else Colors.BORDER_DARK)
```

Common Colors attributes:
- Light theme: `LIGHT_BG`, `LIGHT_SURFACE`, `LIGHT_BORDER`, `LIGHT_BORDER_STRONG`
- Dark theme: `PRIMARY_900`, `PRIMARY_800`, `PRIMARY_700`, `PRIMARY_600`
- Accent: `ACCENT_500`, `ACCENT_400`, `ACCENT_600`
- Status: `GREEN_500`, `YELLOW_500`, `ORANGE_500`, `RED_500`, `BLUE_500`
- Text: `TEXT_DARK`, `TEXT_DARK_MUTED`, `TEXT_LIGHT`, `TEXT_LIGHT_MUTED`

### Flet UI Testing
Flet apps defer errors until runtime. You won't see AttributeError or NameError until:
1. Page instance is created (`PageClass(page)`)
2. `build()` method is called
3. User interacts with the UI

**Therefore:** Always launch the full app, don't just test imports.

### Path Issues
Always use absolute imports:
```python
# CORRECT
from services.app_state import get_last_scan

# WRONG
from .app_state import get_last_scan
```

## Testing After Large Changes

If you modify:
- **theme.py** → Test all pages (theme changes affect everything)
- **services/app_state.py** → Test cross-page navigation
- **main.py** → Test full app launch + all tabs
- **Any page** → Test that specific page + app launch

## Why This Matters

**Real Example**: The CC Setup Wizard feature shipped with `Typography.BODY` which doesn't exist. App crashed on startup. This was preventable with proper testing.

**Impact**:
- Wastes user's time
- Breaks confidence in the tool
- Requires immediate hotfix
- Could have been caught in 30 seconds

## Time Investment

- Import tests: **10 seconds**
- App launch test: **20 seconds**
- Navigation test: **30 seconds**
- User flow test: **2 minutes**
- **Total: ~3 minutes to prevent hours of debugging**

## When to Skip Tests

**NEVER**. Even for "trivial" changes:
- Typo fixes in UI text → Still test (might have syntax error)
- Constant changes → Still test (might break references)
- Service updates → Still test (might break imports)

## Test Automation (Future)

Once C3 matures, consider:
- Pytest tests for services
- Flet UI testing framework
- CI/CD with GitHub Actions
- Pre-commit hooks that run import tests

For now: **Manual testing is mandatory.**
