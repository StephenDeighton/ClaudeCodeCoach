---
slug: message-queue
title: Message Queue Pattern with Agents
category: advanced-patterns
difficulty: advanced
keywords: message queue agents async coordination
commands: []
related: [parallel-subagents, when-use-subagents]
---

# Message Queue Pattern with Agents

## Summary

Use message passing to coordinate work between main session and subagents. Agents process work items from queue, enabling async task distribution.

## Pattern

```
Main Session (Coordinator)
    ↓ (enqueue tasks)
Task Queue
    ↓ (dequeue work)
Agents (Workers)
    ↓ (report results)
Main Session (Collect)
```

## Implementation

```markdown
# Queue file: .claude/queue.json
{
  "tasks": [
    {"id": 1, "type": "test", "file": "auth.test.ts", "status": "pending"},
    {"id": 2, "type": "test", "file": "api.test.ts", "status": "pending"},
    {"id": 3, "type": "test", "file": "db.test.ts", "status": "pending"}
  ]
}
```

## Coordinator Agent

```markdown
# Main session creates queue
1. Break work into tasks
2. Write to queue file
3. Spawn worker agents
4. Monitor progress
5. Collect results
```

## Worker Agent

```markdown
# Agent workflow
1. Read queue
2. Claim pending task (mark in_progress)
3. Execute task
4. Write result
5. Mark complete
6. Repeat
```

## Use Cases

### Test Parallelization
```
Queue: 50 test files
3 agents: Each runs 16-17 tests
Time: 3x faster
```

### File Processing
```
Queue: 100 files to migrate
5 agents: Each handles 20 files
Parallel processing
```

### API Generation
```
Queue: 30 endpoints to build
3 agents: Each builds 10 endpoints
Coordinated development
```

## Benefits

- True parallelism
- Load balancing
- Fault tolerance
- Progress tracking
- Scalable

## Key Takeaway

Message queue pattern enables true parallel work distribution. Main session enqueues tasks, worker agents claim and process items, results collected centrally. Use for parallelizable batch operations like testing, migration, or generation tasks.
