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
$configFile = Join-Path $ConfigRoot 'opencode.json'
$jsoncFile = Join-Path $ConfigRoot 'opencode.jsonc'
if (Test-Path -LiteralPath $jsoncFile) {
    throw 'Existe opencode.jsonc: no se modificará automáticamente. Consulta docs/instalacion.md.'
}
$config = if (Test-Path -LiteralPath $configFile) {
    $rawConfig = Get-Content -LiteralPath $configFile -Raw
    if (-not $rawConfig.Trim()) { throw 'opencode.json está vacío; no se modificará.' }
    try { $rawConfig | ConvertFrom-Json } catch { throw 'opencode.json no es JSON válido; no se modificará.' }
} else { [pscustomobject]@{} }
if ($null -eq $config -or $config -is [array] -or $config -isnot [pscustomobject]) {
    throw 'opencode.json debe contener un objeto JSON.'
}
$modelNames = @()
if (Get-Command opencode -ErrorAction SilentlyContinue) {
    try {
        $modelNames = @(opencode models 2>$null)
        if ($LASTEXITCODE -ne 0) { $modelNames = @() }
    } catch { $modelNames = @() }
}
function Select-AvailableModel([string[]]$Candidates) {
    foreach ($candidate in $Candidates) {
        if ($modelNames -contains $candidate) { return $candidate }
    }
    return $null
}
$fast = Select-AvailableModel @('openai/gpt-6-luna', 'openai/gpt-5.6-luna')
$balanced = Select-AvailableModel @('openai/gpt-6.1-terra', 'openai/gpt-5.6-terra')
$deep = Select-AvailableModel @('openai/gpt-6.2-sol', 'openai/gpt-6.1-sol', 'openai/gpt-5.6-sol')
$files = @(Get-ChildItem -LiteralPath $source -File -Recurse)
if ($files.Count -eq 0) { throw 'No se encuentran los archivos del paquete.' }
$items = @($files | ForEach-Object {
    $relative = $_.FullName.Substring($source.Length).TrimStart('\', '/')
    [pscustomobject]@{ Source = $_.FullName; Target = Join-Path $ConfigRoot $relative }
})
$conflicts = @($items | Where-Object { Test-Path -LiteralPath $_.Target })
Write-Host "Destino: $ConfigRoot"
Write-Host "Agente inicial: asistente-farma (nuevas sesiones)"
Write-Host "Modelos detectados: rapido=$fast; equilibrado=$balanced; profundo=$deep"
Write-Host "Se integraran estas preferencias en $configFile conservando el resto."
Write-Host "Archivos: $($items.Count); existentes: $($conflicts.Count)"
$items | ForEach-Object { Write-Host "  $($_.Target)" }
if ($conflicts.Count -gt 0 -and -not $Update) {
    Write-Host 'Hay archivos existentes. No se ha modificado nada. Consulta docs/instalacion.md.'
    if (-not $DryRun) { exit 1 }
}
if ($DryRun) { Write-Host 'Simulación: no se ha escrito nada.'; exit 0 }
$answer = Read-Host '¿Continuar? Escribe SI para confirmar'
if ($answer -cne 'SI') { Write-Host 'Cancelado.'; exit 0 }
if ($conflicts.Count -gt 0 -or (Test-Path -LiteralPath $configFile)) {
    $backup = Join-Path $ConfigRoot ("farma-backup-" + [guid]::NewGuid().ToString('N'))
    foreach ($item in $conflicts) {
        $relative = $item.Target.Substring($ConfigRoot.Length).TrimStart('\', '/')
        $destination = Join-Path $backup $relative
        New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
        Copy-Item -LiteralPath $item.Target -Destination $destination
    }
    if (Test-Path -LiteralPath $configFile) {
        New-Item -ItemType Directory -Path $backup -Force | Out-Null
        Copy-Item -LiteralPath $configFile -Destination (Join-Path $backup 'opencode.json')
    }
    Write-Host "Copia de seguridad de archivos existentes: $backup"
}
function Set-Property($Object, [string]$Name, $Value) {
    if ($Object.PSObject.Properties[$Name]) { $Object.$Name = $Value }
    else { $Object | Add-Member -NotePropertyName $Name -NotePropertyValue $Value }
}
if (-not $config.PSObject.Properties['$schema']) {
    Set-Property $config '$schema' 'https://opencode.ai/config.json'
}
Set-Property $config 'default_agent' 'asistente-farma'
$instructionFile = (Join-Path $ConfigRoot 'farma-eficiencia.md').Replace('\', '/')
if (-not $config.PSObject.Properties['instructions']) {
    Set-Property $config 'instructions' @($instructionFile)
} elseif ($config.instructions -is [array]) {
    if ($config.instructions -notcontains $instructionFile) {
        Set-Property $config 'instructions' (@($config.instructions) + @($instructionFile))
    }
} else { throw 'La configuración instructions existente no es una lista.' }
if (-not $config.PSObject.Properties['agents']) { Set-Property $config 'agents' ([pscustomobject]@{}) }
if ($config.agents -isnot [pscustomobject]) { throw 'La configuración agents existente no es un objeto.' }
$profiles = @(
    @{ id = 'asistente-farma'; model = $balanced },
    @{ id = 'redactor-farma'; model = $balanced },
    @{ id = 'analista-farma'; model = $balanced },
    @{ id = 'investigador-farma'; model = $deep },
    @{ id = 'revisor-farma'; model = $deep },
    @{ id = 'especialista-texto'; model = $balanced },
    @{ id = 'especialista-analisis'; model = $balanced },
    @{ id = 'especialista-revision'; model = $deep },
    @{ id = 'build'; model = $balanced },
    @{ id = 'plan'; model = $deep }
)
foreach ($profile in $profiles) {
    if (-not $config.agents.PSObject.Properties[$profile.id]) {
        Set-Property $config.agents $profile.id ([pscustomobject]@{})
    }
    $entry = $config.agents.($profile.id)
    if ($entry -isnot [pscustomobject]) { throw "El agente $($profile.id) no es un objeto." }
    if ($profile.model) { Set-Property $entry 'model' $profile.model }
}
Set-Property $config.agents.build 'description' 'Trabajo práctico reproducible con uso eficiente de herramientas'
Set-Property $config.agents.plan 'description' 'Planificación sin modificar archivos y con uso eficiente de contexto'
if ($balanced -and -not $config.PSObject.Properties['model']) {
    Set-Property $config 'model' $balanced
}
foreach ($item in $items) {
    New-Item -ItemType Directory -Path (Split-Path -Parent $item.Target) -Force | Out-Null
    Copy-Item -LiteralPath $item.Source -Destination $item.Target -Force
}
$json = $config | ConvertTo-Json -Depth 100
[System.IO.File]::WriteAllText($configFile, $json, (New-Object System.Text.UTF8Encoding($false)))
Write-Host 'Instalación completada. Abre OpenCode desde tu proyecto.'
if (-not $balanced) { Write-Host 'Conecta OpenAI y vuelve a ejecutar con -Update para detectar modelos.' }
