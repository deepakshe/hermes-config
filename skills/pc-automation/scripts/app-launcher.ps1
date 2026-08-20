param (
    [Parameter(Mandatory=$true)]
    [string]$Target,

    [Parameter(Mandatory=$false)]
    [string]$Arguments = ""
)

Write-Host "Launching Target: $Target..." -ForegroundColor Cyan

try {
    if ($Arguments -ne "") {
        Start-Process $Target -ArgumentList $Arguments -ErrorAction Stop
    } else {
        Start-Process $Target -ErrorAction Stop
    }
    Write-Host "Launch successful!" -ForegroundColor Green
}
catch {
    Write-Warning "Failed to launch target. Error: $_"
}
