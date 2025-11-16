
Context-aware flags for real development workflows. Default behavior: **fail-fast, in-place modification**.

## 🎯 Development Style Flags

**--fail-fast** (DEFAULT BEHAVIOR - no flag needed)
- **Purpose**: Rapid development with immediate error discovery
- **Behavior**:
  - Overwrite functions directly (no `_old` backups)
  - Run immediately and fix errors iteratively
  - Minimal defensive coding, trust version control
- **Context Messages**:
  - Write: "⚡ Overwrite directly, no backup needed"
  - Edit: "🔄 Replace functions completely, no _old versions"
  - Bash: "🏃 Run immediately, fix errors as they appear"
- **Philosophy**: Move fast, break things, fix quickly

**--prototype**
- **Purpose**: Quick and dirty implementation
- **Behavior**: Working code over clean code, skip edge cases
- **When to use**: Early development, proof of concept

**--production**
- **Purpose**: Production-ready code with all safety nets
- **Behavior**:
  - Create backup functions before changes
  - Comprehensive error handling
  - Full test coverage
- **When to use**: Deploying to production, critical systems

**--safe-mode**
- **Purpose**: Maximum validation and conservative execution
- **Behavior**: Extra safety checks, rollback instructions, defensive coding
- **When to use**: Working on critical code, unfamiliar systems

## 🧠 Problem-Solving Approach Flags

**--first-principles**
- **Purpose**: Break down to fundamentals and rebuild
- **Behavior**: Question assumptions, derive from core truths
- **Context Messages**:
  - Read: "🧠 Understand fundamental concepts, ignore implementation details"
  - Task: "🔬 Break down to basics, rebuild from core truths"
- **When to use**: Complex problems, unclear requirements

**--pattern-match**
- **Purpose**: Find and adapt similar solutions
- **Behavior**: Search for proven patterns, adapt existing solutions
- **Context Messages**:
  - Grep: "🔎 Search for similar patterns in codebase"
  - Read: "📋 Identify reusable patterns"
- **When to use**: Common problems, existing solutions available

**--divide-conquer**
- **Purpose**: Split complex problems into manageable pieces
- **Behavior**: Break into independent subproblems
- **Context Messages**:
  - Task: "✂️ Break into independent subproblems"
  - Write: "🧩 Implement one piece at a time"
- **When to use**: Large features, multi-component systems

**--hypothesis**
- **Purpose**: Scientific method for debugging
- **Behavior**: Form theory, test, adjust based on results
- **Context Messages**:
  - Read: "🔬 Form theory about behavior"
  - Bash: "🧪 Test hypothesis with experiments"
- **When to use**: Debugging unknown issues, exploring behavior

## ✏️ Code Modification Flags

**--minimal**
- **Purpose**: Smallest possible change
- **Behavior**: Change only what's broken, surgical fixes
- **When to use**: Hot fixes, production bugs

**--refactor**
- **Purpose**: Improve without changing behavior
- **Behavior**: Clean up code, preserve functionality
- **When to use**: Code cleanup, technical debt

**--aggressive**
- **Purpose**: Major restructuring allowed
- **Behavior**: Rewrite if it improves significantly
- **When to use**: Major refactoring, architecture changes

## 🎯 Focus Mode Flags

**--focused**
- **Purpose**: Stay on specific task only
- **Behavior**: Don't fix unrelated problems, narrow scope
- **When to use**: Time constraints, specific bugs

**--exploratory**
- **Purpose**: Understand the entire system
- **Behavior**: Follow interesting paths, map architecture
- **When to use**: New codebase, learning phase

**--debug**
- **Purpose**: Problem investigation mode
- **Behavior**: Add logging, trace execution, insert debug statements
- **When to use**: Investigating bugs, understanding flow

## 📁 File Control Flags

**--ao [minimal|brief|standard]**
- **Purpose**: Answer only, no file operations
- **Behavior**: Console output only, blocks ALL file operations
- **Output Levels**:
  - minimal: One word/line
  - brief: 1-3 sentences
  - standard: Normal answer, no preamble (default)
- **Context Messages**:
  - Write/Edit: "❌ BLOCKED - Answer only mode"
  - Read: "📖 Analyze for understanding only"
- **When to use**: Getting information, explanations

**--uo** (Update Only)
- **Purpose**: Modify existing files only, no new creation
- **Behavior**: Block new file creation, allow edits
- **Context Messages**:
  - Write: "❌ Cannot create new files. Use --new if needed"
  - Edit: "✏️ Modify existing code, preserve structure"
  - Read: "🔍 Focus on understanding current patterns"
  - Bash: "🧪 Test modifications to existing functionality"
- **When to use**: Bug fixes, refactoring existing code

**--new**
- **Purpose**: Explicitly allow new file creation
- **Behavior**: Create files without confirmation prompts
- **Context Messages**:
  - Write: "✅ Create necessary new files"
  - Edit: "🔨 Refactor may include new supporting files"
- **When to use**: Adding features, new modules

## 🔧 Tool Enhancement Flags

**--c7 / --context7**
- **Purpose**: Use official documentation
- **When injected**: Only when imports/libraries detected
- **Behavior**: Fetch up-to-date library docs

**--seq / --sequential**
- **Purpose**: Structured multi-step reasoning
- **When injected**: Only for complex problems
- **Behavior**: Systematic problem breakdown
