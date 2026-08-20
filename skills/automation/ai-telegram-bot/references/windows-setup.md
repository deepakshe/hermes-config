# Windows Setup for Telegram Bot

## Python Path
Windows MSYS/Git-bash environment:
- Python: `C:/Users/admin/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe`
- Run with: `python -u script.py` (unbuffered output)
- pip: `pip install <package>`

## Path Conventions
- Forward slashes work: `C:/Users/admin/Downloads/bot.py`
- Backslashes work in cmd: `C:\Users\admin\Downloads\bot.py`
- Do NOT mix: `C:\Users/admin\Downloads` fails in git-bash

## curl on Windows
MSYS curl works for API testing:
```bash
curl -s 'https://api.telegram.org/bot<TOKEN>/getMe'
```
Use single quotes around URLs with special characters.

## Python Libraries
- `requests` — for Telegram API (urllib has token encoding issues on Windows)
- Install: `pip install requests`

## Running Background Processes
```bash
# Start in background (MSYS)
terminal(background=true, command="python -u C:/path/to/bot.py")

# Or use Windows start
cmd.exe /c "start BotTitle python -u C:\path\to\bot.py"
```

## Token Redaction
Hermes logs redact tokens after first display:
- `8927696890:AAH1wt...` → `8927696890:***`
- Read raw config file: `cat ~/.hermes/config.yaml`
- Or ask user to re-paste token
