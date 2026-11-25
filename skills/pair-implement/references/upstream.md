# Resolve playbook and upstream guidance

Start from the standards and skill dependency index routed by the project's `AGENTS.md` or other effective guidance. Use its adopted revision for playbook policies and approved skill scopes. For missing pointers, resolve the playbook from the developer-supplied checkout path, `AI_ENGINEERING_PLAYBOOK_ROOT`, or two levels up from the real path of this skill directory. Check for `standards/README.md` and `registry/skills.yaml`. If a newly affected surface lacks project guidance, consult the applicable playbook policy and discuss any adoption decision before editing.

Use the adopted registry or its scoped entries in the project index to resolve guidance by trigger, phase, required status, dependencies, contract, and compatibility. Start with the available-skills list and the active plugin or standalone installation, including explicit-only entries. Verify the actual source, revision, and relevant technology and tooling versions. Read the installed `SKILL.md` and resolve companions relative to it. For reference-only entries, limit use to the approved, verified source and supporting prose. Check any invocation, scripts, network access, and writes against the current increment and approvals.

Report missing or incompatible required guidance by ID, expected source, missing resource or contract, and blocked phase. End the turn before work that depends on it. Route any installation or update through separate approval, for example using `$bootstrap-project` to reconcile project setup. For optional unavailable guidance, disclose the fallback to version-matched maintainer docs and project checks.

## Project configuration

Read the upstream `## Agent skills` pointers from the repository's `AGENTS.md` or `CLAUDE.md`. Use the configured tracker, domain guidance, and triage labels where relevant. If required setup is missing, recommend `$bootstrap-project` or the compatible upstream setup entry point. The glossary and ADR directory can be created lazily where the upstream domain contract allows it.

## Ticket scope

Resolve the parent through the configured native relation, body reference, or spec path. For GitHub, inspect the native parent relation as well as explicit references. For local Markdown, check the configured feature spec. Retrieve and read the parent when present, including the constraints and acceptance criteria relevant to the ticket. If no parent exists, report that and use the ticket as the scope source when it is complete. If a referenced parent is historical or unavailable, surface that status and confirm how current scope is established. Report missing requirements or conflicting scope and stop for clarification. Verify blockers independently. Consult `to-spec` and `to-tickets` for upstream formats when needed to interpret existing records.

## Blocker verification

Use the configured backend. On GitHub use `gh` for the full ticket, then verify the native incoming dependency links (`gh issue view --json blockedBy` or the corresponding read API). Verify that all blockers are closed, paginating API results or checking the open-blocker summary when necessary. Check explicit `Blocked by` references too, especially when native dependencies are unavailable. Keep the configured repository and host explicit when resolving bare numbers and cross-repo links. For GitLab use configured native incoming links or the textual fallback. For local Markdown use the configured `Blocked by` entries and resolution convention. A verified empty blocker list allows work. A failed or incomplete lookup supplies no evidence that the ticket is unblocked. For a custom tracker, use its configured read path and stop if it cannot establish blocker state.

## Prototypes

Use the upstream references for the approved design question. Keep the experiment isolated from the implementation working tree. Report what the prototype established. Obtain approval for any prototype commit, tracker write, or promotion to production code.

## Learning

Explain small concepts in context. Offer learning mode for a concrete hands-on opportunity and agree on what the developer owns before preparing a scaffold or test. For substantial structured learning, recommend a separate invocation of Matt Pocock's `teach` from the developer's chosen teaching directory. Verify the actual entry point and read its own format companions for that session. In v1.3.2, the directory of invocation is the workspace for `MISSION.md`, `RESOURCES.md`, `GLOSSARY.md`, `NOTES.md`, `lessons/`, `reference/`, `learning-records/`, and `assets/`. Leave teaching artifacts in that workspace.
