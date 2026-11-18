import { Plugin } from "@opencode/plugin/tui"
import { Rpc } from "@opencode/plugin/rpc"
import { createEffect, createSignal } from "solid-js"
import { decision, estimate } from "./politica.mjs"

// Reuse the installed Codex Limits server; this plugin never handles credentials.
const Limits = Rpc.define({
  id: "codex-limits",
  methods: {
    read: {
      input: {
        type: "object",
        properties: { refresh: { type: "boolean" } },
        additionalProperties: false,
      },
      output: {
        type: "object",
        properties: {
          status: { type: "string", enum: ["ready", "stale", "unavailable"] },
          fiveHour: { type: "object" },
          weekly: { type: "object" },
        },
        required: ["status"],
      },
    },
  },
  events: {},
})

type Window = { remainingPercent?: number; resetsAt?: number }
type Result = { status: string; fiveHour?: Window; weekly?: Window }

function format(label: string, value?: Window): string {
  if (typeof value?.remainingPercent !== "number") return `${label} —`
  const used = Math.round(Math.max(0, Math.min(100, 100 - value.remainingPercent)))
  const reset = typeof value.resetsAt === "number"
    ? new Intl.DateTimeFormat("es-ES", {
        weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false,
      }).format(new Date(value.resetsAt * 1000))
    : "hora desconocida"
  return `${label} ${used}% ↻ ${reset}`
}

export default Plugin.define({
  id: "farma.barra",
  setup(ctx) {
    const [display, setDisplay] = createSignal<Result>()
    const [status, setStatus] = createSignal("Codex: consultando límites…")
    const rpc = ctx.client.rpc(Limits)
    let disposed = false
    let last: Result | undefined

    async function refresh() {
      try {
        const result = await rpc.read({}, {
          location: ctx.location ?? ctx.data.location.default(),
          signal: AbortSignal.timeout(10000),
        }) as Result
        if (disposed) return
        if (result.fiveHour || result.weekly) last = result
        const data = (result.fiveHour || result.weekly) ? result : last
        if (!data) {
          setStatus("Codex: límites no disponibles")
          return
        }
        const stale = result.status !== "ready"
        setDisplay(data)
        setStatus(stale ? "  ·  sin actualizar" : "")
      } catch {
        if (!disposed) setStatus(last ? "  ·  sin actualizar" : "Codex: límites no disponibles")
      }
    }

    const synced = new Set<string>()
    const [locks, updateLocks] = ctx.storage.store("compact-locks", { initial: {} as Record<string, boolean> })
    const busy = new Set<string>()
    const removeContext = ctx.ui.slot({
      append: "session.composer.top",
      render: (input) => {
        const sid = input.sessionID
        if (!sid) return null
        if (!synced.has(sid)) {
          synced.add(sid)
          void ctx.data.session.message.sync(sid).catch(() => synced.delete(sid))
          void ctx.data.location.model.sync(ctx.location ?? ctx.data.location.default()).catch(() => {})
        }
        const current = () => {
          const messages = ctx.data.session.message.list(sid) ?? []
          const last = [...messages].reverse().find((m) => m.type === "assistant" && m.tokens)
          if (!last || last.type !== "assistant" || !last.tokens) return undefined
          const t = last.tokens
          const used = estimate(t)
          const models = ctx.data.location.model.list(ctx.location ?? ctx.data.location.default()) ?? []
          const model = models.find((m) => m.providerID === last.model.providerID && m.id === last.model.id)
          const limit = model?.limit?.context
          if (!limit || used === undefined || used <= 0) return undefined
          return { used, percent: Math.min(100, Math.round(100 * used / limit)) }
        }
        createEffect(() => {
          const messages = ctx.data.session.message.list(sid) ?? []
          const action = decision(messages, locks[sid] === true)
          if (busy.has(sid) || action.action === "wait") return
          busy.add(sid)
          if (action.action === "unlock") {
            void updateLocks((draft) => { delete draft[sid] }).finally(() => busy.delete(sid))
            return
          }
          void (async () => {
            try {
              // Persist before requesting. On failure retain the lock: never retry in a loop.
              await updateLocks((draft) => { draft[sid] = true })
              await ctx.client.session.compact({ sessionID: sid, id: action.id })
              ctx.ui.toast.show({ title: "Contexto", message: "Compactación solicitada (estimación ≥ 300k).", variant: "warning" })
            } catch {
              ctx.ui.toast.show({ title: "Contexto", message: "No se pudo solicitar la compactación. Usa /compact.", variant: "error" })
            } finally {
              busy.delete(sid)
            }
          })()
        })
        const color = () => (current()?.used ?? 0) >= 250000 ? ctx.theme.text.feedback.error.base : (current()?.used ?? 0) >= 150000 ? ctx.theme.text.feedback.warning.base : ctx.theme.text.feedback.success.base
        const label = () => {
          const value = current()
          if (!value) return "Contexto: sin datos"
          const zone = value.used >= 300000 ? "AUTO 300k" : value.used >= 250000 ? "AVISO 250k" : value.used >= 150000 ? "WARN 150k" : "SMART"
          const filled = Math.max(0, Math.min(5, Math.round(value.percent * 5 / 100)))
          return `${"■".repeat(filled)}${"□".repeat(5 - filled)} ${zone} (${Math.round(value.used / 1000)}k)`
        }
        return <box flexDirection="row">
          <text fg={color()}>{label()}</text>
          <text fg={ctx.theme.text.muted}>{"  |  "}</text>
          <text fg={(100 - (display()?.fiveHour?.remainingPercent ?? 100)) >= 95 ? ctx.theme.text.feedback.error.base : (100 - (display()?.fiveHour?.remainingPercent ?? 100)) >= 70 ? ctx.theme.text.feedback.warning.base : ctx.theme.text.feedback.success.base}>
            {display() ? format("Cuota 5 horas", display()?.fiveHour) : ""}
          </text>
          <text fg={ctx.theme.text.muted}>{display() ? "  |  " : ""}</text>
          <text fg={(100 - (display()?.weekly?.remainingPercent ?? 100)) >= 95 ? ctx.theme.text.feedback.error.base : (100 - (display()?.weekly?.remainingPercent ?? 100)) >= 70 ? ctx.theme.text.feedback.warning.base : ctx.theme.text.feedback.success.base}>
            {display() ? format("Cuota semanal", display()?.weekly) : ""}
          </text>
          <text fg={ctx.theme.text.muted}>{status()}</text>
        </box>
      },
    })
    const timer = setInterval(() => void refresh(), 120000)
    void refresh()
    return () => {
      disposed = true
      clearInterval(timer)
      removeContext()
    }
  },
})
