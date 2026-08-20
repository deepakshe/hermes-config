# Telegram Bot + Hermes + Ollama — Windows Setup

## Complete Setup Guide (Tested on Windows 11)

### Prerequisites
- Hermes Agent installed (v3.x)
- Ollama installed with at least one model (hermes3:3b recommended)
- Docker Desktop for n8n

### Step 1: Create Telegram Bot
1. Open Telegram → search `@BotFather`
2. Send `/newbot` → choose name → choose username
3. Copy the token (format: `1234567890:ABC...`)

### Step 2: Configure Hermes
```bash
hermes config set platforms.telegram.bot_token <TOKEN>
hermes gateway restart
```

### Step 3: Test
Open Telegram → search your bot → send `/start`

## n8n MCP Bridge Setup (Windows)

The standard installer fails on Windows. Manual steps:

```bash
cd C:/Users/admin/AppData/Local/hermes/mcp-installs/n8n
python3 -m venv --copies .venv
.venv/Scripts/pip install -r requirements.txt
```

**If pydantic-core version mismatch:**
```bash
.venv/Scripts/pip install pydantic-core==2.46.4 --force-reinstall
```

**Create env file:**
```bash
mkdir C:/Users/admin/.config/n8n-mcp
echo N8N_BASE_URL=http://127.0.0.1:5678 > C:/Users/admin/.config/n8n-mcp/env
echo N8N_API_KEY=<key from n8n UI> >> C:/Users/admin/.config/n8n-mcp/env
```

**Add to Hermes config:**
```bash
hermes mcp add n8n --command "C:/Users/admin/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe" --args "C:/Users/admin/AppData/Local/hermes/mcp-installs/n8n/server.py" --env N8N_MCP_ENV=C:/Users/admin/.config/n8n-mcp/env
```

Type `y` when prompted to enable all tools.

### Step 4: Verify
```bash
hermes mcp test n8n
```

## Troubleshooting

### 409 Conflict Error
**Symptom:** `terminated by other getUpdates request`
**Cause:** Multiple processes polling Telegram API simultaneously
**Fix:**
```bash
taskkill /F /IM python.exe
```
Then use ONLY Hermes gateway — do NOT run standalone bot scripts alongside.

### 401 Unauthorized (n8n)
**Cause:** API key invalid or not set in env file
**Fix:** Regenerate in n8n UI → Settings → API → update env file

### Ollama Not Responding
```bash
ollama serve
curl http://localhost:11434/api/tags
```

### Bot Gives Generic Responses
**Cause:** Intent classification too narrow or keyword matching failing
**Fix:** Expand intent matching to include common Hindi/Hinglish phrases. Use `any(word in text.lower() for word in [...])` patterns.

## Key Lesson: Listen to Intent, Not Exact Words

User might say:
- "kr ab automate" → means "do the automation NOW"
- "setup karo" → means "you set it up, don't explain"
- "band kar do" → means "stop it", not "close the window"

**Always interpret the underlying intent, not just the surface keywords.**
