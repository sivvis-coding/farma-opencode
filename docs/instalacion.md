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

El script solo copia archivos del directorio `package` a la configuración global
de OpenCode; no modifica `opencode.json` ni `cli.json`. Respeta
`XDG_CONFIG_HOME`, si existe. La ejecución requiere escribir `SI`. Si encuentra
archivos con el mismo nombre, se detiene antes de copiar.

## Actualizar

Descarga la nueva versión, revisa los cambios y ejecuta:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Update
```

Se pide confirmación y se guardan copias de los archivos existentes que se
reemplazarán en una carpeta `farma-backup-*` bajo la configuración de OpenCode.
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
