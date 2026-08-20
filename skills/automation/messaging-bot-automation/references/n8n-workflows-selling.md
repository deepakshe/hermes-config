# n8n Workflow Templates for PDF Selling Automation

## Workflow 1: Telegram Payment Handler

Trigger: Telegram message containing "buy", "purchase", "kharido"

Nodes:
1. Telegram Trigger (webhook)
2. IF: message contains "buy" or "purchase"
3. Send Message: "Thank you! Payment ke liye UPI ID: [your UPI]\n\nPayment ke baad screenshot bhejo!"
4. Wait for next message (30 min timeout)
5. IF: message contains photo (screenshot)
6. Send Document: PDF file
7. Send Message: "PDF mili? Best of luck for exam! 🍀"
8. Else (timeout): Send Message: "Payment nahi aaya? Dobara try karo!"

## Workflow 2: Email Order Notification

Trigger: New row in CSV/Google Sheets

Nodes:
1. Google Sheets Trigger (new row)
2. Extract Data: email, name, amount, product
3. Send Email (via n8n Email node):
   - Subject: "Order Confirmed: [Product Name]"
   - Body: "Hi [Name], your order for [Product] (₹[Amount]) is confirmed!"
4. Send Telegram notification to admin

## Workflow 3: Daily Sales Summary

Schedule: Every day at 9 PM

Nodes:
1. Cron Trigger (daily 21:00)
2. Read CSV: today's orders
3. Calculate: total orders, total revenue
4. Send Telegram message:
   "📊 Today's Summary
   Orders: [count]
   Revenue: ₹[amount]
   Top product: [name]"

## Workflow 4: Social Media Auto-Poster

Trigger: Manual or scheduled

Nodes:
1. Cron Trigger (every 3 hours)
2. Read content queue (Google Sheets)
3. Select next post
4. IF: Instagram → Instagram node
5. IF: Twitter → Twitter node
6. IF: Facebook → Facebook node
7. Mark as posted in queue

## Workflow 5: Lead Scraper + Notifier

Trigger: Schedule (weekly)

Nodes:
1. Cron Trigger (weekly Monday 8 AM)
2. HTTP Request: scrape target website
3. Parse HTML: extract business names, emails, phones
4. Store in Google Sheets
5. Send Telegram notification: "X new leads scraped!"

## Important n8n Windows Configuration

### Docker Setup
```bash
docker run -d --name n8n -p 5678:5678 n8nio/n8n
```

### Environment Variables
```
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=yourpassword
N8N_HOST=localhost
N8N_PORT=5678
```

### API Key Generation
1. Open http://localhost:5678
2. Create owner account
3. Settings → API → Create API Key
4. Copy key to .env file

## CSV Format for Order Tracking

```csv
timestamp,name,phone,email,product,amount,payment_status,delivered
2026-08-16 10:00,Rahul,9876543210,r@gmail.com,IBPS_PDF,50,paid,yes
```
