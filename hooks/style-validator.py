#!/usr/bin/env python3
"""
Code Style Validator Hook

Validates and auto-fixes code style violations before Write/Edit operations.
Provides feedback to Claude about what was fixed.

Installation:
  1. Save to: ~/.claude/hooks/style-validator.py
  2. chmod +x ~/.claude/hooks/style-validator.py
  3. Add to hooks.json (see Configuration section)
"""

import json
import sys
import re
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    filename='/tmp/claude-style-validator.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('style-validator')

# Configuration
CODE_EXTENSIONS = ('.py', '.js', '.ts', '.tsx', '.java', '.go', '.rs', '.cpp', '.c', '.h')
MAX_LINE_LENGTH = 120
INDENT_SIZE = 4  # Spaces per indent level


def remove_emoji(text):
    """Remove all emoji characters from text"""
    # Unicode emoji ranges
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)


def strip_trailing_whitespace(text):
    """Remove trailing whitespace from all lines"""
    lines = text.split('\n')
    return '\n'.join(line.rstrip() for line in lines)


def replace_tabs_with_spaces(text, spaces=4):
    """Replace tabs with spaces"""
    return text.replace('\t', ' ' * spaces)


def validate_line_lengths(text, max_length=120):
    """Check for lines exceeding max length (warning only)"""
    long_lines = []
    for i, line in enumerate(text.split('\n'), 1):
        if len(line) > max_length:
            long_lines.append((i, len(line)))
    return long_lines


def detect_and_fix_non_ascii(text):
    """
    Detect and fix common non-ASCII UTF-8 characters in code

    Returns:
        tuple: (fixed_text, found_chars_info, remaining_non_ascii)
    """
    # Common problematic UTF-8 characters and their ASCII replacements
    replacements = {
        # Smart quotes
        '\u201c': '"',  # Left double quotation mark
        '\u201d': '"',  # Right double quotation mark
        '\u2018': "'",  # Left single quotation mark
        '\u2019': "'",  # Right single quotation mark
        '\u0060': "'",  # Grave accent (backtick used as quote)

        # Dashes
        '\u2013': '-',  # En dash
        '\u2014': '-',  # Em dash
        '\u2212': '-',  # Minus sign

        # Spaces
        '\u00a0': ' ',  # Non-breaking space
        '\u2003': ' ',  # Em space
        '\u2002': ' ',  # En space

        # Ellipsis
        '\u2026': '...',  # Horizontal ellipsis

        # Other common symbols
        '\u00d7': '*',  # Multiplication sign
        '\u00f7': '/',  # Division sign
        '\u2260': '!=', # Not equal to
        '\u2264': '<=', # Less than or equal to
        '\u2265': '>=', # Greater than or equal to
    }

    found_chars = {}
    fixed_text = text

    # Apply replacements
    for utf8_char, ascii_char in replacements.items():
        if utf8_char in fixed_text:
            count = fixed_text.count(utf8_char)
            char_name = f"U+{ord(utf8_char):04X}"
            found_chars[char_name] = (utf8_char, ascii_char, count)
            fixed_text = fixed_text.replace(utf8_char, ascii_char)

    # Detect remaining non-ASCII characters (not auto-fixable)
    remaining_non_ascii = []
    for i, char in enumerate(fixed_text):
        if ord(char) > 127 and char not in ['\n', '\r', '\t']:
            # Get line number for better reporting
            line_num = fixed_text[:i].count('\n') + 1
            char_info = f"U+{ord(char):04X} ('{char}') at line {line_num}"
            if char_info not in remaining_non_ascii:
                remaining_non_ascii.append(char_info)

    return fixed_text, found_chars, remaining_non_ascii


def validate_and_fix(content, file_path):
    """
    Validate and auto-fix style violations

    Args:
        content: File content to validate
        file_path: Path to file being written

    Returns:
        tuple: (fixed_content, violations, was_modified)
    """
    original_content = content
    violations = []

    # Only process code files
    if not file_path.endswith(CODE_EXTENSIONS):
        return content, violations, False

    # Rule 0: Detect and fix non-ASCII UTF-8 characters
    fixed_utf8, found_chars, remaining_non_ascii = detect_and_fix_non_ascii(content)
    if found_chars:
        # Report what was auto-fixed
        fixes = [f"{info[0]}→{info[1]} ({info[2]}x)" for info in found_chars.values()]
        content = fixed_utf8
        violations.append(f"Fixed UTF-8 chars: {', '.join(fixes[:3])}")
        logger.info(f"Fixed UTF-8 characters in {file_path}: {found_chars}")

    if remaining_non_ascii:
        # Warn about non-fixable UTF-8 characters
        count = len(remaining_non_ascii)
        violations.append(f"Warning: {count} non-ASCII chars remain: {remaining_non_ascii[:3]}")
        logger.warning(f"{file_path} has non-ASCII characters: {remaining_non_ascii}")

    # Rule 1: Remove emoji
    if re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF]', content):
        content = remove_emoji(content)
        violations.append("Removed emoji from code")
        logger.info(f"Removed emoji from {file_path}")

    # Rule 2: Strip trailing whitespace
    stripped = strip_trailing_whitespace(content)
    if stripped != content:
        content = stripped
        violations.append("Removed trailing whitespace")
        logger.info(f"Stripped trailing whitespace from {file_path}")

    # Rule 3: Replace tabs with spaces
    no_tabs = replace_tabs_with_spaces(content, INDENT_SIZE)
    if no_tabs != content:
        content = no_tabs
        violations.append(f"Replaced tabs with {INDENT_SIZE} spaces")
        logger.info(f"Replaced tabs in {file_path}")

    # Rule 4: Check line lengths (warning only, no fix)
    long_lines = validate_line_lengths(content, MAX_LINE_LENGTH)
    if long_lines:
        count = len(long_lines)
        violations.append(f"Warning: {count} lines exceed {MAX_LINE_LENGTH} chars")
        logger.warning(f"{file_path} has {count} long lines: {long_lines[:3]}")

    was_modified = (content != original_content)

    return content, violations, was_modified


def main():
    """Main hook entry point"""
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        logger.debug(f"Hook triggered: {input_data.get('hook_event_name')}")

        # Extract relevant fields
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # Only process Write/Edit tools
        if tool_name not in ["Write", "Edit"]:
            logger.debug(f"Skipping tool: {tool_name}")
            sys.exit(0)

        # Get file path and content
        file_path = tool_input.get("file_path", "")
        content = tool_input.get("content") or tool_input.get("new_string", "")

        if not content or not file_path:
            logger.warning("No content or file_path in tool_input")
            sys.exit(0)

        logger.info(f"Validating {file_path} ({len(content)} bytes)")

        # Validate and fix
        fixed_content, violations, was_modified = validate_and_fix(content, file_path)

        if was_modified:
            # Return modified content
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "updatedInput": {
                        "content": fixed_content,      # For Write tool
                        "new_string": fixed_content    # For Edit tool
                    }
                }
            }

            # Provide feedback to Claude
            feedback = f"✓ Auto-fixed: {', '.join(violations)}"
            print(feedback, file=sys.stderr)
            logger.info(f"Fixed {file_path}: {violations}")

            # Output JSON to stdout
            print(json.dumps(output))
            sys.exit(0)

        # If only warnings (no modifications)
        if violations:
            feedback = f"⚠️  {', '.join(violations)}"
            print(feedback, file=sys.stderr)
            logger.warning(f"Warnings for {file_path}: {violations}")

        # Allow operation (no modifications needed)
        sys.exit(0)

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON input: {e}")
        print(f"⚠️  Hook error: Invalid input", file=sys.stderr)
        sys.exit(0)  # Don't block on error

    except Exception as e:
        logger.error(f"Hook error: {e}", exc_info=True)
        print(f"⚠️  Hook error (allowing anyway): {e}", file=sys.stderr)
        sys.exit(0)  # Don't block on error


if __name__ == "__main__":
    main()
