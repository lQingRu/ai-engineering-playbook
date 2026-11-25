---
name: bootstrap-project
description: Reconcile engineering setup, documentation, skill dependencies, and quality gates in a new or existing project.
---

# Bootstrap Project

Run `$bootstrap-project` in the target repository. Reconcile its setup in place and keep application code outside bootstrap scope.

## Inspect

1. Establish the target root, repository status and local changes. Identify the stack and versions, entry points, runtime and module boundaries, integrations, data stores and migrations, existing docs and ADRs, tracker, tools, CI, hooks, and agent instructions. Check effective `AGENTS.md` routing, including overrides. Distinguish a new project from an existing implementation using repository evidence.
2. Read [the reconciliation procedure](references/reconciliation.md) and locate the playbook. Inspect existing Matt Pocock configuration and artifacts before deciding which gaps need upstream setup. Inspect the actual available skills, their versions, and the relevant resources and permissions.
3. Select standards from the playbook's standards index. Resolve specialist guidance through the registry and check the required dependencies of the chosen workflows. Read the applicable documentation templates. In an existing project, trace what works today to code, configuration, migrations, tests, or runtime evidence. In a new project, record design status and open decisions.

## Agree

1. Discuss decisions the repository evidence cannot settle. For existing projects, confirm whether observed practices are approved conventions. Show discrepancies between docs and implementation, what will be preserved, and any proposed exception or deliberate change.
2. Present the exact reconciliation scope: upstream setup gaps and proposed actions, documentation destinations and decisions, standards and guidance references, the dependency list, and quality gates. List missing or incompatible dependencies by ID, source, candidate revision, reason, companion requirements, and affected workflow. Separate required blockers from optional guidance. Preview repository writes and external actions separately.

**Checkpoint.** End the turn for approval of the proposed changes. Installation needs explicit approval for the named dependencies and revisions. Tracker writes, including label creation, need explicit approval for the named actions and destination. Approval of documentation or setup edits covers only those edits. A reconcile with no changes can proceed directly to verification.

On resumption, re-read the current repository and dependency state. Use prior approval only when the explicit approval and the exact action it covers are available and still match the evidence. Otherwise present the remaining scope and end the turn for fresh approval. Existing files and partial changes establish progress only.

## Reconcile

1. Recheck the approved plan against current state. For approved dependencies, use the applicable supported installation route and verify the installed instructions, companions, and contract before using them. Report remaining blockers by workflow. Apply independent approved changes when a dependency still blocks another part.
2. Complete approved missing Matt Pocock setup using the compatible upstream instructions. Preserve existing valid choices, artifacts, and unrelated edits. Follow upstream's own checkpoints and keep remote or tracker actions within separately approved scope.
3. Apply the approved documentation, standards, dependency record, agent routing, and quality gates using the [reconciliation procedure](references/reconciliation.md). For an existing project, write the approved missing setup and evidence-backed documentation. Preserve documented decisions unless the plan explicitly changes them. Resolve conflicts through another approval checkpoint.

## Verify

Inspect the actual diff and run the verification steps in the reference. Report which changes were applied, which workflows are ready or blocked, the check results, and what evidence remains unavailable. Confirm a repeat with the same inputs proposes no changes. End before staging, committing, or publishing.
