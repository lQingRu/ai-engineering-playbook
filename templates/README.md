# Project documentation templates

Use the templates for the surfaces the project has or is actively designing. Treat the suggested destinations as defaults when the repository has no equivalent location. Use the prompts to extend existing documentation and keep each decision, command, or fact in its canonical location. Replace prompts with project-specific content and omit sections that do not apply.

- **Existing projects.** Verify current capabilities, architecture, and constraints against source, manifests, configuration, migrations, tests, or runtime evidence as appropriate. Link the evidence and mark unresolved facts as unverified. Confirm which observed practices are approved conventions.
- **New projects.** Label proposed designs and approved designs awaiting implementation with their status. Link to active planning records when readers need that context. List capabilities and architecture as implemented only when there is evidence for them. Use the same distinction for planned changes in an existing project.
- **Specialist guidance.** Start with the applicable [engineering standard](../standards/README.md). Record the selected guidance, the task or technology that triggers it, and a source reference. For skills, use the ID and scope in the [approved registry](../registry/skills.yaml). Keep skill instructions at their source.
- **Approved exceptions.** Link each affected convention to its approved exception in the existing ticket, PR, or ADR. Record the policy, scope, reason, risk, alternate verification, and approval in that record. Include an expiry or review trigger when applicable.

## Engineering decisions

| Engineering standard | Template | Suggested application location and scope |
| --- | --- | --- |
| [Architecture](../standards/architecture.md) | [Architecture overview](docs/architecture.md) | `docs/architecture.md` for runtime structure, repository layout, and dependency constraints |
| [Frontend](../standards/frontend.md) | [Frontend conventions](docs/standards/frontend.md) | `docs/standards/frontend.md` for client implementation conventions |
| [UI/UX](../standards/ui-ux.md) | [Design system](docs/design-system.md) | `docs/design-system.md` for design foundations, design ownership, and rendered checks |
| [Backend and database](../standards/backend.md) | [Backend conventions](docs/standards/backend.md) | `docs/standards/backend.md` for APIs, jobs, integrations, or persistence conventions |
| [Testing](../standards/testing.md) | [Testing and verification](docs/standards/testing.md) | `docs/standards/testing.md` for test boundaries and executable quality checks |
| [Security](../standards/security.md) | [Security conventions](docs/standards/security.md) | `docs/standards/security.md` for access, sensitive data, and security checks |
| [Git](../standards/git.md) | [Git and delivery](docs/standards/git.md) | Existing contributor guidance or `docs/standards/git.md` for repository delivery settings |
| [Ticket creation](../standards/tickets.md) | [Project ticket workflow](docs/standards/tickets.md) | Existing tracker guidance or `docs/standards/tickets.md` for project settings and workflow pointers |

## Implementation and product documentation

| Template | Suggested application location | Use when |
| --- | --- | --- |
| [Product overview and current capabilities](docs/product.md) | Existing product overview or `docs/product.md` | Readers need to understand who the project serves and what works today |
| [Module responsibilities](docs/module.md) | Existing module docs or module README | A module needs local ownership, contract, or dependency details beyond the architecture overview |
| [Data model](docs/data-model.md) | `docs/data-model.md` or context-local documentation | A persistent or shared data model needs an explanation of ownership and invariants |
| [Known limitations](docs/known-limitations.md) | Existing product or operations docs, or `docs/known-limitations.md` | Users or maintainers need a durable record of verified constraints and workarounds |
| [Project agent guidance](project-AGENTS.md) | Existing `AGENTS.md` or `CLAUDE.md` | Agents need pointers to project conventions, checks, and documentation |

## Specs, domain vocabulary, and decisions

Use the [specification lifecycle](../standards/tickets.md#specification-lifecycle) and [long-lived documentation policy](../standards/architecture.md#long-lived-documentation) to decide where information belongs.

Follow Matt Pocock’s `domain-modeling` and its `GLOSSARY-FORMAT.md` and `ADR-FORMAT.md` companions. Keep the root `GLOSSARY.md` for a single context or the root `GLOSSARY-MAP.md` pointing to context glossaries for multiple contexts. Use numbered ADRs in the appropriate system-wide or context-local `docs/adr/`. Create these artifacts as needed and link to them from architecture and data model documentation.

When `grill-with-docs` produces a glossary entry or ADR, use that artifact as the source for the term or decision rationale. Describe the implemented model and architecture in the relevant repository docs.
