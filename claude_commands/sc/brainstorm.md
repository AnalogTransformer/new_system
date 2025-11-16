---
description: Interactive requirements discovery through Socratic dialogue
argument-hint: <topic/idea> [--strategy systematic|agile] [--depth shallow|normal|deep]
allowed-tools: mcp__qdrant-loader__*, mcp__sequential-thinking__*, mcp__Context7__*, TodoWrite(*), Read(*), AskUserQuestion(*)
---

Perform requirements discovery on the following topic: **$ARGUMENTS**
USE -> AskUserQuestion(*) tool with any interaction with user
## Methodology

Apply Socratic dialogue to transform vague ideas into concrete specifications:

1. **Explore** - Ask probing questions to understand the concept, context, and goals
2. **Analyze** - Apply domain expertise and assess technical feasibility
3. **Validate** - Verify requirements are complete, realistic, and well-scoped
4. **Specify** - Generate concrete, actionable specifications with clear acceptance criteria
5. **Handoff** - Create implementation brief with architecture recommendations

## Strategy Handling

Parse flags from arguments:
- `--strategy systematic`: Structured, comprehensive exploration with deep analysis
- `--strategy agile`: Quick iterative discovery, focus on MVP and iteration
- `--depth shallow`: High-level requirements only
- `--depth normal`: Standard depth with key details (default)
- `--depth deep`: Comprehensive analysis using Sequential MCP for complex reasoning

## MCP Integration

- **Sequential MCP**: Use for complex multi-component analysis or when `--depth deep` specified
- **Context7 MCP**: Query for framework-specific feasibility, patterns, and best practices

## Output Format

Deliver structured requirement specification:
- **Intent**: What problem this solves and why it matters
- **Requirements**: Functional and non-functional requirements
- **Constraints**: Technical, resource, and timeline constraints
- **Architecture**: High-level approach and technology recommendations
- **Next Steps**: Prioritized implementation phases
