---
name: pair-implement
description: Pair on one implementation ticket with approval before each increment, commit, and PR publication.
---

# Pair Implement

Use `$pair-implement <ticket identifier or URL> [pairing|learning]` in the application repository. Default to `pairing`. Ask only when the ticket, repository, or requested mode is ambiguous. In `learning`, agree on core logic for the developer to write. Keep their ownership unless they explicitly change it.

Use [upstream resolution](references/upstream.md) to locate the playbook's standards and approved skill registry. Read installed Matt Pocock instructions and their companions at the point of use. This skill owns state transitions. Use upstream methods within the current state's scope. Do not run `implement` or `implement-spec`.

## Approval and resumption

- At a checkpoint, finish with a final response that names the state, identifies the ticket, and states exactly what action awaits approval. End the turn there. A commentary update, queued plan, or subagent report never opens a gate.
- Require a subsequent, explicit user approval for the specific action presented. Match it to the ticket, scope, and current evidence. Silence, a time limit, a vague acknowledgement, or approval of a different action grants no permission. Material changes to behaviour, scope, seams, ownership, or the reviewed diff invalidate the affected approval. Return to the relevant checkpoint.
- Give any nested skill or subagent the current scope and stop condition. Keep approvals and mutations with the main agent. Subagents may perform read-only design or review work within the current state. Keep push, PR publication, merge, tracker closure, and other tickets outside automatic execution. Stop if required configuration, dependencies, or evidence cannot be verified.
- On a fresh session, resolve the ticket's scope and blockers as in **DISCOVERY** and reconstruct progress from the configured tracker (GitHub issues for GitHub projects), Git history, branch/base, index, and working tree. Treat evidence of completed work as progress only. If state or approval is uncertain, return to **REVIEW** for an identifiable pending diff, **FINAL REVIEW** for completed committed work, or **DISCOVERY** when no pending increment can be established. If ownership of changes or a prior learning handoff is unclear, show the evidence and confirm the increment and ownership before editing. Never infer approval from code, commits, tracker status, or an absent transcript. Keep proposals and approval evidence in the conversation. Use the existing ticket and Git history for durable context.

## State 1 — DISCOVERY

1. Load repository instructions, including applicable path-scoped guidance and the existing Matt Pocock setup pointers. Read the ticket and its comments in the configured tracker. Verify blockers and resolve the [current implementation scope](references/upstream.md#ticket-scope). State the ticket title.
2. Read repository guidance and the applicable playbook standards, domain docs and ADRs, then inspect the relevant code, tests, and repository commands. Establish the intended target branch/base and distinguish existing local changes from ticket work. Explain the intended behaviour, affected modules, significant decisions and trade-offs, and any ADR conflict.
3. Assess whether the ticket is small and specified enough. If it needs clarification or splitting, show the gaps or proposed vertical slices and stop for direction. Use `codebase-design` when a module interface or seam is unsettled. Use `prototype` when a logic or UI experiment can resolve a specific question, within the discovery contract in the reference.
4. Present the approach and numbered, independently verifiable behavioural increments. Map each to acceptance criteria and name the proposed public test seam and what it covers. Identify meaningful learning opportunities and, in learning mode, propose which core logic the developer will write. Offer a short explanation when an unfamiliar or significant concept comes up.

**Checkpoint.** End the turn with the proposed increments and ask the developer to approve one named increment and its test seam. Discovery approval covers that implementation scope only.

## State 2 — IMPLEMENTATION

Enter only with explicit approval of one increment and its seam, if applicable. Recheck the ticket, blockers, and local baseline if they may have changed. Preserve unrelated work. For behavioural changes, read `tdd` and both companion files. Use its one-behaviour, one-test, red-to-green cycle at the agreed public seam. Verify that the test fails for the intended reason, then take the smallest step to green. Keep refactoring proposals for review. Follow repository standards and run the targeted tests and relevant checks. When test-first is impractical, present an exception with alternate evidence for approval before changing the increment. For a documentation-only increment, verify the claims against the implementation and run applicable documentation checks.

When an increment reserves core logic for the developer, prepare the agreed failing test or scaffold, explain the expected behaviour and offer a hint, then end the turn with a developer handoff. When they say it is ready, inspect their changes and run validation within the same increment. If scope changes, end the turn for fresh approval before expanding it.

Transition to **REVIEW** with the actual result, including any incomplete work or failed checks. Leave staging for commit preparation and leave the next increment pending.

## State 3 — REVIEW

Inspect the actual diff, including relevant staged, unstaged, and new files. Use the [Git approval procedure](references/git-approval.md) to record the exact commit candidate and separate unrelated changes. If unrelated local edits can affect check results, validate the candidate in an isolated checkout or clearly qualify the available evidence. For this candidate, report:

- Changed files and what their diff does.
- Significant implementation decisions and relevant engineering concepts. Offer a brief explanation and suggest a separate `teach` session when deeper work would help.
- Tests and checks run, their results, and remaining concerns.
- The proposed commit message using repository conventions, or the personal default if none exist, and the candidate's Git identity.

**Checkpoint.** End the turn. Ask the developer to approve committing that candidate. If they request changes, get approval for any revised implementation scope and present a fresh review before committing.

## State 4 — COMMIT

Enter only after explicit approval to commit the reviewed candidate. Follow the [Git approval procedure](references/git-approval.md). Verify branch, `HEAD`, approved diff, and proposed message before committing. Commit only the approved changes and verify the resulting commit. Report its SHA. If evidence differs or staging cannot safely isolate the approved patch, return to **REVIEW** and end the turn.

When all acceptance criteria are met, transition to **FINAL REVIEW**. Otherwise end the turn and advance only after the user explicitly authorises another specific increment. Return to **DISCOVERY** first if it needs a new proposal.

## State 5 — FINAL REVIEW

1. Pin the target base and reviewed `HEAD` by SHA. Confirm that the proposed comparison contains the complete ticket change set and can be published without unrelated changes. Read `code-review` and run its independent **Standards** and **Spec** reviews against that comparison, using the ticket and any parent spec that supplies current requirements. Map every acceptance criterion to evidence. Run the repository's relevant quality checks against the reviewed tree, including the full suite where applicable. If local edits would affect results, validate in an isolated checkout. For UI changes, exercise the rendered flow and capture observations or screenshots.
2. Present unresolved findings before fixing them. If fixes are needed, propose a bounded increment and end the turn for approval. Route approved fixes through **IMPLEMENTATION**, **REVIEW**, and **COMMIT**, then rerun the affected final checks. Material changes require a new final review.
3. Update affected product and architecture docs in their established locations. Consult `domain-modeling` for domain changes and record qualifying decisions using its ADR criteria and format. When documentation or ADR changes are still needed, present them as one scoped increment and end the turn for approval before editing. Route those changes through the same review and commit gates, then verify the final diff includes them.
4. Report the final verification evidence. When the project delivers without a PR, report the reviewed commits and any remaining delivery action that needs approval. When the project delivers through a PR, prepare its description using `pr`. Report acceptance criteria coverage, separate Standards and Spec findings, quality and UI evidence, documentation changes, unresolved concerns, and a concise technical learning recap. Identify the reviewed head, target base, and proposed PR destination. Use a non-closing ticket reference.

**PR checkpoint.** End the turn with the proposed PR description and ask for explicit approval before publication. Before publishing, revalidate the approved head, base, destination, and body. If any differ, return to this checkpoint with updated review evidence. If publishing requires a push, obtain explicit authorisation for that push. Publication approval never grants permission to merge or change ticket state.
