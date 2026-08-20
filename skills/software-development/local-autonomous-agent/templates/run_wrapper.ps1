# Run wrapper for a local autonomous agent.
# Clears the leaking global PYTHONPATH so the project venv is used cleanly,
# then activates the venv, integrity-checks, and launches bot.py.
$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition

# 1. Clear leaking PYTHONPATH (global env injects Hermes venv paths)
$env:PYTHONPATH = ""

# 2. Determine python interpreter (project venv preferred)
$VenvPy = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (Test-Path $VenvPy) { $Python = $VenvPy }
else {
    Write-Warning "Project .venv not found. Run: python -m venv .venv ; .venv\Scripts\pip install -r requirements.txt"
    $Python = "python"
}

# 3. Integrity checks before launch
& $Python -m py_compile bot.py agent/*.py tools/*.py hospital/*.py storage/*.py
if ($LASTEXITCODE -ne 0) { Write-Error "Syntax check failed. Aborting."; exit 1 }
& $Python -m pip check
if ($LASTEXITCODE -ne 0) { Write-Warning "pip check reported issues (non-fatal)." }

# 4. Launch
Write-Host "Launching bot.py ..."
& $Python (Join-Path $ProjectRoot "bot.py")
