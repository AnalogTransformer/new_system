# Claude Code: Raspberry Pi 5 Custom Slash Commands Fix

## Problem

Custom slash commands in Claude Code do not appear on Raspberry Pi 5 (and other ARM systems with 16KB page sizes).

## Root Cause

The bundled `ripgrep` binary in Claude Code was compiled with jemalloc configured for **4KB page size**, but RPi5 uses **16KB pages**. This causes ripgrep to fail silently, preventing Claude Code from discovering `.md` command files.

## Solution

Replace the broken bundled ripgrep with a symlink to the system ripgrep (compiled correctly for RPi5).

### Step 1: Install System Ripgrep

```bash
sudo apt update
sudo apt install -y ripgrep
```

### Step 2: Verify System Ripgrep Works

```bash
/usr/bin/rg --version
```

Should output version info (e.g., `ripgrep 14.1.1`)

### Step 3: Replace Bundled Ripgrep

```bash
# Backup broken binary
sudo mv /usr/lib/node_modules/@anthropic-ai/claude-code/vendor/ripgrep/arm64-linux/rg \
   /usr/lib/node_modules/@anthropic-ai/claude-code/vendor/ripgrep/arm64-linux/rg.broken

# Create symlink to system ripgrep
sudo ln -s /usr/bin/rg \
   /usr/lib/node_modules/@anthropic-ai/claude-code/vendor/ripgrep/arm64-linux/rg
```

### Step 4: Verify Fix

```bash
# Test command discovery
rg --files ~/.claude/commands/
```

Should list all `.md` files in the commands directory.

### Step 5: Restart Claude Code

Exit all Claude Code instances completely and restart.

## Command Directory Structure

Custom commands must be in the correct location:

```
~/.claude/commands/          # Personal commands
.claude/commands/            # Project commands
```

**Important Notes:**
- Directory name must be lowercase `commands` (Linux is case-sensitive)
- Files must have `.md` extension
- Files should include YAML frontmatter with `description` field
- Command files can be in subdirectories, but filename (not path) becomes the command name

## Example Command File

```markdown
---
description: Brief description of what this command does
argument-hint: "[optional-args]"
---

Your command prompt here using $ARGUMENTS for parameters
```

## Verification

After restart, commands should appear when you type `/` or run `/help`.

## References

- GitHub Issue: https://github.com/anthropics/claude-code/issues/9462
- Claude Code Docs: https://code.claude.com/docs/en/slash-commands.md

## Fixed: 2025-11-16
