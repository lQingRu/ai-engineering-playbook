---
name: pair-implement
description: Pair on one implementation ticket with approval before each increment, commit, and PR publication.
---

# Pair Implement

Use `$pair-implement <ticket identifier or URL> [pairing|learning]` in the application repository. Default to `pairing`. Ask only when the ticket, repository, or requested mode is ambiguous. In `learning`, agree on core logic for the developer to write. Keep their ownership unless they explicitly change it.

Use [upstream resolution](references/upstream.md) to read the project's adopted standards and resolve approved skills. This workflow owns approvals and state transitions. Use compatible upstream methods within the current state's scope. Reserve autonomous whole-ticket orchestration for the project's separate autonomous workflow.

## Approval and resumption

- At a checkpoint, finish with a final response that names the state, identifies the ticket, and states exactly what action awaits approval. End the turn there. A commentary update, queued plan, or subagent report never opens a gate.
- Require a subsequent, explicit user approval for the specific action presented. Match it to the ticket, scope, and current evidence. Silence, a time limit, a vague acknowledgement, or approval of a different action grants no permission. Material changes to behaviour, scope, seams, ownership, or the reviewed diff invalidate the affected approval. Return to the relevant checkpoint.
- Give any nested skill or subagent the current scope and stop condition. Keep approvals and mutations with the main agent. Subagents may perform read-only design or review work within the current state. Keep push, PR publication, merge, tracker closure, and other tickets outside automatic execution. Stop if required configuration, dependencies, or evidence cannot be verified.
- Use the repository's permissions, trusted hooks, and automated checks where they cover an action. Markdown defines the handoffs. It supplies no tool-level enforcement of approval.
- On a fresh session, resolve the ticket's scope and blockers as in **DISCOVERY** and reconstruct progress from the configured tracker (GitHub issues for GitHub projects), Git history, branch/base, index, and working tree. Treat evidence of completed work as progress only. If state or approval is uncertain, return to **REVIEW** for an identifiable pending diff, **FINAL REVIEW** for completed committed work, or **DISCOVERY** when no pending increment can be established. If ownership of changes or a prior learning handoff is unclear, show the evidence and confirm the increment and ownership before editing. Never infer approval from code, commits, tracker status, or an absent transcript. Keep proposals and approval evidence in the conversation. Use the existing ticket and Git history for durable context.

## State 1 — DISCOVERY

1. Load repository instructions, including applicable path-scoped guidance and the existing Matt Pocock setup pointers. Read the ticket, comments, and [parent specification](references/upstream.md#ticket-scope) through the configured tracker or repository. Verify blockers and state the ticket title and scope sources.
2. Read the relevant project conventions, domain and architecture docs, ADRs, and adopted engineering standards. Inspect relevant code, tests, and commands. Establish the intended target branch and base, and identify existing local changes.
3. Resolve specialist skills for the affected technology and phases using the project dependency record and approved registry. Read the actual instructions and companions relevant to design and the proposed increment before recommending an approach. Surface missing or incompatible dependencies and their effect on the workflow. Use `codebase-design` for an unsettled interface or test seam. Consult the [prototype procedure](references/upstream.md#prototypes) if a specific unknown merits an experiment.
4. Discuss significant decisions, trade-offs, and ADR conflicts. If the ticket needs clarification or splitting, present the gaps or proposed vertical slices and end the turn for direction. Otherwise propose numbered, independently verifiable increments. Map each to acceptance criteria and name its public test seam and coverage where applicable. Explain small concepts inline and [offer learning mode](references/upstream.md#learning) when the developer could own meaningful logic.

**Checkpoint.** End the turn with the proposed increments and ask the developer to approve one named increment and its test seam. Discovery approval covers that implementation scope only.

## State 2 — IMPLEMENTATION

Enter only with explicit approval of one increment and its seam, if applicable. Recheck the ticket, blockers, dependencies, and local baseline if they may have changed. Preserve unrelated work. For behavioural changes, use the installed `tdd` instructions and companions. Follow the one-behaviour, one-test, red-to-green cycle at the agreed public seam. Verify that the test fails for the intended reason, then take the smallest step to green. Keep refactoring proposals for review. Apply the identified standards and specialist guidance. Run the targeted tests and relevant checks. When test-first is impractical, present an exception with alternate evidence for approval before changing the increment. For a documentation-only increment, verify the claims against the implementation and run applicable documentation checks.

When an increment reserves core logic for the developer, prepare the agreed failing test or scaffold, explain the expected behaviour and offer a hint, then end the turn with a developer handoff. When they say it is ready, inspect their changes and run validation within the same increment. If scope changes, end the turn for fresh approval before expanding it.

Transition to **REVIEW** with the actual result, including any incomplete work or failed checks. Leave staging for commit preparation and leave the next increment pending.

## State 3 — REVIEW

Inspect the actual diff, including relevant staged, unstaged, and new files. Use the [Git approval procedure](references/git-approval.md) to record the exact commit candidate and separate unrelated changes. If unrelated local edits can affect check results, validate the candidate in an isolated checkout or clearly qualify the available evidence. For this candidate, report:

- The actual candidate diff, inline or through a readable patch, with a technical walkthrough of the changed behaviour, decisions, and tests.
- Findings against the applicable project standards. Cite significant specialist guidance applied, violations, and approved exceptions with their rationale and alternate verification. Identify unresolved findings and their impact.
- Automated checks run and their results, including red and green evidence where applicable. Identify checks that could not run.
- The proposed commit message using repository conventions, or the personal default if none exist, and the candidate's Git identity.

**Checkpoint.** End the turn. Ask the developer to approve committing that candidate. If they request changes, get approval for any revised implementation scope and present a fresh review before committing.

## State 4 — COMMIT

Enter only after explicit approval to commit the reviewed candidate. Follow the [Git approval procedure](references/git-approval.md). Verify branch, `HEAD`, approved diff, and proposed message before committing. Commit only the approved changes and verify the resulting commit. Report its SHA. If evidence differs or staging cannot safely isolate the approved patch, return to **REVIEW** and end the turn.

When all acceptance criteria are met, transition to **FINAL REVIEW**. Otherwise end the turn and advance only after the user explicitly authorises another specific increment. Return to **DISCOVERY** first if it needs a new proposal.

## State 5 — FINAL REVIEW

1. Pin the target base and reviewed `HEAD` by SHA. Confirm that the proposed comparison contains the complete ticket change set and can be published without unrelated changes. Resolve `code-review` and run its independent **Standards** and **Spec** reviews in fresh, read-only contexts. Supply the applicable standards and specialist review guidance to Standards, and the ticket and parent spec to Spec. If independent reviewers are unavailable, report the blocked review and end the turn for an independent review arrangement. Map every acceptance criterion to evidence. Run the repository's relevant quality checks against the reviewed tree, including the full suite where applicable. If local edits would affect results, validate in an isolated checkout. For UI changes, exercise the rendered flow and capture observations or screenshots using the project's verification guidance.
2. Present unresolved findings before fixing them. If fixes are needed, propose a bounded increment and end the turn for approval. Route approved fixes through **IMPLEMENTATION**, **REVIEW**, and **COMMIT**, then rerun the affected final checks. Material changes require a new final review.
3. Update affected product and architecture docs in their established locations. Use the playbook templates for missing documentation where applicable. Consult `domain-modeling` and its format companions for glossary changes or qualifying ADRs. When documentation changes remain, present them as a scoped increment and end the turn for approval before editing. Route those changes through the same review and commit gates, then review the new head.
4. Report the final verification evidence. When the project delivers without a PR, report the reviewed commits and any remaining delivery action that needs approval. When the project delivers through a PR, prepare its description using `pr`. Report acceptance criteria coverage, separate Standards and Spec findings, quality and UI evidence, documentation changes, unresolved concerns, and a concise technical learning recap. Identify the reviewed head, target base, and proposed PR destination. Use a non-closing ticket reference.

**PR checkpoint.** End the turn with the proposed PR description and ask for explicit approval before publication. Before publishing, revalidate the approved head, base, destination, and body. If any differ, return to this checkpoint with updated review evidence. If publishing requires a push, obtain explicit authorisation for that push. Publication approval never grants permission to merge or change ticket state.
