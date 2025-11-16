---
description: Code analysis across quality, security, performance, and architecture
argument-hint: "[target] [--focus quality|security|performance|architecture] [--depth quick|deep]"
---

Analyze the following target: **$ARGUMENTS**

If no target specified, analyze current working directory.

## Process

1. **Discover** - Identify and categorize source files, detect languages and frameworks
2. **Scan** - Apply domain-specific analysis patterns based on focus area
3. **Evaluate** - Generate prioritized findings with severity ratings (critical/high/medium/low)
4. **Recommend** - Provide actionable improvements with implementation guidance
5. **Report** - Present findings with code locations, examples, and remediation steps

## Focus Areas

Parse `--focus` flag to target specific domain (default: all domains):

### Quality
- Code smells and anti-patterns
- Maintainability issues
- Duplication and complexity
- Test coverage and quality

### Security
- Vulnerability scanning (injection, XSS, CSRF, etc.)
- Authentication and authorization flaws
- Sensitive data exposure
- Dependency vulnerabilities

### Performance
- Bottleneck identification
- Inefficient algorithms and queries
- Memory leaks and resource usage
- Optimization opportunities

### Architecture
- Structural issues and violations
- Dependency analysis
- Design pattern adherence
- Component coupling and cohesion

## Analysis Depth

Parse `--depth` flag:
- `quick`: Fast scan with high-confidence issues only (~5 min analysis)
- `deep`: Comprehensive analysis using Sequential MCP for complex reasoning (~15-30 min)

## Severity Ratings

- **Critical**: Must fix immediately (security vulnerabilities, data loss risks)
- **High**: Fix soon (major bugs, significant performance issues)
- **Medium**: Should fix (code quality, maintainability)
- **Low**: Nice to have (minor optimizations, style issues)
