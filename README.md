# Claude Code Flag System - Installation Package

**Version:** 2.0 - Production Ready
**Date:** 2025-11-16

---

## What's Included

This package contains everything you need to set up the Claude Code flag system with Context7 and Sequential Thinking MCP servers:

**📁 Files:**
```
new_system/
├── README.md                      # This file
├── configs/
│   ├── settings.json              # Hook configurations
│   └── .claude.json               # MCP server configurations
├── claude_commands/
│   ├── CLAUDE.md                  # Main command loader
│   ├── FLAGS.md                   # All 17 flag definitions
│   ├── CORE_RULES.md              # Fail-fast core principles
│   └── sc/                        # Slash commands (analyze, brainstorm, etc.)
└── hooks/
    ├── flag-detector.py           # Detects flags from user input
    ├── flag-reminder.py           # Enforces permissions & injects context
    ├── session-cleanup.py         # Cleans state files
    └── style-validator.py         # Validates code style on Write/Edit
```

**🎯 Features:**
- **17 Context-Aware Flags** for controlling development workflow
- **Hard Permission Enforcement** (blocks operations before they happen)
- **Smart Context Injection** (reduces token usage by 75%)
- **Code Style Validation** (automatic style checking on Write/Edit)
- **Multi-Instance Safe** (works across multiple Claude sessions)
- **Auto-Cleanup** (state files auto-delete after 1 hour)

---

## Prerequisites

Before installing, ensure you have:

1. **Claude Code** installed and working
2. **Node.js** installed (for npx commands)
3. **Python 3** installed (for hook scripts)
4. **Unix-like system** (macOS, Linux, WSL on Windows)

**Check your system:**
```bash
claude --version    # Should show Claude Code version
node --version      # Should show Node.js version (v16+)
python3 --version   # Should show Python 3.x
```

---

## Installation

### Step 1: Backup Current Configuration

**IMPORTANT:** Back up your existing configuration before proceeding.

```bash
# Backup settings.json (if it exists)
cp ~/.claude/settings.json ~/.claude/settings.json.backup

# Backup .claude.json (if it exists)
cp ~/.claude.json ~/.claude.json.backup

# Backup hooks directory (if it exists)
cp -r ~/.claude/hooks ~/.claude/hooks.backup
```

### Step 2: Install Hook Scripts

Copy the hook scripts to your Claude Code hooks directory:

```bash
# Create hooks directory if it doesn't exist
mkdir -p ~/.claude/hooks

# Copy hook scripts
cp hooks/flag-detector.py ~/.claude/hooks/
cp hooks/flag-reminder.py ~/.claude/hooks/
cp hooks/session-cleanup.py ~/.claude/hooks/
cp hooks/style-validator.py ~/.claude/hooks/

# Make scripts executable
chmod +x ~/.claude/hooks/flag-detector.py
chmod +x ~/.claude/hooks/flag-reminder.py
chmod +x ~/.claude/hooks/session-cleanup.py
chmod +x ~/.claude/hooks/style-validator.py
```

### Step 3: Configure Hooks in settings.json

**Option A: Fresh Installation (no existing settings.json)**

```bash
# Copy settings.json to Claude config directory
cp configs/settings.json ~/.claude/settings.json
```

**Option B: Merge with Existing settings.json**

If you already have `~/.claude/settings.json`, manually merge the hooks configuration:

1. Open your existing `~/.claude/settings.json`
2. Add or merge the `"hooks"` section from `configs/settings.json`
3. Save the file

**Note:** The settings.json includes 4 hooks:
- `flag-detector.py` - Flag detection
- `flag-reminder.py` - Permission enforcement & context injection
- `session-cleanup.py` - State file cleanup
- `style-validator.py` - Code style validation (60 second timeout)

### Step 4: Configure MCP Servers

**Option A: Fresh Installation (no existing .claude.json)**

```bash
# Copy .claude.json to home directory
cp configs/.claude.json ~/.claude.json
```

**Option B: Merge with Existing .claude.json**

If you already have `~/.claude.json`, manually merge the MCP servers:

1. Open your existing `~/.claude.json`
2. Add or merge the `"mcpServers"` section from `configs/.claude.json`:
   - `sequential-thinking` - Structured multi-step reasoning (--seq flag)
   - `context7` - Official library documentation (--c7 flag)
3. Save the file

**Note:** Both MCPs use npx, so Node.js must be installed.

### Step 5: Install Claude Commands (Optional)

To use the included FLAGS.md and CORE_RULES.md as global instructions:

```bash
# Option 1: Copy to global ~/.claude/ directory
cp claude_commands/CLAUDE.md ~/.claude/
cp claude_commands/FLAGS.md ~/.claude/
cp claude_commands/CORE_RULES.md ~/.claude/

# Option 2: Copy to project-specific .claude/ directory
# (Do this in your project directory)
mkdir -p .claude
cp claude_commands/CLAUDE.md .claude/
cp claude_commands/FLAGS.md .claude/
cp claude_commands/CORE_RULES.md .claude/

# Option 3: Reference in existing CLAUDE.md
# Add this line to your existing CLAUDE.md:
# @/path/to/FLAGS.md
# @/path/to/CORE_RULES.md
```

**Included slash commands:**
The `claude_commands/sc/` directory includes 7 slash commands:
- `/sc:analyze` - Code analysis
- `/sc:brainstorm` - Requirements discovery
- `/sc:design` - System architecture design
- `/sc:document` - Generate documentation
- `/sc:explain` - Code explanations
- `/sc:implement` - Feature implementation
- `/sc:troubleshoot` - Issue diagnosis

Copy these to `.claude/commands/sc/` to use them.

### Step 6: Restart Claude Code

After installation, restart all Claude Code sessions:

```bash
# Exit all running Claude instances
# Then start Claude Code again
claude
```

---

## Verification

### Test 1: Check Hooks Are Loaded

Run this command in Claude Code:

```bash
/hooks
```

You should see:
- `SessionStart` → `session-cleanup.py`
- `SessionEnd` → `session-cleanup.py`
- `PreCompact` → `session-cleanup.py`
- `UserPromptSubmit` → `flag-detector.py`
- `PreToolUse` → `flag-reminder.py` (for flag enforcement)
- `PreToolUse` → `style-validator.py` (for style validation)

### Test 2: Test Flag Detection

Type a message with a flag:

```
Test message --uo
```

You should see:
```
Active flags: --uo
```

### Test 3: Test Permission Blocking

With `--uo` flag active, ask Claude to create a new file:

```
Create a test file --uo
```

Claude should be BLOCKED from creating new files and show:
```
⚠️ REMINDER: Update only mode - you cannot create new files
```

### Test 4: Test MCP Servers

Check if MCP servers are loaded:

```bash
/mcp
```

You should see:
- `sequential-thinking` (running)
- `context7` (running)

### Test 5: Test State Cleanup

Check state files are created:

```bash
ls /tmp/claude-flags-*.json
```

You should see at least one state file with your session ID.

After exiting Claude Code, state files should be cleaned up within 1 hour or immediately on session end.

### Test 6: Test Style Validator (Optional)

The style-validator.py hook runs on Write/Edit operations with a 60-second timeout:

```
Ask Claude to write or edit a file
```

The style validator will check code style and provide feedback if issues are found.

**Note:** Check `/tmp/claude-style-validator.log` for style validation details.

---

## How to Use Flags

### Basic Usage

Add flags to the end of your messages:

```bash
"Fix this bug --uo"                    # Update only, no new files
"Explain how this works --ao"          # Answer only, no file operations
"Add new feature --new"                # Allow new file creation
"Debug this issue --hypothesis"        # Use scientific debugging approach
"Refactor code --minimal --focused"    # Minimal changes, stay on task
```

### Flag Categories

**📁 File Control:**
- `--ao [minimal|brief|standard]` - Answer only, blocks ALL file operations
- `--uo` - Update only, blocks new file creation
- `--new` - Explicitly allow new file creation

**🎯 Development Style:**
- `--fail-fast` - DEFAULT (no flag needed): fast iteration, fix errors as they appear
- `--prototype` - Quick and dirty implementation
- `--production` - Full safety nets, comprehensive error handling
- `--safe-mode` - Maximum validation and conservative execution

**🧠 Problem-Solving Approach:**
- `--first-principles` - Break down to fundamentals
- `--pattern-match` - Find and adapt similar solutions
- `--divide-conquer` - Split into manageable pieces
- `--hypothesis` - Scientific method debugging

**✏️ Code Modification:**
- `--minimal` - Smallest possible change
- `--refactor` - Improve without changing behavior
- `--aggressive` - Major restructuring allowed

**🎯 Focus Mode:**
- `--focused` - Stay on specific task only
- `--exploratory` - Understand entire system
- `--debug` - Add logging/traces for investigation

**🔧 Tool Enhancement:**
- `--c7` or `--context7` - Use official library documentation
- `--seq` or `--sequential` - Structured multi-step reasoning

### Flag Persistence

**Rules:**
- New flags REPLACE old flags
- No flags in message = KEEP existing flags
- Use `--clear-flags` to explicitly clear all flags
- `/compact` command clears all flags

**Example:**
```bash
User: "Fix bug --uo"          → Flags: [uo]
User: "Which file?"            → Flags: [uo] (kept)
User: "Refactor --minimal"     → Flags: [minimal] (replaced)
User: "--clear-flags"          → Flags: [] (cleared)
```

---

## Troubleshooting

### Issue: Flags Not Detected

**Symptom:** Type `--uo` but no "Active flags" message appears.

**Solution:**
```bash
# 1. Check hook configuration
grep -A 5 "UserPromptSubmit" ~/.claude/settings.json

# 2. Check hook is executable
ls -la ~/.claude/hooks/flag-detector.py

# 3. Check logs
tail -20 /tmp/claude-flag-detector.log

# 4. Manual test
echo '{"user_input": "test --uo", "session_id": "test", "cwd": "/tmp"}' | \
  ~/.claude/hooks/flag-detector.py
# Should output: Active flags: --uo
```

### Issue: Operations Not Blocked

**Symptom:** Have `--uo` flag but Claude creates new files anyway.

**Solution:**
```bash
# 1. Verify state file exists
ls -la /tmp/claude-flags-*.json

# 2. Check state file content
cat /tmp/claude-flags-*.json

# 3. Check flag-reminder logs
tail -20 /tmp/claude-flag-reminder-pre.log

# 4. Manual test blocking
echo '{"tool_name": "Write", "tool_input": {"file_path": "/tmp/new.py"}, "session_id": "test", "cwd": "/tmp"}' | \
  ~/.claude/hooks/flag-reminder.py
# Should exit with code 2 (blocked)
echo $?  # Should show: 2
```

### Issue: MCP Servers Not Loading

**Symptom:** `/mcp` shows servers as "not running" or "error".

**Solution:**
```bash
# 1. Check Node.js is installed
node --version

# 2. Test npx command
npx -y @modelcontextprotocol/server-sequential-thinking --help

# 3. Check .claude.json syntax
cat ~/.claude.json | python3 -m json.tool

# 4. Check MCP logs
# Look in Claude Code output for MCP startup errors
```

### Issue: State Files Accumulating

**Symptom:** Many old state files in /tmp.

**Solution:**
```bash
# Manual cleanup (safe)
rm /tmp/claude-flags-*.json
rm /tmp/claude-*-injection-state-*.json

# Files auto-clean after 1 hour or on SessionEnd
# Verify session-cleanup is configured
grep -A 5 "SessionStart" ~/.claude/settings.json
```

### Issue: Wrong Session Blocked

**Symptom:** One Claude instance affected by another's flags.

**This should NOT happen.** Each instance has unique session ID.

**If it does:**
```bash
# 1. Restart all Claude instances
# 2. Clear all state files
rm /tmp/claude-flags-*.json

# 3. Check session IDs are different
for f in /tmp/claude-flags-*.json; do
  echo "$f:"
  cat "$f" | grep session_id
done
```

---

## Logs and State Files

**Logs (for debugging):**
```
/tmp/claude-flag-detector.log
/tmp/claude-flag-reminder-pre.log
/tmp/claude-session-cleanup.log
/tmp/claude-style-validator.log
```

**State Files (auto-managed):**
```
/tmp/claude-flags-{session_id}.json                    # Active flags
/tmp/claude-pre-injection-state-{session_id}.json      # Timing state
```

**Log Viewing:**
```bash
# View recent flag detections
tail -20 /tmp/claude-flag-detector.log

# View permission decisions
tail -20 /tmp/claude-flag-reminder-pre.log

# View session cleanup events
tail -20 /tmp/claude-session-cleanup.log

# View style validation results
tail -20 /tmp/claude-style-validator.log

# Follow logs in real-time
tail -f /tmp/claude-flag-detector.log
```

---

## Uninstallation

To remove the flag system:

### Step 1: Remove Hooks from settings.json

Edit `~/.claude/settings.json` and remove the `"hooks"` section.

### Step 2: Remove Hook Scripts

```bash
rm ~/.claude/hooks/flag-detector.py
rm ~/.claude/hooks/flag-reminder.py
rm ~/.claude/hooks/session-cleanup.py
rm ~/.claude/hooks/style-validator.py
```

### Step 3: Remove MCP Servers (Optional)

Edit `~/.claude.json` and remove:
- `sequential-thinking`
- `context7`

Or remove entire `.claude.json` if only using it for these MCPs:
```bash
rm ~/.claude.json
```

### Step 4: Clean State Files

```bash
rm /tmp/claude-flags-*.json
rm /tmp/claude-*-injection-state-*.json
```

### Step 5: Restore Backups (If Needed)

```bash
# Restore original settings
cp ~/.claude/settings.json.backup ~/.claude/settings.json

# Restore original .claude.json
cp ~/.claude.json.backup ~/.claude.json

# Restore original hooks
rm -rf ~/.claude/hooks
cp -r ~/.claude/hooks.backup ~/.claude/hooks
```

---

## Advanced Configuration

### Customizing Timeouts

Edit `~/.claude/settings.json` to adjust hook timeouts:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/flag-detector.py",
            "timeout": 10  // Increase timeout to 10 seconds
          }
        ]
      }
    ]
  }
}
```

### Disabling Specific Hooks

Remove or comment out specific hook events in `settings.json`:

```json
{
  "hooks": {
    // "SessionStart": [...],  // Disabled
    "UserPromptSubmit": [...]   // Enabled
  }
}
```

### Adding More Flags

To add custom flags:

1. Edit `hooks/flag-detector.py` - Add pattern to `FLAG_PATTERNS`
2. Edit `hooks/flag-reminder.py` - Add context to `FLAG_CONTEXTS`
3. Reinstall hooks (copy to `~/.claude/hooks/`)

---

## Support and Documentation

**Full Documentation:**
- See `/Users/mechatronmike/Documents/Projects/Memory_System/working_memory/finished_implementations/FLAG_SYSTEM_COMPLETE.md` for complete system documentation
- See `/Users/mechatronmike/Documents/Projects/Memory_System/hooks/CLAUDE_CODE_HOOKS_EXPLAINED.md` for hooks deep dive

**Quick Reference:**
- See `hooks/QUICK_REFERENCE.md` (if included) for flag cheat sheet

**Issues:**
- Check logs in `/tmp/claude-*.log`
- Review troubleshooting section above
- Check hook is executable: `ls -la ~/.claude/hooks/*.py`

---

## Version Information

**Flag System:** v2.0 (Production Ready)
**Compatible with:** Claude Code 2.0+
**Last Updated:** 2025-11-16

---

## What This System Does

### Permission Enforcement (Hard Blocking)

**`--ao` (Answer Only):**
- Blocks: ALL file operations (Write, Edit, NotebookEdit)
- Use case: Getting information, explanations

**`--uo` (Update Only):**
- Blocks: NEW file creation only
- Allows: Editing existing files
- Use case: Bug fixes, refactoring existing code

**`--new`:**
- Allows: Creating new files
- Use case: Adding features, new modules

### Context Injection (Guidance)

All other flags provide context-aware guidance to Claude:
- Different messages per tool (Write, Edit, Read, Bash, etc.)
- Smart injection timing (reduces token usage by 75%)
- Tool-specific recommendations

**Example:**
```
Flags: [debug, minimal]
Tool: Read

Context Injected:
"🔬 CONTEXT: Debug mode - Look for logging points
 ✂️ CONTEXT: Minimal changes - Surgical fixes only"
```

---

## Success Criteria

After installation, you should be able to:

1. ✅ Type messages with flags and see "Active flags: ..." confirmation
2. ✅ Use `--uo` flag and have NEW file creation blocked
3. ✅ Use `--ao` flag and have ALL file operations blocked
4. ✅ Use problem-solving flags and see context-aware guidance
5. ✅ Use `--c7` flag and access official library documentation
6. ✅ Use `--seq` flag and see structured multi-step reasoning
7. ✅ Run `/mcp` and see both MCP servers running
8. ✅ Exit Claude and have state files auto-clean

---

**That's it! You're ready to use the Claude Code flag system.** 🎉

For questions or issues, check the logs and troubleshooting section above.
