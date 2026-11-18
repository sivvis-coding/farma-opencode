# Instalación y mantenimiento en Windows

## Requisitos

- Windows y OpenCode V2: descarga el binario apropiado desde
  [OpenCode](https://opencode.ai/docs/), siguiendo sus instrucciones oficiales.
- Una cuenta y método de conexión admitido por OpenCode. ChatGPT y API pueden
  tener condiciones y facturación diferentes.
- Python 3.8+ para el exportador REDCap incluido. R y Python son opcionales para
  análisis; el paquete no los instala.

Descarga y descomprime este repositorio en una carpeta permanente. Abre PowerShell
en esa carpeta. Para ver los cambios sin escribir:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -DryRun
```

Para instalar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
```

El script copia los archivos de `package` e integra en el `opencode.json`
global el agente inicial, instrucciones y preferencias de modelos. Conserva las
otras propiedades y crea una copia previa de la configuración existente; no
modifica `cli.json`. Respeta `XDG_CONFIG_HOME`, si existe. La ejecución requiere
escribir `SI`. Si encuentra archivos del paquete con el mismo nombre, se
detiene antes de copiar, salvo que se indique `-Update`. Si existe
`opencode.jsonc`, o el JSON no se puede interpretar, se detiene sin modificarlo:
revisa la configuración manualmente antes de continuar.

Si OpenAI todavía no estaba conectado al instalar, ejecuta `/connect`, conecta
la cuenta y vuelve a ejecutar el instalador con `-Update`. La detección consulta
`opencode models`, no solicita ni guarda tokens. Si no encuentra un modelo de un
nivel deja ese nivel sin configurar. Los modelos y planes pueden cambiar.

## Actualizar

Descarga la nueva versión, revisa los cambios y ejecuta:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Update
```

Se pide confirmación y se guardan copias de los archivos existentes que se
reemplazarán y el `opencode.json` anterior en una carpeta `farma-backup-*` bajo
la configuración de OpenCode.
Una actualización sí reemplaza los archivos instalados con los mismos nombres:
si los personalizaste, compara y recupera tus cambios desde la copia. No elimina
otros archivos ni versiones anteriores. El instalador no es transaccional; ante
un error revisa la copia y los archivos mostrados.

## Personalizar

Los agentes están en `~/.config/opencode/agents`, las skills en `skills` y los
comandos en `commands`. Cambia sus descripciones o instrucciones con un editor;
el nombre del archivo identifica al agente. Guarda una copia de tus cambios antes
de actualizar. Evita nombres idénticos a los de otras configuraciones.

La interfaz se configura aparte en `~/.config/opencode/cli.json` o mediante
`Ctrl+P` → **Open settings**. Prueba tema, pestañas y ratón. El instalador no
sobrescribe esta configuración. Para abrir una carpeta: en el Explorador entra en
ella, escribe `powershell` en la barra de direcciones y ejecuta `opencode`.

### Barra de cuota y árbol de archivos: instalación opcional

La barra y el árbol dependen de complementos de terceros, que ejecutan código;
revisa sus políticas, procedencia y autorización antes de activarlos. La
disponibilidad de cuotas depende de la cuenta y del complemento.

1. Haz una copia de `opencode.json` y `cli.json` existentes. Si no existen,
   créalos como objetos JSON; no sustituyas propiedades o plugins existentes.
2. En el array `plugins` de `opencode.json`, añade
   `"@yassirh/opencode-codex-limits-plugin@0.1.1"` y, si quieres el árbol,
   `"opencode-dir-tree-tui@1.0.6"`.
3. En el array `plugins` de `cli.json`, añade la ruta absoluta a
   `plugins/farma-barra` dentro de la carpeta de configuración, usando barras
   `/`. Para evitar barras duplicadas, añade también `"-codex-limits.tui"` y
   `"-opencode.sidebar.context"`. Mantén todos los demás elementos.
4. En OpenCode ejecuta `/reload` y comprueba que aparecen la barra y el árbol.
   Si falta la cuota, revisa la conexión compatible sin mostrar credenciales.

Estas instrucciones son manuales: la prueba automatizada del instalador no
comprueba la descarga ni la presentación real de estos complementos.
