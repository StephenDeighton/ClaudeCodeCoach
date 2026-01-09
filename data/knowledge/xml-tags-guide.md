---
title: XML Tags in Claude Code
category: advanced-patterns
commands: []
keywords: xml-tags anthropic-xml thinking-tags structured-output formatting
related_topics: [claude-md-best-practices]
difficulty: advanced
---

# XML Tags in Claude Code

## Summary

Claude Code uses XML-like tags for structured thinking and output formatting. While useful in API contexts, these tags should generally be avoided in CLAUDE.md files to prevent confusion.

## What Are XML Tags?

Claude's API supports XML-style tags for structured interaction:

```xml
<thinking>
Let me analyze this step by step...
</thinking>

<answer>
The solution is...
</answer>
```

## Why Avoid in CLAUDE.md?

**Problem**: Tags in CLAUDE.md may confuse Claude Code's parser

**Bad** (CLAUDE.md):
```markdown
## Instructions
<important>
Always run tests before committing
</important>
```

**Good** (CLAUDE.md):
```markdown
## Instructions
**IMPORTANT**: Always run tests before committing
```

Or:
```markdown
## Instructions
> ⚠️ **Critical**: Always run tests before committing
```

## Appropriate Use Cases

### 1. API Integration

If you're building tools that call Claude's API directly:

```python
prompt = """
Please analyze this code:

<code>
def process_payment(amount):
    # implementation
    pass
</code>

<requirements>
- Check for security issues
- Verify error handling
- Assess performance
</requirements>
"""
```

### 2. Structured Prompts in Skills

Skills can use tags if they're generating prompts:

```markdown
# analyze-code.md
---
description: Perform detailed code analysis
---

Generate a structured analysis in this format:

<analysis>
  <security>Security findings here</security>
  <performance>Performance findings here</performance>
  <maintainability>Maintainability findings here</maintainability>
</analysis>
```

### 3. Code Generation Templates

When generating code that uses XML/HTML:

```markdown
# add-react-component.md
Generate a React component with PropTypes:

```jsx
import PropTypes from 'prop-types';

export const MyComponent = ({ title, children }) => {
  return (
    <div className="component">
      <h2>{title}</h2>
      {children}
    </div>
  );
};

MyComponent.propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.node
};
```
```

## Alternative Formatting

Instead of XML tags, use Markdown:

### For Emphasis

```markdown
❌ <important>Run tests first</important>
✅ **IMPORTANT**: Run tests first
✅ > ⚠️ Run tests first
```

### For Sections

```markdown
❌ <context>This is background info</context>
✅ ## Context
   This is background info
```

### For Code

```markdown
❌ <code>function example() {}</code>
✅ `function example() {}`
✅ ```javascript
   function example() {}
   ```
```

### For Lists

```markdown
❌ <requirements>
     <req>Item 1</req>
     <req>Item 2</req>
   </requirements>

✅ **Requirements**:
   - Item 1
   - Item 2
```

## Special Case: HTML/XML Projects

If you're building web applications with HTML/XML:

**CLAUDE.md**:
```markdown
## HTML/XML Conventions
- Use semantic HTML5 tags: `<article>`, `<section>`, `<nav>`
- Accessibility: Always include `alt` attributes on `<img>` tags
- Forms: Wrap inputs in `<label>` tags

Note: These are HTML tags for the application, not meta-tags for Claude
```

**Skills**:
````markdown
# add-html-component.md
Create an accessible HTML component:

```html
<article class="card">
  <header>
    <h2>Title</h2>
  </header>
  <section class="content">
    <p>Content here</p>
  </section>
</article>
```
````

## Common Mistakes

### ❌ Using Tags for Instructions

```markdown
<instruction>
Follow these steps carefully
</instruction>
```

**Why bad**: Parser may interpret this as a special command

### ❌ Nesting Complex Structures

```markdown
<project>
  <backend>
    <database>PostgreSQL</database>
    <api>FastAPI</api>
  </backend>
</project>
```

**Why bad**: Overly complex, hard to read, no benefit over Markdown

### ❌ Mixing Conventions

```markdown
## Tech Stack
- <language>Python</language>
- <framework>Django</framework>
```

**Why bad**: Inconsistent formatting

## When XML Makes Sense

### API Response Parsing

If your project parses XML:

```markdown
## XML Processing
We parse API responses in this format:

```xml
<response>
  <status>success</status>
  <data>
    <user id="123">
      <name>John</name>
    </user>
  </data>
</response>
```

Use `xml.etree.ElementTree` for parsing.
```

This is documenting your application's XML format, not using XML to structure the CLAUDE.md.

## Best Practice Summary

**In CLAUDE.md**:
- ✅ Use Markdown formatting
- ✅ Use bold, italics, quotes for emphasis
- ✅ Use code blocks for code examples
- ❌ Avoid XML-style tags for meta-instructions

**In Skills**:
- ✅ XML tags if generating structured API prompts
- ✅ HTML/XML in code examples for web projects
- ❌ XML for skill instructions

**In Code**:
- ✅ HTML/XML as appropriate for your project
- ✅ Document your project's XML format
- ❌ Don't confuse project XML with meta-tags

## Migration Guide

If you have XML tags in CLAUDE.md:

**Before**:
```markdown
<important>
All commits must pass tests
</important>

<convention>
Use snake_case for functions
</convention>
```

**After**:
```markdown
> ⚠️ **IMPORTANT**: All commits must pass tests

## Naming Conventions
Functions: `snake_case`
```

## Key Takeaway

XML tags are powerful in Claude's API context, but in Claude Code's CLAUDE.md, stick to standard Markdown formatting. Reserve XML/HTML for documenting your application's actual markup, not for structuring instructions to Claude.
