# Personal Engineering Guidelines

## Objectives

Optimise for product quality, engineering quality and developer learning, rather than implementation speed alone.

## Development Modes

- Pairing: default for non-trivial implementation.
- Learning: guide me while I implement selected code personally.
- Autonomous: available only when explicitly requested.

## Human Approval

For non-trivial work:

- Discuss significant technical and architectural decisions before implementation.
- Present alternatives, trade-offs and a recommendation when meaningful choices exist.
- Obtain approval before introducing dependencies, changing schemas or altering architectural boundaries.
- Stop at explicit workflow checkpoints.
- Approval applies only to the stated scope.
- Do not treat silence or an ambiguous response as approval.
- Do not delegate work to another agent to bypass approval checkpoints.

## Feature Planning

- Preserve the project's primary development framework.
- Discuss requirements before creating specifications.
- Obtain approval before publishing specifications and implementation tickets.
- Do not duplicate existing task trackers or specification artifacts.

## Implementation

- Work in pairing mode by default on non-trivial implementation. Invoke `$pair-implement` explicitly for the playbook's one-ticket workflow.
- Follow project architecture decisions. When using this playbook, read the standards index in the playbook checkout for the surfaces affected by the change.

## Learning

- Explain significant technical decisions and unfamiliar concepts.
- Identify meaningful opportunities for hands-on implementation.
- Recommend structured teaching when a concept requires more than a short explanation.
- Do not interrupt routine implementation with unnecessary tutorials.

## Version Control

- Prefer Conventional Commits unless repository conventions differ.
- Obtain approval before committing, pushing, publishing or merging.
- Never automatically proceed to another ticket.

## Completion

- Clearly report unresolved limitations.

## Skill Composition

- Respect the designated primary development framework.
- Do not combine incompatible orchestration workflows.
- Preserve existing skill dependencies and generated artifacts.
- Use independent specialist skills where relevant.
- Report conflicting instructions before performing affected actions.
