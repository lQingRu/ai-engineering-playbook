# AI Engineering Playbook

A personal collaboration workflow for Codex. Matt Pocock’s skills provide the engineering methods. This playbook adds personal working agreements, reusable [standards](standards/README.md), [project templates](templates/README.md), and two explicit workflow entry points.

## Install

Keep the checkout at a stable location. The scripts use a POSIX shell, Git, and Python 3.11+ with PyYAML. If needed, install PyYAML in a virtual environment of your choice and set `PYTHON` to its interpreter.

```sh
./scripts/install.sh --dry-run
./scripts/install.sh
./scripts/verify.sh
```

Review the dry run before applying it. The installer merges one managed block into `${CODEX_HOME:-$HOME/.codex}/AGENTS.md`, backs up the previous file when it changes, and symlinks the two custom skills under `$HOME/.agents/skills`. The links keep each skill’s references and playbook resources accessible from the checkout. Existing Codex configuration, plugins, and other skills stay in place. Identical reruns are no-ops. Install Matt Pocock’s framework separately through its supported distribution after reviewing the revision and approving the change. [Codex instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md) · [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) · [Approved registry](registry/skills.yaml)

## Use in a project

- Start a fresh Codex session in the target repository. Use `/skills` or type `$` to find the two entry points.
- Run `$bootstrap-project` to set up a new project or reconcile an existing one. Review its proposed paths, standards, dependencies, and quality gates before approving edits. Bootstrap selects guidance by the actual stack, task, and workflow. Approve third-party installs and tracker writes separately.
- Run `$pair-implement <ticket>` for one ticket. Approve a named increment when the workflow ends its discovery turn. Review the resulting diff before separately approving a commit or PR publication. In a fresh session, confirm any pending action whose prior approval cannot be established.

## Verify and troubleshoot

- `./scripts/verify.sh --local-only` checks global guidance, custom skill links and invocation metadata, plus playbook resources. The default check also inspects the inventory of potentially required upstream skills. Repeat `--require ID` to check the dependencies selected for a project or task.
- Add `--project /path/to/project` to inspect project instruction routing and name collisions. Add `--enforcement` to inspect local hook, rule, sandbox, and approval configuration.
- Resolve reported overrides, duplicate skills, disabled entries, edited managed blocks, and broken paths before proceeding. Compare instruction prose for conflicts and use a fresh session to confirm enabled skills and effective guidance. A plugin cache gives static evidence about its contents. Confirm the active distribution in Codex.
- Inspect `/hooks` for trust and verify required checks with the project’s CI or branch protection. The Markdown checkpoints guide the session. Tool, hook, and CI controls cover the operations they are configured to enforce. [Codex hook configuration](https://learn.chatgpt.com/docs/hooks)

## Maintain

Use the [maintenance guide](docs/maintenance.md) to review upstream changes, update the registry, revise personal preferences, reconcile adopted project versions, and roll back an installation. The [acceptance checks](tests/README.md) describe the disposable-home suite and how to exercise model behavior in an isolated session.
