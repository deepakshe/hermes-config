# Telegram Bot Setup (via Hermes Gateway)

## Overview

Connect a Telegram bot to Hermes Agent for automated selling of digital products. The bot can answer queries, send free samples, process payments, and deliver PDFs.

## Prerequisites

- Telegram account
- Hermes Agent installed with gateway running
- Digital product ready (PDF, study material, etc.)

## Step 1: Create Bot via BotFather

1. Open Telegram → Search **@BotFather**
2. Send `/newbot`
3. Follow prompts:
   - **Bot Name:** Display name (e.g., "IBPS Practice Bot")
   - **Bot Username:** Must end with `bot` (e.g., `ibps_practice_exam_bot`)
4. Copy the token (format: `1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ`)
5. Set description and profile picture via BotFather commands

## Step 2: Configure in Hermes

### Set bot token
```bash
hermes config set platforms.telegram.bot_token <your-bot-token>
```

### Restart gateway (MUST be done OUTSIDE the gateway process)
```bash
hermes gateway restart
```

**CRITICAL:** Do NOT run restart from inside a gateway-managed terminal. The gateway will SIGTERM your command before it completes.

## Step 3: Verify Bot is Active

1. Open Telegram → Search your bot
2. Send `/start`
3. Bot should respond with a welcome message
4. Check Hermes logs: `tail -f ~/.hermes/logs/gateway.log`

## Bot Commands to Set Up

Use `/setcommands` via BotFather to define bot commands:

```
start - Welcome message and free sample
sample - Get free 20 questions
buy - Purchase full PDF (₹299)
help - How to use this bot
contact - Contact seller
```

## Selling Workflow in Telegram

### 1. Customer discovers bot
- Posts in Telegram groups: "Free IBPS PO practice questions — DM @YourBot"
- Searches for "IBPS practice" and finds bot

### 2. Customer starts bot
- `/start` → Welcome message + 5 free questions
- `/sample` → Full 20-question sample PDF

### 3. Customer wants to buy
- `/buy` → Payment instructions (UPI QR code, payment link)
- After payment → Auto-send full PDF via bot

### 4. Post-purchase
- Thank you message + quick revision tips
- Referral link: "Share with friends and earn ₹50 per sale"

## Advanced: Webhook Integration

For payment automation:

1. Set up Razorpay/Stripe webhook
2. Configure webhook receiver in Hermes or n8n
3. On payment success → trigger bot to send PDF

### Example: n8n + Telegram
- **Webhook Trigger** → Razorpay payment.succeeded
- **Telegram Node** → Send PDF to customer via bot
- **Email Node** → Backup copy to customer email

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Bot doesn't respond to /start | Gateway not restarted | Restart from outside gateway |
| "Unauthorized" from Telegram API | Invalid token | Regenerate via BotFather, update config |
| Bot commands not showing | Not set via /setcommands | Send command list to BotFather |
| Messages not delivering | Bot blocked by user | User must unblock and send /start |
| Gateway won't start | Port conflict | Check `hermes gateway status` |

## Security Notes

- Never share bot token publicly
- Bot token grants full access to bot — treat like password
- If token leaked → Revoke via BotFather → Generate new token
