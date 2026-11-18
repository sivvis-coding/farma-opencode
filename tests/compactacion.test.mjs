import assert from "node:assert/strict"
import { decision, estimate } from "../package/plugins/farma-barra/politica.mjs"

const msg = (n) => ({ id: "msg_test", type: "assistant", time: { completed: 1 }, tokens: {
  input: n, output: 0, reasoning: 0, cache: { read: 0, write: 0 },
} })
assert.equal(estimate(msg(150000).tokens), 150000)
assert.equal(estimate({ input: NaN }), undefined)
assert.equal(decision([msg(299999)], false).action, "wait")
assert.equal(decision([msg(300000)], false).action, "compact")
assert.equal(decision([msg(300000)], false).id, "msg_farma_compact_test")
assert.equal(decision([{ ...msg(300000), id: undefined }], false).action, "wait")
assert.equal(decision([msg(300000)], true).action, "wait")
assert.equal(decision([msg(100000)], true).action, "unlock")
assert.equal(decision([msg(300000), { type: "compaction" }], false).action, "wait")
assert.equal(decision([{ ...msg(300000), time: {} }], false).action, "wait")
console.log("Política de compactación: pruebas superadas")
