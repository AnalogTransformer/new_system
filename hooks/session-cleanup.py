#!/usr/bin/env python3
"""
Smart Session Cleanup Hook
Handles cleanup for SessionStart, SessionEnd, and PreCompact events
- SessionStart: Clean OLD sessions (not current), preserve recent other instances
- SessionEnd: Clean CURRENT session
- PreCompact: Clean CURRENT session (user wants fresh start after /compact)
"""

import json
import sys
import os
import glob
import time
from datetime import datetime, timedelta
import logging

logging.basicConfig(
    filename='/tmp/claude-session-cleanup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('session-cleanup')

def cleanup_current_session(session_id):
    """Clean CURRENT session's state files (for SessionEnd/PreCompact)"""
    try:
        patterns = [
            f'/tmp/claude-flags-{session_id}.json',
            f'/tmp/claude-injection-state-{session_id}.json',
            f'/tmp/claude-pre-injection-state-{session_id}.json'
        ]

        removed_count = 0
        for file_path in patterns:
            if os.path.exists(file_path):
                os.remove(file_path)
                removed_count += 1
                logger.info(f"Removed current session file: {file_path}")

        if removed_count > 0:
            logger.info(f"Cleaned {removed_count} files for session {session_id}")

    except Exception as e:
        logger.error(f"Current session cleanup error: {e}")

def cleanup_old_sessions(current_session_id, age_threshold_hours=1):
    """Clean OLD sessions, preserve current and recent others (for SessionStart)"""
    try:
        patterns = [
            '/tmp/claude-flags-*.json',
            '/tmp/claude-injection-state-*.json',
            '/tmp/claude-pre-injection-state-*.json'
        ]

        current_time = time.time()
        age_threshold = age_threshold_hours * 3600  # Convert to seconds
        total_removed = 0

        for pattern in patterns:
            state_files = glob.glob(pattern)

            for file_path in state_files:
                try:
                    # Don't clean current session
                    if current_session_id and current_session_id in file_path:
                        logger.debug(f"Skipping current session: {file_path}")
                        continue

                    # Check file age
                    file_age = current_time - os.path.getmtime(file_path)

                    # Clean if older than threshold
                    if file_age > age_threshold:
                        os.remove(file_path)
                        total_removed += 1
                        logger.info(f"Removed old session file: {file_path} (age: {file_age/3600:.1f}h)")

                except Exception as e:
                    logger.warning(f"Could not process {file_path}: {e}")
                    # Try to remove corrupt files
                    try:
                        os.remove(file_path)
                        total_removed += 1
                        logger.info(f"Removed corrupt file: {file_path}")
                    except:
                        pass

        if total_removed > 0:
            logger.info(f"SessionStart cleanup: removed {total_removed} old session files")
        else:
            logger.info("SessionStart cleanup: no old files to remove")

    except Exception as e:
        logger.error(f"Old sessions cleanup error: {e}")

def main():
    """Main hook entry point - handles SessionStart, SessionEnd, PreCompact"""
    try:
        # Parse input to determine event type
        input_data = json.load(sys.stdin)
        hook_event = input_data.get("hook_event_name", "SessionStart")
        session_id = input_data.get("session_id", "unknown")

        logger.info(f"Cleanup triggered by {hook_event} for session {session_id}")

        if hook_event == "SessionStart":
            # Clean OLD sessions, preserve current and recent others
            cleanup_old_sessions(session_id, age_threshold_hours=1)
            logger.info(f"SessionStart: cleaned old sessions, preserved {session_id}")

        elif hook_event in ["SessionEnd", "PreCompact"]:
            # Clean CURRENT session (user wants fresh start)
            cleanup_current_session(session_id)
            logger.info(f"{hook_event}: cleaned current session {session_id}")

        else:
            logger.warning(f"Unknown hook event: {hook_event}")

        sys.exit(0)

    except Exception as e:
        logger.error(f"Hook error: {e}", exc_info=True)
        sys.exit(0)

if __name__ == "__main__":
    main()