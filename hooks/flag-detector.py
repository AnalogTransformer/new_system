#!/usr/bin/env python3
"""
Flag Detection Hook (UserPromptSubmit)
Detects flags from user input and saves to session state
This runs ONCE when user submits a prompt, before Claude processes
"""

import json
import sys
import os
import re
import logging
import hashlib
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    filename='/tmp/claude-flag-detector.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('flag-detector')

# Flag definitions - matching FLAGS.md
FLAG_PATTERNS = {
    # File control flags (--ao can have minimal|brief|standard parameter)
    r'\s--ao(?:\s+(minimal|brief|standard))?\b': 'ao',
    r'\s--uo\b': 'uo',
    r'\s--new\b': 'new',

    # Development style flags
    r'\s--fail-fast\b': 'fail-fast',
    r'\s--prototype\b': 'prototype',
    r'\s--production\b': 'production',
    r'\s--safe-mode\b': 'safe-mode',

    # Problem-solving approach flags
    r'\s--first-principles\b': 'first-principles',
    r'\s--pattern-match\b': 'pattern-match',
    r'\s--divide-conquer\b': 'divide-conquer',
    r'\s--hypothesis\b': 'hypothesis',

    # Code modification flags
    r'\s--minimal\b': 'minimal',
    r'\s--refactor\b': 'refactor',
    r'\s--aggressive\b': 'aggressive',

    # Focus mode flags
    r'\s--focused\b': 'focused',
    r'\s--exploratory\b': 'exploratory',
    r'\s--debug\b': 'debug',

    # Tool enhancement flags
    r'\s--c7\b': 'c7',
    r'\s--context7\b': 'c7',  # Alternative spelling
    r'\s--seq\b': 'seq',
    r'\s--sequential\b': 'seq',  # Alternative spelling
}

def get_session_id_from_input(input_data):
    """Get stable session ID from Claude (not generated)"""
    # Use Claude's provided session_id
    session_id = input_data.get("session_id")
    if session_id:
        return session_id

    # Fallback: use transcript_path hash (unique per session)
    transcript = input_data.get("transcript_path", "")
    if transcript:
        return hashlib.md5(transcript.encode()).hexdigest()[:16]

    # Last resort: use cwd + timestamp (not ideal)
    cwd = input_data.get("cwd", os.getcwd())
    cwd_hash = hashlib.md5(cwd.encode()).hexdigest()[:8]
    date_str = datetime.now().strftime('%Y%m%d_%H%M')
    return f"{cwd_hash}_{date_str}"

def get_state_file_path(session_id):
    """Get path to session state file"""
    return f"/tmp/claude-flags-{session_id}.json"

def load_session_state(state_file):
    """Load existing session state if available"""
    try:
        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                state = json.load(f)
                # Ensure backward compatibility
                if 'flag_metadata' not in state:
                    state['flag_metadata'] = {}
                logger.info(f"Loaded session state: {state['flags']}")
                return state
    except Exception as e:
        logger.warning(f"Could not load state file: {e}")
    return None

def save_session_state(state_file, flags, flag_metadata, session_id, cwd):
    """Save session state atomically with flag parameters"""
    try:
        state = {
            "session_id": session_id,
            "flags": list(flags),
            "flag_metadata": flag_metadata,
            "detected_at": datetime.now().isoformat(),
            "cwd": cwd
        }

        # Atomic write: temp file + rename
        temp_file = state_file + '.tmp'
        with open(temp_file, 'w') as f:
            json.dump(state, f, indent=2)
        os.rename(temp_file, state_file)

        logger.info(f"Saved session state with flags: {flags}, metadata: {flag_metadata}")
        return True
    except Exception as e:
        logger.error(f"Failed to save state: {e}")
        return False

def parse_flags_from_input(user_input):
    """Parse flags directly from user input string"""
    flags = set()
    flag_metadata = {}

    try:
        # Search for all flag patterns
        for pattern, flag_name in FLAG_PATTERNS.items():
            match = re.search(pattern, user_input)
            if match:
                flags.add(flag_name)

                # Capture flag parameters if present
                if match.groups():
                    flag_metadata[flag_name] = match.group(1)

        if flags:
            logger.info(f"Parsed flags from user input: {flags}")

    except Exception as e:
        logger.error(f"Error parsing flags from input: {e}")

    return flags, flag_metadata

def has_new_flags(user_input):
    """Check if user input contains flag patterns"""
    return bool(re.search(r'\s--\w+', user_input))

def handle_user_prompt_submit(user_input, session_id, cwd):
    """
    Smart flag detection and persistence on UserPromptSubmit

    Logic:
    - If --clear-flags: Clear all flags
    - If new flags detected: REPLACE existing flags with new ones
    - If no flags: KEEP existing flags (user just adding clarification)
    """
    try:
        state_file = get_state_file_path(session_id)

        # Load existing state
        existing_state = load_session_state(state_file)
        existing_flags = set(existing_state['flags']) if existing_state else set()
        existing_metadata = existing_state.get('flag_metadata', {}) if existing_state else {}

        # Smart update logic
        if "--clear-flags" in user_input:
            # Explicit clear requested
            flags = set()
            metadata = {}
            logger.info("Flags explicitly cleared by user")
        elif has_new_flags(user_input):
            # New flags detected - REPLACE existing flags
            flags, metadata = parse_flags_from_input(user_input)
            logger.info(f"New flags detected, replacing old: {flags}")
        else:
            # No new flags - KEEP existing flags
            flags = existing_flags
            metadata = existing_metadata
            logger.info(f"No new flags, keeping existing: {flags}")

        # Save state for flag-reminder to use
        if save_session_state(state_file, flags, metadata, session_id, cwd):
            # Optionally output flag summary for user visibility
            if flags:
                flag_list = [f"--{f}" for f in sorted(flags)]
                print(f"Active flags: {' '.join(flag_list)}")

    except Exception as e:
        logger.error(f"Error handling user prompt: {e}", exc_info=True)

def main():
    """Main hook entry point for UserPromptSubmit"""
    try:
        # Parse input
        input_data = json.load(sys.stdin)

        user_input = input_data.get("user_input", "")
        cwd = input_data.get("cwd", os.getcwd())

        # Get stable session ID from Claude
        session_id = get_session_id_from_input(input_data)

        logger.debug(f"UserPromptSubmit for session {session_id}")
        logger.debug(f"User input: {user_input[:100]}...")

        # Handle flag detection and persistence
        handle_user_prompt_submit(user_input, session_id, cwd)

        # Always exit 0 for UserPromptSubmit (we just detect, don't block)
        sys.exit(0)

    except Exception as e:
        logger.error(f"Hook error: {e}", exc_info=True)
        # Fail-open: allow operation on error
        sys.exit(0)

if __name__ == "__main__":
    main()
