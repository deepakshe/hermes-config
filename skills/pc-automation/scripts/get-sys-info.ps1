# get-sys-info.ps1 - Gathers system resource information and prints a clean report

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "         WINDOWS SYSTEM REPORT           " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# 1. OS & Machine Info
$os = Get-CimInstance Win32_OperatingSystem
$computerName = $env:COMPUTERNAME
Write-Host "Computer Name: $computerName"
Write-Host "Operating System: $($os.Caption) (Version $($os.Version))"
Write-Host "System Uptime: $((Get-Date) - $os.LastBootUpTime)"
Write-Host ""

# 2. CPU Usage
Write-Host "--- CPU Status ---" -ForegroundColor Yellow
$cpu = Get-CimInstance Win32_Processor
Write-Host "CPU Model: $($cpu.Name)"
Write-Host "Cores / Logical Processors: $($cpu.NumberOfCores) / $($cpu.NumberOfLogicalProcessors)"
$cpuLoad = (Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples.CookedValue
Write-Host "Current CPU Load: $([Math]::Round($cpuLoad, 2))%"
Write-Host ""

# 3. Memory Usage
Write-Host "--- Memory Status ---" -ForegroundColor Yellow
$totalRam = [Math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
$freeRam = [Math]::Round($os.FreePhysicalMemory / 1MB, 2)
$usedRam = $totalRam - $freeRam
$ramPercent = [Math]::Round(($usedRam / $totalRam) * 100, 2)
Write-Host "Total Memory: $totalRam GB"
Write-Host "Used Memory : $usedRam GB ($ramPercent%)"
Write-Host "Free Memory : $freeRam GB"
Write-Host ""

# 4. Disk Usage
Write-Host "--- Disk Space ---" -ForegroundColor Yellow
Get-Volume | Where-Object { $_.DriveLetter -ne $null } | ForEach-Object {
    $sizeGB = [Math]::Round($_.Size / 1GB, 2)
    $freeGB = [Math]::Round($_.SizeRemaining / 1GB, 2)
    $usedGB = $sizeGB - $freeGB
    $percent = [Math]::Round(($usedGB / $sizeGB) * 100, 2)
    Write-Host "Drive $($_.DriveLetter): [$($_.FileSystemLabel)] | Size: $sizeGB GB | Used: $usedGB GB ($percent%) | Free: $freeGB GB"
}
Write-Host ""

# 5. Network Adapters
Write-Host "--- Active IP Addresses ---" -ForegroundColor Yellow
Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notmatch "Loopback" } | ForEach-Object {
    Write-Host "Interface: $($_.InterfaceAlias) | IP Address: $($_.IPAddress)"
}
Write-Host "=========================================" -ForegroundColor Cyan
