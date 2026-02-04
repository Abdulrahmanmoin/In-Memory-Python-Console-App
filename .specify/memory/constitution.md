<!--
SYNC IMPACT REPORT:
Version change: 3.0.0 → 3.1.0
Modified principles: None (existing principles retained)
Added sections:
  - Principle #4: Infrastructure as Code
  - Container Standards (Image Requirements, Local Validation)
  - Orchestration Standards (Deployment Requirements, Health & Monitoring, Networking)
  - AI-Assisted Operations Standards (Usage Guidelines, Documentation Requirement)
  - Container & Deployment Security (subsection under Security Standards)
  - Before Container Deployment (subsection under Quality Gates)
  - Before Orchestrated Deployment (subsection under Quality Gates)
  - Container & Orchestration Development (subsection under Platform Requirements)
  - Containerized Deployment Success Criteria (added to Success Criteria)
  - Enhanced Documentation subsection with deployment and AI tools requirements
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending (verify Container/Orchestration standards alignment)
  - .specify/templates/spec-template.md: ⚠ pending (verify deployment requirements sections)
  - .specify/templates/tasks-template.md: ⚠ pending (add container/orchestration task types)
  - .specify/templates/commands/*.md: ⚠ pending (verify no outdated references)
Follow-up TODOs: None
-->
# Project Constitution

## Project Identity

**Name**: Generic Software Project
**Type**: Software development project
**Constitution Version**: 3.1.0
**Methodology**: Spec-Driven Development with Clean Code Practices

## Core Principles

### 1. Spec-First Development
Every feature begins with a written specification. Specifications are living documents - update when requirements change. All specs must be versioned in git. No implementation without approved specification.

### 2. Clean Code Always
Follow language-specific best practices (PEP 8, TypeScript style guides). Maintain separation of concerns at every layer. Enforce type safety (Python type hints, TypeScript strict mode). Use meaningful names that reveal intent. Write self-documenting code with appropriate comments.

### 3. Security by Default
User data strictly isolated - no cross-user access permitted. All secrets in environment variables (never hardcoded). JWT tokens required on authenticated endpoints. JWT tokens must expire (7 days recommended).

### 4. Infrastructure as Code
All infrastructure configurations must be version controlled. Deployments must be reproducible from code alone. No manual environment modifications without corresponding code changes. Maintain environment parity between local and production.

## Code Quality Standards

### Type Safety
- Python: Type hints on all functions and methods
- TypeScript: Strict mode enabled, avoid any types

### Error Handling
- Never fail silently
- Provide meaningful error messages
- Use appropriate error types (HTTP status codes, exception classes)
- Log errors with sufficient debugging context

### Documentation
- README.md must enable newcomers to run the project
- CLAUDE.md provides AI development context at appropriate levels
- API endpoints documented with request/response examples
- Docstrings/JSDoc on all public APIs
- Deployment documentation required for containerized applications
- AI tools usage must be documented when used for infrastructure operations

### Code Organization
- Maximum function length: 50 lines (guideline)
- Maximum file length: 300 lines (consider splitting beyond this)
- Commit messages follow conventional commits format

## Repository Structure Requirements

```
project-root/
├── .spec-kit/config.yaml
├── specs/
│   ├── overview.md
│   ├── features/
│   ├── api/
│   ├── database/
│   └── ui/
├── CLAUDE.md (root)
├── README.md
└── [phase-specific folders with their own CLAUDE.md]
```

## Container Standards

### Image Requirements
- Use multi-stage builds to minimize image size
- Run containers as non-root user
- Include health check instructions
- Pin base image versions (avoid `latest` tag)
- No secrets baked into images

### Local Validation
- Multi-container local testing required before orchestrated deployment
- All containers must pass integration tests locally

## Orchestration Standards

### Deployment Requirements
- All deployments managed via package managers (Helm or equivalent)
- Configuration must be parameterized for different environments
- Minimum 2 replicas for production workloads
- Resource limits and requests defined for all containers

### Health & Monitoring
- Liveness and readiness probes required for all deployments
- Meaningful health check endpoints exposed

### Networking
- Internal services use cluster-internal communication
- External access through controlled ingress points
- Service discovery via DNS (no hardcoded IPs)

## AI-Assisted Operations Standards

### Usage Guidelines
- Document all AI tool commands used for infrastructure operations
- Verify AI-generated configurations before applying
- Review AI suggestions against security standards
- Maintain fallback procedures when AI tools unavailable

### Documentation Requirement
- Maintain log of AI-assisted operations for team knowledge sharing
- Record both successful commands and manual fallbacks

## Security Standards

### Authentication & Authorization
- Return 401 Unauthorized for missing/invalid tokens
- Return 403 Forbidden for insufficient permissions
- Same shared secret (BETTER_AUTH_SECRET) across all services

### Data Protection
- Never expose sensitive data in error messages
- SQL injection prevention through ORM (no raw SQL queries)
- Tokens include minimum necessary claims (user_id, email)

### Container & Deployment Security
- No root containers in production environments
- Secrets managed through environment variables or secret management tools
- Network isolation between components where applicable
- Configuration and secrets separated from application code

## Quality Gates

### Before Phase Completion
- All functional requirements working
- Code follows quality standards
- Security measures implemented
- Documentation accurate and complete
- Application runs in clean environment

### Before Container Deployment
- Dockerfiles follow container standards
- Images build successfully
- Local integration tests pass
- Security scan completed (when tooling available)

### Before Orchestrated Deployment
- Package manager validation passes (e.g., helm lint)
- Health probes configured
- Resource limits defined
- Application accessible and functional in target environment

## Platform Requirements

Windows Users: Must use WSL 2 (Ubuntu-22.04) for all development

### Container & Orchestration Development
- Container runtime required (Docker Desktop or equivalent)
- Local orchestration tool for development (Minikube or equivalent)
- Sufficient system resources allocated for local clusters

## Success Criteria

A phase is successful when:
- All functional requirements work correctly
- Code quality standards are met
- Security measures are implemented
- Deliverables are complete and usable

### Containerized Deployment Success Criteria
- All containers running and healthy
- Deployments show desired state achieved
- Application accessible via defined endpoints
- End-to-end functionality verified in deployed environment
- Reproducible deployment from version-controlled code

## Evaluation Weights

- Functional Completeness: 30%
- Code Quality: 25%
- Process Adherence: 25%
- Documentation Quality: 20%

## Constitution Governance

### Updates
- Constitution updated when requirements or standards change
- Version number incremented on changes following semantic versioning
- Changes documented in git commit
- Team review for major changes

### Enforcement
- This constitution governs ALL development activities
- Claude Code must reference constitution when making decisions
- Human reviewers evaluate against constitution criteria
- Violations block phase progression

---

**RATIFICATION_DATE**: 2025-12-30
**LAST_AMENDED_DATE**: 2026-01-25
**Applies To**: All development activities
**Authority**: Project Constitution - Final
**Compliance**: Mandatory for project success