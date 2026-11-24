# Engineering standards

Read the standards that apply to the change. Owned policies apply across projects. External guidance applies when the task and technology match.

| Standard | Owned policy | External guidance |
| --- | --- | --- |
| [Architecture](architecture.md) | Cohesion, coupling, module boundaries, and accurate documentation | Matt Pocock's architecture and domain guidance |
| [Frontend](frontend.md) | Clear component responsibilities and state ownership | Vercel React guidance where applicable |
| [UI/UX](ui-ux.md) | Design consistency, accessible interaction, and rendered validation | W3C, Vercel, and scoped design and polish skills |
| [Backend and database](backend.md) | Stable contracts, data integrity, and safe migrations | Version-matched framework and database docs |
| [Testing](testing.md) | Behavioural, deterministic tests and regression coverage | Matt Pocock's TDD |
| [Security](security.md) | No hardcoded secrets and least privilege | OWASP and platform security guidance |
| [Git](git.md) | Atomic commits and human approval | Conventional Commits and Matt Pocock's PR guidance |
| [Ticket creation](tickets.md) | Small vertical slices and reviewability | Matt Pocock's ticket and spec workflows |

Record project choices in existing repository guidance, configuration, or ADRs. Use the [project templates](../templates/README.md) to identify which choices need documenting. Resolve skill names through the [approved registry](../registry/skills.yaml) and check the installed technology version. If an optional skill is unavailable, use maintainer documentation and the project's existing checks.

For an exception, record the scope, reason, risk, and alternate verification in the existing ticket, PR, or ADR. Follow the [personal approval policy](../global/AGENTS.md) and report any checks that could not run.
