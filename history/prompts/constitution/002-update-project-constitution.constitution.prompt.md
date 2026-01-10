---
id: 2
title: Update Project Constitution
stage: constitution
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Claude
command: sp.constitution
labels: [constitution, governance, standards]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - constitution validation
---

## Prompt

```text
Core Principles
Spec-First Development

Every feature begins with a written specification
Specifications are living documents - update when requirements change
All specs must be versioned in git

Clean Code Always

Follow language-specific best practices (PEP 8, TypeScript style guides)
Separation of concerns at every layer
Type safety enforced (Python type hints, TypeScript strict mode)
Meaningful names that reveal intent
Self-documenting code with appropriate comments

Security by Default

User data strictly isolated - no cross-user access permitted
All secrets in environment variables (never hardcoded)
JWT tokens required on authenticated endpoints
JWT tokens must expire (7 days recommended)

Code Quality Standards
Type Safety

Python: Type hints on all functions and methods
TypeScript: Strict mode enabled, avoid any types

Error Handling

Never fail silently
Provide meaningful error messages
Use appropriate error types (HTTP status codes, exception classes)
Log errors with sufficient debugging context

Documentation

README.md must enable newcomers to run the project
CLAUDE.md provides AI development context at appropriate levels
API endpoints documented with request/response examples
Docstrings/JSDoc on all public APIs

Code Organization

Maximum function length: 50 lines (guideline)
Maximum file length: 300 lines (consider splitting beyond this)
Commit messages follow conventional commits format

Repository Structure Requirements
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
Security Standards
Authentication & Authorization

Return 401 Unauthorized for missing/invalid tokens
Return 403 Forbidden for insufficient permissions
Same shared secret (BETTER_AUTH_SECRET) across all services

Data Protection

Never expose sensitive data in error messages
SQL injection prevention through ORM (no raw SQL queries)
Tokens include minimum necessary claims (user_id, email)

Quality Gates
Before Phase Completion

 All functional requirements working
 Code follows quality standards
 Security measures implemented
 Documentation accurate and complete
 Application runs in clean environment

Platform Requirements
Windows Users: Must use WSL 2 (Ubuntu-22.04) for all development
Success Criteria
A phase is successful when:

All functional requirements work correctly
Code quality standards are met
Security measures are implemented
Deliverables are complete and usable

Evaluation Weights

Functional Completeness: 30%
Code Quality: 25%
Process Adherence: 25%
Documentation Quality: 20%
```

## Response snapshot

Updated the project constitution file (.specify/memory/constitution.md) to reflect the new core principles provided by the user. The updated constitution now includes:

1. Spec-First Development: Every feature begins with a written specification, specifications are living documents updated when requirements change, and all specs must be versioned in git.

2. Clean Code Always: Follow language-specific best practices, maintain separation of concerns, enforce type safety, use meaningful names, and write self-documenting code.

3. Security by Default: User data isolation, secrets in environment variables, JWT tokens on authenticated endpoints with 7-day expiry.

4. Code Quality Standards: Type safety requirements, error handling guidelines, documentation standards, and code organization rules.

5. Repository Structure Requirements: Defined standard project structure.

6. Security Standards: Authentication/authorization requirements and data protection measures.

7. Quality Gates: Requirements before phase completion.

8. Platform Requirements: WSL 2 requirement for Windows users.

9. Success Criteria: What defines a successful phase.

10. Evaluation Weights: How success is measured across different aspects.

The constitution version was updated from 2.0.0 to 3.0.0 to reflect the major changes in principles and structure.

## Outcome

- ✅ Impact: Updated project constitution with new core principles and governance structure
- 🧪 Tests: Constitution validation completed successfully
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: Ready for feature development following new constitution
- 🧠 Reflection: Constitution now provides clear governance framework for project development

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Constitution updated successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature development following new constitution principles