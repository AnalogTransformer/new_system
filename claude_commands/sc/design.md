---
description: Design system architecture, APIs, and component interfaces
argument-hint: <target> [--type architecture|api|component|database] [--format diagram|spec|code]
---

Design the following system component: **$ARGUMENTS**

## Process

1. **Analyze** - Examine requirements and system context
2. **Plan** - Define design approach and structure based on type
3. **Design** - Create specifications following best practices and design patterns
4. **Validate** - Ensure maintainability, scalability, and alignment with system architecture
5. **Document** - Generate clear design documentation in requested format

## Design Types

Parse `--type` flag to determine design approach:
- `architecture`: System architecture with component relationships, data flow, and integration points
- `api`: RESTful/GraphQL API specification with endpoints, request/response schemas, authentication
- `component`: Component interfaces with contracts, dependencies, and interaction patterns
- `database`: Entity relationships, schema design, normalization, and indexing strategy

## Output Formats

Parse `--format` flag for output style:
- `diagram`: Mermaid diagrams or structured visual representation
- `spec`: Detailed specification document with technical details
- `code`: Code scaffolding with interfaces, types, and structure

## Design Principles

Apply these principles to all designs:
- **SOLID**: Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion
- **Modularity**: Clear boundaries and separation of concerns
- **Scalability**: Design for growth and changing requirements
- **Maintainability**: Clear structure, documented decisions, refactoring-friendly
