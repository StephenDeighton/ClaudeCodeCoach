# Next Session Task: Fix CC Setup Wizard Score Target

## Problem

The CC Setup Wizard currently achieves **0/100 score** instead of the promised **≥50 score**.

**Test case:** After running wizard on `/Users/stevedeighton/Library/CloudStorage/Dropbox/A_Coding/Locker`, the health scan shows 0/100 with 12 issues.

## Root Cause

The health checker uses **subtractive scoring**:
- Starts at 100
- CRITICAL issues: -20 points each
- WARNING issues: -10 points each
- INFO issues: -5 points each

With 12 issues detected, score drops to 0.

## What Wizard Currently Creates

✅ Files created:
- `.claude/settings.json` (with model, thinking tokens, hooks)
- `.claude/CLAUDE.md` (tech-specific template, <50 lines)
- `.gitignore` (with .env, settings.local.json)
- `status.md` (with dated setup entry)
- `.claude/skills/` directory (empty)
- `.claude/commands/` directory (empty)
- `README.md` (tech-specific template)

## What's Still Missing (Causing 12 Issues)

Based on test results, the wizard still doesn't create:

**WARNING checks (12 issues, approx breakdown):**
1. No tests directory (`tests/`) - -10 points
2. No subagents directory (`.claude/subagents/`) - -10 points
3. No architecture docs (`.claude/ARCHITECTURE.md` or `docs/architecture.md`) - -10 points
4. No changelog (`CHANGELOG.md`) - -10 points
5. No planning docs (`.claude/planning/` or `docs/planning/`) - -10 points
6. Large files check might be failing - -10 points
7. Other warnings...

**INFO checks:**
1. No /commit command (`.claude/commands/commit.md`) - -5 points
2. No /init command (`.claude/commands/init.md`) - -5 points
3. No GitHub Actions (`.github/workflows/`) - -5 points
4. Other info checks...

## Task for Next Session

**Fix `services/project_setup_service.py` to create additional files/directories so wizard achieves ≥50 score.**

### Step 1: Analyze Exact Failures

Run wizard on a test folder, then check which specific detectors are still failing:

```bash
./start.sh
# Run wizard on test folder
# Navigate to Fix tab
# Note all 12 issues that appear
```

### Step 2: Add Missing Files/Directories

Update `setup_project()` method in `services/project_setup_service.py` to create:

**Critical (must fix for score):**
- `.claude/subagents/` directory
- `tests/` directory
- `.claude/commands/commit.md` (basic template)
- `.claude/commands/init.md` (basic template)
- `CHANGELOG.md` (empty template)

**Optional (for ≥60 score):**
- `.claude/planning/` directory
- `.claude/ARCHITECTURE.md` (or `docs/architecture.md`)
- `.github/workflows/` directory

### Step 3: Test End-to-End

**CRITICAL: Actually test this time!**

```bash
# 1. Delete .claude/ from test folder
rm -rf /path/to/test/folder/.claude

# 2. Run wizard
./start.sh
# Complete wizard flow

# 3. Scan the folder
# Should show ≥50/100 score

# 4. Go to Fix tab and verify <5 issues remain
```

### Step 4: Update Expected Score Calculation

In `setup_project()`, update the score calculation comments to match reality:

```python
result.expected_score += 10  # skills dir
result.expected_score += 10  # commands dir
result.expected_score += 10  # README.md
result.expected_score += 10  # tests dir
result.expected_score += 10  # subagents dir
result.expected_score += 10  # commit command
result.expected_score += 10  # init command
# ... etc
# Total should be ≥50 after all fixes deducted
```

## Success Criteria

- [ ] Wizard completes without errors
- [ ] Health scan shows **≥50/100 score**
- [ ] No more than 5 issues remaining
- [ ] All CRITICAL issues resolved
- [ ] Most WARNING issues resolved
- [ ] Tested on at least 2 different project types (Python, JavaScript)

## Files to Modify

- `services/project_setup_service.py` - Add more file/directory creation
- `pages/setup_wizard.py` - Update expected score display (if needed)

## Testing Checklist

- [ ] Run `./start.sh` to ensure clean launch
- [ ] Complete wizard flow end-to-end
- [ ] Verify health scan shows ≥50/100
- [ ] Navigate to Fix tab and count remaining issues
- [ ] Test with Python project
- [ ] Test with JavaScript project
- [ ] Commit with proper testing confirmation

## Reference

- Wizard implementation: `pages/setup_wizard.py`
- Setup service: `services/project_setup_service.py`
- Health checks: `health_checks/critical/`, `health_checks/warning/`, `health_checks/info/`
- Scoring algorithm: `services/health_checker.py` line 88-117

---

**Remember:** Test the wizard end-to-end BEFORE committing. Launch app, run wizard, scan, verify score ≥50.
