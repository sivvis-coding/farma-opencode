param(
    [switch]$Update,
    [switch]$DryRun,
    [string]$ConfigRoot
)

$ErrorActionPreference = 'Stop'
if (-not $ConfigRoot) {
    if ($env:XDG_CONFIG_HOME) { $ConfigRoot = Join-Path $env:XDG_CONFIG_HOME 'opencode' }
    else { $ConfigRoot = Join-Path $HOME '.config\opencode' }
}
$source = Join-Path $PSScriptRoot 'package'
$files = @(Get-ChildItem -LiteralPath $source -File -Recurse)
if ($files.Count -eq 0) { throw 'No se encuentran los archivos del paquete.' }
$items = @($files | ForEach-Object {
    $relative = $_.FullName.Substring($source.Length).TrimStart('\', '/')
    [pscustomobject]@{ Source = $_.FullName; Target = Join-Path $ConfigRoot $relative }
})
$conflicts = @($items | Where-Object { Test-Path -LiteralPath $_.Target })
Write-Host "Destino: $ConfigRoot"
Write-Host "Archivos: $($items.Count); existentes: $($conflicts.Count)"
$items | ForEach-Object { Write-Host "  $($_.Target)" }
if ($conflicts.Count -gt 0 -and -not $Update) {
    Write-Host 'Hay archivos existentes. No se ha modificado nada. Consulta docs/instalacion.md.'
    if (-not $DryRun) { exit 1 }
}
if ($DryRun) { Write-Host 'Simulación: no se ha escrito nada.'; exit 0 }
$answer = Read-Host '¿Continuar? Escribe SI para confirmar'
if ($answer -cne 'SI') { Write-Host 'Cancelado.'; exit 0 }
if ($conflicts.Count -gt 0) {
    $backup = Join-Path $ConfigRoot ("farma-backup-" + [guid]::NewGuid().ToString('N'))
    foreach ($item in $conflicts) {
        $relative = $item.Target.Substring($ConfigRoot.Length).TrimStart('\', '/')
        $destination = Join-Path $backup $relative
        New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
        Copy-Item -LiteralPath $item.Target -Destination $destination
    }
    Write-Host "Copia de seguridad de archivos existentes: $backup"
}
foreach ($item in $items) {
    New-Item -ItemType Directory -Path (Split-Path -Parent $item.Target) -Force | Out-Null
    Copy-Item -LiteralPath $item.Source -Destination $item.Target -Force
}
Write-Host 'Instalación completada. Abre OpenCode desde tu proyecto.'
