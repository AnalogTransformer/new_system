#!/usr/bin/env python3
"""
Flag Reminder Hook (PreToolUse)
Injects context-specific flag reminders BEFORE tool execution to guide Claude's behavior
This runs BEFORE actions so Claude knows what flags are active and how to behave
"""

import json
import sys
import os
import re
import logging
from datetime import datetime, timedelta
import hashlib
import time

# Configure logging
logging.basicConfig(
    filename='/tmp/claude-flag-reminder-pre.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('flag-reminder-pre')

# Flag patterns - matching FLAGS.md (same as flag-detector.py for consistency)
FLAG_PATTERNS = {
    # File control flags
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
    r'\s--context7\b': 'c7',
    r'\s--seq\b': 'seq',
    r'\s--sequential\b': 'seq',
}

# Context-aware messages for BEFORE tool execution
FLAG_CONTEXTS = {
    # File Control Flags
    "--ao": {
        "Write": "⚠️ STOP: Answer only mode - provide console output instead of creating files",
        "Edit": "⚠️ STOP: Answer only mode - explain changes instead of making them",
        "Read": "📖 Remember: Answer only mode - analyze for explanation, not modification",
        "Bash": "⚠️ CAUTION: Answer only - observe don't modify",
        "DEFAULT": "💬 Answer only mode active - no file operations"
    },

    "--uo": {
        "Write": "⚠️ REMINDER: Update only mode - you cannot create new files, only modify existing ones",
        "Edit": "✅ OK: Update existing files, but preserve overall structure",
        "Read": "📋 CONTEXT: Looking for improvements in existing code",
        "Grep": "🔍 PURPOSE: Finding patterns to enhance existing implementation",
        "Bash": "🧪 GOAL: Test changes to existing functionality",
        "Task": "🎯 FOCUS: Improve what exists, don't add new files",
        "DEFAULT": "📝 Update only - enhance existing code"
    },

    "--new": {
        "Write": "✅ OK: You may create new files as needed",
        "Edit": "✅ OK: Refactoring may include new supporting files",
        "DEFAULT": "➕ New files allowed"
    },

    # Development Style Flags
    "--fail-fast": {
        "Write": "⚡ APPROACH: Overwrite directly, no backup functions",
        "Edit": "🔄 STYLE: Replace functions completely, no _old versions needed",
        "Bash": "🏃 METHOD: Run immediately to discover errors",
        "Read": "🎯 GOAL: Find minimal fix that works",
        "DEFAULT": "💨 Fail fast - iterate quickly"
    },

    "--prototype": {
        "Write": "🏗️ PRIORITY: Make it work, clean it up later",
        "Edit": "🔧 APPROACH: Quick fixes are fine",
        "Bash": "⚡ FOCUS: Test core functionality only",
        "DEFAULT": "🚀 Prototype mode - speed matters"
    },

    "--production": {
        "Write": "🛡️ REQUIREMENT: Include comprehensive error handling",
        "Edit": "🔒 CRITICAL: Maintain backward compatibility",
        "Bash": "✅ MANDATE: Full test coverage required",
        "Read": "📋 IMPORTANT: Consider all edge cases",
        "DEFAULT": "🏭 Production mode - safety critical"
    },

    "--safe-mode": {
        "Write": "⚠️ CAUTION: Create backup before changes",
        "Edit": "🔒 CAREFUL: Document rollback procedure",
        "Bash": "🛡️ VALIDATE: Check thoroughly before execution",
        "DEFAULT": "🔒 Safe mode - maximum caution"
    },

    # Problem-Solving Flags
    "--first-principles": {
        "Read": "🧠 APPROACH: Question assumptions, understand fundamentals first",
        "Task": "🔬 METHOD: Break down to basics before solving",
        "Write": "📐 THINK: Build from core concepts",
        "DEFAULT": "🎓 First principles thinking"
    },

    "--pattern-match": {
        "Grep": "🔎 OBJECTIVE: Find similar patterns we can adapt",
        "Read": "📋 LOOK FOR: Reusable patterns and solutions",
        "Write": "♻️ APPROACH: Adapt existing patterns",
        "DEFAULT": "🔄 Pattern matching mode"
    },

    "--divide-conquer": {
        "Task": "✂️ STRATEGY: Split into independent subproblems first",
        "Write": "🧩 METHOD: Implement one piece at a time",
        "Edit": "🔧 APPROACH: Fix components independently",
        "DEFAULT": "🧩 Divide and conquer"
    },

    "--hypothesis": {
        "Read": "🔬 FIRST: Form a theory about the behavior",
        "Bash": "🧪 THEN: Design experiment to test theory",
        "Edit": "📝 FINALLY: Adjust based on test results",
        "DEFAULT": "🔬 Hypothesis-driven approach"
    },

    # Code Modification Flags
    "--minimal": {
        "Edit": "✂️ CONSTRAINT: Change only what's absolutely necessary",
        "Write": "📌 LIMIT: Minimal code to fix the issue",
        "Read": "🎯 FIND: Precise problem location first",
        "DEFAULT": "🔧 Minimal changes only"
    },

    "--refactor": {
        "Edit": "♻️ RULE: Preserve exact functionality while cleaning",
        "Read": "👃 IDENTIFY: Code smells and improvements",
        "Bash": "✅ VERIFY: Behavior must remain unchanged",
        "DEFAULT": "♻️ Refactoring mode"
    },

    "--aggressive": {
        "Edit": "💪 PERMISSION: Rewrite entirely if it improves significantly",
        "Write": "🔥 ALLOWED: Replace whole modules if needed",
        "Read": "🏗️ LOOK FOR: Architectural improvements",
        "DEFAULT": "🚀 Aggressive restructuring allowed"
    },

    # Focus Mode Flags
    "--focused": {
        "Read": "🎯 DISCIPLINE: Only look at task-relevant code",
        "Edit": "⚡ RESIST: Don't fix unrelated issues you see",
        "Grep": "🔍 NARROW: Search within task scope only",
        "DEFAULT": "🎯 Stay focused on the specific task"
    },

    "--exploratory": {
        "Read": "🗺️ FREEDOM: Follow interesting paths",
        "Grep": "🌐 BROAD: Wide searches to understand system",
        "Task": "📊 GOAL: Map the system architecture",
        "DEFAULT": "🔭 Exploration mode"
    },

    "--debug": {
        "Read": "🔍 TRACE: Follow execution paths carefully",
        "Bash": "📝 ADD: Logging and inspection points",
        "Edit": "🐛 INSERT: Debug statements for visibility",
        "Grep": "🔗 FIND: All references and connections",
        "DEFAULT": "🐛 Debug mode - investigate thoroughly"
    },

    # Tool Enhancement Flags
    "--c7": {
        "Read": "📚 DOCS: Check Context7 for library documentation",
        "Write": "📖 VERIFY: Confirm API usage with Context7",
        "Edit": "📚 REFERENCE: Use Context7 for correct patterns",
        "DEFAULT": "📚 Context7 documentation enabled"
    },

    "--seq": {
        "Task": "🔢 SEQUENTIAL: Use structured multi-step reasoning",
        "Read": "📐 SYSTEMATIC: Analyze step by step",
        "DEFAULT": "🔢 Sequential thinking enabled"
    }
}

# Smart injection rules for PreToolUse
INJECTION_RULES = {
    "ALWAYS": ["Write", "Edit"],  # Critical operations - always remind
    "FREQUENT": ["Bash", "Task"],  # Every 2 calls
    "OCCASIONAL": ["Read", "Grep", "Glob"],  # Every 3 calls
    "PERIODIC_SAFETY": 8,  # Every 8 operations as safety net
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

def get_pre_injection_state_file_path(session_id):
    """Get path to pre-injection tracking state file"""
    return f"/tmp/claude-pre-injection-state-{session_id}.json"

def parse_transcript_for_flags(transcript_path):
    """Parse ENTIRE transcript for flags (fallback when no state file exists)"""
    flags = set()
    flag_metadata = {}

    try:
        if not transcript_path or not os.path.exists(transcript_path):
            logger.warning(f"Transcript not found: {transcript_path}")
            return flags, flag_metadata

        # Parse from beginning to find FIRST user message with flags
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    msg = json.loads(line.strip())

                    # Only process user messages
                    if msg.get('role') == 'user':
                        content = msg.get('content', '')

                        # Handle both string and array content
                        if isinstance(content, list):
                            text = ' '.join(
                                item.get('text', '') for item in content
                                if isinstance(item, dict)
                            )
                        else:
                            text = content

                        # Search for all flag patterns
                        for pattern, flag_name in FLAG_PATTERNS.items():
                            match = re.search(pattern, text)
                            if match:
                                flags.add(flag_name)

                                # Capture flag parameters if present
                                if match.groups():
                                    flag_metadata[flag_name] = match.group(1)

                        # If we found flags, we can stop
                        if flags:
                            logger.info(f"Parsed flags from transcript: {flags}")
                            break

                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    logger.warning(f"Error parsing line: {e}")
                    continue

    except Exception as e:
        logger.error(f"Error parsing transcript: {e}")

    return flags, flag_metadata

def save_session_state(state_file, flags, metadata, transcript_path, cwd, session_id):
    """Save session state (same format as flag-detector)"""
    try:
        state = {
            "session_id": session_id,
            "flags": list(flags),
            "flag_metadata": metadata,
            "detected_at": datetime.now().isoformat(),
            "transcript_path": transcript_path,
            "cwd": cwd
        }

        # Atomic write: temp file + rename
        temp_file = state_file + '.tmp'
        with open(temp_file, 'w') as f:
            json.dump(state, f, indent=2)
        os.rename(temp_file, state_file)

        logger.info(f"Saved session state with flags: {flags}")
        return True
    except Exception as e:
        logger.error(f"Failed to save state: {e}")
        return False

def load_active_flags(session_id, transcript_path=None, cwd=None):
    """Load active flags and metadata from session state or parse transcript"""
    try:
        state_file = get_state_file_path(session_id)

        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                state = json.load(f)
                flags = state.get('flags', [])
                metadata = state.get('flag_metadata', {})
                logger.debug(f"Loaded flags from state file: {flags}")
                return flags, metadata
        else:
            logger.debug("No state file found, parsing transcript")
            # Parse transcript as fallback
            if transcript_path:
                flags, metadata = parse_transcript_for_flags(transcript_path)
                if flags:
                    # Save for future calls
                    save_session_state(state_file, flags, metadata, transcript_path, cwd, session_id)
                return list(flags), metadata

    except Exception as e:
        logger.warning(f"Could not load flags: {e}")

    return [], {}

def load_injection_state(session_id):
    """Load pre-injection tracking state"""
    try:
        state_file = get_pre_injection_state_file_path(session_id)

        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "operation_count": 0,
                "tool_counts": {},
                "last_injection_time": 0,
                "last_injection_operation": 0
            }

    except Exception as e:
        logger.warning(f"Could not load injection state: {e}")
        return {
            "operation_count": 0,
            "tool_counts": {},
            "last_injection_time": 0,
            "last_injection_operation": 0
        }

def save_injection_state(session_id, state):
    """Save injection tracking state"""
    try:
        state_file = get_pre_injection_state_file_path(session_id)

        # Atomic write
        temp_file = state_file + '.tmp'
        with open(temp_file, 'w') as f:
            json.dump(state, f, indent=2)
        os.rename(temp_file, state_file)

        return True

    except Exception as e:
        logger.error(f"Could not save injection state: {e}")
        return False

def should_inject(tool_name, state, flags):
    """Determine if we should inject flag reminder BEFORE tool execution"""

    if not flags:
        return False

    operation_count = state["operation_count"]
    tool_count = state["tool_counts"].get(tool_name, 0)
    last_injection_time = state["last_injection_time"]

    # Always inject for critical tools (Write/Edit)
    if tool_name in INJECTION_RULES["ALWAYS"]:
        logger.info(f"Always injecting before {tool_name}")
        return True

    # Periodic safety net
    if operation_count > 0 and operation_count % INJECTION_RULES["PERIODIC_SAFETY"] == 0:
        logger.info(f"Periodic safety injection at operation {operation_count}")
        return True

    current_time = time.time()

    # Frequent tools - every 2 calls or 2 minutes
    if tool_name in INJECTION_RULES["FREQUENT"]:
        if tool_count % 2 == 0 or (current_time - last_injection_time) > 120:
            logger.info(f"Frequent injection before {tool_name}")
            return True

    # Occasional tools - every 3 calls or 3 minutes
    if tool_name in INJECTION_RULES["OCCASIONAL"]:
        if tool_count % 3 == 0 or (current_time - last_injection_time) > 180:
            logger.info(f"Occasional injection before {tool_name}")
            return True

    logger.debug(f"No injection before {tool_name} (op: {operation_count}, tool: {tool_count})")
    return False

def get_context_message(flag, tool_name, metadata):
    """Get PREVENTIVE context message for flag and tool"""

    # Handle flag parameters
    if flag in metadata and metadata[flag]:
        flag_display = f"{flag} {metadata[flag]}"
    else:
        flag_display = flag

    # Get preventive context for this flag
    contexts = FLAG_CONTEXTS.get(flag, {})

    # Try specific tool message
    if tool_name in contexts:
        message = contexts[tool_name]
    else:
        message = contexts.get("DEFAULT", f"Flag {flag_display} is active")

    return f"{flag_display}: {message}"

def format_preventive_reminder(flags, metadata, tool_name):
    """Format preventive reminder BEFORE tool execution"""

    if not flags:
        return None

    # Build preventive messages
    messages = []

    # Prioritize restrictive flags first
    priority_order = ["--ao", "--uo", "--safe-mode", "--production", "--minimal"]
    sorted_flags = sorted(flags, key=lambda f: priority_order.index(f"--{f}") if f"--{f}" in priority_order else 999)

    for flag in sorted_flags:
        flag_key = f"--{flag}" if not flag.startswith('--') else flag
        message = get_context_message(flag_key, tool_name, metadata)
        messages.append(message)

    # Format for LLM (clear guidance BEFORE action)
    if len(messages) == 1:
        llm_context = f"[BEFORE {tool_name}: {messages[0]}]"
    else:
        llm_context = f"[BEFORE {tool_name} - ACTIVE FLAGS:\n" + "\n".join(messages) + "]"

    # User sees minimal indicator
    flag_list = [f"--{f}" if not f.startswith('--') else f for f in flags]
    user_visible = f"🚦 Pre-check: {' '.join(flag_list)}"

    return llm_context, user_visible

def check_file_exists(file_path, cwd):
    """Safely check if file exists"""
    try:
        if not os.path.isabs(file_path):
            file_path = os.path.join(cwd, file_path)

        abs_path = os.path.abspath(file_path)

        # Security: prevent directory traversal
        if '..' in file_path:
            logger.warning(f"Potential directory traversal: {file_path}")
            return False

        return os.path.exists(abs_path)

    except Exception as e:
        logger.error(f"Error checking file: {e}")
        return False

def make_permission_decision(tool_name, file_path, flags, file_exists):
    """Make permission decision based on flags"""

    # Priority 1: --ao blocks EVERYTHING
    if 'ao' in flags:
        return ('deny',
                'File operation blocked by --ao flag (answer only mode). '
                'Claude should provide console output instead of creating files.')

    # Priority 2: Edit/NotebookEdit are always allowed (unless --ao)
    if tool_name in ['Edit', 'NotebookEdit']:
        return ('allow', f'{tool_name} operation allowed')

    # Priority 3: Write operations
    if tool_name == 'Write':
        # --new explicitly allows new files
        if 'new' in flags:
            return ('allow', 'New file creation allowed by --new flag')

        # --uo blocks new files
        if 'uo' in flags:
            if file_exists:
                return ('allow', 'Updating existing file in --uo mode')
            else:
                return ('deny',
                        f'New file creation blocked by --uo flag (update only mode). '
                        f'File does not exist: {os.path.basename(file_path)}. '
                        f'Use --new flag to allow new file creation.')

        # No flags: ask for new files, allow updates
        if file_exists:
            return ('allow', 'Updating existing file')
        else:
            return ('ask', f'Confirm creation of new file: {os.path.basename(file_path)}')

    # Default: allow
    return ('allow', 'Operation allowed')

def main():
    """Main hook entry point - provides context AND enforces permissions"""
    try:
        # Parse input
        input_data = json.load(sys.stdin)

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})
        cwd = input_data.get("cwd", os.getcwd())
        transcript_path = input_data.get("transcript_path", "")

        # Get stable session ID from Claude
        session_id = get_session_id_from_input(input_data)

        # Skip if not Write/Edit/Bash/Read/Grep/Task
        relevant_tools = ["Write", "Edit", "Bash", "Read", "Grep", "Glob", "Task", "NotebookEdit"]
        if tool_name not in relevant_tools:
            sys.exit(0)

        logger.debug(f"PreToolUse for {tool_name} in session {session_id}")

        # Load active flags (with transcript fallback)
        flags, metadata = load_active_flags(session_id, transcript_path, cwd)

        if not flags:
            sys.exit(0)

        # PERMISSION ENFORCEMENT for Write/Edit/NotebookEdit
        # This runs BEFORE context injection to hard-block operations
        if tool_name in ["Write", "Edit", "NotebookEdit"]:
            # Get file path (NotebookEdit uses notebook_path instead of file_path)
            if tool_name == "NotebookEdit":
                file_path = tool_input.get("notebook_path", "")
            else:
                file_path = tool_input.get("file_path", "")

            if file_path:
                # Check file existence
                file_exists = check_file_exists(file_path, cwd)

                # Make permission decision
                decision, reason = make_permission_decision(tool_name, file_path, flags, file_exists)

                logger.info(f"Permission check for {file_path}: {decision} - {reason}")

                # Handle decision
                if decision == 'deny':
                    # BLOCK operation with exit code 2
                    output = {
                        "hookSpecificOutput": {
                            "hookEventName": "PreToolUse",
                            "permissionDecision": "deny",
                            "permissionDecisionReason": reason
                        }
                    }
                    print(f"⚠️  {reason}", file=sys.stderr)
                    print(json.dumps(output))
                    logger.warning(f"BLOCKED: {reason}")
                    sys.exit(2)  # Exit code 2 blocks the operation

                elif decision == 'ask':
                    # Let Claude Code handle the user prompt
                    logger.info(f"Asking user: {reason}")
                    # Continue to context injection...

                # If 'allow', continue to context injection below

        # Load injection state
        state = load_injection_state(session_id)

        # Update counts
        state["operation_count"] += 1
        state["tool_counts"][tool_name] = state["tool_counts"].get(tool_name, 0) + 1

        # Check if we should inject
        if not should_inject(tool_name, state, flags):
            save_injection_state(session_id, state)
            logger.debug(f"Skipping pre-injection for {tool_name}")
            sys.exit(0)

        # Format preventive reminder
        reminder = format_preventive_reminder(flags, metadata, tool_name)

        if reminder:
            llm_context, user_visible = reminder

            # Update injection tracking
            state["last_injection_time"] = time.time()
            state["last_injection_operation"] = state["operation_count"]

            # Save updated state
            save_injection_state(session_id, state)

            # Output context for Claude BEFORE tool execution
            # According to Claude Code docs, stdout with exit code 0 provides context
            print(llm_context)
            logger.info(f"Injected preventive context before {tool_name}: {flags}")

        sys.exit(0)

    except Exception as e:
        logger.error(f"Hook error: {e}", exc_info=True)
        sys.exit(0)

if __name__ == "__main__":
    main()