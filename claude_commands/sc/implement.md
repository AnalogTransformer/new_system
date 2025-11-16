---
description: Feature implementation with planning, coding, testing, and integration
argument-hint: <feature-description> [--type component|api|service|feature] [--framework react|vue|express|etc] [--with-tests]
---

Implement the following feature: **$ARGUMENTS**

## Process

1. **Analyze** - Examine requirements and understand technology context
2. **Plan** - Choose implementation approach based on type and constraints
3. **Generate** - Create code following framework-specific best practices
4. **Validate** - Apply quality checks, security review, and performance assessment
5. **Integrate** - Update documentation, add tests, ensure compatibility

## Implementation Types

Parse `--type` flag to determine scope and approach:
- `component`: UI component with props, state, styling, and events
- `api`: API endpoint with request validation, business logic, and response formatting
- `service`: Service module with data access, business rules, and error handling
- `feature`: Full feature spanning multiple components/services with complete integration

## Framework Handling

Parse `--framework` flag for framework-specific patterns:
- Framework patterns (hooks, composition, middleware, etc.)
- State management conventions
- Routing and navigation patterns
- Testing approaches specific to framework
- Build and deployment considerations

Use **Context7 MCP** to query official framework documentation for current best practices and patterns.

## Testing Integration

If `--with-tests` flag present:
- Generate unit tests for business logic
- Add integration tests for API endpoints
- Include component tests for UI elements
- Provide test data and fixtures
- Ensure test coverage meets quality standards

## Code Quality Standards

All implementations must follow:
- **SOLID principles**: Clean, maintainable architecture
- **Error handling**: Comprehensive error cases with clear messages
- **Type safety**: Strong typing where applicable (TypeScript, etc.)
- **Security**: Input validation, sanitization, authentication/authorization
- **Performance**: Efficient algorithms, appropriate caching, lazy loading
- **Documentation**: Clear inline comments, JSDoc/docstrings, README updates

## MCP Integration

- **Context7 MCP**: Framework documentation and patterns
- **Sequential MCP**: Use for complex multi-component features requiring systematic planning

## Output

Deliver complete implementation:
1. Production-ready code with no placeholders or TODOs
2. Tests if `--with-tests` specified
3. Documentation updates
4. Integration instructions
5. Any migration or deployment notes
