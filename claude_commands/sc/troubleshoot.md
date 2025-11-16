---
description: Diagnose and resolve issues in code, builds, and deployments
argument-hint: <issue> [--type bug|build|performance|deployment] [--trace] [--fix]
---

Troubleshoot the following issue: **$ARGUMENTS**

## Process

1. **Analyze** - Examine issue description and gather system state (logs, errors, stack traces)
2. **Investigate** - Identify potential root causes through systematic debugging
3. **Debug** - Structured investigation with evidence collection and hypothesis testing
4. **Propose** - Validate solution approaches and assess risks
5. **Resolve** - Apply fixes and verify resolution with testing

## Issue Types

Parse `--type` flag to focus troubleshooting approach:

### Bug
- Stack trace analysis and error interpretation
- Reproduce issue and identify conditions
- Root cause analysis with code examination
- Targeted fix with regression prevention

### Build
- Build log analysis and dependency resolution
- Configuration validation
- Compilation and bundling errors
- Safe fix application with verification

### Performance
- Profiling and bottleneck identification
- Query optimization and caching strategies
- Resource usage analysis (CPU, memory, I/O)
- Optimization guidance with benchmarking

### Deployment
- Environment analysis and configuration validation
- Dependency and service availability checks
- Container, network, and infrastructure issues
- Rollback strategies and safe deployment

## Troubleshooting Flags

Parse additional flags:
- `--trace`: Enable detailed execution tracing and step-by-step debugging
- `--fix`: After diagnosis, apply safe fixes automatically (with user confirmation for risky changes)

## Debugging Methodology

1. Reproduce the issue reliably
2. Form hypotheses about root cause
3. Test hypotheses systematically
4. Isolate the failing component
5. Verify fix resolves issue without side effects
