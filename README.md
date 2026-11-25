# AI Engineering Playbook

## 1. Overview

This playbook sets up a human-led engineering workflow for Codex. It favors one reviewable increment at a time, explicit approval of significant decisions and writes, evidence from real checks, and documentation that reflects current behavior. Pairing is the personal default for non-trivial implementation, with room for hands-on learning and explicitly requested autonomy.

The playbook owns personal [working agreements](global/AGENTS.md), reusable [engineering standards](standards/README.md), [project templates](templates/README.md), and two explicit skills. `bootstrap-project` reconciles project setup. `pair-implement` runs one ticket. Matt Pocock’s skills supply the tracker, planning, design, TDD, review, domain modeling, and PR methods used within those workflows. [Approved skill registry](registry/skills.yaml)

## 2. Quick Start

With an authenticated Codex CLI, Python with PyYAML, and the compatible Matt Pocock plugin ready, run these **terminal commands**. For first-time dependency setup, see [First-Time Installation](#4-first-time-installation). Replace `/path/to/playbook` and `/path/to/project` with your checkout and application paths.

```sh
cd /path/to/playbook
./scripts/install.sh --dry-run
```

Review the proposed paths, then continue in the **terminal**.

```sh
./scripts/install.sh
./scripts/verify.sh --project /path/to/project
cd /path/to/project
codex
```

In **Codex**, select `$bootstrap-project` and review its setup proposal before approving changes. Once bootstrap reports pairing ready, run `$pair-implement <ticket>`, replacing `<ticket>` with an unblocked issue number, URL, or local ticket path. Expect a proposal for one increment and its test seam before implementation begins.

## 3. Prerequisites

- **Local scripts.** A POSIX shell, Git, and Python 3.11+ with PyYAML. Keep the playbook checkout at a stable path. The scripts use `python3` unless you set `PYTHON` to another interpreter.
- **Codex.** Use a client that discovers local skills and supports explicit invocation. The commands below use the CLI and its plugin commands. Sign in for interactive work and use the same `CODEX_HOME` throughout if you set one. The default profile is `$HOME/.codex`. User skill links are shared across profiles in `$HOME/.agents/skills`. Check for disabled skills and a non-empty global `AGENTS.override.md` before installing. [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)
- **Upstream.** The registry records Matt Pocock v1.3.2 as the reviewed release. Verify the active distribution and the named skills and companion files for your workflow. Independent final review needs fresh read-only review contexts. [Registry](registry/skills.yaml) · [Upstream resolution](skills/pair-implement/references/upstream.md)
- **Project tools.** Use authenticated `gh` for a GitHub tracker, `glab` for a GitLab tracker, or the configured read and write path for another tracker. Local Markdown needs no remote tracker credentials. Publishing a PR also requires the project's Git remote access and publication permissions. Run project checks with the stack tools the repository specifies.

## 4. First-Time Installation

1. **Terminal — check prerequisites.** Run the GitHub checks only if you use GitHub, from the application repository for `gh repo view`. Use `glab auth status` and `glab repo view` for GitLab.

   ```sh
   git --version
   python3 -c 'import sys; import yaml; assert sys.version_info >= (3, 11); print(sys.version.split()[0], yaml.__version__)'
   codex --version
   codex login status
   ```

   ```sh
   gh --version
   gh auth status
   gh repo view
   ```

   If needed, run `codex login` or `gh auth login` for the corresponding service. If a suitable Python lacks PyYAML, create a virtual environment outside the checkout and run the remaining script commands in the same shell.

   ```sh
   python3 -m venv "$HOME/.venvs/engineering-playbook"
   "$HOME/.venvs/engineering-playbook/bin/python" -m pip install PyYAML
   export PYTHON="$HOME/.venvs/engineering-playbook/bin/python"
   "$PYTHON" -c 'import sys; import yaml; assert sys.version_info >= (3, 11); print(sys.version.split()[0], yaml.__version__)'
   ```

2. **Terminal — install upstream.** For a fresh marketplace registration, use the reviewed ref with the Codex CLI's `--ref` option. If you already have the plugin, check the active version and its compatibility before changing the installation. Use one distribution to avoid duplicate skills. [Upstream installation](https://github.com/mattpocock/skills/blob/v1.3.2/README.md#installation-30-second-setup) · [Reviewed release](https://github.com/mattpocock/skills/releases/tag/v1.3.2)

   ```sh
   codex plugin marketplace add mattpocock/skills --ref v1.3.2
   codex plugin add mattpocock-skills@mattpocock
   codex plugin list --marketplace mattpocock
   ```

3. **Terminal — preview, install, and verify.** Run the installer after reviewing the dry run.

   ```sh
   cd /path/to/playbook
   ./scripts/install.sh --dry-run
   ./scripts/install.sh
   ./scripts/verify.sh
   ```

   Expect one managed block in `${CODEX_HOME:-$HOME/.codex}/AGENTS.md` and two directory symlinks under `$HOME/.agents/skills`. When replacing an existing global file, the installer prints its backup path and original mode. It preserves text outside the managed block, existing configuration, plugins, and unrelated skills. An identical rerun reports `Already installed. No changes.` Verification should end with `Static checks passed`. [Installer and verifier](scripts/playbook.py)

4. **Terminal → Codex — restart and check discovery.** Exit any running Codex session and start it from the application checkout.

   ```sh
   cd /path/to/project
   codex
   ```

   In Codex, use `/skills` or type `$` and select the entries for `bootstrap-project` and `pair-implement`. Both are explicit-only. Check the relevant upstream entries too, including `setup-matt-pocock-skills` if setup is missing. Confirm the active plugin in Codex, since file inspection can see cached revisions. When an upstream name is qualified in the picker, select that entry. [Codex commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli)

## 5. Existing Project Setup

1. **Codex prompt in the application repository:** `$bootstrap-project Reconcile this existing application in place. Preserve its tracker, specifications, tickets, ADRs, and working configuration. Propose pairing as the default for non-trivial ticket implementation.` The skill infers the mode from repository evidence. The words after the skill name are prompt text.
2. Review the inventory of effective instructions, docs, tracker and domain pointers, runtime and module boundaries, integrations, data, and checks. Ask bootstrap to trace current architecture, product capabilities, and known limitations to source, configuration, migrations, tests, or runtime evidence. Resolve discrepancies and confirm which observed practices should become conventions. Keep uncertain facts marked as unverified.
3. Review the proposed gaps. Reuse canonical destinations and existing tracker, triage, glossary, ADR, spec, and ticket artifacts. Fill missing project standards using the applicable [templates](templates/README.md). Select specialist guidance by stack version, task, and phase, with required blockers and optional fallbacks recorded. If upstream setup is genuinely missing, invoke `$setup-matt-pocock-skills` for the agreed gap when Codex requires explicit invocation, then resume bootstrap. Preserve an established upstream block in `CLAUDE.md` and route to it from root `AGENTS.md` where applicable.
4. Approve the exact repository edits after previewing them. Authorize dependency installations by revision and tracker writes by action and destination separately. Approved edits can add or update setup docs, standards and dependency references, agent routing, and agreed quality gates. Application code stays outside bootstrap scope. Bootstrap ends before staging, committing, or publishing. [Reconciliation procedure](skills/bootstrap-project/references/reconciliation.md)
5. Route ticket work to `$pair-implement` in the project's agent guidance, within its approved workflow. Select it explicitly to start a ticket. For GitHub, separately review open issues against the [ticket standard](standards/tickets.md). Each should describe one independently verifiable outcome, with acceptance criteria and real blockers. Keep small implementation increments within the same issue. If an issue needs splitting, preview a `$to-tickets` proposal and authorize tracker edits separately. Bootstrap preserves the backlog.
6. Inspect `git diff` and `git status --short` in the **terminal**. From the playbook checkout, run `./scripts/verify.sh --project /path/to/project`. In a fresh Codex session, confirm the routing and skill availability. Check tracker reads and run the approved project checks. Repeating bootstrap with the same inputs should propose no further writes. Its report should identify any workflows that remain blocked.

## 6. New Project Setup

1. **Terminal.** Create an empty Git repository and launch Codex in it.

   ```sh
   mkdir -p /path/to/project
   cd /path/to/project
   git init
   codex
   ```

2. **Codex prompt:** `$bootstrap-project Set up this new application for a local Markdown tracker and pairing. Help me establish the architecture and checks from the product requirements we have so far.` Substitute the intended tracker. A remote tracker needs a reachable project and any remote or label actions need separate authorization.
3. Agree on the known product purpose, stack, architecture boundaries, and decisions worth documenting as ADRs. Choose the tracker and domain layout. If upstream setup is missing, use `$setup-matt-pocock-skills` for the approved gap when prompted. Glossaries and ADR directories can be created when there is content for them.
4. Establish the conventions for the surfaces you plan to build. Select registry guidance based on the chosen stack and workflows. Reuse available checks or agree on supported tooling, commands, and required versus advisory gates. For decisions that depend on future requirements, record the open decision and what would resolve it. Mark proposed and approved-but-unimplemented designs with their status. Add checks and guidance for those surfaces when the choices are settled.
5. Review and approve the setup scope. Expect project guidance and approved documentation and check configuration. Inspect the diff, verify dependencies and tracker access, and run the commands that can execute in the new repo. Review and separately approve the initial Git commit before pairing on a ticket, since the pairing commit procedure needs a parent `HEAD`. Start the first feature discussion in Codex once the needed workflows are ready. Bootstrap leaves application scaffolding and feature implementation for separately scoped work.

## 7. Daily Development Workflow

Run the following **Codex prompts** in the application repository. Use the skill picker if the installed plugin shows a qualified name.

| Step | Action | Approval or evidence |
| --- | --- | --- |
| Discover | Discuss the user outcome, constraints, alternatives, and test seams. Use `$grilling <idea>` for a structured interview, or `$grill-with-docs <idea>` when the discussion also needs glossary or ADR updates. | Agree on requirements and significant decisions. Scope any documentation writes. |
| Specify | Use `$to-spec Draft the agreed spec and pause for approval before publishing.` after discovery when the work needs a new spec. | Confirm the seam and approve publication of the previewed spec. |
| Slice | Use `$to-tickets <spec>` to draft vertical slices and blocking links in the configured tracker. | Review granularity and blockers, then approve publication. |
| Implement | Use `$pair-implement <ticket>`. The skill reads the ticket and parent, verifies blockers, and proposes increments. For behavioral changes it uses TDD at the agreed public seam. | Approve one named increment. Approve scope changes and any test-first exception with alternate evidence separately. |
| Commit | Review the candidate diff, check results, and proposed message. | Approve the exact candidate. The skill rechecks the branch, parent commit, and candidate tree before making an atomic commit and reporting its SHA. Approve the next increment separately. |
| Final review | After all criteria are met, the skill pins the comparison by SHA, runs independent Standards and Spec reviews, and gathers check results. For UI changes, exercise the rendered flow and capture browser or runtime evidence. | Review findings and any blocked checks. Approve fixes and durable documentation updates as increments, then review the new head. |
| Deliver | The skill drafts the PR with upstream `pr` if the project uses PRs. It presents the reviewed head, base, destination, body, and non-closing ticket reference. | Approve publication and any needed push explicitly. Approve merge and tracker closure separately under project conventions. |

**Example.** A bill tracker needs an overdue filter. Discuss which dates and statuses count as overdue and how users clear the filter. Use `$to-spec`, approve the draft, then use `$to-tickets <spec>` and approve the breakdown. Suppose GitHub issue 42 covers filtering the existing list. Run `$pair-implement 42` in that repository. Approve the increment for filtering and clearing through the list's public UI, then review the failing and passing test evidence and approve the commit. At final review, check the Standards and Spec findings and confirm the rendered list, reset, and empty states. Approve a documentation increment if the product overview needs updating. Approve the PR and push after reviewing the proposed delivery, then approve merge and close the ticket through the project tracker. Keep the spec available while open work or reviews depend on it. [Git approval procedure](skills/pair-implement/references/git-approval.md) · [Specification lifecycle](standards/tickets.md#specification-lifecycle)

## 8. Development Modes

These are **Codex prompts**. The ticket number is illustrative and resolves in the configured tracker.

| Mode | Example | Behavior |
| --- | --- | --- |
| Pairing | `$pair-implement 42` or `$pair-implement 42 pairing` | Default within the skill. Review each proposed increment and commit. Ask for brief explanations inline. |
| Learning | `$pair-implement 42 learning` | Agree on the core logic you will write. Codex prepares the agreed failing test or scaffold, explains the target, and hands control back. Tell it when your changes are ready for validation. |
| Autonomous | `$implement Work autonomously on issue 42 within the project's rules. Stop before committing, pushing, publishing, merging, or changing tracker state.` | Example using Matt Pocock's separate `implement` skill where the project permits it and the entry is available. The upstream skill itself asks for a commit, so state the stop explicitly. `pair-implement` accepts only `pairing` and `learning`. Upstream `implement-spec` orchestrates a whole spec and includes worktree, PR, and ticket-resolution actions. Check project permissions and resolve any workflow conflicts before invoking it. |

Use these upstream skills when their scope fits. Discovery of optional entries depends on the installed distribution.

- `$teach Explain how to choose a public test seam.` Start in a dedicated teaching directory for a structured learning session and its persistent lesson files.
- `$prototype Compare two keyboard interactions for the overdue filter.` Agree on an isolated experiment. Approve any prototype commit, ticket write, or promotion separately.
- `$codebase-design Help compare the public interfaces for the filter module.` Use for module boundaries, interfaces, and test seams. Use `$improve-codebase-architecture <area>` for an upstream architecture survey where available. Use `$domain-modeling` for resolved vocabulary or qualifying ADRs.
- `$diagnosing-bugs Find why clearing the filter sometimes returns a stale result.` Use for hard bugs or regressions to establish a repeatable failure and test hypotheses. Route a pairing fix through the normal checkpoints.

[Upstream skill catalogue](https://github.com/mattpocock/skills/tree/v1.3.2#reference) · [Pairing modes and upstream guidance](skills/pair-implement/references/upstream.md)

## 9. Resuming Work

Open a fresh Codex session in the same application checkout and invoke `$pair-implement <ticket>` again, with `learning` if appropriate. Include the branch or worktree and any pending action you know about. For example, enter `$pair-implement 42 pairing` and add “Continue on the current branch and show the pending candidate” in the prompt.

The skill rereads the ticket and parent and verifies blockers. It inspects branch and base, Git history, the index, and the working tree to recover progress. An identifiable pending diff goes to **REVIEW**, completed committed work goes to **FINAL REVIEW**, and work with no established pending increment returns to **DISCOVERY**. Confirm ownership before continuing if a learning handoff or unrelated edit is unclear.

Prior approval can carry forward when the explicit approval is available and matches the exact action and current evidence. A changed scope, seam, or candidate needs fresh approval. Git history and tracker state establish progress. When the earlier approval is unavailable or ambiguous, expect a new checkpoint. Partial bootstrap work follows the same principle for the remaining changes. [Pairing state and approvals](skills/pair-implement/SKILL.md) · [Bootstrap checkpoints](skills/bootstrap-project/SKILL.md)

## 10. Command Reference

| Command | Purpose | When to use | Skill owner | Expected human approval checkpoints |
| --- | --- | --- | --- | --- |
| **Terminal** `./scripts/install.sh [--dry-run]` | Preview or apply global block and skill links | Install or refresh | Playbook script | Review dry run before applying |
| **Terminal** `./scripts/verify.sh [--project PATH] [--enforcement]` | Inspect local install, upstream inventory, and optional project or enforcement files | After setup or changes | Playbook script | Read-only |
| **Terminal** `./scripts/verify.sh --local-only` or `./scripts/verify.sh --require ID --require ID` | Skip upstream checks or select registry IDs | Isolate an install problem or check a project's dependencies | Playbook script | Read-only. Choose one scope. |
| **Codex** `$bootstrap-project` | Reconcile project setup | New project, migration, or refresh | Playbook | Approve proposed repo edits, installations, and tracker actions in scope |
| **Codex** `$setup-matt-pocock-skills` | Configure tracker, domain, and applicable triage pointers | Required setup is missing | Matt Pocock | Confirm choices and drafts. Authorize tracker or label actions separately. |
| **Codex** `$grilling <idea>` / `$grill-with-docs <idea>` | Resolve requirements or design questions | Before drafting a spec | Matt Pocock | Confirm shared understanding and any documentation scope |
| **Codex** `$to-spec` / `$to-tickets <spec>` | Prepare a spec or slice work into tickets | Planning | Matt Pocock | Confirm seams or breakdown and approve tracker publication |
| **Codex** `$pair-implement <ticket> [pairing\|learning]` | Implement one ticket in reviewed increments | An unblocked ticket is ready | Playbook | Increment, commit, follow-up increments, and PR publication. Push, merge, and closure require separate authorization. |
| **Codex** `$code-review <base>` / `$pr` | Review a fixed comparison or draft a PR body | Final review or delivery | Matt Pocock | Review is read-only. Approve follow-up edits and publication separately. |
| **Codex** `$teach <topic>` | Start structured learning | From a dedicated teaching directory | Matt Pocock | Agree on the learning goal |
| **Codex** `$prototype <question>` / `$codebase-design <question>` | Run an experiment or discuss boundaries and test seams | A design decision needs evidence | Matt Pocock | Agree on scope and significant choices. Authorize writes separately. |
| **Codex** `$diagnosing-bugs <symptom>` | Reproduce and isolate a hard bug | Debugging or performance diagnosis | Matt Pocock | Approve a proposed fix under the project workflow |
| **Codex** `$implement <ticket>` | Run upstream implementation outside pairing | Explicitly requested autonomy under project rules | Matt Pocock | Agree on scope and stop conditions. Retain explicit Git and tracker approvals. |

The default verifier checks every registry entry marked required, even if a particular project phase does not need it. Repeat `--require ID` for a targeted check. Either dependency selector can be combined with `--project PATH` and `--enforcement`. [Verifier options](scripts/playbook.py)

## 11. Engineering Standards and Specialist Skills

- **Reusable policy** covers architecture, frontend, UI/UX, backend and data, testing, security, Git, and tickets. **Project conventions** record decisions such as the supported stack, test commands, compatibility and accessibility targets, ADR locations, tracker rules, and required checks. Root and scoped agent guidance route by change type to the canonical docs and the project playbook index. Approved policy exceptions belong in the relevant ticket, PR, or ADR. [Standards index](standards/README.md) · [Project templates](templates/README.md)
- **The registry** records sources, reviewed revisions where available, stable IDs, triggers, phases, required status, dependencies, contracts, and compatibility limits. Bootstrap checks the stack and versions, enabled inventory, installed revision and companions, and any required tool permissions. It records the adopted playbook revision and applicable guidance in the project's existing index or `docs/standards/playbook/README.md`. Required gaps block the dependent phase. Optional gaps can use documented maintainer guidance and project checks. [Registry](registry/skills.yaml)
- **Pairing** reads that adopted guidance for the affected surface and phase, verifies the actual installed skill or approved prose reference, and uses it within the current increment. For example, Vercel composition guidance applies to React component APIs, Supabase guidance to relevant PostgreSQL work, and Thermos can supply a standalone rubric for the Standards review. Impeccable is scoped to prose references. The pairing skill owns approvals and transitions. [Upstream resolution](skills/pair-implement/references/upstream.md)
- **To add or update a specialist**, inspect the source revision and companions, update the registry contract and compatibility limits, and link the applicable standard. List effects such as scripts, downloads, and writes when defining its scope. Prefer bounded advice or a standalone review rubric when the upstream package contains its own orchestrator. Add `companion_files` for resources the verifier should check. Verify the selected entry where applicable, and adopt the approved change through bootstrap. [Maintenance guide](docs/maintenance.md#registry-changes)

## 12. Updating the Playbook

1. Review the checkout changes before updating a linked installation. Edit reusable global guidance in [global/AGENTS.md](global/AGENTS.md) and keep machine-specific prose outside the managed markers in the installed file. Preview with `./scripts/install.sh --dry-run` and apply with `./scripts/install.sh`. The installed block is a copy and needs this refresh.
2. Custom skills and their relative resources follow the symlinked checkout, including local edits. Edit the skill or metadata at its source, verify it, and start a fresh Codex session. If the checkout moved, resolve the stale links before reinstalling.
3. Update reusable standards, templates, and registry entries at their source. Unpinned checkout references follow those edits. A project's pinned links or local snapshots stay on the adopted revision until explicitly reconciled.
4. Compare upstream releases for changed entry points, templates, companion files, behavior, added tooling, and writes. Review and approve the exact revision through its distribution mechanism. Verify the active version after installation, and test tracker setup, TDD, the two review axes, and PR drafting for the workflows affected. Run the local suite and, where applicable, `./scripts/verify.sh --require <skill-id>`. [Acceptance checks](tests/README.md) · [Upstream compatibility checklist](docs/maintenance.md#upstream-revisions-and-compatibility)
5. Run `$bootstrap-project` in each affected application with the approved new revision. Review the proposed changes to project references, dependency records, and gates. Verify the resulting setup and repeat with the same inputs to check for churn.

## 13. Troubleshooting and Rollback

| Symptom | Action |
| --- | --- |
| Skills missing from Codex | Run `./scripts/verify.sh --local-only --project /path/to/project`. Check the effective profile, project trust and config, disabled skill selectors, duplicates, and the active plugin. Restart Codex and use `/skills` or the `$` picker. |
| Missing upstream dependency | Run `./scripts/verify.sh --require <skill-id>`. Check the source, active revision, and companion files. Approve installation or repair before retrying the affected phase. For optional guidance, use the recorded fallback. |
| Conflicting instructions | Inspect the project candidates reported by `--project` and read the effective global, root, and scoped instructions. Resolve shadowing or conflicting workflow rules explicitly. For an edited managed block, save a copy, move intended personal prose outside the markers, remove the old block, and preview reinstalling. |
| Broken links or resources | Inspect each skill with `readlink` and confirm the checkout and referenced files exist. For a moved checkout, remove only a confirmed stale symlink with `unlink`, then dry-run and reinstall from the new path. Restore missing resources from the approved revision. |
| Partial or failed bootstrap | Inspect the actual diff, tracker read access, prerequisites, and failed checks. Rerun `$bootstrap-project` with the same scope. Reuse approvals only when the original action and evidence still match. Approve any changed plan. |
| Unexpected autonomy or a skipped checkpoint | Stop the run, inspect the worktree, index, commits, and any remote activity. Confirm the effective workflow and invoke `$pair-implement` explicitly. Re-establish the pending action and approval scope before continuing. Use `--enforcement` to inspect configuration and `/hooks` to check hook trust. Verify any required CI and branch protection in the project host. |

To roll back, use the backup path and original mode printed by the installer. Restore the previous global file if no personal text changed since installation. Otherwise compare the backup and current file and restore only the managed portion. For a newly created file, remove the managed block and remove the file only if empty. Remove only the links created by that install after checking their targets and any other profiles sharing them. For project changes use the project's approved revert or reconciliation process. For upstream changes use the upstream distribution's rollback route. See the maintenance guide for source rollbacks and interrupted installs with stale lock directories. [Rollback procedure](docs/maintenance.md#roll-back)

## 14. Limitations

`AGENTS.md` and `SKILL.md` direct Codex to pause for explicit approval. They provide no deterministic guarantee that a model will pause, keep scope, or recover approval evidence in a fresh session. Tool approval prompts are separate from workflow approval. Sandboxes, command rules, trusted hooks, CI, and branch protection can enforce the specific operations and checks configured in their host. The installer ships no enforcement configuration. [Approval policy](global/AGENTS.md) · [Codex hooks](https://learn.chatgpt.com/docs/hooks)

The verifier is an offline inventory and file check. It can report paths, companions, some revision mismatches, instruction candidates, and enforcement configuration. Active skill selection, semantic conflicts, hook trust, tracker permissions, and behavior at checkpoints need checks in the corresponding client or project. Reference-only guidance can require direct inspection of its approved source. The acceptance suite distinguishes CLI discovery checks from authenticated model exercises. [Acceptance checks](tests/README.md)

**Implementation gaps to account for.** Bootstrap's modes are inferred from repository evidence and your prompt. Backlog review is a separate planning task. Pairing is an explicit skill with two modes and leaves merge and tracker closure to separately authorized actions. Upstream orchestration prompts can request broader actions by default. Use the active project workflow and its approval scope when invoking them.
