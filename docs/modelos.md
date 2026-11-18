# Modelos, contexto y costes

En `/models` elige entre los modelos que tu cuenta realmente ofrece. Para
correcciones sencillas prueba uno rápido y económico; para interpretación
metodológica compleja o una revisión difícil, considera uno más capaz y revisa
el resultado. Ningún modelo sustituye una revisión científica independiente.
Los nombres y precios cambian: consulta los precios actuales del proveedor.

## Selección preparada

El instalador busca en el catálogo conectado modelos OpenAI para tres niveles:
Luna para tareas concretas y repetitivas, Terra para redacción, asistencia y análisis, y Sol para
investigación y revisión profunda. Solo configura candidatos que aparezcan en
`opencode models`; si no hay uno, deja ese ajuste sin fijar. El catálogo no
garantiza que la solicitud esté permitida por el plan o por políticas posteriores.
La instalación configura también preferencias de modelo para Build y Plan, sin
cambiar las restricciones de edición del agente Plan.

La asignación inicial es Terra estándar para asistente, redactor, analista,
especialistas de texto y análisis y Build; Sol estándar para investigación,
revisión, especialista de revisión y Plan. Luna queda como opción manual para
extracción y tareas acotadas. Si no se detecta un modelo se mantiene la
preferencia anterior, si existe. Son preferencias, no pruebas de superioridad
en farmacoepidemiología. Comprueba las tareas y el consumo con datos sintéticos.

OpenAI describe Fast como mayor velocidad del mismo modelo con mayor consumo
de cuota o créditos; no implica menor capacidad. Estas preferencias usan las
referencias estándar, sin sufijo `-fast`. Una sesión existente puede conservar
otro modelo o velocidad. Disponibilidad y consumo dependen del plan y cliente.
Fuentes: [modelos de Codex](https://developers.openai.com/codex/models) y
[velocidad Fast y Ultrafast](https://developers.openai.com/codex/agent-configuration/speed).

## Skills y perfiles

Una skill proporciona instrucciones de trabajo; cargarla no selecciona ni
cambia el modelo. El agente utiliza el modelo efectivo de su sesión, y un
subagente el que tenga configurado o, si falta, el heredado.

| Skill | Perfil inicial sugerido | Cuándo considerar revisión adicional |
| --- | --- | --- |
| `farma-word` | Terra: redacción y documentos | Sol para crítica metodológica compleja. |
| `farma-analisis` | Terra: R, Python y comprobaciones | Sol para diseño o inferencia complejos. |
| `farma-redcap` | Terra: integración y exportación segura | Sol para dudas metodológicas sustanciales; no sustituye permisos. |
| `farma-epidemiologia` | Sol: diseño y revisión | Terra puede responder preguntas sencillas. |
| `farma-evidencia` | Sol: síntesis y revisión compleja | Terra para una búsqueda o comprobación acotada. |

Estas asociaciones son orientativas, no cambian de modelo automáticamente ni
implican que deba delegarse cada tarea. Ambas skills metodológicas pueden ser
necesarias en un análisis; usa solo las pertinentes. La revisión independiente
no se activa automáticamente y no reemplaza la revisión experta humana.

Asistente farma puede delegar tareas especializadas a `especialista-texto`,
`especialista-analisis` o `especialista-revision` con el modelo de su nivel.
Una tarea sencilla se resuelve directamente. Los subagentes heredan el modelo
del padre si no se pudo asignar uno: no equivale a una selección óptima.
Delegar implica llamadas adicionales y no garantiza ahorro. La elección se
basa en instrucciones al modelo, no en un clasificador determinista; para
contenido confidencial hace falta autorización del usuario y de la institución.

Los comandos `/revisar-texto`, `/analizar-datos`, `/protocolo` y
`/revision-profunda` seleccionan su agente y, cuando existe, su modelo
preferido. La selección manual de un agente principal **no cambia** el modelo
ya elegido en una sesión; usa `/models` para cambiarlo. El asistente puede
delegar, pero no hay garantía de ahorro o calidad. Si una
solicitud falla por indisponibilidad, usa `/models` y selecciona uno disponible.

La **ventana de contexto** es el espacio para la conversación y el material que
recibe el modelo. Los **tokens** son unidades procesadas; el **coste** depende
del modelo, entrada, salida, caché y contrato. Una estimación local no es una
factura. No prometemos límites de gasto automáticos: configúralos en el proveedor
si ofrece esa opción y revisa su panel.

OpenCode muestra información y límites de uso según el proveedor y la interfaz.
Para una conversación larga, inicia otra sesión con un resumen revisado. Puede
haber compactación automática; verifica que conserve las decisiones importantes.
