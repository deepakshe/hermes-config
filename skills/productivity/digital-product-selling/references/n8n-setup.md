# n8n Setup on Windows (Docker + MCP Bridge)

## Quick Setup

### 1. Run n8n via Docker
```bash
docker run -d --name n8n -p 5678:5678 n8nio/n8n
```

### 2. Initial Setup
1. Open `http://localhost:5678` in browser
2. Create owner account (email, name, password)
3. Verify email if prompted

### 3. Generate API Key
1. Bottom-left → Settings (gear icon) → API
2. Click "Create API Key"
3. Copy the key immediately (format: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`)

### 4. Connect n8n MCP Bridge to Hermes

#### Install MCP bridge
```bash
hermes mcp install n8n
```

#### Store API key in env file
```bash
mkdir -p ~/.config/n8n-mcp
cat > ~/.config/n8n-mcp/env << 'EOF'
N8N_BASE_URL=http://127.0.0.1:5678
N8N_API_KEY=<your-jwt-api-key>
N8N_MCP_TIMEOUT=30
N8N_CONTAINER_NAME=n8n
N8N_MCP_ALLOW_DOCKER_LOGS=true
EOF
```

#### Register with Hermes
```bash
hermes mcp add n8n \
  --command "C:/Users/admin/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe" \
  --args "C:/Users/admin/AppData/Local/hermes/mcp-installs/n8n/server.py" \
  --env N8N_MCP_ENV=C:/Users/admin/.config/n8n-mcp/env
```

When prompted to enable all tools, answer `y`.

### 5. Test Connection
```bash
curl -s -H "X-N8N-API-KEY: <your-jwt-api-key>" http://127.0.0.1:5678/api/v1/workflows
```
Expected: `{"data":[],"nextCursor":null}`

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `pydantic_core._pydantic_core` missing | Venv doesn't include system packages | Use `--system-site-packages` or `--copies` flag when creating venv |
| `HTTP 401 unauthorized` | Invalid API key | Regenerate key in n8n Settings → API |
| `Connection closed` during add | Server can't start | Check env file path and permissions |
| `Port 5678 already in use` | n8n already running | `docker ps` then use existing or `docker rm -f n8n` |
| `.venv/bin/pip` not found (Windows) | Wrong path separator | Use `.venv/Scripts/pip` on Windows |

## Workflow Basics

### Creating a Workflow
1. Click "Create Workflow" in n8n UI
2. Add nodes (triggers, actions, conditions)
3. Connect nodes with edges
4. Save and activate

### Key Nodes for Digital Product Selling
- **Trigger:** Webhook, Schedule, Manual
- **Payment:** Stripe, Razorpay (via HTTP Request)
- **Message:** Telegram, WhatsApp, Email
- **Logic:** IF/Switch, Wait, Merge
- **Data:** Function (code), Set, IF/Then

### Example: Payment → PDF Delivery Flow
1. **Webhook Trigger** → Receives payment notification
2. **IF Node** → Check payment status = "success"
3. **HTTP Request** → Fetch customer email from payment data
4. **Email Node** → Send PDF download link
5. **Telegram Node** → Confirm delivery via bot message
