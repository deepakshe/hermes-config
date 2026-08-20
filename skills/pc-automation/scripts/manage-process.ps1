param (
    [Parameter(Mandatory=$false)]
    [ValidateSet("List", "Kill")]
    [string]$Action = "List",

    [Parameter(Mandatory=$false)]
    [string]$ProcessName = "",

    [Parameter(Mandatory=$false)]
    [int]$ProcessId = 0
)

if ($Action -eq "List") {
    Write-Host "--- Top 10 CPU Consuming Processes ---" -ForegroundColor Yellow
    Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 -Property Id, ProcessName, @{Name="CPU(s)";Expression={[Math]::Round($_.CPU, 2)}}, @{Name="WorkingSet(MB)";Expression={[Math]::Round($_.WorkingSet / 1MB, 2)}} | Format-Table -AutoSize

    Write-Host "`n--- Top 10 Memory Consuming Processes ---" -ForegroundColor Yellow
    Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10 -Property Id, ProcessName, @{Name="WorkingSet(MB)";Expression={[Math]::Round($_.WorkingSet / 1MB, 2)}}, CPU | Format-Table -AutoSize
}
elseif ($Action -eq "Kill") {
    if ($ProcessId -ne 0) {
        Write-Host "Attempting to terminate process with ID $ProcessId..." -ForegroundColor Cyan
        Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue
        if ($?) {
            Write-Host "Successfully terminated process ID $ProcessId." -ForegroundColor Green
        } else {
            Write-Warning "Failed to terminate process ID $ProcessId. Please run with higher permissions or check the ID."
        }
    }
    elseif ($ProcessName -ne "") {
        Write-Host "Attempting to terminate process(es) matching name '$ProcessName'..." -ForegroundColor Cyan
        Stop-Process -Name $ProcessName -Force -ErrorAction SilentlyContinue
        if ($?) {
            Write-Host "Successfully terminated process(es) named '$ProcessName'." -ForegroundColor Green
        } else {
            Write-Warning "Failed to terminate process(es) named '$ProcessName'. Check if name is correct."
        }
    }
    else {
        Write-Warning "For Action='Kill', you must specify either -ProcessName or -ProcessId."
    }
}
