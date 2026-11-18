"""Two real TUIs and an isolated server with an imported synthetic transcript."""
import base64
import json
import os
import shutil
import socket
import subprocess
import tempfile
import threading
import time
import urllib.request
from pathlib import Path

import pyte
from winpty import PtyProcess

repo = Path(__file__).resolve().parents[1]
root = Path(tempfile.mkdtemp(prefix="farma-dos-tui-", dir=os.environ["FARMA_TEST_TMP"]))
config = root / "config" / "opencode"
plugin = config / "plugins" / "farma-barra"
plugin.mkdir(parents=True)
for file in ("tui.tsx", "politica.mjs"):
    shutil.copy2(repo / "package" / "plugins" / "farma-barra" / file, plugin / file)
(root / "ensayo_sintetico.txt").write_text("archivo de prueba", encoding="utf-8")
(config / "opencode.json").write_text(json.dumps({
    "$schema": "https://opencode.ai/config.json", "update": "disable",
    "plugins": ["opencode-dir-tree-tui@1.0.6"],
    "policies": [{"action": "provider.use", "resource": "*", "effect": "deny"},
                 {"action": "integration.use", "resource": "*", "effect": "deny"},
                 {"action": "websearch.use", "resource": "*", "effect": "deny"}],
}), encoding="utf-8")
(config / "cli.json").write_text(json.dumps({
    "plugins": [plugin.as_posix(), "-opencode.sidebar.context"],
    "session": {"sidebar": "auto"},
}), encoding="utf-8")
env = {k: v for k, v in os.environ.items() if not any(
    term in k.upper() for term in ("TOKEN", "API_KEY", "PASSWORD", "CREDENTIAL", "SECRET")
)}
env.update({
    "XDG_CONFIG_HOME": str(root / "config"),
    "XDG_DATA_HOME": str(root / "data"),
    "XDG_STATE_HOME": str(root / "state"),
    "XDG_CACHE_HOME": os.environ["FARMA_TEST_PLUGIN_CACHE"],
    "OPENCODE_DISABLE_FREE_MODELS": "1",
    "OPENCODE_SERVER_PASSWORD": "farma-isolated-test-only",
    "OPENCODE_SERVER_USERNAME": "opencode",
    "NO_PROXY": "localhost,127.0.0.1",
})
with socket.socket() as sock:
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
base = f"http://127.0.0.1:{port}"
auth = "Basic " + base64.b64encode(b"opencode:farma-isolated-test-only").decode()
exe = os.environ["FARMA_OPENCODE_EXE"]
server = subprocess.Popen([exe, "serve", "--hostname", "127.0.0.1", "--port", str(port)],
                          cwd=root, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
processes = []


def request(method, route, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(base + route, data=data, method=method,
                                 headers={"Authorization": auth, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as response:
        return response.read().decode("utf-8")


try:
    for _ in range(200):
        try:
            request("GET", "/api/info")
            break
        except OSError:
            if server.poll() is not None:
                raise RuntimeError("Servidor no arrancó")
            time.sleep(0.1)
    else:
        raise RuntimeError("Servidor no respondió")
    info = json.loads(request("POST", "/api/session", {"title": "Plantilla sintética"}))["data"]
    info["id"] = "ses_farma_two_tui_synthetic"
    message = {
        "id": "msg_farma_source_300k", "type": "assistant", "agent": "build",
        "model": {"providerID": "openai", "id": "synthetic"},
        "time": {"created": 1700000000000, "completed": 1700000001000},
        "content": [{"type": "text", "text": "Respuesta sintética."}],
        "tokens": {"input": 300000, "output": 0, "reasoning": 0, "cache": {"read": 0, "write": 0}},
    }
    imported = json.loads(request("POST", "/api/experimental/session/import",
                                  {"info": info, "messages": [message]}))["data"]
    sid = imported["id"]
    received = json.loads(request("GET", f"/api/session/{sid}/message"))["data"]
    assert any(m.get("id") == message["id"] and m.get("tokens", {}).get("input") == 300000 for m in received)
    screens = []

    def start_tui():
        proc = PtyProcess.spawn([exe, "--server", base, "--session", sid], cwd=str(root), env=env, dimensions=(45, 180))
        processes.append(proc)
        screen = pyte.Screen(180, 45)
        screens.append(screen)
        stream = pyte.Stream(screen)

        def read():
            try:
                while proc.isalive():
                    stream.feed(proc.read(4096))
            except (EOFError, OSError):
                pass
        threading.Thread(target=read, daemon=True).start()

    start_tui()
    start_tui()
    time.sleep(12)
    history = json.loads(request("GET", f"/api/session/{sid}/message"))["data"]
    relevant = [m for m in history if m.get("type") == "compaction"]
    print("Compactaciones en historial desde dos TUI:", len(relevant))
    print("Árbol visible con archivo sintético:", any("ensayo_sintetico.txt" in "\n".join(s.display) for s in screens))
    assert len(relevant) == 1, f"Compactaciones: {relevant}"
    assert relevant[0]["id"] == "msg_farma_compact_farma_source_300k"
    assert relevant[0]["status"] == "failed" and relevant[0]["error"]["type"] == "provider.no-route"
    assert any("ensayo_sintetico.txt" in "\n".join(s.display) for s in screens), "Árbol sintético no visible"
    print("Error esperado provider.no-route: no se invocó un modelo")
    print("Dos TUI reales: una solicitud de compactación y árbol visibles")
finally:
    for proc in processes:
        if proc.isalive():
            proc.terminate(force=True)
    server.terminate()
    try:
        server.wait(timeout=10)
    except subprocess.TimeoutExpired:
        server.kill()
        server.wait(timeout=5)
