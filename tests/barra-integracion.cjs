// Isolated integration of the actual TUI module with a simulated host and client.
const assert = require("node:assert/strict")
const fs = require("node:fs")
const vm = require("node:vm")
const path = require("node:path")
const { pathToFileURL } = require("node:url")

async function main() {
  const ts = require(process.env.FARMA_TYPESCRIPT || "typescript")
  const root = path.join(__dirname, "..", "package", "plugins", "farma-barra")
  const policy = await import(pathToFileURL(path.join(root, "politica.mjs")))
  const source = fs.readFileSync(path.join(root, "tui.tsx"), "utf8")
  const code = ts.transpileModule(source, { compilerOptions: {
    module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022,
    jsx: ts.JsxEmit.React, jsxFactory: "h",
  }}).outputText
  const effects = []
  const mocks = {
    "@opencode/plugin/tui": { Plugin: { define: (x) => x } },
    "@opencode/plugin/rpc": { Rpc: { define: (x) => x } },
    "solid-js": {
      createEffect: (fn) => { effects.push(fn); fn() },
      createSignal: (initial) => { let v = initial; return [() => v, (next) => { v = next }] },
    },
    "./politica.mjs": policy,
  }
  const module = { exports: {} }
  vm.runInNewContext(code, {
    module, exports: module.exports, require: (name) => {
      if (!mocks[name]) throw Error(`Unexpected import: ${name}`)
      return mocks[name]
    },
    h: (type, props, ...children) => ({ type, props, children }),
    setInterval: () => 1, clearInterval: () => {}, AbortSignal, Intl, Date,
    Number, Math, Promise, Set,
  }, { filename: "tui.tsx" })
  const plugin = module.exports.default
  assert.equal(plugin.id, "farma.barra")
  const lock = {}
  const calls = []
  const toasts = []
  let messages = []
  let renderer
  let fail = false
  const context = {
    storage: { store: () => [lock, async (mutate) => mutate(lock)] },
    client: {
      rpc: () => ({ read: async () => ({ status: "unavailable" }) }),
      session: { compact: async (input) => {
        calls.push(input.sessionID)
        if (fail) throw Error("simulated failure")
      }},
    },
    data: {
      session: { message: { list: () => messages, sync: async () => {} } },
      location: { default: () => ({}), model: { sync: async () => {}, list: () => [] } },
    },
    ui: {
      slot: ({ render }) => { renderer = render; return () => {} },
      toast: { show: (toast) => toasts.push(toast) },
    },
    theme: { text: { muted: "", feedback: {
      error: { base: "" }, warning: { base: "" }, success: { base: "" },
    }}},
  }
  const cleanup = plugin.setup(context)
  renderer({ sessionID: "ses_test" })
  const tick = async () => { for (let i = 0; i < 8; i++) await Promise.resolve() }
  const trigger = async () => { for (const effect of effects) effect(); await tick() }
  const msg = (n) => ({ id: "msg_test", type: "assistant", time: { completed: 1 }, tokens: {
    input: n, output: 0, reasoning: 0, cache: { read: 0, write: 0 },
  }})
  messages = [msg(299999)]
  await trigger()
  assert.equal(calls.length, 0)
  messages = [msg(300000)]
  await trigger()
  assert.equal(calls.length, 1)
  assert.equal(lock.ses_test, true)
  await trigger()
  assert.equal(calls.length, 1, "must not issue duplicate")
  messages = [msg(300000), { type: "compaction", status: "completed" }]
  await trigger()
  assert.equal(calls.length, 1)
  messages.push(msg(100000))
  await trigger()
  assert.equal(lock.ses_test, undefined, "must unlock after context falls")
  messages.push(msg(300000))
  fail = true
  await trigger()
  assert.equal(calls.length, 2)
  assert.equal(lock.ses_test, true, "retain lock after failure")
  await trigger()
  assert.equal(calls.length, 2, "failure must not cause retry loop")
  assert.ok(toasts.some((t) => t.variant === "error"))
  cleanup()
  // Two TUI instances race with independent stale lock replicas. Model the
  // server's documented idempotency: same session + request ID admits once.
  effects.length = 0
  messages = [msg(300000)]
  const requests = []
  const admitted = new Set()
  const makeContext = () => {
    const localLock = {}
    return {
      ...context,
      storage: { store: () => [localLock, async (mutate) => mutate(localLock)] },
      client: {
        ...context.client,
        session: { compact: async (input) => {
          requests.push(input)
          admitted.add(`${input.sessionID}:${input.id}`)
        }},
      },
    }
  }
  const stop1 = plugin.setup(makeContext())
  renderer({ sessionID: "ses_concurrent" })
  const stop2 = plugin.setup(makeContext())
  renderer({ sessionID: "ses_concurrent" })
  await tick()
  assert.equal(requests.length, 2, "exercise concurrent requests")
  assert.equal(requests[0].id, requests[1].id, "requests must be idempotent")
  assert.equal(admitted.size, 1, "simulated server admits one request")
  stop1()
  stop2()
  console.log("TUI simulada: carga, umbral, solicitud única, desbloqueo y fallo OK")
  console.log("Dos TUI simuladas: mismo ID; servidor simulado admite una compactación")
}
main().catch((error) => { console.error(error); process.exitCode = 1 })
