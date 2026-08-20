# Venv isolation leak on Windows + Hermes

## Symptom
A project `.venv` (e.g. `C:\Users\admin\Desktop\autopioletbot\.venv`) reports:
- `pip install` says "Not uninstalling X at c:\...\hermes-agent\venv\lib\site-packages, outside environment"
- `import greenlet` → `ModuleNotFoundError: No module named 'greenlet._greenlet'`
- `import pydantic_core` → missing `_pydantic_core`
- `import google.auth` reports an OLD version (e.g. 2.55.1) even after "upgrading"

## Root cause
A GLOBAL `PYTHONPATH` is set to the Hermes agent venv:
```
PYTHONPATH=C:\Users\admin\AppData\Local\hermes\hermes-agent;C:\Users\admin\AppData\Local\hermes\hermes-agent\venv\Lib\site-packages
```
This is prepended to every Python's `sys.path`, so even a fresh project venv imports Hermes' packages first, and pip targets Hermes' site-packages instead of the project venv.

## Confirm
```bat
echo %PYTHONPATH%
```
If it contains `hermes-agent`, the leak is active.

## Fix (per-command, safe, does not alter the global env)
Prefix every `python`/`pip` invocation for the project with `PYTHONPATH=` to clear it:
```bat
cd C:\Users\admin\Desktop\autopioletbot
PYTHONPATH= .venv\Scripts\python.exe -m pip install -r requirements.txt
PYTHONPATH= .venv\Scripts\python.exe -c "import crawl4ai; print('ok')"
```
In `bash`/git-bash the same prefix works.

## If the venv is already corrupted
Rebuild it cleanly (non-destructive; creates fresh env):
```bat
cd C:\Users\admin\Desktop\autopioletbot
rmdir /s /q .venv
"C:\Users\admin\AppData\Local\Python\pythoncore-3.12-64\python.exe" -m venv .venv
PYTHONPATH= .venv\Scripts\python.exe -m pip install -r requirements.txt
PYTHONPATH= .venv\Scripts\python.exe -m pip check
```
Then re-run with `PYTHONPATH=` until `pip check` says "No broken requirements found."

## Gotchas
- A venv created via `python3 -m venv` may use system Python (3.14) instead of the project's 3.12. Use the explicit `pythoncore-3.12-64` interpreter path to match the spec / Playwright prebuilt Chromium.
- `playwright` the package may silently NOT install if pip targeted Hermes. After repair, `PYTHONPATH= .venv\Scripts\python.exe -m pip install playwright` then `playwright install chromium`.
- crawl4ai pulls many transitive deps (rich, aiohttp, httpx, dotenv, requests, numpy). Install the full requirements with `PYTHONPATH=` cleared or they land in Hermes, not the venv.
- **PowerShell scripts must pass explicit file list to py_compile** because patterns like `agent/*.py` fail with "[Errno 22] Invalid argument". Build file array in script:

```powershell
$PythonFiles = @("bot.py", "agent\agent_core.py", "agent\registry.py", ...)
$FileArgs = $PythonFiles | ForEach-Object { Join-Path $ProjectRoot $_ }
& $Python -m py_compile -- $FileArgs
```

## PowerShell runner with isolated venv

Create `run_project.ps1` that:
1. Clears `PYTHONPATH` to prevent Hermes leak
2. Uses project `.venv\Scripts\python.exe`
3. Runs py_compile with explicit file list
4. Launches bot.py

Key PowerShell patterns:
```powershell
# Clear PYTHONPATH
$null = $env:PYTHONPATH
$env:PYTHONPATH = ""

# Build file list
$PythonFiles = @("bot.py", "agent\agent_core.py", ...)
$FileArgs = $PythonFiles | ForEach-Object { Join-Path $ProjectRoot $_ }

# Syntax check with explicit list (not glob patterns)
& $Python -m py_compile -- $FileArgs

# Launch
& $Python (Join-Path $ProjectRoot "bot.py")
```

Run with: `powershell -ExecutionPolicy Bypass -File "run_project.ps1"`
