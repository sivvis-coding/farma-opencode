# Guía rápida

Abre PowerShell en la carpeta del proyecto y escribe `opencode`. Usa `/connect`
para conectar OpenAI y `/models` para elegir un modelo. Selecciona
`asistente-farma` desde la lista de agentes. `Ctrl+P` abre la paleta de comandos;
`Ctrl+O` permite acceder a proyectos y sesiones recientes.

Puedes escribir en español o inglés. Ejemplos:

- «Revisa `manuscrito.docx` en inglés y explícame en español las mejoras sin
  modificar el original».
- «Propón una versión revisada en un archivo nuevo. Conserva todas las cifras y
  dime qué referencias tengo que comprobar».
- «Using the synthetic dataset, propose an R analysis and explain the assumptions.»
- «Revisa este protocolo observacional: exposición, comparador, tiempo cero y
  posibles sesgos».
- «Ayúdame a preparar una exportación REDCap autorizada. No me pidas el token».

Los comandos `/revisar-texto`, `/analizar-datos`, `/protocolo` y
`/redcap-ayuda` son atajos opcionales. El contenido de archivos que el agente
lea puede transmitirse al modelo: comprueba primero las normas de tu institución.
Una confirmación en OpenCode no sustituye esa autorización.

Para trabajos de varios pasos, usa `/objetivo-farma` para acordar el objetivo,
entregables y criterios de éxito antes de empezar. Usa `/bitacora-farma` para
preparar un resumen de decisiones y próximos pasos; revisa y autoriza cualquier
archivo antes de guardarlo. No incluyas información personal o confidencial.
OpenCode también ofrece `/goal` para mantener un objetivo de trabajo, con
opciones `pause`, `resume` y `clear`. Úsalo para tareas largas y bien acotadas,
con criterios verificables; revisa los permisos y conserva la supervisión humana.

Para localizar un archivo escribe `@` en el mensaje y selecciónalo. Adjuntarlo
puede enviar su contenido al modelo. Para abrir un documento en Word, usa el
Explorador de Windows; la interfaz aún no incluye un explorador propio de archivos.

La barra compacta experimental de `plugins/farma-barra` requiere el plugin de
terceros `@yassirh/opencode-codex-limits-plugin@0.1.1` instalado por separado y
una conexión Codex compatible. Muestra porcentajes gastados y hora local del
reinicio; a partir del 70 % usa color de aviso y a partir del 95 %, color de
error. La instalación de agentes por sí sola no instala esa dependencia ni
activa la barra en `cli.json`; hay que configurarlas y probarlas por separado.
La barra usa una estimación del último mensaje completo para mostrar WARN desde
150.000 tokens y AVISO desde 250.000. Desde 300.000 solicita compactación
automática mientras la barra TUI está activa. Es una estimación, no el cálculo
interno exacto; puede activar antes o después. Guarda un bloqueo por sesión para
evitar solicitudes repetidas: tras un fallo usa `/compact`. La compactación
propia de OpenCode es independiente y puede actuar antes, según el modelo.
En un entorno aislado se probó la barra con dos TUI reales y un mensaje
sintético de 300k: se registró una compactación y el árbol mostró un archivo
de prueba. La prueba bloqueó proveedores, por lo que no se generó un resumen.
La lectura de cuota autenticada requiere comprobarse en el equipo de destino.

La [guía para investigadoras](guia-investigadora.md) explica el uso cotidiano.

Abre los documentos generados en Word y comprueba tablas, notas, referencias,
imágenes y formato. La comparación de archivos de OpenCode no sustituye el
control de cambios de Word para archivos DOCX.
