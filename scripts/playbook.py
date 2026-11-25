"""Local installation and offline inspection for the engineering playbook."""

import argparse
from contextlib import ExitStack, contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import tomllib
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError:
    sys.exit("Install PyYAML in your chosen Python 3.11+ environment and set PYTHON to its interpreter.")

ROOT = Path(__file__).resolve().parents[1]
CUSTOM = ("bootstrap-project", "pair-implement")
MARKER = "ai-engineering-playbook"
END = f"<!-- END {MARKER} -->"
BEGIN = re.compile(rf"(?m)^<!-- BEGIN {MARKER} sha256=([a-f0-9]{{64}}) -->\r?\n")
LOCAL_LINK = re.compile(r"\]\((<[^>\n]+>|[^\s)]+)(?:\s+\"[^\n]*\")?\)")
PLUGIN = "mattpocock-skills@mattpocock"


class Conflict(Exception):
    pass


def require(condition, message):
    if not condition:
        raise Conflict(message)


def warn(message):
    print(f"WARNING: {message}")


def read_yaml(path):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"Expected a YAML mapping in {path}")
    return data


def metadata(path):
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^---[ \t]*$", text, maxsplit=2)
    require(len(parts) == 3 and not parts[0].strip(), f"Missing YAML frontmatter in {path}")
    data = yaml.safe_load(parts[1])
    require(isinstance(data, dict), f"Invalid YAML frontmatter in {path}")
    for key in ("name", "description"):
        require(isinstance(data.get(key), str) and data[key].strip(),
                f"Missing or empty {key} in {path}")
    return data


def links(path):
    errors = []
    text = path.read_text(encoding="utf-8")
    # Check inline Markdown links outside fenced code. Remote URLs are offline.
    text = re.sub(r"(?ms)^ *```[^\n]*\n.*?^ *```[^\n]*", "", text)
    for match in LOCAL_LINK.finditer(text):
        target = match[1].strip("<>")
        url = urlsplit(target)
        if url.scheme or url.netloc:
            continue
        dest = path.parent / unquote(url.path) if url.path else path
        if not dest.exists():
            errors.append(f"{path}: broken local link {target}")
        elif url.fragment and dest.is_file() and dest.suffix.lower() == ".md":
            headings = re.findall(r"(?m)^#{1,6} +(.+?) *#* *$", dest.read_text(encoding="utf-8"))
            anchors = {re.sub(r"[^\w -]", "", name.lower()).replace(" ", "-") for name in headings}
            if unquote(url.fragment) not in anchors:
                errors.append(f"{path}: missing heading {target}")
    return errors


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def managed_text(before, body):
    match = BEGIN.search(before)
    if match:
        require(before.count(f"<!-- BEGIN {MARKER}") == 1 and before.count(END) == 1,
                "Duplicate or malformed managed instruction markers")
        stop = before.find(END, match.end())
        require(stop >= 0 and before[stop - 1:stop] == "\n", "Unclosed managed instruction block")
        require(digest(before[match.end():stop]) == match[1],
                "Managed instruction block was edited. Review and reconcile it before installing.")
        prefix, suffix = before[:match.start()], before[stop + len(END):]
    else:
        require(f"<!-- BEGIN {MARKER}" not in before and END not in before,
                "Malformed managed instruction markers")
        prefix = before + ("\n\n" if before else "")
        suffix = "\n"
    # Legacy hand-installed guidance needs an intentional merge.
    require("# Personal Engineering Preferences" not in prefix + suffix,
            "Overlapping unmanaged playbook instructions. Review the existing global file first.")
    return f"{prefix}<!-- BEGIN {MARKER} sha256={digest(body)} -->\n{body}{END}{suffix}"


def directories(root):
    if not root.is_dir():
        return
    seen = set()
    for current, children, files in os.walk(root, followlinks=True):
        real = Path(current).resolve()
        if real in seen or (Path(current).name.startswith(".") and Path(current) != root):
            children[:] = []
            continue
        seen.add(real)
        if "SKILL.md" in files:
            yield Path(current) / "SKILL.md"
            children[:] = []


def inventory(roots, names):
    matches = {name: {} for name in names}
    for root in dict.fromkeys(roots):
        for path in directories(root):
            try:
                name = metadata(path)["name"]
            except (Conflict, OSError, UnicodeError, yaml.YAMLError):
                # Invalid metadata at an expected destination is checked separately.
                continue
            if name in matches:
                matches[name].setdefault(path.resolve(), path)
    return matches


def load_config(path):
    if not os.path.lexists(path):
        return {}
    config = tomllib.loads(path.read_text(encoding="utf-8"))
    for key in ("skills", "plugins", "hooks"):
        require(isinstance(config.get(key, {}), dict), f"{path}: {key} must be a table")
    rules = config.get("skills", {}).get("config", [])
    require(isinstance(rules, list), f"{path}: skills.config must be an array of tables")
    for rule in rules:
        require(isinstance(rule, dict) and type(rule.get("enabled", True)) is bool,
                f"{path}: skill selectors take a boolean enabled setting")
        selectors = [rule[key] for key in ("name", "path") if key in rule]
        require(len(selectors) == 1 and isinstance(selectors[0], str) and selectors[0].strip(),
                f"{path}: each skill rule needs one name or path selector")
    fallbacks = config.get("project_doc_fallback_filenames", [])
    require(isinstance(fallbacks, list) and all(isinstance(value, str) for value in fallbacks),
            f"{path}: project_doc_fallback_filenames must be an array of strings")
    return config


def enabled(name, path, configs, *aliases):
    result = True
    paths = {candidate.resolve() for candidate in (path, *aliases)}
    for config in configs:
        for rule in config.get("skills", {}).get("config", []):
            selector = rule.get("path")
            by_path = selector and Path(selector).is_absolute() and Path(selector).resolve() in paths
            if rule.get("name") == name or by_path:
                result = rule.get("enabled", True)
    return result


def git(path, *args):
    result = subprocess.run(["git", "-C", str(path), *args], capture_output=True, text=True,
                            check=False, env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
    return result.stdout.strip() if result.returncode == 0 else ""


def revision(file):
    parent = file if file.is_dir() else file.parent
    ref = git(parent, "rev-parse", "HEAD")
    if not ref:
        return "", ""
    tag = git(parent, "describe", "--exact-match", "--tags", "HEAD")
    dirty = git(parent, "status", "--porcelain", "--", "." if file.is_dir() else file.name)
    return ref, f"{ref}{f' ({tag})' if tag else ''}{' with local changes' if dirty else ''}"


def resources():
    required = [
        ROOT / "standards/README.md", ROOT / "templates/README.md",
        ROOT / "templates/project-AGENTS.md", ROOT / "registry/skills.yaml", ROOT / "global/AGENTS.md",
    ]
    for path in required:
        require(path.is_file(), f"Missing resource {path}")
    registry = read_yaml(required[3])
    sources, skills = registry.get("sources"), registry.get("skills")
    require(isinstance(sources, dict) and isinstance(skills, dict), "Registry needs sources and skills mappings")
    for name, source in sources.items():
        require(isinstance(source, dict) and str(source.get("repository", "")).startswith("https://"),
                f"Registry source {name} needs an HTTPS repository")
    for name, entry in skills.items():
        require(isinstance(entry, dict) and entry.get("source") in sources, f"Invalid registry source for {name}")
        for field in ("responsibility", "applies_when", "contract", "compatibility"):
            require(isinstance(entry.get(field), str) and entry[field].strip(), f"Missing {name}.{field}")
        require(type(entry.get("required")) is bool, f"Expected a boolean for {name}.required")
        for field in ("phases", "dependencies", "companion_files"):
            values = entry.get(field, [] if field == "companion_files" else None)
            require(isinstance(values, list) and all(isinstance(value, str) and value for value in values),
                    f"Expected a string list for {name}.{field}")
        for item in [entry.get("path"), *entry.get("companion_files", [])]:
            require(isinstance(item, str) and item and not Path(item).is_absolute() and ".." not in Path(item).parts,
                    f"Invalid registry resource path for {name}: {item}")
        require(Path(entry["path"]).name == "SKILL.md", f"Expected a SKILL.md path for {name}")
    for name in CUSTOM:
        skill = ROOT / "skills" / name
        require(metadata(skill / "SKILL.md")["name"] == name, f"Unexpected skill name in {skill}")
        policy = read_yaml(skill / "agents/openai.yaml").get("policy")
        require(isinstance(policy, dict) and policy.get("allow_implicit_invocation") is False,
                f"{name} needs policy.allow_implicit_invocation: false in agents/openai.yaml")
    issues = [
        issue
        for folder in ("standards", "templates", "skills", "global")
        for path in sorted((ROOT / folder).rglob("*.md"))
        for issue in links(path)
    ]
    require(not issues, "\n".join(issues))
    return registry


class Layout:
    def __init__(self):
        home = Path.home().resolve()
        self.codex = Path(os.environ.get("CODEX_HOME") or home / ".codex").expanduser().resolve()
        self.user_skills = home / ".agents/skills"
        self.skill_roots = [self.user_skills, self.codex / "skills", Path("/etc/codex/skills")]
        self.instructions = self.codex / "AGENTS.md"
        for path in (self.codex, self.user_skills):
            require(not os.path.lexists(path) or path.is_dir(), f"Expected a directory at {path}")
        self.config = load_config(self.codex / "config.toml")
        override = self.codex / "AGENTS.override.md"
        if os.path.lexists(override):
            require(override.is_file(), f"Invalid global override {override}")
            require(not override.read_text(encoding="utf-8").strip(),
                    f"Global instructions shadowed by {override}. Decide how to merge before continuing.")
        require(not self.instructions.is_symlink(), f"Resolve symlinked global file manually: {self.instructions}")

    def plan(self):
        # Decode bytes directly so existing CRLF and missing final newlines survive.
        before = self.instructions.read_bytes().decode("utf-8") if self.instructions.exists() else ""
        body = (ROOT / "global/AGENTS.md").read_text(encoding="utf-8").rstrip() + "\n"
        # JSON encoding preserves the absolute path even when it contains spaces or quotes.
        body += f"\nPlaybook checkout: {json.dumps(str(ROOT), ensure_ascii=False)}. Use it to resolve standards, templates, and the registry.\n"
        after = managed_text(before, body)
        limit = self.config.get("project_doc_max_bytes", 32768)
        require(type(limit) is int and limit >= 0, "project_doc_max_bytes must be a non-negative integer")
        require(len(after.encode("utf-8")) <= limit, f"Global file would exceed project_doc_max_bytes ({limit})")
        roots = inventory(self.skill_roots, CUSTOM)
        missing = []
        for name in CUSTOM:
            source = ROOT / "skills" / name
            target = self.user_skills / name
            if os.path.lexists(target):
                require(target.is_symlink() and target.resolve() == source,
                        f"Skill destination conflict at {target}. Preserve or relocate the existing skill manually.")
            else:
                missing.append((target, source))
            duplicates = set(roots[name]) - {source / "SKILL.md"} if target.is_symlink() else set(roots[name])
            require(not duplicates, f"Duplicate {name} in another skill location: {', '.join(map(str, sorted(duplicates)))}")
            require(enabled(name, target / "SKILL.md", [self.config], source / "SKILL.md"),
                    f"{name} is disabled in {self.codex / 'config.toml'}")
        return before, after, missing


def install(layout, dry_run):
    def report(before, after, missing):
        if before != after:
            print(f"Merge managed instructions into {layout.instructions}")
            if layout.instructions.exists():
                print(f"Back up the previous file under {layout.codex / 'playbook-backups'}")
            if before:
                warn("Review existing personal prose for conflicting instructions before applying the merge.")
        for target, source in missing:
            print(f"Link {target} -> {source}")
        if before == after and not missing:
            print("Already installed. No changes.")

    if dry_run:
        report(*layout.plan())
        return

    # Validate before creating any profile files. The skill root is shared
    # between profiles and a profile can also be shared between home directories.
    before, after, missing = layout.plan()
    if before == after and not missing:
        report(before, after, missing)
        return
    layout.codex.mkdir(parents=True, exist_ok=True)
    layout.user_skills.parent.mkdir(parents=True, exist_ok=True)
    with ExitStack() as locks:
        for parent in dict.fromkeys(path.resolve() for path in (layout.codex, layout.user_skills.parent)):
            locks.enter_context(install_lock(parent))
        apply_install(Layout(), report)


@contextmanager
def install_lock(parent):
    lock = parent / ".engineering-playbook-install.lock"
    try:
        lock.mkdir()
    except FileExistsError as error:
        raise Conflict(f"Another installation may be active. Inspect {lock}") from error
    try:
        yield
    finally:
        lock.rmdir()


def apply_install(layout, report):
    created = []
    try:
        before, after, missing = layout.plan()
        report(before, after, missing)
        if missing:
            layout.user_skills.mkdir(parents=True, exist_ok=True)
        for target, source in missing:
            target.symlink_to(source, target_is_directory=True)
            created.append(target)
        if before != after:
            path = layout.instructions
            existed = path.exists()
            current = path.read_bytes() if existed else b""
            require(not path.is_symlink() and current == before.encode("utf-8"),
                    f"Global instructions changed during installation: {path}")
            mode = stat.S_IMODE(path.stat().st_mode) if existed else 0o600
            if existed:
                backups = layout.codex / "playbook-backups"
                backups.mkdir(mode=0o700, exist_ok=True)
                with tempfile.NamedTemporaryFile(dir=backups, prefix="AGENTS.md.", delete=False) as backup:
                    backup.write(current)
                print(f"Backup: {backup.name} (original mode {mode:o})")
            with tempfile.TemporaryDirectory(dir=layout.codex, prefix=".playbook-") as directory:
                candidate = Path(directory) / "AGENTS.md"
                candidate.write_bytes(after.encode("utf-8"))
                candidate.chmod(mode)
                candidate.replace(path)
    except (Exception, KeyboardInterrupt):
        for path in reversed(created):
            if path.is_symlink() and path.resolve() == ROOT / "skills" / path.name:
                path.unlink()
        raise


def project_paths(project):
    if project is None:
        return []
    require(project.is_dir(), f"Project directory does not exist: {project}")
    git_root = git(project, "rev-parse", "--show-toplevel")
    root = Path(git_root).resolve() if git_root else project
    return [root, *(root / part for part in reversed(project.relative_to(root).parents) if part != Path(".")),
            *([project] if root != project else [])]


def verify(layout, args, registry):
    before, after, missing = layout.plan()
    errors = []
    if before != after:
        errors.append(f"Missing or stale managed instructions in {layout.instructions}. Run install.sh --dry-run.")
    if layout.instructions.is_file():
        errors.extend(links(layout.instructions))
    if missing:
        errors.extend(f"Missing user skill: {target}" for target, _ in missing)

    project = args.project.resolve() if args.project else None
    directories = project_paths(project)
    configs = [layout.config]
    for path in directories:
        config_path = path / ".codex/config.toml"
        if config_path.is_file():
            warn(f"Project config {config_path} considered statically. Codex trust determines whether it loads.")
            configs.append(load_config(config_path))
        override, normal = (path / name for name in ("AGENTS.override.md", "AGENTS.md"))
        candidates = [override, normal]
        for config in configs:
            candidates.extend(path / name for name in config.get("project_doc_fallback_filenames", []))
        for file in candidates:
            if file.is_symlink() and not file.is_file():
                errors.append(f"Broken instruction path: {file}")
        active = [file for file in dict.fromkeys(candidates)
                  if file.is_file() and file.read_text(encoding="utf-8").strip()]
        if active:
            print(f"Project instruction candidate: {active[0]}")
            errors.extend(links(active[0]))
        if len(active) > 1:
            warn(f"{active[0]} shadows {', '.join(map(str, active[1:]))}. Review effective guidance.")

    roots = [*layout.skill_roots, *(path / ".agents/skills" for path in directories)]
    packages = []
    plugin = layout.config.get("plugins", {}).get(PLUGIN, {})
    require(isinstance(plugin, dict), f"Expected a plugin configuration table for {PLUGIN}")
    if plugin.get("enabled") is True:
        packages = sorted(path for path in (layout.codex / "plugins/cache/mattpocock/mattpocock-skills").glob("*")
                          if (path / "skills").is_dir())
        if packages:
            warn("Configured Matt Pocock plugin cache inspected. Confirm the active version in Codex.")
        if len(packages) > 1:
            warn("Multiple Matt Pocock cache revisions. Static checks cannot select the active version.")
    tracked = registry["skills"]
    selected = [] if args.local_only else args.require or [name for name, entry in tracked.items() if entry["required"]]
    unknown = set(selected) - tracked.keys()
    require(not unknown, f"Registry has no entries for: {', '.join(sorted(unknown))}")
    inventory_roots = roots + [path / "skills" for path in packages]
    found = inventory(inventory_roots, [*CUSTOM, *selected])

    for name in CUSTOM:
        target = layout.user_skills / name / "SKILL.md"
        different = set(found[name]) - {target.resolve()}
        if different:
            errors.append(f"Duplicate {name}: {', '.join(map(str, sorted(different)))}")
        if not enabled(name, target, configs):
            errors.append(f"{name} is disabled in inspected configuration")

    for name in dict.fromkeys(selected):
        entry = tracked[name]
        hits = [file for file in found[name].values() if enabled(name, file, configs)]
        if len(hits) != 1:
            state = "missing or disabled" if not hits else "ambiguous: " + ", ".join(map(str, hits))
            errors.append(f"{name} ({entry['source']}, {', '.join(entry['phases'])}): {state}")
            continue
        path = hits[0]
        real = path.resolve()
        source = registry["sources"][entry["source"]]
        package = next((p for p in packages if path.is_relative_to(p)), None)
        if package:
            expected = package / entry["path"]
            if not expected.is_file() or expected.resolve() != real:
                errors.append(f"{name}: expected registry path {expected}, found {path}")
        for companion in entry.get("companion_files", []):
            if not (real.parent / companion).is_file():
                errors.append(f"{name}: missing companion {real.parent / companion}")
        errors.extend(links(real))
        reviewed = source.get("reviewed_revision")
        commit, label = revision(real.parent)
        tag = git(real.parent, "describe", "--tags", "--exact-match", "HEAD") if commit else ""
        package_release = package.name.removeprefix("v") if package else ""
        observed = label or "unknown"
        if package_release:
            observed = f"cache {package_release}, Git {observed}"
        print(f"{name}: {path} | observed {observed} | reviewed {reviewed or 'unrecorded'}")
        if reviewed and package_release and reviewed.startswith("v") and reviewed[1:] != package_release:
            errors.append(f"{name}: cache release differs from reviewed {reviewed}")
        elif reviewed and commit and re.fullmatch(r"[0-9a-f]{40}", reviewed) and commit != reviewed:
            errors.append(f"{name}: Git revision differs from reviewed {reviewed}")
        elif reviewed and reviewed not in (commit, tag) and package_release != reviewed.removeprefix("v"):
            warn(f"{name}: installed content could not be tied to the reviewed revision.")
        if "with local changes" in label:
            warn(f"{name}: installed skill files have local changes. Review before use.")

    if args.enforcement:
        for config in configs:
            for field in ("approval_policy", "sandbox_mode"):
                if field in config:
                    print(f"Configured {field}: {config[field]}")
            inline = config.get("hooks", {})
            events = [name for name in inline if name != "state"]
            if events:
                print(f"Inline hook entries: {', '.join(sorted(events))}")
        state = layout.config.get("hooks", {}).get("state", {})
        if state:
            print(f"Found {len(state)} hook state record(s) in user config. Check trust in Codex.")
        for base in [Path("/etc/codex"), layout.codex, *(path / ".codex" for path in directories)]:
            hooks = base / "hooks.json"
            if hooks.exists():
                data = json.loads(hooks.read_text(encoding="utf-8"))
                require(isinstance(data, dict) and isinstance(data.get("hooks"), dict),
                        f"Expected a hooks object in {hooks}")
                print(f"Hook configuration: {hooks}")
            for rule in sorted((base / "rules").glob("*.rules")):
                print(f"Rule file: {rule}")
        print("Enforcement inspection covers file presence and basic config. Confirm trusted hooks, tool decisions, and CI gates in their respective hosts.")

    if errors:
        raise Conflict("\n".join(errors))
    print(f"Playbook checkout revision: {revision(ROOT)[1] or 'unverifiable'}")
    print("Static checks passed. Review instruction prose for semantic conflicts, and check project workflow and approvals in a fresh Codex session.")


def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    installer = commands.add_parser("install", help="Merge global guidance and link the two custom user skills")
    installer.add_argument("--dry-run", action="store_true", help="Show proposed changes without writing files")
    verifier = commands.add_parser("verify", help="Inspect local installation and configuration without running skills")
    verifier.add_argument("--project", type=Path, help="Inspect instruction and skill routing for this project directory")
    scope = verifier.add_mutually_exclusive_group()
    scope.add_argument("--local-only", action="store_true", help="Skip upstream presence checks")
    scope.add_argument("--require", action="append", metavar="ID",
                       help="Check specific registry IDs instead of the full required inventory; repeat to add IDs")
    verifier.add_argument("--enforcement", action="store_true", help="Inspect optional local hooks, rules and settings")
    args = parser.parse_args()
    try:
        registry = resources()
        layout = Layout()
        if args.command == "install":
            install(layout, args.dry_run)
        else:
            verify(layout, args, registry)
    except (Conflict, OSError, UnicodeError, ValueError, yaml.YAMLError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
