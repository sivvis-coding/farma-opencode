"""Small, opt-in benchmark. Makes four real model calls and consumes quota."""
import json
import os
import subprocess
import time
from pathlib import Path

exe = os.environ["FARMA_OPENCODE_EXE"]
directory = Path(os.environ["FARMA_TEST_TMP"]) / "farma-benchmark-sintetico"
directory.mkdir(parents=True, exist_ok=True)
output = Path(os.environ["FARMA_BENCHMARK_OUTPUT"])
if output.exists():
    raise SystemExit("La salida ya existe; no se sobrescribirá.")
model = "openai/gpt-6.1-terra"
cases = {
    "conteo": ("Prueba sintética: grupo A tiene eventos 1,0,1 y grupo B tiene "
               "0,1,0. Indica personas y eventos por grupo y si se puede inferir "
               "causalidad. Responde en pocas líneas, sin herramientas."),
    "metodologia": ("Prueba sintética: un estudio observacional comienza el "
                    "seguimiento antes de que se determine quién recibe el "
                    "tratamiento. Señala un posible sesgo y por qué puede "
                    "ocurrir. Responde en pocas líneas, sin herramientas."),
}
records = []
for case, prompt in cases.items():
    for agent in ("build", "asistente-farma"):
        start = time.monotonic()
        result = subprocess.run(
            [exe, "run", "--model", model, "--agent", agent, "--archived",
             "--format", "json", prompt],
            cwd=directory, capture_output=True, text=True, encoding="utf-8", timeout=120,
        )
        if result.returncode:
            raise RuntimeError(f"Falló {case}/{agent}: código {result.returncode}")
        events = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        text = "\n".join(event["part"]["text"] for event in events if event.get("type") == "text")
        steps = [event["part"]["tokens"] for event in events if event.get("type") == "step_finish"]
        if not text or not steps:
            raise RuntimeError(f"Faltan texto o métricas: {case}/{agent}")
        records.append({
            "scenario": case, "agent": agent, "model_requested": model,
            "elapsed_seconds": round(time.monotonic() - start, 2),
            "tokens_by_step": steps,
            "tool_events": sum(event.get("type") == "tool_use" for event in events),
            "response": text,
        })
output.parent.mkdir(parents=True, exist_ok=True)
with output.open("x", encoding="utf-8") as target:
    json.dump({"method": "one independent archived session per case and agent; synthetic data",
               "limitations": "one run per cell; build shares global configuration; token counts are not quota",
               "records": records}, target, ensure_ascii=False, indent=2)
print(f"Guardado: {output}")
for row in records:
    print(json.dumps({"scenario": row["scenario"], "agent": row["agent"],
                      "tokens_by_step": row["tokens_by_step"],
                      "tool_events": row["tool_events"], "response": row["response"]},
                     ensure_ascii=False))
