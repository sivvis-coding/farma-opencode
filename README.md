# Asistente de investigación farmacológica

Paquete personalizable para OpenCode V2 en Windows, pensado para investigación en
farmacoepidemiología, REDCap, Word y análisis en R o Python. Funciona en español e inglés.

## Empezar

1. Descarga este repositorio como ZIP y descomprímelo en una carpeta permanente.
2. Instala OpenCode V2 para Windows desde la [documentación oficial](https://opencode.ai/docs/).
3. Abre PowerShell en la carpeta descargada y ejecuta:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
   ```

   El instalador muestra los destinos y pide confirmación. Si ya existe uno de
   los archivos gestionados, se detiene sin sobrescribirlo. Para actualizaciones
   consulta `docs/instalacion.md`.
4. Abre una carpeta de trabajo y ejecuta `opencode`. Usa `/connect` para conectar
   OpenAI y `/models` para elegir un modelo disponible.
5. Selecciona **asistente-farma** desde la lista de agentes. También puedes usar
   analista-farma, redactor-farma, revisor-farma o investigador-farma.

No hace falta que los proyectos sean repositorios Git. Los agentes y skills se
instalan en la configuración global del usuario, no dentro de cada proyecto.

## Instalar con ayuda de OpenCode

Si ya tienes OpenCode instalado y conectado a un modelo, ábrelo y pega el enlace
de este repositorio junto con este mensaje:

> Ayúdame a instalar este paquete en Windows. Primero lee su README y el script
> de instalación, explícame los cambios y pídeme confirmación. No sobrescribas
> configuraciones existentes sin avisar. No me pidas que escriba claves o tokens
> en esta conversación. Guíame paso a paso para conectar OpenAI y, después,
> REDCap sin enviar datos confidenciales al modelo.

Revisa el enlace y los archivos antes de aprobar la ejecución de un script.
OpenCode puede ayudarte a descargar el repositorio y ejecutar el instalador,
pero necesitará conexión de red y las aprobaciones que correspondan. La
autorización para acceder a REDCap y compartir datos sigue siendo independiente.

## Empieza por aquí

- [Guía rápida y ejemplos bilingües](docs/uso.md)
- [Instalación, actualización y personalización](docs/instalacion.md)
- [REDCap y protección de datos](docs/redcap.md)
- [Modelos, contexto y costes](docs/modelos.md)
- [Fuentes externas evaluadas](docs/fuentes.md)
- [Ejemplo con datos sintéticos](examples/README.md)

## Alcance de esta primera versión

Incluye instrucciones, agentes, comandos, un exportador local de REDCap y
ejemplos. **No instala ni configura automáticamente OpenCode, R, Python, Word,
un MCP, paquetes externos o un proveedor de IA**. No garantiza control de
cambios nativo de Word ni la preservación de todos sus elementos: hay que
comprobar cada documento en Word. La interfaz usa las funciones nativas de
OpenCode; no incluye un panel de archivos ni un indicador de costes propio.

Los resultados son borradores que requieren revisión profesional. El acceso a
REDCap no autoriza enviar datos, metadatos o documentos a un proveedor de IA.
