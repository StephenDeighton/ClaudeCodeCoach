---
slug: theme-settings
title: Theme Settings
category: configuration
difficulty: beginner
keywords: theme dark light colors appearance UI customization
commands: ["/theme"]
related: [config-menu, settings-files]
---

# Theme Settings

## Summary

Customize Claude Code's appearance with light/dark themes and color customization through the `/theme` command or settings files.

## Quick Theme Switch

```bash
# Toggle between light/dark
/theme toggle

# Set specific theme
/theme light
/theme dark
/theme system  # Follows OS setting
```

## Available Themes

### Dark Theme (Default)

```
Background: #1E1E1E
Foreground: #D4D4D4
Accent: #007ACC
Success: #4CAF50
Warning: #FFC107
Error: #F44336
```

### Light Theme

```
Background: #FFFFFF
Foreground: #333333
Accent: #0066CC
Success: #2E7D32
Warning: #F57C00
Error: #C62828
```

### System Theme

Automatically switches based on OS:
- macOS: Follows System Preferences
- Windows: Follows Settings > Personalization
- Linux: Follows desktop environment

## Configuration File

Edit `~/.claude/settings.json`:

```json
{
  "theme": {
    "mode": "dark",
    "colors": {
      "primary": "#007ACC",
      "accent": "#4CAF50",
      "background": "#1E1E1E",
      "foreground": "#D4D4D4"
    },
    "syntax": {
      "keyword": "#569CD6",
      "string": "#CE9178",
      "comment": "#6A9955",
      "function": "#DCDCAA"
    }
  }
}
```

## Custom Colors

### Override Specific Colors

```json
{
  "theme": {
    "mode": "dark",
    "customColors": {
      "primary": "#FF6B6B",
      "accent": "#4ECDC4",
      "warning": "#FFE66D"
    }
  }
}
```

### Syntax Highlighting

```json
{
  "theme": {
    "syntax": {
      "keyword": "#C678DD",
      "string": "#98C379",
      "number": "#D19A66",
      "comment": "#5C6370",
      "function": "#61AFEF",
      "class": "#E5C07B",
      "variable": "#E06C75"
    }
  }
}
```

## Terminal Colors

Claude Code respects terminal color schemes:

```bash
# Use terminal colors
claude --terminal-colors

# Override with Claude theme
claude --no-terminal-colors
```

## Accessibility

### High Contrast

```json
{
  "theme": {
    "mode": "dark",
    "highContrast": true
  }
}
```

### Reduced Motion

```json
{
  "theme": {
    "animation": false
  }
}
```

### Font Size

```json
{
  "theme": {
    "fontSize": 14,
    "lineHeight": 1.5
  }
}
```

## Theme Presets

```bash
# List available presets
/theme list

Available presets:
  1. default-dark
  2. default-light
  3. high-contrast
  4. solarized-dark
  5. solarized-light
  6. monokai

# Apply preset
/theme preset monokai
```

## Creating Custom Themes

Create `~/.claude/themes/mytheme.json`:

```json
{
  "name": "My Theme",
  "mode": "dark",
  "colors": {
    "background": "#282C34",
    "foreground": "#ABB2BF",
    "primary": "#61AFEF",
    "accent": "#98C379",
    "success": "#98C379",
    "warning": "#E5C07B",
    "error": "#E06C75"
  }
}
```

Load custom theme:
```bash
/theme load mytheme
```

## Key Takeaway

Use `/theme` for quick switches between light/dark, or customize colors in settings.json for a personalized experience. System theme automatically adapts to your OS preferences.
