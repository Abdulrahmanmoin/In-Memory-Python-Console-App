<!--
SYNC IMPACT REPORT:
Version change: 2.0.0 → 3.0.0
Modified principles: Spec-Driven Development First → Spec-First Development, Agentic Development Workflow → Clean Code Always, Progressive Complexity → Security by Default, Technology Stack Adherence → Code Quality Standards, Repository Structure → Repository Structure Requirements, Quality and Security First → Security Standards, Quality Gates → Quality Gates, Platform-Specific Requirements → Platform Requirements, Success Criteria by Phase → Success Criteria, Review Criteria → Evaluation Weights
Added sections: Type Safety, Error Handling, Documentation, Code Organization, Authentication & Authorization, Data Protection, Before Phase Completion requirements
Removed sections: Technology Stack Standards, API Design Standards, Database Standards, Performance Requirements, Spec-Kit Plus Integration, Prohibited Practices, Development Workflow
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending
  - .specify/templates/spec-template.md: ⚠ pending
  - .specify/templates/tasks-template.md: ⚠ pending
  - .specify/templates/commands/*.md: ⚠ pending
Follow-up TODOs: None
-->
# Project Constitution

## Project Identity

**Name**: Generic Software Project
**Type**: Software development project
**Constitution Version**: 3.0.0
**Methodology**: Spec-Driven Development with Clean Code Practices

## Core Principles

### 1. Spec-First Development
Every feature begins with a written specification. Specifications are living documents - update when requirements change. All specs must be versioned in git. No implementation without approved specification.

### 2. Clean Code Always
Follow language-specific best practices (PEP 8, TypeScript style guides). Maintain separation of concerns at every layer. Enforce type safety (Python type hints, TypeScript strict mode). Use meaningful names that reveal intent. Write self-documenting code with appropriate comments.

### 3. Security by Default
User data strictly isolated - no cross-user access permitted. All secrets in environment variables (never hardcoded). JWT tokens required on authenticated endpoints. JWT tokens must expire (7 days recommended).

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

## Security Standards

### Authentication & Authorization
- Return 401 Unauthorized for missing/invalid tokens
- Return 403 Forbidden for insufficient permissions
- Same shared secret (BETTER_AUTH_SECRET) across all services

### Data Protection
- Never expose sensitive data in error messages
- SQL injection prevention through ORM (no raw SQL queries)
- Tokens include minimum necessary claims (user_id, email)

## Quality Gates

### Before Phase Completion
- All functional requirements working
- Code follows quality standards
- Security measures implemented
- Documentation accurate and complete
- Application runs in clean environment

## Platform Requirements

Windows Users: Must use WSL 2 (Ubuntu-22.04) for all development

## Success Criteria

A phase is successful when:
- All functional requirements work correctly
- Code quality standards are met
- Security measures are implemented
- Deliverables are complete and usable

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
**LAST_AMENDED_DATE**: 2025-12-30
**Applies To**: All development activities
**Authority**: Project Constitution - Final
**Compliance**: Mandatory for project success