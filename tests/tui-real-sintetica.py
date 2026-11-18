"""Windows-only isolated TUI smoke test; requires pywinpty and OpenCode V2."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

from winpty import PtyProcess
import pyte

repo = Path(__file__).resolve().parents[1]
parent = Path(os.environ["FARMA_TEST_TMP"])
root = Path(tempfile.mkdtemp(prefix="farma-tui-", dir=parent))
config = root / "config" / "opencode"
plugin = config / "plugins" / "farma-barra"
plugin.mkdir(parents=True)
for file in ("tui.tsx", "politica.mjs"):
    shutil.copy2(repo / "package" / "plugins" / "farma-barra" / file, plugin / file)
settings = {"$schema": "https://opencode.ai/config.json", "update": "disable"}
if os.environ.get("FARMA_TEST_UI_FULL") == "1":
    settings["plugins"] = ["@yassirh/opencode-codex-limits-plugin@0.1.1", "opencode-dir-tree-tui@1.0.6"]
(config / "opencode.json").write_text(json.dumps(settings))
(config / "cli.json").write_text(json.dumps({"plugins": [plugin.as_posix(), "-codex-limits.tui", "-opencode.sidebar.context"]}))
env = {k: v for k, v in os.environ.items() if not any(
    term in k.upper() for term in ("TOKEN", "API_KEY", "PASSWORD", "CREDENTIAL", "SECRET")
)}
for name in ("XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME", "XDG_STATE_HOME"):
    env[name] = str(root / name.lower())
env["XDG_CONFIG_HOME"] = str(root / "config")
env["OPENCODE_DISABLE_FREE_MODELS"] = "1"
exe = os.environ["FARMA_OPENCODE_EXE"]
created = subprocess.run(
    [exe, "api", "post", "/api/session", "--data", '{"title":"Prueba sintética"}', "--standalone"],
    cwd=str(root), env=env, capture_output=True, text=True, encoding="utf-8", timeout=30, check=True,
)
session_id = json.loads(created.stdout)["data"]["id"]
proc = PtyProcess.spawn([exe, "--standalone", "--session", session_id], cwd=str(root), env=env, dimensions=(40, 160))
parts = []
screen = pyte.Screen(160, 40)
stream = pyte.Stream(screen)


def read_output():
    try:
        while proc.isalive():
            data = proc.read(4096)
            parts.append(data)
            stream.feed(data)
    except (EOFError, OSError):
        pass


reader = threading.Thread(target=read_output, daemon=True)
reader.start()
try:
    end = time.monotonic() + 30
    while time.monotonic() < end and proc.isalive():
        display = "\n".join(screen.display)
        if "Contexto: sin datos" in display and (os.environ.get("FARMA_TEST_UI_FULL") != "1"
                                               or "Codex:" in display):
            print("TUI real aislada: barra cargada y muestra 'Contexto: sin datos'")
            if os.environ.get("FARMA_TEST_UI_FULL") == "1":
                print("TUI real aislada: indicador Codex presente")
            print("Configuración y datos temporales:", root)
            sys.exit(0)
        time.sleep(0.2)
    print("TUI real: no se detectó la barra. Pantalla:\n", "\n".join(screen.display))
    sys.exit(1)
finally:
    if proc.isalive():
        proc.terminate(force=True)
