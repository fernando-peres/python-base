# Consulting and Maintaining Specifications

Use this skill before implementing or modifying features. Specifications are the single source of truth; check specs before implementation and update them when code or requirements change.

## Before Implementation

1. **Look for an existing spec** in `docs/specs/` (or project-equivalent): search by feature name or related keywords.
2. **If a spec exists**: Read it; review business and technical requirements, data models, flows, constraints, and edge cases.
3. **If no spec exists**: Create one first (e.g. from `docs/specs/TEMPLATE.md` or project template); document requirements, then implement.
4. **Check ADRs**: Review relevant Architecture Decision Records in `docs/adr/` for decisions and constraints.

## During Implementation

1. **Implement according to the spec**: Use the specified DTOs and data models; follow documented flows and constraints.
2. **Reference the spec in code**: Add a short comment pointing to the spec (e.g. `# See docs/specs/thumbnail-generation-spec.md`).
3. **If you must deviate**: Update the spec with the change and reason; add a changelog entry so the spec stays accurate.

## After Implementation

1. **Keep the spec in sync**: If implementation details differ from the spec, update the spec and document deviations in the changelog.
2. **Commit messages**: Include a reference to the spec when relevant (e.g. "Implements X as specified in docs/specs/x-spec.md").

## Locations (adjust to project)

- **Feature specs**: `docs/specs/` — e.g. `feature-name-spec.md`; template: `docs/specs/TEMPLATE.md`
- **ADRs**: `docs/adr/` — e.g. `NNNN-decision-name.md`
- **Architecture docs**: `docs/architecture/` — e.g. overview, messaging, use-cases

## DO

- Check for existing specs before implementing features
- Read and understand specs before coding
- Create specs for new features before implementation
- Follow specifications during implementation
- Update specs when code or requirements change
- Reference specs in code comments and commit messages
- Review related ADRs for context

## DON'T

- Implement features without checking for specs
- Ignore existing specifications
- Deviate from specs without updating them
- Forget to update specs when requirements change

## Checklist

Before implementing or modifying features:

- [ ] Checked for existing spec in `docs/specs/`
- [ ] Read and understood the specification
- [ ] Checked related ADRs in `docs/adr/`
- [ ] Created spec if it doesn't exist
- [ ] Implemented according to spec
- [ ] Added spec reference in code comments
- [ ] Updated spec if implementation deviates
- [ ] Included spec reference in commit message where relevant
