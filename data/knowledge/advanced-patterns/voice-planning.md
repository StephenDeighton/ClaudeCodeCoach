---
slug: voice-planning
title: Voice Planning Pattern
category: advanced-patterns
difficulty: intermediate
keywords: voice audio dictation planning thinking
commands: []
related: [planning-phase]
---

# Voice Planning Pattern

## Summary

Use voice input to rapidly brainstorm and plan features before coding. Speaking is faster than typing for exploring ideas and design decisions.

## Pattern

```
1. Think out loud (voice)
2. Claude transcribes + organizes
3. Refine plan (text)
4. Execute
```

## When to Use

- Complex feature planning
- Design discussions
- Architecture decisions
- Brainstorming sessions
- Requirements gathering

## Example Session

```
User: [Voice] "I'm thinking about adding user authentication.
We need JWT tokens, probably store them in httpOnly cookies for security.
The backend needs a login endpoint, register endpoint, and middleware
to protect routes. Frontend should have a useAuth hook. We should
also add refresh tokens but maybe that's phase 2. What do you think?"

Claude: [Text] "Great overview. Let me organize this:

## Authentication Plan

### Phase 1 (MVP)
1. JWT tokens in httpOnly cookies
2. Backend endpoints:
   - POST /auth/login
   - POST /auth/register
   - Middleware for protected routes
3. Frontend: useAuth hook

### Phase 2
- Refresh token mechanism

Questions:
- Token expiration time?
- Password hashing method?
- Rate limiting on auth endpoints?

Shall I proceed with Phase 1?"
```

## Benefits

- Faster than typing
- Natural thought flow
- Capture stream of consciousness
- Claude organizes ideas
- Easy iteration

## Best Practices

✅ Speak naturally
✅ Think out loud
✅ Mention concerns/questions
✅ Let Claude organize
✅ Refine in text

## Key Takeaway

Voice planning accelerates feature design. Speak your thoughts naturally, let Claude transcribe and organize into structured plan, then refine details via text. Combines speed of speech with precision of text.
