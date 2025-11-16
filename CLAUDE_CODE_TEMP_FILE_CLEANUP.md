# Claude Code: Temporary File Pollution Issues & Fixes

## Problem

Claude Code creates temporary files that accumulate and are not automatically cleaned up, polluting the filesystem.

## Two Distinct Issues

### 1. `/tmp/claude-*-cwd` Files (Confirmed Bug)

**Description:** Every Bash command execution creates a working directory tracking file that is never deleted.

**Evidence:**
- Files accumulate at ~14.5 per hour during active use
- One user reported 174 files in a single day
- 2,018 files over 4 days in another case

**Root Cause:** Claude Code reads these files to track working directory changes but omits the cleanup step.

**Status:** Open bug (GitHub Issue #8856) - fix identified but not yet merged

### 2. `.claude.json.tmp.*` Files (Hook Error Bug)

**Description:** Temporary files like `.claude.json.tmp.8980.1763254562083` accumulate in home directory.

**Normal Behavior:** These files are part of atomic write operations and should be immediately deleted after being renamed to `.claude.json`.

**When They Accumulate:**
- During UserPromptSubmit hook infinite loops
- "Lock file is already being held" errors
- Hook crashes or errors
- Can cause 70-80% CPU usage and unresponsive CLI

**Status:** Related to Issue #9849

## Current State

Cleaned up **36 accumulated files** from `/tmp/claude-*-cwd` on this system.

## Manual Cleanup

### One-time Cleanup

```bash
# Clean /tmp files
rm -f /tmp/claude-*-cwd

# Clean .claude.json.tmp files (if they exist)
rm -f ~/.claude.json.tmp.*
```

### Automated Daily Cleanup (Recommended)

Create a systemd timer for automatic cleanup:

```bash
# Create cleanup script
cat > ~/cleanup-claude-tmp.sh << 'EOF'
#!/bin/bash
# Clean Claude Code temporary files
rm -f /tmp/claude-*-cwd 2>/dev/null
rm -f ~/.claude.json.tmp.* 2>/dev/null
EOF

chmod +x ~/cleanup-claude-tmp.sh

# Create systemd service
mkdir -p ~/.config/systemd/user/

cat > ~/.config/systemd/user/claude-cleanup.service << 'EOF'
[Unit]
Description=Clean up Claude Code temporary files

[Service]
Type=oneshot
ExecStart=/home/lab/cleanup-claude-tmp.sh
EOF

# Create systemd timer (runs daily at 2am)
cat > ~/.config/systemd/user/claude-cleanup.timer << 'EOF'
[Unit]
Description=Daily Claude Code cleanup timer

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Enable and start timer
systemctl --user daemon-reload
systemctl --user enable claude-cleanup.timer
systemctl --user start claude-cleanup.timer
```

### Verify Timer Status

```bash
# Check timer status
systemctl --user status claude-cleanup.timer

# List upcoming runs
systemctl --user list-timers | grep claude
```

## Cron Alternative (If not using systemd)

```bash
# Add to crontab
crontab -e

# Add this line (runs daily at 2am)
0 2 * * * rm -f /tmp/claude-*-cwd ~/.claude.json.tmp.* 2>/dev/null
```

## System Default Cleanup

Most Linux systems have `systemd-tmpfiles-clean` that automatically cleans `/tmp`:
- Typically runs daily at 07:15
- Only cleans `/tmp` directory (not home directory `.claude.json.tmp` files)
- May not run in Docker containers without systemd

## Prevention

### For `.claude.json.tmp` Issues:
1. Check hooks configuration if seeing infinite loops
2. Disable problematic UserPromptSubmit hooks
3. Monitor for "Lock file is already being held" errors

### For `/tmp/claude-*-cwd` Issues:
- No user-side prevention available
- Waiting for upstream fix to be merged
- Use automated cleanup scripts

## Monitoring

Check accumulation with:

```bash
# Count files
echo "/tmp files: $(find /tmp -name 'claude-*-cwd' 2>/dev/null | wc -l)"
echo "Home tmp files: $(find ~ -maxdepth 1 -name '.claude.json.tmp.*' 2>/dev/null | wc -l)"

# Show disk usage
du -sh /tmp/claude-*-cwd 2>/dev/null | tail -1
```

## References

- Issue #8856: Memory leak with /tmp/claude-*-cwd files
- Issue #9849: Infinite loop causing .claude.json.tmp accumulation
- Issue #195: Massive files in /tmp directory

## Cleanup Script Location

`~/cleanup-claude-tmp.sh` - Manual or automated execution

## Last Cleanup: 2025-11-16
