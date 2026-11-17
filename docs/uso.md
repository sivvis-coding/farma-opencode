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

Abre los documentos generados en Word y comprueba tablas, notas, referencias,
imágenes y formato. La comparación de archivos de OpenCode no sustituye el
control de cambios de Word para archivos DOCX.
