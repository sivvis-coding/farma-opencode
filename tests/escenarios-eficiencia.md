# Comparación de eficiencia y calidad

Usa cuentas, proveedores, modelo, variante y permisos equivalentes en ambos
ensayos. Trabaja exclusivamente con datos sintéticos. Registra por separado
entrada, salida y caché tal como los informe OpenCode; la cuota del proveedor
no necesariamente es proporcional a esos números. Cada prueba usa una sesión
nueva. La caché y la variación de respuestas pueden alterar las cifras.

1. **Redacción:** pide revisar un párrafo con una afirmación causal exagerada.
   Comprueba que no se inventen resultados y que se señale la exageración.
2. **Análisis:** usa `examples/datos_sinteticos.csv`. Debe dar A: 3 personas,
   2 eventos; B: 3 personas, 1 evento, y no afirmar causalidad.
3. **Protocolo:** plantea un estudio observacional con inicio de seguimiento
   anterior a la exposición; debe preguntar o advertir por posible tiempo inmortal.
4. **Referencias:** incluye un DOI inexistente y comprueba que no se declare
   verificado sin fuente. No consultes documentos confidenciales en la prueba.

Repite cada escenario y compara respuestas, pasos, tokens y tiempo con una
configuración de control. Una reducción solo es aceptable si conserva los puntos
de calidad y seguridad.

## Comprobación parcial del 18 de noviembre de 2026

Con `asistente-farma` y `openai/gpt-6.1-terra`, en sesiones nuevas archivadas,
se comprobó que el modelo contó correctamente los eventos del escenario 2,
evitó atribuir causalidad, reformuló la frase del escenario 1, advirtió del
riesgo condicionado del escenario 3 y no dio por verificado un DOI no
consultado. Los datos y el enunciado fueron sintéticos. La comprobación del DOI
no incluyó una búsqueda. No se comparó con un control, no se midió consumo y
no se probó la delegación real: esto no demuestra ahorro.

Se ejecutaron además pruebas locales sintéticas de creación y modificación de
una copia DOCX con `python-docx`, comprobando cifras, una tabla y el hash del
original; no se verificaron notas, imágenes o control de cambios. Una API REDCap
simulada permitió probar escritura CSV, rechazo de JSON y no sobrescritura, sin
conectar REDCap ni emplear credenciales reales. Son pruebas de componentes,
no una validación de la instalación institucional ni de la respuesta de un agente.

`tests/barra-integracion.cjs` carga el módulo TUI transpilado en un host
simulado. Comprueba una solicitud a 300k, bloqueo, recuperación y error sin
reintentos en bucle. Dos interfaces simuladas usan el mismo ID.

`tests/compactacion-servidor-aislado.py` envió al servidor real dos solicitudes
concurrentes con el mismo ID y comprobó que ambas respuestas eran idénticas y
había una sola solicitud en cola. Proveedores y búsqueda estaban bloqueados;
no se ejecutó un modelo.

La TUI real se abrió en una configuración aislada y mostró «Contexto: sin
datos» en una sesión vacía, sin solicitar respuestas de un modelo. No se
generó una conversación real de 300k tokens. El agente de redacción leyó un
DOCX sintético, identificó una afirmación causal y conservó cifras y tabla.
El analista identificó que el exportador no restringe filas, sin contactar
REDCap ni solicitar tokens; no pudo inspeccionar el script por permisos.

Con `tests/dos-tui-servidor.py`, dos TUI reales conectadas a un servidor
aislado mostraron el árbol con un archivo sintético y generaron una sola
compactación en el historial a partir de un mensaje importado de 300k tokens.
La compactación terminó con el error esperado `provider.no-route`, pues no
había proveedor habilitado. No prueba la calidad de un resumen ni una lectura
de cuota autenticada; tampoco se validó en el equipo de la investigadora.

## Comparación acotada: 18 de noviembre de 2026

`comparar-modelos-sinteticos.py` ejecutó dos preguntas sintéticas, una vez con
Build y otra con `asistente-farma`, usando el mismo `openai/gpt-6.1-terra`,
sin herramientas y con una sesión nueva archivada por ejecución. El control
Build comparte la configuración e instrucciones globales de este equipo: no
es una instalación estándar limpia. Respuestas y métricas por paso están en
`resultado-comparacion-sintetica-20261118.json`.

Para repetirlo, configura `FARMA_OPENCODE_EXE`, `FARMA_TEST_TMP` y una ruta
inexistente en `FARMA_BENCHMARK_OUTPUT`, y ejecuta el script con Python. Se
requiere una cuenta conectada con acceso al modelo y se harán **cuatro llamadas
reales que consumen cuota**. El script no debe utilizarse con datos privados.

| Escenario | Agente | Entrada | Salida | Caché leída/escrita |
| --- | --- | ---: | ---: | ---: |
| Conteo | Build | 5.840 | 55 | 0 / 0 |
| Conteo | Asistente | 5.654 | 58 | 0 / 0 |
| Tiempo inmortal | Build | 5.833 | 72 | 0 / 0 |
| Tiempo inmortal | Asistente | 5.647 | 71 | 0 / 0 |

Ambas respuestas de conteo identificaron grupos y eventos correctos y evitaron
una conclusión causal automática. Ambas respuestas metodológicas identificaron
el posible tiempo inmortal y explicaron la atribución errónea del tiempo.
Es una revisión puntual, no una evaluación ciega ni validación clínica.

En estas cuatro ejecuciones el asistente empleó aproximadamente un 3,2 % menos
de tokens de entrada en conjunto, pero algo más de salida. Solo hay una
ejecución por celda; no se midió cuota de cinco horas, variabilidad, desempeño
en documentos ni efecto de subagentes. El resultado **no demuestra ahorro
general**, ni permite convertir tokens en cuota.
