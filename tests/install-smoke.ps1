$ErrorActionPreference = 'Stop'
$root = Join-Path $env:TEMP ("opencode\farma-test-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $root -Force | Out-Null
$original = '{"plugins":["existing-plugin@1.2.3"],"model":"existing/model","agents":{"plan":{"permissions":[{"action":"edit","resource":"*","effect":"deny"}]}},"instructions":["existing.md"]}'
[System.IO.File]::WriteAllText((Join-Path $root 'opencode.json'), $original)
$installer = Join-Path (Split-Path -Parent $PSScriptRoot) 'install.ps1'
'SI' | powershell -NoProfile -ExecutionPolicy Bypass -File $installer -ConfigRoot $root
if ($LASTEXITCODE -ne 0) { throw "Install failed: $LASTEXITCODE" }
$config = Get-Content -LiteralPath (Join-Path $root 'opencode.json') -Raw | ConvertFrom-Json
if ($config.default_agent -ne 'asistente-farma') { throw 'Default agent not set' }
if ($config.model -ne 'existing/model') { throw 'Existing default model changed' }
if ($config.plugins[0] -ne 'existing-plugin@1.2.3') { throw 'Plugin removed' }
if ($config.agents.plan.permissions[0].effect -ne 'deny') { throw 'Plan restrictions changed' }
if ($config.instructions -notcontains 'existing.md') { throw 'Instructions removed' }
if (-not (Test-Path -LiteralPath (Join-Path $root 'skills\farma-modelos\SKILL.md'))) { throw 'Model skill missing' }
if (-not (Test-Path -LiteralPath (Join-Path $root 'plugins\farma-barra\politica.mjs'))) { throw 'Compaction policy missing' }
if (@(Get-ChildItem -LiteralPath $root -Directory -Filter 'farma-backup-*').Count -ne 1) { throw 'Backup missing' }
Write-Host "Smoke test OK: $root"
