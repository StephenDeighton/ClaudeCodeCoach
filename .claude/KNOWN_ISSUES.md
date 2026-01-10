# Known Issues and Fixes

## Platform-Specific Issues

### Flet FilePicker Broken on macOS (Flet 0.28.3)

**Issue**: Flet's built-in `FilePicker` component crashes or doesn't work on macOS in Flet 0.28.3

**GitHub Issue**: https://github.com/flet-dev/flet/issues/5886

**Status**: Fixed in Flet 0.8x+, but we're on 0.28.3

**Our Solution**: Use AppleScript via `subprocess` for native macOS dialogs

**Implementation**:
- File: `utils/platform_specific.py`
- Functions: `pick_folder()`, `save_file_dialog()`
- Uses `osascript -e` to run AppleScript commands
- Returns POSIX paths as Path objects

**CRITICAL**:
- **NEVER** use Flet's `ft.FilePicker` on macOS
- **ALWAYS** use `pick_folder()` from `utils/platform_specific`
- When upgrading Flet to 0.8x+, can migrate to native Flet API

**Example Usage**:
```python
from utils.platform_specific import pick_folder

folder_path = pick_folder()  # Opens native macOS folder picker
if folder_path:
    # User selected a folder
    print(f"Selected: {folder_path}")
```

**Files Using This**:
- `pages/health_scan.py` - _on_pick_directory()
- `pages/setup_wizard.py` - _on_pick_directory() (inline AppleScript, should use pick_folder!)

---

## Shell Quoting in Hooks

**Issue**: Single quotes inside JSON strings inside shell commands cause parsing errors

**Example of Error**:
```json
{
  "command": "echo 'message'"  // WRONG - single quotes fail
}
```

**Fix**:
```json
{
  "command": "echo \"message\""  // CORRECT - use double quotes
}
```

**Where Fixed**:
- `health_checks/warning/no_hooks.py` - Line 32 fix_prompt template
- User's `.claude/settings.json` files

---

## Flet UI Update Patterns

**Issue**: Calling `page.update()` alone doesn't rebuild component properties

**Example**: Button's `disabled` property evaluated once at build time

```python
# WRONG - button stays disabled
self.button.disabled = False
self.page.update()

# CORRECT - rebuild the container content
self.button.disabled = False
self.container.content = self._build_ui()
self.page.update()
```

**Where This Bit Us**:
- `pages/setup_wizard.py` - Analyze button didn't show results
- `pages/setup_wizard.py` - Choose Directory didn't enable Analyze button

**Solution**: Always rebuild `container.content` with a new UI tree, then call `page.update()`

---

## Theme Constants

**Issue**: Easy to guess wrong constant names

### Typography
❌ **WRONG**: `Typography.BODY`
✅ **CORRECT**: `Typography.BODY_MD`, `Typography.BODY_SM`, `Typography.BODY_LG`

**Available**:
- Display: `DISPLAY_LG`, `DISPLAY_MD`, `DISPLAY_SM` (32, 28, 24)
- Headers: `H1`, `H2`, `H3` (22, 18, 16)
- Body: `BODY_LG`, `BODY_MD`, `BODY_SM` (15, 14, 13)
- Small: `CAPTION`, `TINY` (12, 11)

### Colors
❌ **WRONG**: `Colors.BORDER_LIGHT`, `Colors.BORDER_DARK`
✅ **CORRECT**: `Colors.LIGHT_BORDER`, `Colors.PRIMARY_700`

**Pattern**:
- Light theme: `LIGHT_BG`, `LIGHT_SURFACE`, `LIGHT_BORDER`, `LIGHT_BORDER_STRONG`
- Dark theme: `PRIMARY_900`, `PRIMARY_800`, `PRIMARY_700`, `PRIMARY_600`
- Accent: `ACCENT_500`, `ACCENT_400`, `ACCENT_600`
- Status: `GREEN_500`, `YELLOW_500`, `ORANGE_500`, `RED_500`, `BLUE_500`
- Text: `TEXT_DARK`, `TEXT_DARK_MUTED`, `TEXT_LIGHT`, `TEXT_LIGHT_MUTED`

**Where This Bit Us**:
- `pages/setup_wizard.py` - App startup crash (Typography.BODY)
- `pages/setup_wizard.py` - Wizard tab crash (Colors.BORDER_LIGHT)

---

## Migration Notes

### When Upgrading Flet to 0.8x+ or 1.0

**File Picker**:
- Replace all `pick_folder()` calls with native `ft.FilePicker`
- Remove `utils/platform_specific.py`
- Test on macOS to ensure dialog works

**References**:
- See comments in `utils/platform_specific.py`
- GitHub issue: https://github.com/flet-dev/flet/issues/5886
