# Acceptance checks

From the checkout, run with the Python environment used for installation.

```sh
python -B -m unittest discover -s tests -v
PLAYBOOK_TEST_CODEX=1 python -B -m unittest discover -s tests -v
```

The suite creates separate temporary homes and profiles, mock skill fixtures, and disposable Git repositories. It checks dry-run, fresh and repeated installs, managed updates, exact instruction and configuration preservation, backups and rollback, missing required skills and companions, broken links, conflicts, and optional enforcement file inspection. The optional CLI test uses `app-server` with an unreachable loopback model endpoint and runs `debug prompt-input`. It checks discovery in new React and existing Vue repositories, profile precedence, project and global instruction loading, and explicit invocation of both skills alongside their exclusion from the implicit catalog. It also checks that a fresh pairing turn receives the approval resumption instructions. It was exercised with Codex CLI 0.171.0.

## Model-driven acceptance

Run these cases in disposable repositories with an authenticated test Codex profile and the reviewed Matt Pocock distribution. Use a local Markdown tracker and local Git only. Start with a clean Git baseline or otherwise save a before snapshot. At each checkpoint inspect the worktree, index, and history as well as the response. Record the client and model version, the installed playbook and upstream revisions, the prompts, and the observed changes.

| Case | Exercise | Pass condition |
| --- | --- | --- |
| New project and React selection | Make a new repository with a `package.json` declaring React 19 and no implemented product. Invoke `$bootstrap-project` for a reusable React component API and a rendering-performance question using a local tracker. Approve named documentation or setup changes after previewing them. | The first turn ends at the approval checkpoint. The proposal identifies the applicable React composition and performance guidance, scopes it to its triggers, and labels product designs as planned. After scoped approval, the diff contains only approved changes. Repeating with the same inputs produces no writes. |
| Existing project and non-React selection | Create a Vue repository with a working component, an existing `AGENTS.md`, a local tracker pointer and corresponding file, and one real documentation gap. Invoke `$bootstrap-project` for that gap. | The plan preserves the existing tracker and conventions, ties current capability claims to source, and scopes guidance to Vue. After approving only the named gap, confirm that baseline files and unrelated setup are preserved. Re-run and confirm no writes. |
| Dependency approval | In either fixture leave a required skill absent or disabled. Approve documentation only. | The response identifies the missing prerequisite, affected workflow, and candidate revision if known. The skill remains uninstalled and dependent work stays pending. Independent approved documentation can proceed. |
| Implementation, commit, and publication checkpoints | Add an unblocked local ticket and invoke `$pair-implement <ticket>`. Approve one named increment and test seam, then wait at review before giving commit approval. For a PR scenario, use a disposable target with no external publication credentials. | Discovery makes no edits. The approved implementation changes only its scope and review ends before staging or commit. After explicit commit approval, only the reviewed candidate is committed. A publication proposal stops for its own approval. |
| Fresh session without approval evidence | Leave an identifiable pending diff in the pairing fixture and start a new session without the earlier transcript. Invoke the same ticket with “continue”. Repeat with a partially reconciled bootstrap. | The agent re-reads the ticket or project and actual Git state, identifies pending work, and asks for scoped approval before the next write or commit. It treats existing files and commits as progress evidence and leaves unrelated edits intact. |

The model-driven cases require judgment about agent behavior. The isolated CLI checks establish discovery and model input. An authenticated model turn is needed to observe workflow selection, edits, checkpoint compliance, or approval handling on resumption.
