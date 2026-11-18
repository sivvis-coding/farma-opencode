---
name: farma-modelos
description: Consultar y recomendar modelos de IA según tarea, calidad, consumo de cuota y precios actuales; current model selection, usage limits and costs
---

# Recomendación actualizada de modelos

Usa esta skill cuando se solicite comparar, elegir o revisar modelos, variantes,
costes o consumo de cuota, también para asignaciones de agentes y skills.

1. Identifica tarea, calidad y urgencia deseadas, proveedor, plan, forma de
   conexión (suscripción o API) y prioridad de cuota. Pregunta solo si una
   diferencia es decisiva; de otro modo indica las suposiciones.
2. Consulta información vigente en fuentes oficiales del proveedor: catálogo,
   modelos, disponibilidad por plan, límites y precios; para OpenCode consulta
   además su documentación V2. Busca la documentación oficial actual si los
   enlaces cambian. Usa búsqueda y consulta web disponibles, sin enviar datos
   confidenciales, nombres de pacientes, credenciales ni material privado.
3. Si es pertinente, consulta el catálogo disponible de OpenCode sin acceder
   a credenciales. Distingue modelos listados de acceso realmente confirmado;
   no lances solicitudes de prueba que consuman cuota sin autorización.
4. Distingue cuota incluida, créditos adicionales y facturación API: no
   traduzcas precios de API o créditos directamente a cuota de suscripción.
   Comprueba velocidades estándar, Fast o equivalentes, su consumo publicado,
   esfuerzo de razonamiento y disponibilidad. No supongas que un modelo
   anterior consume menos. Considera contexto, caché, herramientas y delegación.
5. Recomienda opciones concretas para la tarea, explica el equilibrio entre
   calidad, velocidad y consumo, cita enlaces y fecha de consulta. Declara
   incertidumbres y discrepancias entre documentación, plan e indicadores; no
   prometas ahorro, calidad o disponibilidad. Si no hay acceso a información
   actual, dilo y ofrece solo una recomendación provisional sin inventar datos.
6. Explica en lenguaje cotidiano qué modelo se usa, para qué sirve y su consumo
   relativo orientativo: bajo, medio o alto, aclarando que no es una medición.
   Ofrece una alternativa más económica y menciona que la velocidad rápida o
   una delegación adicional pueden aumentar el consumo, cuando corresponda.
   Si no puedes comprobar el modelo efectivo, dilo sin adivinarlo.
7. Una vez que la persona elija un perfil, úsalo realmente cuando sea posible:
   para una tarea especializada, delega en un subagente configurado con ese
   modelo cuando corresponda y esté permitido. Indica qué agente y modelo
   se solicitan y que la llamada adicional consume cuota. Si no es posible
   verificar o seleccionar el modelo, dilo y explica cómo elegirlo en
   `/models`; nunca afirmes que lo has cambiado si no lo has hecho. Una skill
   por sí sola no cambia el modelo y la sesión puede conservar el anterior.
8. No pidas permiso de nuevo para utilizar el modelo elegido para esa tarea.
   Antes de una opción especialmente costosa o una delegación no prevista,
   advierte y ofrece alternativa. Cambiar de manera permanente modelos de
   agentes o configuración requiere autorización para ese cambio; conserva
   ajustes ajenos, crea copias y verifica.

Fuentes iniciales, sujetas a cambio:
- https://developers.openai.com/codex/models
- https://developers.openai.com/codex/pricing
- https://developers.openai.com/codex/agent-configuration/speed
- https://developers.openai.com/api/docs/pricing
- https://opencode.ai/docs/models

## Actualización y memoria

Antes de recomendar modelos, consulta de forma autónoma las fuentes oficiales
actuales pertinentes si hay acceso a búsqueda o web. No trates estos enlaces,
una respuesta anterior ni precios guardados como vigentes sin verificarlos.
Si una página no contiene la tabla esperada, busca su nueva ubicación oficial y
comprueba la fecha, plan y modalidad. Diferencia falta de datos de ausencia de
límites. No supongas que una tabla para Codex se aplica idénticamente a otra
integración. No hagas pruebas con IA que consuman cuota sin autorización.

Si no puedes consultar o verificar la información, explica en lenguaje sencillo:
«Ahora no puedo verificar la tabla actual. Puedo ayudarte con una recomendación
provisional o puedes indicarme una fuente actualizada». Especifica qué falta,
ofrece volver a buscar cuando sea posible y no inventes cifras. No le pidas
buscar si tú puedes completar la consulta con las herramientas disponibles.

Puedes proponer guardar un resumen breve con fecha, enlaces, alcance y dudas
en una memoria o archivo local autorizado, sin credenciales ni datos sensibles.
Pide autorización antes de crear o modificar esa memoria; no afirmes haberla
guardado si no existe una herramienta o permiso para hacerlo. La memoria es un
registro histórico, no una actualización automática ni una fuente definitiva:
vuelve a verificar antes de usarla para decisiones actuales. No prometas
vigilancia continua, consultas programadas o cambios automáticos de modelos
salvo que estén efectivamente configurados y autorizados.
