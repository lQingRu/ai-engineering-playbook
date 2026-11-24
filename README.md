# AI Engineering Playbook

A personal, stack-independent collaboration workflow for AI-assisted software development with Codex. Matt Pocock’s skills provide the engineering methods. This playbook adds personal working agreements and two entry points for using those methods across projects.

## Layout

```text
ai-engineering-playbook/
├── README.md
├── global/
│   └── AGENTS.md
├── standards/
├── registry/
│   └── skills.yaml
├── skills/
│   ├── pair-implement/
│   │   └── SKILL.md
│   └── bootstrap-project/
│       └── SKILL.md
├── templates/
│   └── README.md
└── scripts/
    ├── install.sh
    └── verify.sh
```

The bootstrap skill and installation scripts are planned.

## Standards and project documentation

- [`standards/`](standards/README.md) defines reusable engineering policies and links to applicable external guidance. The [skill registry](registry/skills.yaml) records approved external skills and when they apply.
- [`templates/`](templates/README.md) supplies prompts for decisions and documentation a project needs.
- The application repository owns its approved conventions and the record of what it implements. Use its existing documentation and configuration as the source of truth for the project.

## Collaboration workflow

- **Set up or document a project** with Matt Pocock’s upstream setup and the applicable [project templates](templates/README.md). Record project decisions in existing repository guidance. Use the [standards index](standards/README.md) to find policies and specialist guidance by change type.
- **Implement a task** with `pair-implement`. Start from the task’s existing issue, active spec, or request and use the relevant Matt Pocock skills. Record durable changes where the project already keeps them and follow the [specification lifecycle](standards/tickets.md#specification-lifecycle) for completed work.
- **Carry personal preferences across repositories** through `global/AGENTS.md` and the user-level skills. Each project owns its standards. Codex loads both global and project guidance when starting a session. [Codex guidance discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

## Planned installation and verification

`scripts/install.sh` will install the global guidance at `${CODEX_HOME:-$HOME/.codex}/AGENTS.md` and the custom skill folders under `$HOME/.agents/skills`. An identical rerun will be a no-op. The installer will report conflicts and preserve existing files for explicit resolution. [Codex guidance discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) · [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)

`scripts/verify.sh` will check the installed files and flag conditions that can affect discovery, such as a global `AGENTS.override.md`. Verification will also cover whether Codex discovers the guidance and the two custom skills in a fresh session.

For manual pairing use, make the playbook root reachable by linking the skill folder to this checkout, setting `AI_ENGINEERING_PLAYBOOK_ROOT` to the checkout, or supplying its path at invocation. Use Matt Pocock’s upstream distribution for its skills.

## Maintain the registry

[registry/skills.yaml](registry/skills.yaml) is the inventory of approved external skills. Optional skills apply only to the recorded task and stack. Approval covers the stated use and leaves installation and updates to a separate, explicit decision.

Review an entry when upgrading the relevant stack or skill, when a source is deprecated, or when a conflict surfaces. Compare upstream instructions and companion files, check version and artifact contracts, and look for new scripts, network calls, permissions, or writes. Verify a representative task before recording a tested revision and state what was tested. Replace or remove guidance whose scope or compatibility no longer fits. Keep framework details in upstream sources and project decisions in the application repository.
