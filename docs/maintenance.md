# Maintenance

## Registry changes

1. Open [the registry](../registry/skills.yaml) and the affected [standards](../standards/README.md). To add a skill, record the upstream repository and reviewed revision, then add the skill’s stable ID, upstream `SKILL.md` path, responsibility, trigger, phases, required status, dependencies, contract, and compatibility limits. Use `companion_files` for files the verifier should require relative to `SKILL.md`. For a requirement conditional on a phase, describe the trigger precisely. Keep reference-only scope and optional fallbacks explicit.
2. To remove a skill, find its ID in standards, templates, workflows, and project adoption records. Update affected guidance and agree on a fallback or replacement for required uses. Remove the registry entry and remove the source entry if it has no remaining skills. Removing an entry changes future selection. Uninstalling a third-party skill and changing an existing project’s approved workflow each require approval.
3. Run the [acceptance suite](../tests/README.md). Use `verify.sh --require <id>` against a disposable installation for a selected skill, where applicable. Reference-only usage may instead require inspecting a reviewed checkout directly.

## Upstream revisions and compatibility

- Fetch upstream into a disposable checkout or compare release contents in the upstream repository. Compare the old and candidate revisions of instructions, companion files, metadata, scripts, hooks, artifact paths, tool and permission requirements, and framework or runtime assumptions.
- For Matt Pocock upgrades, check the setup contract against both a fresh project and existing `## Agent skills` pointers. Exercise the applicable tracker, triage, and domain templates, TDD companions, separate Standards and Spec review, and PR drafting. Confirm named entry points and explicit-only behavior in the supported Codex client. For any external reviewer, keep its role inside the project’s approved review scope.
- Record `reviewed_revision` after reviewing source. Use a release tag or commit SHA. Record test evidence separately in the registry’s verification note or linked review, with the exact revision, client and relevant stack versions, cases, and results. A packaged cache version, a Git commit, and a source review establish different evidence. If the revision of a standalone copy cannot be established, record it as unverified.
- Update affected registry entries and references together. Preview the project impact and get approval for the exact third-party version before using the upstream installation or upgrade mechanism. Check the active version after the change. The playbook scripts perform local reads and install only their own files and links.

## Personal configuration

- Put machine-specific preferences outside the managed markers in the global `AGENTS.md`. Put reusable preferences in [global/AGENTS.md](../global/AGENTS.md), preview with `install.sh --dry-run`, and rerun the installer after reviewing. The installer preserves text outside the block and stops when the block was edited. To resolve an edited block, back it up, keep the intended personal lines outside the markers, and remove the old managed block before reinstalling.
- Manage the Codex profile and optional rules or hooks through Codex configuration. Run `verify.sh --enforcement` to inspect local files and `/hooks` to check whether definitions are trusted. Review effective instructions with project-specific guidance in mind. Resolve differences in workflow or approval expectations explicitly.
- Skill links follow the live checkout, including local edits. Review changes before updating that checkout. Use a stable checkout at an approved revision when you want to control when changes take effect. An installed path collision, including a link to a moved checkout, requires manual resolution after checking the link target.

## Reconcile existing projects

1. Run `$bootstrap-project` in the target repository and supply the approved new playbook revision. Compare it with the project’s current adoption record and working configuration.
2. Review the proposed change list. Keep existing tracker, domain, and standards decisions unless the reconciliation explicitly changes them. Prefer stable links pinned to a revision, or an approved local snapshot when readers lack access. Update the project’s adoption record, guidance pointers, and approved gaps together. Approve installation, tracker actions, and enforcement changes within their own scope.
3. Verify links, enabled skills, and approved checks. Re-run reconciliation with the same inputs. Expect no new writes when the adopted setup is complete.

## Roll back

1. Record the links and backup path printed by the installer. If the previous global file is unchanged outside the managed block since installation, restore the named `playbook-backups/AGENTS.md.*` over the installed file and keep the original mode reported during installation. The backup contains the exact previous bytes. If personal edits followed installation, compare the backup and current file and restore only the managed portion. For a newly created global file, remove only the managed block and remove the file itself if it is empty.
2. For a first-install rollback, remove only the links created by that invocation. Confirm each path is a symlink under `$HOME/.agents/skills` and `readlink` points to the expected checkout’s matching skill directory. Use `unlink` on the link itself. Other Codex profiles in the same home share those links, so check they can tolerate removal.
3. To roll back a playbook source update, return the linked checkout to the prior reviewed revision after preserving any local changes. Restore or regenerate the corresponding managed block, then verify and start a fresh session. Use the project’s normal approved revert or reconciliation process for committed project changes and its upstream distribution mechanism for separately approved third-party rollbacks.
4. If an interrupted install left `.engineering-playbook-install.lock` under the Codex profile or `$HOME/.agents`, confirm no installer is running, inspect the managed block, backups, and skill links, then remove the empty lock directory and rerun the dry run. An interrupted first install may leave valid links for the next run to reuse.
