# REDCap: acceso local por API

El paquete incluye `tools/redcap_export.py`, una herramienta de solo lectura
independiente de OpenCode. No es un servidor MCP ni conecta automáticamente el
asistente; esta primera versión evita que el token o la respuesta API aparezcan
en una herramienta del modelo.

## Antes de empezar

1. Confirma que tu institución autoriza el acceso mediante API, el almacenamiento
   local y, por separado, cualquier envío a un proveedor de IA.
2. Comprueba con el administrador los permisos de exportación y los campos
   necesarios. Los derechos dependen del usuario y proyecto.
3. Instala Python 3.8 o posterior si no está instalado. Obtén la URL HTTPS de la
   API en REDCap y el token correspondiente. **Nunca lo pegues en la conversación,
   el código, Git ni una captura de pantalla.**
4. Elige una carpeta local protegida autorizada para los resultados. Los metadatos,
   las tablas agregadas y los datos supuestamente anonimizados también pueden ser
   sensibles; eliminar identificadores no garantiza anonimización.

## Exportar diccionario de datos

Desde PowerShell, en la carpeta donde descomprimiste este paquete:

```powershell
py .\tools\redcap_export.py --url "https://tu-institucion.example/api/" --tipo metadata --salida "C:\ruta-protegida\diccionario.csv"
```

Sustituye la URL y ruta. La carpeta de salida debe existir. Tras confirmar
escribiendo `SI`, introduce el token en el prompt oculto. La herramienta no
sobrescribe archivos y no muestra la respuesta. Rechaza redirecciones y requiere
HTTPS con verificación de certificado.

## Exportar registros

Solo si está permitido y después de identificar los campos imprescindibles:

```powershell
py .\tools\redcap_export.py --url "https://tu-institucion.example/api/" --tipo record --campo campo_a --campo campo_b --salida "C:\ruta-protegida\datos.csv"
```

**Importante:** esta opción solicita **todos los registros accesibles** para los
campos seleccionados; no implementa filtros por registro ni anonimización. No la
uses si necesitas restringir filas o si no tienes autorización para esta exportación.
Verifica los campos y las restricciones reales del proyecto antes de ejecutar.

La herramienta no importa ni modifica REDCap. Su certificado, acceso y respuesta
dependen de la instancia; puede requerir adaptación y validación local. No envíes
el CSV al asistente ni lo abras en una sesión que pueda leerlo sin comprobar
primero la autorización institucional. Si se necesita una integración
conversacional directa o MCP, requiere una revisión independiente de seguridad y
aprobación antes de activarse.
