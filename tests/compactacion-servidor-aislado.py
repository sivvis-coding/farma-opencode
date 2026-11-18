"""OpenCode server idempotency test, loopback only and providers hard-denied."""
import concurrent.futures
import base64
import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

root = Path(tempfile.mkdtemp(prefix="farma-server-", dir=os.environ["FARMA_TEST_TMP"]))
config = root / "config" / "opencode"
config.mkdir(parents=True)
settings = {
    "$schema": "https://opencode.ai/config.json",
    "update": "disable",
    "policies": [
        {"action": "provider.use", "resource": "*", "effect": "deny"},
        {"action": "integration.use", "resource": "*", "effect": "deny"},
        {"action": "websearch.use", "resource": "*", "effect": "deny"},
    ],
}
if os.environ.get("FARMA_TEST_UI_FULL") == "1":
    settings["plugins"] = [
        "@yassirh/opencode-codex-limits-plugin@0.1.1",
        "opencode-dir-tree-tui@1.0.6",
    ]
(config / "opencode.json").write_text(json.dumps(settings), encoding="utf-8")
env = {k: v for k, v in os.environ.items() if not any(
    term in k.upper() for term in ("TOKEN", "API_KEY", "PASSWORD", "CREDENTIAL", "SECRET")
)}
env["XDG_CONFIG_HOME"] = str(root / "config")
for name in ("XDG_DATA_HOME", "XDG_CACHE_HOME", "XDG_STATE_HOME"):
    env[name] = str(root / name.lower())
env["OPENCODE_DISABLE_FREE_MODELS"] = "1"
env["OPENCODE_LOG_LEVEL"] = "DEBUG"
env["OPENCODE_SERVER_PASSWORD"] = "farma-isolated-test-only"
env["OPENCODE_SERVER_USERNAME"] = "opencode"
env["NO_PROXY"] = "127.0.0.1,localhost"
with socket.socket() as sock:
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
base = f"http://127.0.0.1:{port}"
process = subprocess.Popen(
    [os.environ["FARMA_OPENCODE_EXE"], "serve", "--hostname", "127.0.0.1", "--port", str(port)],
    cwd=root, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)


def request(method, route, body=None):
    data = None if body is None else json.dumps(body).encode()
    basic = base64.b64encode(b"opencode:farma-isolated-test-only").decode()
    req = urllib.request.Request(base + route, data=data, method=method,
                                 headers={"Content-Type": "application/json", "Authorization": "Basic " + basic})
    with urllib.request.urlopen(req, timeout=10) as response:
        return response.read().decode("utf-8")


try:
    last_error = None
    for _ in range(200):
        try:
            request("GET", "/api/info")
            break
        except (OSError, urllib.error.URLError) as exc:
            last_error = (type(exc).__name__, getattr(exc, "code", None))
            if process.poll() is not None:
                raise RuntimeError("Servidor aislado no arrancó")
            time.sleep(0.1)
    else:
        raise RuntimeError(f"Servidor aislado no respondió: {last_error}")
    sid = json.loads(request("POST", "/api/session", {"title": "idempotencia sintética"}))["data"]["id"]
    if os.environ.get("FARMA_TEST_UI_FULL") == "1":
        request("POST", "/api/location/reload", {})
        required = {"codex-limits.server", "opencode-dir-tree-tui"}
        active = set()
        for _ in range(1800):
            plugins = json.loads(request("GET", "/api/plugin"))["data"]
            active = {item["id"] for item in plugins if item.get("state", {}).get("status") == "active"}
            if required <= active:
                break
            time.sleep(0.1)
        if not required <= active:
            missing = sorted(required - active)
            non_builtin = [(item["id"], item.get("state", {}).get("status"))
                           for item in plugins if not item["id"].startswith("opencode.")]
            effective = json.loads(request("GET", "/api/config"))
            raise AssertionError(f"Complementos no activos: {missing}; encontrados: {non_builtin}; "
                                 f"config: {effective}; datos temporales: {root}")
        print("Perfil limpio: servidor de cuota y complemento de árbol activos")
        sys.exit(0)
    gate = threading.Barrier(2)
    body = {"id": "msg_farma_compact_synthetic", "delivery": "queue"}

    def compact():
        gate.wait(timeout=5)
        return json.loads(request("POST", f"/api/session/{sid}/compact", body))["data"]

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(compact) for _ in range(2)]
        results = [future.result(timeout=20) for future in futures]
    assert all(item["id"] == body["id"] and item["type"] == "compaction" for item in results), results
    assert results[0] == results[1], "Las respuestas no apuntan a la misma admisión"
    inbox = json.loads(request("GET", f"/api/session/{sid}/inbox"))["data"]
    enqueued = [item for item in inbox if item["id"] == body["id"]]
    assert len(enqueued) == 1, f"Esperada 1 compactación en cola; hay {len(enqueued)}"
    messages = json.loads(request("GET", f"/api/session/{sid}/message"))["data"]
    assert messages == [], "La sesión aislada no debería haber invocado un modelo"
    print("Servidor OpenCode aislado: 2 peticiones concurrentes con mismo ID -> 1 admisión")
    print("Proveedores, integraciones y búsqueda bloqueados por política; sin credenciales ni modelo.")
    print("Datos temporales:", root)
finally:
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)
