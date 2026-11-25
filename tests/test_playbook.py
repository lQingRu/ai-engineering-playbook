"""Isolated acceptance checks. Set PLAYBOOK_TEST_CODEX=1 for local CLI checks."""

import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
CUSTOM = {"bootstrap-project", "pair-implement"}


def skill(path, name):
    path.mkdir(parents=True, exist_ok=True)
    (path / "SKILL.md").write_text(f"---\nname: {name}\ndescription: Acceptance fixture\n---\n")


class PlaybookTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="playbook acceptance ")
        self.addCleanup(temporary.cleanup)
        self.temp = Path(temporary.name).resolve()
        self.home, self.profile = self.temp / "home", self.temp / "codex profile"
        self.home.mkdir()
        self.profile.mkdir()
        self.env = {**os.environ, "HOME": str(self.home), "CODEX_HOME": str(self.profile),
                    "PYTHON": sys.executable, "TMPDIR": str(self.temp)}
        for key in ("OPENAI_API_KEY", "CODEX_API_KEY", "AI_ENGINEERING_PLAYBOOK_ROOT"):
            self.env.pop(key, None)
        self.skills = self.home / ".agents/skills"
        self.instructions = self.profile / "AGENTS.md"

    def run_script(self, script, *args, cwd=ROOT, message=None, ok=True):
        result = subprocess.run([str(cwd / "scripts" / f"{script}.sh"), *map(str, args)],
                                cwd=cwd, env=self.env, text=True, capture_output=True, timeout=20)
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0 if ok else 1, output)
        if message:
            self.assertIn(message, output)
        return output

    def test_fresh_default_home_and_repeated_installation(self):
        self.env.pop("CODEX_HOME")
        self.run_script("install", "--dry-run", message="Merge managed instructions")
        self.assertEqual(list(self.home.iterdir()), [])
        self.run_script("install")
        self.assertEqual({path.name for path in self.skills.iterdir()}, CUSTOM)
        for name in CUSTOM:
            self.assertEqual((self.skills / name).resolve(), ROOT / "skills" / name)
        global_file = self.home / ".codex/AGENTS.md"
        before = global_file.stat().st_mtime_ns, global_file.read_bytes()
        self.run_script("install", message="No changes")
        self.assertEqual((global_file.stat().st_mtime_ns, global_file.read_bytes()), before)
        self.assertFalse((global_file.parent / "playbook-backups").exists())
        self.run_script("verify", "--local-only")

    def test_merge_backup_and_preserve_personal_config(self):
        original = b"# Personal notes\r\n\r\nKeep this line"
        self.instructions.write_bytes(original)
        self.instructions.chmod(0o640)
        config = self.profile / "config.toml"
        config.write_text('approval_policy = "on-request"\n')
        plugin = self.profile / "plugins/cache/mattpocock/mattpocock-skills/1.3.2"
        sentinel = plugin / "sentinel"
        plugin.mkdir(parents=True)
        sentinel.write_text("upstream content")
        self.run_script("install")
        self.assertTrue(self.instructions.read_bytes().startswith(original))
        self.assertEqual(self.instructions.stat().st_mode & 0o777, 0o640)
        backup, = (self.profile / "playbook-backups").iterdir()
        self.assertEqual(backup.read_bytes(), original)
        self.assertEqual(config.read_text(), 'approval_policy = "on-request"\n')
        self.assertEqual(sentinel.read_text(), "upstream content")
        self.run_script("install", message="No changes")
        self.assertEqual(list(backup.parent.iterdir()), [backup])

        # The documented immediate rollback uses the backup and removes links
        # created by the invocation, preserving the surrounding configuration.
        shutil.copyfile(backup, self.instructions)
        for name in CUSTOM:
            (self.skills / name).unlink()
        self.assertEqual(self.instructions.read_bytes(), original)
        self.assertEqual(sentinel.read_text(), "upstream content")
        self.run_script("verify", "--local-only", ok=False, message="Missing or stale managed instructions")

    def test_missing_required_dependencies_and_companions(self):
        self.run_script("install")
        output = self.run_script("verify", ok=False, message="setup-matt-pocock-skills")
        self.assertIn("tdd", output)
        self.assertNotIn("vercel-react-best-practices", output)
        tdd = self.skills / "tdd"
        skill(tdd, "tdd")
        self.run_script("verify", "--require", "tdd", ok=False, message="missing companion")
        for file in ("tests.md", "mocking.md"):
            (tdd / file).write_text("# Fixture\n")
        self.run_script("verify", "--require", "tdd", message="observed unknown")
        self.run_script("verify", "--require", "tdd", "--require", "pr", ok=False, message="pr (matt-pocock")

    def test_local_resource_breakage_blocks_install_and_verify(self):
        checkout = self.temp / "checkout copy"
        shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        self.run_script("install", cwd=checkout)
        template = checkout / "templates/docs/product.md"
        template.unlink()
        for command, args in (("install", ("--dry-run",)), ("verify", ("--local-only",))):
            self.run_script(command, *args, cwd=checkout, ok=False, message="broken local link docs/product.md")

    def test_managed_update_preserves_personal_changes(self):
        checkout = self.temp / "checkout copy"
        shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        self.run_script("install", cwd=checkout)
        before = self.instructions.read_bytes() + b"\n# Local preferences\n"
        self.instructions.write_bytes(before)
        global_source = checkout / "global/AGENTS.md"
        global_source.write_text(global_source.read_text() + "\n- Updated reusable preference.\n")
        self.run_script("verify", "--local-only", cwd=checkout, ok=False, message="stale managed instructions")
        self.run_script("install", cwd=checkout, message="Backup:")
        backup, = (self.profile / "playbook-backups").iterdir()
        self.assertEqual(backup.read_bytes(), before)
        self.assertIn(b"Updated reusable preference.", self.instructions.read_bytes())
        self.assertTrue(self.instructions.read_bytes().endswith(b"\n# Local preferences\n"))
        self.run_script("install", cwd=checkout, message="No changes")
        self.run_script("verify", "--local-only", cwd=checkout)

    def test_shadow_duplicate_disable_and_edited_block(self):
        override = self.profile / "AGENTS.override.md"
        override.write_text("Global override")
        self.run_script("install", ok=False, message="shadowed")
        override.write_text("")
        legacy = self.profile / "skills/other-name"
        skill(legacy, "pair-implement")
        self.run_script("install", ok=False, message="Duplicate pair-implement")
        shutil.rmtree(legacy)
        config = self.profile / "config.toml"
        config.write_text('[[skills.config]]\nname = "bootstrap-project"\nenabled = false\n')
        self.run_script("install", ok=False, message="is disabled")
        self.assertFalse(self.instructions.exists())
        config.unlink()
        self.run_script("install")
        self.instructions.write_text(self.instructions.read_text().replace("Optimise", "Prioritise", 1))
        self.run_script("install", ok=False, message="was edited")

    def fixtures(self):
        new = self.temp / "new-react"
        existing = self.temp / "existing-vue"
        for project, framework, version, line in (
            (new, "react", "19.0.0", "NEW PROJECT FIXTURE"),
            (existing, "vue", "3.5.0", "EXISTING PROJECT FIXTURE"),
        ):
            project.mkdir()
            subprocess.run(["git", "init", "-q", str(project)], env=self.env, check=True)
            (project / "package.json").write_text(json.dumps({"dependencies": {framework: version}}))
            (project / "AGENTS.md").write_text(f"# {line}\n")
        with (existing / "AGENTS.md").open("a") as file:
            file.write("\n## Agent skills\n\nUse the [local tracker](issues/README.md).\n")
        (existing / "issues").mkdir()
        (existing / "issues/README.md").write_text("# Local ticket convention\n")
        (existing / "issues/1.md").write_text("# 1. Update the greeting\n\nGreet by name.\n\nBlocked by: none\n")
        (existing / "src").mkdir()
        (existing / "src/App.vue").write_text("<template><p>Hello</p></template>\n")
        return new, existing

    def test_new_and_existing_project_routing_is_read_only(self):
        self.run_script("install")
        new, existing = self.fixtures()
        for project in (new, existing):
            with self.subTest(project=project.name):
                before = {p: p.read_bytes() for p in project.rglob("*")
                          if ".git" not in p.relative_to(project).parts and p.is_file()}
                self.run_script("verify", "--local-only", "--project", project,
                                message=f"Project instruction candidate: {project / 'AGENTS.md'}")
                self.assertEqual(before, {p: p.read_bytes() for p in project.rglob("*")
                                         if ".git" not in p.relative_to(project).parts and p.is_file()})
        override = existing / "AGENTS.override.md"
        override.write_text("[Broken tracker link](missing.md)\n")
        self.run_script("verify", "--local-only", "--project", existing, ok=False, message="shadows")
        self.run_script("verify", "--local-only", "--project", existing, ok=False, message="broken local link")

    def test_optional_enforcement_inspection(self):
        self.run_script("install")
        hooks = self.profile / "hooks.json"
        hooks.write_text('{"hooks": {}}')
        (self.profile / "rules").mkdir()
        (self.profile / "rules/default.rules").write_text("# Fixture\n")
        self.run_script("verify", "--local-only", "--enforcement", message="Hook configuration")
        self.run_script("verify", "--local-only", "--enforcement", message="Rule file")
        hooks.write_text("[]")
        self.run_script("verify", "--local-only", "--enforcement", ok=False, message="Expected a hooks object")

    @unittest.skipUnless(os.getenv("PLAYBOOK_TEST_CODEX") == "1", "Set PLAYBOOK_TEST_CODEX=1 to run Codex")
    def test_real_codex_discovery_and_model_visible_instructions(self):
        self.run_script("install")
        skill(self.skills / "visible-control", "visible-control")
        skill(self.profile / "skills/profile-control", "profile-control")
        skill(self.home / ".codex/skills/other-profile-control", "other-profile-control")
        new, existing = self.fixtures()
        # Bind the model transport to an unreachable local endpoint. The
        # app server still assembles and records the explicit skill input.
        (self.profile / "config.toml").write_text(
            'model_provider = "offline"\nmodel = "gpt-5"\n'
            '[model_providers.offline]\nname = "Acceptance fixture"\n'
            'base_url = "http://127.0.0.1:1/v1"\nrequest_max_retries = 0\nstream_max_retries = 0\n'
        )
        with subprocess.Popen(["codex", "-C", str(new), "app-server"], env=self.env,
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True) as proc:
            messages = queue.Queue()

            def receive():
                for line in proc.stdout:
                    messages.put(json.loads(line))

            reader = threading.Thread(target=receive, daemon=True)
            reader.start()

            def send(method, params=None, request_id=None):
                msg = {"jsonrpc": "2.0", "method": method}
                if params is not None:
                    msg["params"] = params
                if request_id is not None:
                    msg["id"] = request_id
                proc.stdin.write(json.dumps(msg) + "\n")
                proc.stdin.flush()
                if request_id is not None:
                    while (response := messages.get(timeout=10)).get("id") != request_id:
                        continue
                    self.assertIn("result", response)
                    return response["result"]

            try:
                init = send("initialize", {"clientInfo": {"name": "playbook-test", "version": "1.0"}}, 1)
                self.assertEqual(Path(init["codexHome"]).resolve(), self.profile)
                send("initialized")
                result = send("skills/list", {"cwds": [str(new), str(existing)], "forceReload": True}, 2)
                self.assertEqual({Path(item["cwd"]).resolve() for item in result["data"]}, {new, existing})
                for item in result["data"]:
                    for name in CUSTOM:
                        match, = [skill for skill in item["skills"] if skill["name"] == name]
                        self.assertTrue(match["enabled"])
                        self.assertEqual(Path(match["path"]).resolve(), ROOT / "skills" / name / "SKILL.md")
                scenarios = [
                    (new, "bootstrap-project", "Set up a reusable React 19 component API.", "Exact reconciliation scope"),
                    (existing, "bootstrap-project", "Reconcile this existing Vue project.", "Use prior approval only"),
                    (existing, "pair-implement", "Continue ticket 1 in a fresh session.", "Never infer approval from code"),
                ]
                for index, (project, name, prompt, expected) in enumerate(scenarios):
                    request = 3 + 3 * index
                    thread = send("thread/start", {"cwd": str(project)}, request)["thread"]
                    turn = send("turn/start", {"threadId": thread["id"], "input": [
                        {"type": "text", "text": f"${name} {prompt}", "text_elements": []},
                        {"type": "skill", "name": name, "path": str(ROOT / "skills" / name / "SKILL.md")},
                    ]}, request + 1)["turn"]
                    deadline = time.monotonic() + 8
                    while time.monotonic() < deadline:
                        rollouts = (self.profile / "sessions").rglob(f"*{thread['id']}.jsonl")
                        if any(expected.lower() in file.read_text().lower() for file in rollouts):
                            break
                        time.sleep(0.05)
                    else:
                        self.fail(f"Codex did not record the explicitly invoked {name} instructions")
                    send("turn/interrupt", {"threadId": thread["id"], "turnId": turn["id"]}, request + 2)
            finally:
                proc.terminate()
                proc.wait(timeout=5)
                reader.join(timeout=5)

        for project, heading in ((new, "NEW PROJECT FIXTURE"), (existing, "EXISTING PROJECT FIXTURE")):
            output = subprocess.run(["codex", "-C", str(project), "debug", "prompt-input", "Show guidance"],
                                    env=self.env, check=True, text=True, capture_output=True, timeout=15).stdout
            self.assertIn(heading, output)
            self.assertIn("Personal Engineering Preferences", output)
            self.assertIn("Get my explicit approval before implementing an increment", output)
            self.assertIn("visible-control", output)
            self.assertIn("profile-control", output)
            self.assertNotIn("other-profile-control", output)
            self.assertNotIn("Reconcile engineering setup, documentation", output)
            self.assertNotIn("Pair on one implementation ticket with approval", output)


if __name__ == "__main__":
    unittest.main()
