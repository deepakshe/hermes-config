---
name: hermes-gateway-and-platforms
description: "Integrate Hermes with n8n, Telegram, webhooks, MCP."
version: 1.0.0
author: Hermes Agent Session
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, gateway, platforms, n8n, telegram, mcp, integration, automation]
    homepage: https://hermes-agent.nousresearch.com/docs/
---

# Hermes Gateway & Platform Integration

Connect Hermes to external automation platforms, messaging bots, and services via MCP bridges, webhooks, and the built-in gateway.

## Platform Access Reality Check

**What Hermes CAN integrate with:**
- **n8n** — local workflow automation via MCP bridge (stdio transport, no public port)
- **Telegram** — bot integration via gateway bot_token
- **Discord, Slack, WhatsApp** — via gateway OAuth/config
- **Figma, Linear, Comfy Cloud** — via official MCP catalog servers (OAuth)
- **Generic webhooks** — inbound event triggers to agent runs

**What Hermes CANNOT do:**
- Direct Instagram/Facebook/WhatsApp API access — no public API for chat automation or account control
- "Full access" via password sharing — not supported. Uses OAuth tokens, API keys, bot tokens only
- Bypass platform ToS restrictions

When users ask for unavailable platform access, redirect to legitimate alternatives. Never claim something is "impossible" without stating what IS possible.

## n8n Local MCP Bridge Setup

Run n8n as a local Docker container and bridge it to Hermes via MCP.

### Requirements
- Docker installed and running
- Hermes gateway running (`hermes gateway status`)
- n8n API key (generated from n8n UI: Settings → API)

### Docker Setup
```bash
docker run -d --name n8n -p 5678:5678 n8nio/n8n
curl http://127.0.0.1:5678/health
```

### MCP Bridge Registration
```bash
hermes mcp add n8n \
  --command "C:/Users/admin/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe" \
  --args "C:/Users/admin/AppData/Local/hermes/mcp-installs/n8n/server.py" \
  --env N8N_MCP_ENV=C:/Users/admin/.config/n8n-mcp/env
```

### Env File (`~/.config/n8n-mcp/env`)
```
N8N_BASE_URL=http://127.0.0.1:5678
N8N_API_KEY=eyJ...your-jwt-token...
N8N_MCP_TIMEOUT=30
N8N_CONTAINER_NAME=n8n
N8N_MCP_ALLOW_DOCKER_LOGS=true
```

### Windows Fix: pydantic-core venv Conflict
Use the Hermes agent venv directly. If pydantic-core mismatch:
```bash
cd C:/Users/admin/AppData/Local/hermes/hermes-agent/venv
Scripts/pip install pydantic-core==2.46.4 --force-reinstall
```

### Available n8n MCP Tools
- `health`, `list_workflows`, `get_workflow`, `find_workflows`
- `list_executions`, `get_execution`, `recent_failures`
- `export_workflow`, `activate_workflow`, `deactivate_workflow`
- `container_logs`

## Telegram Bot Integration

1. Create bot via @BotFather on Telegram
2. Get bot token (format: `1234567890:ABCdef...`)
3. Configure: `hermes config set platforms.telegram.bot_token "YOUR_TOKEN"`
4. Ensure gateway running: `hermes gateway restart`

## Webhook Subscriptions

### Enable
```bash
# config.yaml:
# platforms:
#   webhook:
#     enabled: true
#     extra:
#       port: 8644
#       secret: "your-secret"
```

### Subscribe
```bash
hermes webhook subscribe payment-received \
  --prompt "Payment {data.object.amount} received. Deliver product." \
  --deliver telegram \
  --deliver-chat-id "YOUR_CHAT_ID"
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `Failed to connect` in mcp add | Wrong python path | Use Hermes venv python |
| `pydantic_core._pydantic_core` missing | Version mismatch | Force reinstall pydantic-core==2.46.4 |
| `Connection closed` in mcp add | Server crashed on load | Check env file, verify n8n API key |
| n8n API returns 401 | Wrong/missing API key | Regenerate in n8n UI |
| Telegram bot not responding | Gateway not running | `hermes gateway restart` |

## References

- **Hermes gateway docs**: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/gateway
- **Hermes webhooks**: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks
- **Hermes MCP**: https://hermes-agent.nousresearch.com/docs/user-guide/mcp
- **n8n public MCP bridge**: https://github.com/CyberSamuraiX/hermes-n8n-mcp