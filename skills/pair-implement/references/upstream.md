# Resolve playbook and upstream guidance

Resolve the playbook root from the real path of this skill folder, two levels up, or use `AI_ENGINEERING_PLAYBOOK_ROOT` or a checkout path supplied by the developer. Check that the root contains `standards/README.md` and `registry/skills.yaml`.

Use the standards index to choose guidance for the changed surfaces. Use the registry as the inventory of approved skills, source revisions, dependencies, and artifact contracts. Resolve Matt Pocock skills from the active plugin or standalone installation. Start with the available-skills list, then check the active installation for skills exposed only by explicit invocation. Verify the originating distribution and resolve companions relative to the owning `SKILL.md`.

Use the installed revision after checking that the contracts needed for the current step still match. Report missing or incompatible required guidance at the affected checkpoint. For unfamiliar specialist advice, check its registered scope and the project version first.

## Project configuration

Read the upstream `## Agent skills` pointers from the repository's `AGENTS.md` or `CLAUDE.md`. Use the configured tracker, domain guidance, and triage labels where relevant. If tracker or domain configuration is missing, direct the developer to `setup-matt-pocock-skills`. The glossary and ADR directory can be created lazily where the upstream domain contract allows it.

## Ticket scope

Use `to-spec` and `to-tickets` as format references for an existing ticket. Resolve its parent through the configured relation, body reference, or spec path. Read an active parent when it supplies scope, acceptance criteria, or constraints. For a historical or unavailable parent, proceed only when the ticket or an approved replacement establishes the full current scope. Report missing requirements or conflicting scope and stop for clarification. Verify blockers independently.

## Blocker verification

Use the configured backend. On GitHub use `gh` for the full ticket, then verify the native incoming dependency links (`gh issue view --json blockedBy` or the corresponding read API). Verify that all blockers are closed, paginating API results or checking the open-blocker summary when necessary. Check explicit `Blocked by` references too, especially when native dependencies are unavailable. Keep the configured repository and host explicit when resolving bare numbers and cross-repo links. For GitLab use configured native incoming links or the textual fallback. For local Markdown use the configured `Blocked by` entries and resolution convention. A verified empty blocker list allows work. A failed or incomplete lookup supplies no evidence that the ticket is unblocked. For a custom tracker, use its configured read path and stop if it cannot establish blocker state.

## Prototypes

Use the upstream references for the approved design question. Keep the experiment isolated from the implementation working tree. Report what the prototype established. Obtain approval for any prototype commit, tracker write, or promotion to production code.
