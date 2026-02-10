# Documentation Hub

Welcome to the AI Predictions project documentation. This directory contains all specifications, architecture decisions, and technical documentation for the project.

## Documentation Structure

```
docs/
├── README.md             # This file - documentation index
├── templates/            # Documentation templates
│   ├── adr-template.md   # ADR template
│   └── specs-template.md # Spec template
├── specs/                # Feature specifications
│   └── README.md         # How to write specs
├── adr/                  # Architecture Decision Records
│   ├── README.md         # ADR process guide
│   └── 0000-use-adr.md   # Meta-ADR explaining ADRs
├── architecture/         # System architecture documentation
│   ├── README.md         # Architecture overview
│   ├── overview.md       # High-level system design
│   ├── messaging.md      # RabbitMQ patterns
│   └── use-cases.md      # Use case patterns
└── diagrams/             # Visual diagrams
    └── README.md         # Diagram guidelines
```

## Documentation Types

### 📋 Specifications (`specs/`)

Feature specifications document both business requirements and technical implementation details for each feature.

**When to use:**
- Before implementing a new feature
- When documenting existing features
- When requirements change

**See:** [`specs/README.md`](specs/README.md) for guidelines and [`templates/specs-template.md`](templates/specs-template.md) for the template.

### 🏗️ Architecture Decision Records (`adr/`)

ADRs document important architectural decisions, explaining the context, decision, and consequences.

**When to use:**
- Making significant technical choices (technology, patterns, approaches)
- Explaining why certain decisions were made
- Documenting trade-offs and alternatives considered

**See:** [`adr/README.md`](adr/README.md) for the ADR process and [`templates/adr-template.md`](templates/adr-template.md) for the template.

### 🏛️ Architecture Documentation (`architecture/`)

High-level system architecture, component interactions, and architectural patterns.

**When to use:**
- Understanding the overall system design
- Learning about messaging patterns
- Understanding use case architecture

**See:** [`architecture/README.md`](architecture/README.md) for overview.

### 📊 Diagrams (`diagrams/`)

Visual representations of system components, flows, and relationships.

**When to use:**
- Creating visual documentation
- Explaining complex flows
- System design documentation

**See:** [`diagrams/README.md`](diagrams/README.md) for guidelines.

## Workflow

### Before Implementing a Feature

1. **Check if a spec exists** in `specs/`
2. **If not, create one** using `templates/specs-template.md`
3. **Review related ADRs** in `adr/` for architectural context
4. **Implement according to spec**
5. **Update spec** if implementation deviates

### When Making Architectural Decisions

1. **Create an ADR** using `templates/adr-template.md`
2. **Number sequentially** (e.g., `0001-decision-name.md`)
3. **Document context, decision, and consequences**
4. **Reference in related specs** if applicable

### When Updating Code

1. **Check relevant specs** before making changes
2. **Update specs** if requirements change
3. **Document deviations** in commit messages
4. **Update ADRs** if architectural decisions change

## Quick Links

- [Specification Template](templates/specs-template.md)
- [ADR Template](templates/adr-template.md)
- [Architecture Overview](architecture/overview.md)
- [Messaging Patterns](architecture/messaging.md)
- [Use Case Patterns](architecture/use-cases.md)

## AI Consultation

Cursor AI is configured to automatically consult these specifications during development. The rule in `.cursor/rules/specs-consultation.mdc` ensures that:

- Specs are checked before implementation
- Specs are updated when code changes
- Deviations are documented
- Specs are referenced in code comments

## Contributing

When adding or updating documentation:

1. Follow the templates provided
2. Use clear, concise language
3. Include diagrams where helpful (Mermaid format)
4. Keep documentation up-to-date with code changes
5. Reference related specs/ADRs when relevant
