---
name: digital-product-selling
description: "Create and sell digital products with automated delivery."
version: 1.0.0
author: Hermes Agent Session
license: MIT
platforms: [linux, macos, windows]
---

# Digital Product Selling

Create and sell digital products with automated delivery pipelines.

## User Workflow Preference

**This user wants ACTION, not explanation. DO IT.**

- Generate content, format it, set up infrastructure — don't explain steps
- Only ask for credentials when technically necessary (API keys, tokens)
- Work fast — skip verbose explanations
- Communicate in Hinglish if user does

## Trigger Conditions

Use when user asks to:
- Create/sell eBooks, PDFs, practice sets, study materials
- Set up automated selling pipelines
- Generate exam preparation content
- Configure n8n workflows for digital product delivery
- Set up Telegram/Discord bots for selling

## Workflow

### 1. Content Generation

**For exam prep content:**
- Use local Ollama models (hermes3:3b) for zero-cost generation
- Generate CSV first, then convert to PDF
- Include: question text, options A-E, correct answer, topic tags

**CSV Format:**
```csv
id,subject,topic,questionText,options,correctAnswer
eng_0,English,Error Detection,Q0: Identify error,Part A|Part B|Part C|Part D|No Error,0
```

### 2. PDF Creation

Use `fpdf2` library (`pip install fpdf2`):

```python
from fpdf import FPDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", "B", 24)
pdf.cell(0, 15, "TITLE", ln=1, align="C")
pdf.output("output.pdf")
```

**PDF Structure:**
1. Cover page
2. Formula sheets / strategy guides
3. Practice questions with answers
4. Study plans and tips

### 3. Selling Infrastructure

**Option A: Telegram Bot (Fastest)**
1. User creates bot via @BotFather
2. Get token: `1234567890:ABCdef...`
3. `hermes config set platforms.telegram.bot_token <token>`
4. **Restart gateway OUTSIDE the gateway process**

**Option B: n8n Workflow Automation**
1. `docker run -d --name n8n -p 5678:5678 n8nio/n8n`
2. Access `http://localhost:5678`, create account, generate API key
3. Connect n8n MCP bridge to Hermes
4. Build workflows: payment → PDF delivery → follow-up

**Option C: Direct Sales (Manual)**
- Share PDF via WhatsApp/Telegram
- Collect payment via UPI/PhonePe
- Send download link after payment

### 4. Marketing Strategy

**Free Sample Funnel:**
1. Create 20-question free sample
2. Share in groups: "Free IBPS sample — DM for full 150Q @ ₹99"

**Pricing:**
- Launch: ₹299 | Standard: ₹399 | Bundle: ₹599
- Affiliate: 20% commission

**Channels:** Telegram groups, Facebook groups, WhatsApp broadcast, Instagram reels

## References

- `references/n8n-setup.md` — Windows Docker setup, MCP bridge config, common errors
- `references/telegram-bot-setup.md` — BotFather process, token config, gateway restart
- `references/ibps-po-content-guide.md` — Topic breakdown, marks coverage (2016-2025)

## Pitfalls

1. **Gateway restart must be external** — Never restart from inside gateway process.

2. **n8n venv issues on Windows** — Use `--system-site-packages` or `--copies` flag.

3. **n8n API key format** — Keys are JWT tokens (eyJ...), not UUIDs. Use `X-N8N-API-KEY` header.

4. **fpdf2 deprecation warnings** — `ln=1` deprecated but works.

5. **Telegram bot not starting** — After setting token, gateway MUST be restarted from outside.

## Verification

- `curl http://localhost:5678/health` → n8n running
- `hermes gateway status` → gateway running
- Send `/start` to Telegram bot → should respond
