---
description: Clear explanations of code, concepts, and system behavior
argument-hint: <target> [--level basic|intermediate|advanced] [--format text|examples|interactive]
---

Explain the following: **$ARGUMENTS**

## Process

1. **Analyze** - Examine target to understand structure, purpose, and context
2. **Assess** - Determine appropriate explanation depth based on complexity and level flag
3. **Structure** - Plan logical explanation flow from fundamentals to details
4. **Generate** - Create clear explanations with examples and analogies
5. **Validate** - Verify accuracy, completeness, and clarity

## Explanation Levels

Parse `--level` flag to adjust explanation depth:
- `basic`: Fundamental concepts, simple analogies, minimal jargon
- `intermediate`: Technical details, practical examples, some assumptions of background knowledge (default)
- `advanced`: Deep technical dive, implementation details, edge cases, performance implications

## Output Formats

Parse `--format` flag for delivery style:
- `text`: Clear prose explanation with structured sections
- `examples`: Code examples with inline annotations and progressive complexity
- `interactive`: Q&A style with anticipating follow-up questions

## MCP Integration

- **Sequential MCP**: Use for complex multi-component breakdown or system-level explanations
- **Context7 MCP**: Query official documentation for framework-specific concepts and patterns

## Explanation Structure

Organize explanations to build understanding progressively:
1. **What**: High-level purpose and overview
2. **Why**: Motivation, problem solved, design decisions
3. **How**: Implementation details, mechanics, step-by-step operation
4. **When**: Appropriate use cases, when to apply or avoid
5. **Examples**: Practical demonstrations with clear context
