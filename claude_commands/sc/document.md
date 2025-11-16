---
description: Generate documentation for components, APIs, and features
argument-hint: <target> [--type inline|external|api|guide] [--style brief|detailed]
---

Document the following target: **$ARGUMENTS**

## Process

1. **Analyze** - Examine target structure, functionality, and intended audience
2. **Identify** - Determine documentation requirements and level of detail
3. **Generate** - Create documentation following type-specific conventions
4. **Format** - Apply consistent structure and formatting standards
5. **Integrate** - Ensure compatibility with existing documentation ecosystem

## Documentation Types

Parse `--type` flag to determine format and approach:

### Inline Documentation
- JSDoc comments for JavaScript/TypeScript
- Docstrings for Python
- XML comments for C#/Java
- Include parameters, return values, exceptions, and usage examples

### External Documentation
- README files for modules/packages
- Architecture decision records (ADRs)
- Component library documentation
- Technical specifications

### API Documentation
- Endpoint descriptions with HTTP methods
- Request/response schemas and examples
- Authentication and authorization requirements
- Error codes and handling
- Rate limiting and pagination

### User Guides
- Step-by-step tutorials
- Use case scenarios
- Troubleshooting sections
- Best practices and gotchas

## Documentation Style

Parse `--style` flag for detail level:
- `brief`: Concise documentation covering essentials only
- `detailed`: Comprehensive documentation with examples, edge cases, and context (default)

## Language-Specific Conventions

Apply conventions based on detected language:
- **JavaScript/TypeScript**: JSDoc format
- **Python**: NumPy/Google docstring style
- **Java**: Javadoc
- **C#**: XML documentation comments
- **Go**: Godoc comments
- **Rust**: Rustdoc markdown

## Output Quality

Ensure documentation is:
- **Accurate**: Reflects actual code behavior
- **Complete**: Covers all public APIs and key functionality
- **Clear**: Written for target audience (developers, users, or both)
- **Maintainable**: Easy to keep synchronized with code changes
- **Discoverable**: Properly indexed and linked
