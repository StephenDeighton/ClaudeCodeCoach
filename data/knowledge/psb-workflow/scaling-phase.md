---
slug: scaling-phase
title: Scaling PSB to Large Projects
category: psb-workflow
difficulty: advanced
keywords: scaling large projects parallel agents complex features
commands: []
related: [psb-overview, agents-overview, execution-phase]
---

# Scaling PSB to Large Projects

## Summary

Scale PSB methodology to large projects using parallel workflows, agent delegation, incremental delivery, and hierarchical planning. Break massive features into manageable chunks that can be developed concurrently.

## Scaling Challenges

### Small Project (Works Well)
- Single developer
- One feature at a time
- Linear PSB workflow
- Hours to days

### Large Project (Needs Scaling)
- Multiple features in parallel
- Complex dependencies
- Multiple team members
- Weeks to months

## Scaling Strategies

### 1. Hierarchical PSB

Break large features into nested PSB cycles:

```
Main Feature: User Management System
├─ Sub-feature 1: Authentication
│  ├─ Plan (30min)
│  ├─ Setup (20min)
│  └─ Build (3hr)
├─ Sub-feature 2: User Profiles
│  ├─ Plan (20min)
│  ├─ Setup (15min)
│  └─ Build (2hr)
└─ Sub-feature 3: Permissions
   ├─ Plan (1hr)
   ├─ Setup (30min)
   └─ Build (4hr)
```

Each sub-feature follows full PSB cycle independently.

### 2. Parallel PSB with Agents

Run multiple PSB cycles concurrently:

```bash
# Start three agents for parallel work
claude agent feature "Authentication" &
claude agent feature "User Profiles" &
claude agent feature "Permissions" &

# Each agent does full PSB:
Agent 1: Plan → Setup → Build (Auth)
Agent 2: Plan → Setup → Build (Profiles)
Agent 3: Plan → Setup → Build (Permissions)

# Coordinate integration at the end
```

### 3. Pipeline PSB

Stagger phases across features:

```
Week 1:
  Feature A: Plan → Setup → Build
  Feature B: Plan → Setup
  Feature C: Plan

Week 2:
  Feature A: Testing → Deploy
  Feature B: Build
  Feature C: Setup → Build

Week 3:
  Feature D: Plan → Setup → Build
  Feature B: Testing → Deploy
  Feature C: Testing → Deploy
```

### 4. Incremental PSB

Deliver in small iterations:

```
Iteration 1: MVP
- Plan core features only
- Setup minimal structure
- Build basic functionality

Iteration 2: Enhancements
- Plan next features
- Setup additional structure
- Build enhancements

Iteration 3: Polish
- Plan optimization
- Setup monitoring
- Build performance improvements
```

## Large Feature Decomposition

### Example: E-commerce Platform

#### Top-Level Plan

```markdown
# E-commerce Platform

## Phase 1: Core (2 weeks)
1. Product catalog
2. Shopping cart
3. Basic checkout

## Phase 2: Payments (1 week)
4. Payment integration
5. Order processing

## Phase 3: User Features (2 weeks)
6. User accounts
7. Order history
8. Reviews

## Phase 4: Admin (1 week)
9. Admin dashboard
10. Inventory management
```

#### Feature Breakdown

```
1. Product Catalog
   ├─ 1.1 Product Model (PSB: 4hr)
   ├─ 1.2 Product API (PSB: 6hr)
   ├─ 1.3 Product UI (PSB: 8hr)
   └─ 1.4 Search (PSB: 6hr)

2. Shopping Cart
   ├─ 2.1 Cart Model (PSB: 3hr)
   ├─ 2.2 Cart API (PSB: 4hr)
   ├─ 2.3 Cart UI (PSB: 6hr)
   └─ 2.4 Persistence (PSB: 2hr)
```

Each sub-feature is independently executable PSB cycle.

## Dependency Management

### Identify Dependencies

```
Features:
A: Product Catalog (no dependencies)
B: Shopping Cart (depends on A)
C: Checkout (depends on B)
D: User Accounts (no dependencies)
E: Order History (depends on C, D)

Parallel Groups:
Group 1: A, D (independent)
Group 2: B (after A)
Group 3: C (after B)
Group 4: E (after C and D)
```

### Dependency Graph

```
    A (Product Catalog)
    │
    ├─→ B (Shopping Cart)
    │   │
    │   └─→ C (Checkout)
    │       │
D (User Accounts) ─┴─→ E (Order History)
```

### Execution Plan

```bash
# Phase 1: Start independent features
claude agent feature "Product Catalog" &
claude agent feature "User Accounts" &

# Wait for Product Catalog
# Phase 2: Start dependent features
claude agent feature "Shopping Cart"

# Wait for Shopping Cart and User Accounts
# Phase 3: Start final integration
claude agent feature "Checkout"
claude agent feature "Order History"
```

## Agent Coordination

### Master Coordination Agent

```markdown
---
name: e-commerce-coordinator
type: coordinator
---

# E-commerce Platform Coordinator

## Objective
Coordinate development of e-commerce platform across multiple agents.

## Agents to Spawn

1. catalog-agent: Product catalog
2. cart-agent: Shopping cart (after catalog)
3. checkout-agent: Checkout (after cart)
4. accounts-agent: User accounts (parallel with catalog)
5. history-agent: Order history (after checkout + accounts)

## Coordination Logic
- Start catalog-agent and accounts-agent in parallel
- Monitor progress
- Start cart-agent when catalog-agent reaches 80%
- Start checkout-agent when cart-agent reaches 80%
- Start history-agent when both checkout and accounts complete
- Monitor integration points
- Run integration tests
- Report overall progress
```

### Progress Monitoring

```bash
/agents

Active agents:
✓ catalog-agent (completed)
→ cart-agent (running, 60%)
  accounts-agent (running, 45%)
  checkout-agent (waiting)
  history-agent (waiting)

Dependencies met: 1/4
ETA: 6 hours
```

## Context Management at Scale

### Problem: Context Overflow

```
Large project:
- 100+ files
- 50k+ lines
- Context fills up quickly
```

### Solution: Context Partitioning

```bash
# Main session: Coordination only
claude

# Spawn agents with focused context
claude agent feature "Product Catalog" --context="src/products,tests/products"
# Agent only loads product-related files

claude agent feature "User Accounts" --context="src/users,tests/users"
# Agent only loads user-related files

# Each agent has clean, focused context
```

### Solution: Fresh Sessions per Feature

```bash
# Complete Feature A
claude
"Build product catalog"
/commit
/exit

# Fresh session for Feature B
claude
"Build shopping cart"
# Clean context, no baggage from Feature A
```

## Incremental Integration

### Integration Checkpoints

```
Week 1: Build features independently
Week 2: Integrate A + B
Week 3: Integrate C
Week 4: Full system integration
Week 5: Polish and test

Each checkpoint:
- Plan integration
- Setup integration tests
- Build integration code
- Verify everything works
```

### Integration Testing

```typescript
// tests/integration/e2e.test.ts
describe('E-commerce Flow', () => {
  it('complete purchase flow', async () => {
    // 1. Browse products (Feature A)
    const products = await getProducts();
    expect(products.length).toBeGreaterThan(0);

    // 2. Add to cart (Feature B)
    await addToCart(products[0].id);
    const cart = await getCart();
    expect(cart.items).toHaveLength(1);

    // 3. Checkout (Feature C)
    const order = await checkout(cart.id);
    expect(order.status).toBe('pending');

    // 4. View order history (Feature D)
    const history = await getOrderHistory();
    expect(history).toContainEqual(order);
  });
});
```

## Scaling Best Practices

### ✅ Do:
- Break large features into < 1 day sub-features
- Run independent features in parallel
- Use agents for parallel work
- Maintain clear dependency graph
- Regular integration checkpoints
- Keep context focused per agent
- Document integration points

### ❌ Don't:
- Try to build everything at once
- Ignore dependencies
- Skip integration testing
- Let context overflow
- Forget documentation
- Avoid agent coordination

## Scaling Patterns

### Pattern: Feature Teams

```
Team 1: Frontend
  Agent 1a: Product UI
  Agent 1b: Cart UI

Team 2: Backend
  Agent 2a: Product API
  Agent 2b: Cart API

Team 3: Database
  Agent 3a: Schema
  Agent 3b: Migrations

Coordinate weekly for integration
```

### Pattern: Vertical Slices

```
Week 1: Product vertical (DB → API → UI)
Week 2: Cart vertical (DB → API → UI)
Week 3: Checkout vertical (DB → API → UI)

Each vertical is complete feature
Integrate horizontally at end
```

### Pattern: Layer Completion

```
Month 1: All data models
Month 2: All API endpoints
Month 3: All UI components
Month 4: Integration

Risky but works for stable requirements
```

## Measuring Progress

### Feature Completion Matrix

```
| Feature           | Plan | Setup | Build | Test | Done |
|-------------------|------|-------|-------|------|------|
| Product Catalog   | ✓    | ✓     | ✓     | ✓    | ✓    |
| Shopping Cart     | ✓    | ✓     | 60%   | 0%   | No   |
| Checkout          | ✓    | 40%   | 0%    | 0%   | No   |
| User Accounts     | 100% | 0%    | 0%    | 0%   | No   |
| Order History     | 0%   | 0%    | 0%    | 0%   | No   |

Overall: 25% complete
```

### Velocity Tracking

```
Week 1: 2 features completed
Week 2: 3 features completed
Week 3: 2 features completed

Average: 2.3 features/week
Remaining: 15 features
ETA: 6.5 weeks
```

## Key Takeaway

Scale PSB to large projects by breaking features into sub-features, running parallel PSB cycles with agents, managing dependencies carefully, and integrating incrementally. Each sub-feature should complete a full PSB cycle in < 1 day. Use agents for parallelism and keep context focused per feature.
