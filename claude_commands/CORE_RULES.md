# Core Engineering Rules & Principles

**Prime Directive**: Move fast, break things, fix quickly | Evidence > assumptions | Code > documentation

**Default Mode**: **Fail-fast** - Overwrite directly, run immediately, fix errors iteratively. Trust version control, not backups.

## Philosophy

**Fail-Fast by Default** (no flag needed):
- Overwrite functions directly (no `_old` backups)
- Run immediately and fix errors as they appear
- Minimal defensive coding, trust version control
- Philosophy: Speed → Error → Fix → Learn

**Override with flags when needed**: See FLAGS.md for all flags and when to use them

## Priority Matrix

| Level       | Rule                         | Override |
| ----------- | ---------------------------- | -------- |
| CRITICAL 🔴 | Security, data safety        | Never    |
| IMPORTANT 🟡| Working code, tests pass     | Rarely   |
| NICE 🟢     | Clean code, optimization     | Often    |

## Workflow: Act → React → Adapt

1. **Understand**: Scan quickly, evidence-based
2. **Execute**: Parallel operations, batch calls
3. **Fix**: Errors are discovery, not failure
4. **Validate**: Test, root cause, iterate

## Implementation Rules

| Aspect      | DO ✅                         | DON'T ❌              |
| ----------- | ----------------------------- | --------------------- |
| **Speed**   | Ship fast, iterate            | Perfect first attempt |
| **Features**| Complete what you start       | Leave TODOs/stubs     |
| **Scope**   | MVP first, YAGNI              | Feature creep         |
| **Code**    | Real implementations          | Placeholders, mocks   |
| **Errors**  | Run and fix                   | Overplan edge cases   |
| **Testing** | Write tests, they must pass   | Skip or disable tests |
| **Git**     | Feature branches              | NEVER COMMIT directly |

## File Operations (Fail-Fast Style)

```
Need to change code?
  → Read file
  → Edit directly (overwrite, no _old backups)
  → Run
  → Fix errors
  → Done

Creating new file?
  → Check structure exists
  → Write
  → Absolute paths only
```

**Override**: Use `--uo` to block new files, `--ao` for answer-only mode

## Code Quality: Working > Perfect

**Good Enough:**
- Code runs and tests pass
- Readable by humans
- Follows existing patterns

**Not Required by Default:**
- Extensive error handling (add with `--production`)
- Backup functions (add with `--safe-mode`)
- Edge case coverage (add with `--production`)

**Always Required:**
- Security (NEVER skip)
- Data safety (NEVER skip)
- Tests pass (NEVER disable)

## Design Principles (Keep Simple)

- **YAGNI**: Build what you need NOW
- **DRY**: Don't duplicate, but don't over-abstract
- **KISS**: Simple > clever
- **SOLID**: When it makes code clearer

## Problem-Solving Approach

Use flags to specify approach when needed (see FLAGS.md):
- **Approach**: first-principles, pattern-match, divide-conquer, hypothesis
- **Modification**: minimal, refactor, aggressive
- **Focus**: focused, exploratory, debug

## Tool Selection

```
Complex reasoning?     → Use --seq flag
Library docs?          → Use --c7 flag
Multiple operations?   → Parallel execution
Simple task?           → Just do it
```

## Communication Style

- **No fluff**: Get to the point
- **No marketing**: Avoid "amazing", "powerful", etc.
- **Evidence-based**: Facts, not claims
- **Honest trade-offs**: Pros AND cons
- **Technical precision**: Accurate terms

## Organization (Standard Patterns)

| Type    | Location              | Example                 |
| ------- | --------------------- | ----------------------- |
| Tests   | `tests/` or `__tests__/` | `tests/auth.test.js` |
| Scripts | `scripts/` or `tools/`   | `scripts/deploy.sh`  |
| Docs    | `docs/`               | `docs/API.md`           |
| Source  | By feature/domain     | `components/auth/`      |

## Git Rules (Non-Negotiable)

- **Feature branches**: Always
- **NEVER COMMIT**: Not allowed, ever
- **Work on branches**: Create branch, work, done
- **Don't push --force**: Especially to main

## Risk Assessment

| Risk Type    | Action                      |
| ------------ | --------------------------- |
| Reversible   | Go fast, fix if wrong       |
| Expensive    | Quick check first           |
| Irreversible | Validate before executing   |
| Security     | ALWAYS validate (CRITICAL🔴)|

## Quick Patterns

```bash
# Debugging flow
Run → Error → Understand → Fix → Run → Done

# Feature flow
Understand → Code → Test → Fix → Done

# Analysis flow
Question → Evidence → Conclusion
```

## When to Slow Down

**Fail-fast isn't always right**. Use safety flags from FLAGS.md when:
- Deploying to production
- Working on critical systems
- Unfamiliar codebase
- High-stakes changes

## Remember

- **Default = Fail-fast**: No backups, no overthinking, just ship and fix
- **Version control is your backup**: Git has your back
- **Tests must pass**: Only hard rule for quality
- **Security is non-negotiable**: Always validate
- **Use flags to override**: FLAGS.md has context-specific modes
