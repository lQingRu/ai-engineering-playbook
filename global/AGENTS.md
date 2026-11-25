# Personal Engineering Preferences

## Collaboration

- Optimise for product quality, engineering quality, and my learning as well as delivery speed.
- Pair with me by default on non-trivial implementation. Use `$pair-implement` when I choose the playbook's one-ticket workflow. Work autonomously only at my explicit request.
- Explain small or unfamiliar concepts inline. Offer learning mode when I can write a meaningful part myself, and guide me through that part. Recommend a dedicated teaching session for substantial topics.

## Decisions and approvals

- Discuss requirements with me before drafting a spec. Discuss significant technical and architectural decisions before implementation. When there are meaningful alternatives, explain the trade-offs and recommend one.
- Propose small, independently reviewable increments. Implement one approved increment at a time and report unresolved limitations at review.
- Get my explicit approval before implementing an increment, adding a dependency, changing a schema or architectural boundary, or publishing a spec or ticket. End the turn at explicit workflow checkpoints. Approval covers the stated action and scope, including delegated work.

## Project guidance

- Follow the project's primary engineering workflow. Reuse its tracker, specs, and existing workflow artifacts. Raise conflicts in standards or workflows before acting.
- Consult the applicable project standards and decisions before proposing or making changes. For projects using this playbook, use the playbook checkout's `standards/README.md` when project guidance leaves a gap.
- Use `$bootstrap-project` when I ask to establish or reconcile a project's standards, documentation, or workflow setup.

## Version control

- Keep commits atomic and follow repository conventions. Prefer Conventional Commits when the project has no convention.
- Get my explicit approval before committing, pushing, publishing a PR, merging, or moving on to another ticket.
