---
slug: screenshot-debugging
title: Screenshot Debugging
category: advanced-patterns
difficulty: intermediate
keywords: screenshot visual debugging UI debug image
commands: []
related: []
---

# Screenshot Debugging

## Summary

Share screenshots with Claude to debug visual issues, UI problems, or unexpected application behavior. Claude analyzes images to identify issues and suggest fixes.

## When to Use

- UI rendering issues
- Layout problems
- Visual bugs
- Design implementation gaps
- Mobile responsiveness
- Browser differences

## Workflow

```bash
# Take screenshot
# macOS: Cmd+Shift+4
# Save to project directory

# Share with Claude
claude
"Here's a screenshot of the login page issue"
[Attach screenshot.png]

Claude: [Analyzes image]
"I see the button is cut off. The container has overflow:hidden. 
Let me fix the CSS..."
```

## Use Cases

### Layout Issues
```
Screenshot shows: Button cut off
Claude identifies: Container overflow
Fix: Remove overflow:hidden or adjust width
```

### Visual Bugs
```
Screenshot shows: Text overlapping
Claude identifies: Missing z-index
Fix: Add proper layering
```

### Design Mismatch
```
Screenshot shows: Your implementation
Reference: Design mockup
Claude identifies: Color/spacing differences
Fix: Update to match design
```

### Responsive Issues
```
Screenshot shows: Mobile view broken
Claude identifies: Missing media query
Fix: Add responsive breakpoints
```

## Best Practices

✅ Clear, focused screenshots
✅ Include relevant UI area
✅ Describe expected behavior
✅ Show both actual and expected
✅ Include console errors if any

## Limitations

- Can't inspect DOM directly
- Can't see dynamic behavior
- Best combined with code review

## Key Takeaway

Screenshot debugging lets Claude analyze visual issues directly. Share screenshots of UI problems, and Claude can identify layout issues, CSS bugs, and design mismatches. Most effective for static visual problems combined with code review.
