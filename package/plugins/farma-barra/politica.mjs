// Estimate only: provider token reporting is not a guaranteed context measurement.
export function estimate(tokens) {
  if (!tokens) return undefined
  const values = [tokens.input, tokens.output, tokens.reasoning, tokens.cache?.read, tokens.cache?.write]
  if (!values.every((x) => typeof x === "number" && Number.isFinite(x) && x >= 0)) return undefined
  return values.reduce((a, b) => a + b, 0)
}

export function decision(messages, locked) {
  const list = Array.isArray(messages) ? messages : []
  let last
  for (let i = list.length - 1; i >= 0; i--) {
    const m = list[i]
    if (m.type === "compaction") return { action: "wait" }
    if (m.type === "assistant" && m.tokens && m.time?.completed) {
      last = m
      break
    }
  }
  if (!last) return { action: "wait" }
  const used = estimate(last.tokens)
  if (used === undefined) return { action: "wait" }
  if (locked) return { action: used < 150000 ? "unlock" : "wait", used }
  if (used >= 300000 && typeof last.id === "string" && last.id.startsWith("msg_")) {
    return { action: "compact", used, id: `msg_farma_compact_${last.id.slice(4)}` }
  }
  return { action: "wait", used }
}
