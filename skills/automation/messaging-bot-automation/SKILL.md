---
name: messaging-bot-automation
description: "Build AI messaging bots for Telegram and WhatsApp."
version: 1.0.0
author: Hermes Agent Session
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [telegram, bot, automation, n8n, ollama, messaging, selling, ai]
    homepage: https://hermes-agent.nousresearch.com/docs/
---

# Messaging Bot Automation

Build AI messaging bots for Telegram/WhatsApp. Handles selling, customer service, and content delivery with natural Hinglish responses.

## When to Use

- User wants a Telegram/WhatsApp bot for selling digital products
- User wants natural, human-like AI responses (not corporate/robotic)
- User wants to automate payment handling and product delivery via messaging
- User wants to connect n8n workflows with messaging platforms
- User wants to integrate Ollama/local models with chat interfaces

## User Preferences (MUST FOLLOW)

### Response Style
- **Natural Hinglish** — mix Hindi + English casually, like a real friend
- **NO corporate/robotic language** — avoid "I am here to assist you", "Please find below", formal structures
- **Use emojis naturally** — but don't overdo it
- **Acknowledge emotions** — when user is frustrated, validate it directly ("Bhai, samajh gaya", "Maaf karta hoon")
- **Be direct** — no fluff, get to the point

### Action vs. Instruction
- **DO, don't just TELL** — user wants you to take actions, not give step-by-step instructions
- If user says "setup karo", you SET IT UP — don't explain how
- If user says "fix karo", you FIX IT — don't give debugging steps
- **Ownership mentality** — treat the user's problem as YOUR problem

### Bot Behavior
- **Listen to intent, not keywords** — if user says "kr ab automate", they mean "do the automation now"
- **Never give generic responses** to specific requests
- **No repetition** — don't keep saying "Bata, main yahin hoon!" for every message
- **Context awareness** — remember conversation history

## Technical Setup

### Telegram Bot + Hermes Gateway
1. Create bot via @BotFather → get token
2. `hermes config set platforms.telegram.bot_token <token>`
3. `hermes gateway restart` (from OUTSIDE the gateway process)

**⚠️ CRITICAL: Do NOT run standalone Python bot AND Hermes gateway simultaneously** — 409 conflict. Use ONE.

### n8n MCP Bridge (Windows)
Install fails due to path issues. Manual fix:
```bash
cd C:/Users/admin/AppData/Local/hermes/mcp-installs/n8n
python3 -m venv --copies .venv
.venv/Scripts/pip install -r requirements.txt
```
If pydantic-core mismatch: `pip install pydantic-core==2.46.4 --force-reinstall`

Add: `hermes mcp add n8n --command "...python.exe" --args "...server.py" --env N8N_MCP_ENV=...`

### Ollama Integration
- Default: `hermes3:3b` (2GB, 4GB+ RAM)
- API: `http://localhost:11434/api/generate`

## Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| 409 Conflict | Multiple bot polling | Kill all Python, use ONE |
| 401 Unauthorized | Bad API key | Regenerate in n8n UI |
| Generic bot responses | Ollama down | `ollama serve` |
| PDF not found | Wrong path | Use absolute paths |

## References

- `references/telegram-bot-setup.md` — Complete Windows setup guide (Telegram + Hermes + n8n + Ollama)
- `references/n8n-workflows-selling.md` — 5 n8n workflow templates for PDF selling automation
- `references/social-media-templates.md` — Content for Instagram, Telegram, Facebook, Twitter, WhatsApp

## Cost

All free: Ollama (local), Telegram bot, n8n, Hermes. Gumroad takes 5-10% if used, or use direct UPI.