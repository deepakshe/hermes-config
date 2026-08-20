---
name: ai-telegram-bot
description: "Build polling Telegram bot when Gateway conflicts."
version: 1.0.0
author: Hermes Agent Session
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [telegram, bot, automation, ai, content]
---

# AI Telegram Bot

Standalone polling Telegram bot — full control, no Gateway dependency.

## Trigger
- User wants Telegram bot for selling/content/support
- Need to bypass Hermes Gateway
- 409 Conflict on same token

## User Preferences (HARD)
1. **DO IT, DON'T TELL IT** — Build, run, verify. Never say "do it yourself."
2. **Direct & Fast** — Working code first, explain later.
3. **Hinglish + Emojis** — Natural Hindi+English mix.
4. **Mirror Chat Agent** — Same HTML formatting, tone, helpfulness.
5. **One-shot** — Fully working, tested, runnable file.

## Script Template
```python
import requests, time

TOKEN = "FULL_TOKEN"  # NOT redaacted
API = f"https://api.telegram.org/bot{TOKEN}"

def send(cid, text):
    if len(text) > 4000:
        text = text[:3997] + "..."
    requests.post(f"{API}/sendMessage", json={
        "chat_id": cid, "text": text, "parse_mode": "HTML"
    }, timeout=10)

def handle(msg):
    cid = msg["chat"]["id"]
    txt = msg.get("text", "").strip()
    name = msg.get("from", {}).get("first_name", "User")
    lower = txt.lower()
    
    if txt == "/start":
        send(cid, "<b>Welcome!</b>")
    elif "hi" in lower:
        send(cid, f"Hello {name}! 👋")
    # ... more matchers ...
    else:
        send(cid, "Default response")

offset = None
while True:
    p = {"timeout": 30}
    if offset: p["offset"] = offset
    u = requests.get(f"{API}/getUpdates", params=p, timeout=35).json()
    if u.get("ok"):
        for up in u.get("result", []):
            offset = up["update_id"] + 1
            if "message" in up: handle(up["message"])
    else: time.sleep(5)
```

## Run Steps
```bash
hermes gateway stop     # If same token conflict
python -u bot.py        # Unbuffered output
```

## Pitfalls
| Error | Fix |
|-------|-----|
| 404 Not Found | Use `requests`, not urllib |
| 409 Conflict | Stop Gateway first |
| Token redacted | Read raw config or re-paste |
| Silent failures | Always send fallback |
| Ollama down | Static fallback responses |
| Gateway restart fails | External shell only |

## Quality Checklist
- [ ] HTML formatting works
- [ ] Commands + natural language
- [ ] Always responds (never silent)
- [ ] Truncates >4000 chars
- [ ] Hinglish + emojis

## References
- `references/windows-setup.md` — Windows paths, Python, curl
- `references/bot-patterns.md` — Common response patterns