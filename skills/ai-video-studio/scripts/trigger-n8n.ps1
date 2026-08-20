param (
    [string]$Topic = "ollama",
    [string]$WebhookUrl = "http://localhost:5678/webhook-test/generate-video"
)

Write-Host "Triggering n8n Video Pipeline for topic: '$Topic'..." -ForegroundColor Cyan
try {
    $fullUrl = "$WebhookUrl`?topic=$([System.Uri]::EscapeDataString($Topic))"
    $response = Invoke-RestMethod -Uri $fullUrl -Method GET
    Write-Host "✅ Pipeline Triggered Successfully!" -ForegroundColor Green
    $response | Format-List
} catch {
    Write-Host "❌ Failed to trigger n8n: $($_.Exception.Message)" -ForegroundColor Red
}
