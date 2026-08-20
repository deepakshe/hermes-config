# sys-dashboard.ps1 - Generates a beautiful HTML system monitor dashboard and opens it in the browser

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "     GENERATING SYSTEM MONITOR DASHBOARD  " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Gather info
$os = Get-CimInstance Win32_OperatingSystem
$computerName = $env:COMPUTERNAME
$cpu = Get-CimInstance Win32_Processor
$cpuLoad = [Math]::Round((Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples.CookedValue, 2)
$totalRam = [Math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
$freeRam = [Math]::Round($os.FreePhysicalMemory / 1MB, 2)
$usedRam = $totalRam - $freeRam
$ramPercent = [Math]::Round(($usedRam / $totalRam) * 100, 2)

$disksHtml = ""
Get-Volume | Where-Object { $_.DriveLetter -ne $null } | ForEach-Object {
    $sizeGB = [Math]::Round($_.Size / 1GB, 2)
    $freeGB = [Math]::Round($_.SizeRemaining / 1GB, 2)
    $usedGB = $sizeGB - $freeGB
    $percent = [Math]::Round(($usedGB / $sizeGB) * 100, 2)
    $disksHtml += "
    <div class='bg-gray-800 p-4 rounded-xl border border-gray-700'>
        <div class='flex justify-between text-sm mb-1'>
            <span class='font-semibold text-gray-300'>Drive $($_.DriveLetter): [$($_.FileSystemLabel)]</span>
            <span class='text-gray-400'>$freeGB GB free / $sizeGB GB</span>
        </div>
        <div class='w-full bg-gray-700 h-2.5 rounded-full'>
            <div class='bg-cyan-500 h-2.5 rounded-full' style='width: $percent%'></div>
        </div>
        <div class='text-right text-xs text-cyan-400 mt-1'>$percent% used</div>
    </div>"
}

$processesHtml = ""
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 5 | ForEach-Object {
    $wsMB = [Math]::Round($_.WorkingSet / 1MB, 2)
    $processesHtml += "
    <tr class='border-b border-gray-700 text-sm'>
        <td class='py-2 text-cyan-400 font-mono'>$($_.Id)</td>
        <td class='py-2 text-gray-300 font-semibold'>$($_.ProcessName)</td>
        <td class='py-2 text-right text-gray-400'>$wsMB MB</td>
    </tr>"
}

$htmlContent = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Antigravity System Monitor</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #0f172a; }
    </style>
</head>
<body class="text-white min-h-screen p-8">
    <div class="max-w-4xl mx-auto space-y-6">
        <!-- Header -->
        <div class="flex items-center justify-between border-b border-gray-800 pb-4">
            <div>
                <h1 class="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-indigo-500">Antigravity System Dashboard</h1>
                <p class="text-gray-400 text-sm">Real-time status for <span class="text-gray-200 font-semibold">$computerName</span></p>
            </div>
            <div class="text-right text-xs text-gray-500">
                Generated at: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
            </div>
        </div>

        <!-- Metrics Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- CPU -->
            <div class="bg-gray-900 p-6 rounded-2xl border border-gray-800 shadow-xl flex flex-col justify-between">
                <div>
                    <h2 class="text-lg font-bold text-gray-400 mb-2">CPU Utilization</h2>
                    <p class="text-sm text-gray-500 font-semibold mb-4">$($cpu.Name)</p>
                </div>
                <div class="flex items-baseline space-x-2">
                    <span class="text-5xl font-black text-cyan-400">$cpuLoad%</span>
                    <span class="text-gray-500 text-sm">used</span>
                </div>
                <div class="w-full bg-gray-800 h-3 rounded-full mt-4">
                    <div class="bg-gradient-to-r from-cyan-400 to-cyan-500 h-3 rounded-full" style="width: $cpuLoad%"></div>
                </div>
            </div>

            <!-- RAM -->
            <div class="bg-gray-900 p-6 rounded-2xl border border-gray-800 shadow-xl flex flex-col justify-between">
                <div>
                    <h2 class="text-lg font-bold text-gray-400 mb-2">Memory Load</h2>
                    <p class="text-sm text-gray-500 font-semibold mb-4">Total Capacity: $totalRam GB</p>
                </div>
                <div class="flex items-baseline space-x-2">
                    <span class="text-5xl font-black text-indigo-400">$ramPercent%</span>
                    <span class="text-gray-500 text-sm">($usedRam GB used)</span>
                </div>
                <div class="w-full bg-gray-800 h-3 rounded-full mt-4">
                    <div class="bg-gradient-to-r from-indigo-400 to-indigo-500 h-3 rounded-full" style="width: $ramPercent%"></div>
                </div>
            </div>
        </div>

        <!-- Drives -->
        <div class="bg-gray-900 p-6 rounded-2xl border border-gray-800 shadow-xl">
            <h2 class="text-xl font-bold text-gray-200 mb-4">Storage Volumes</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                $disksHtml
            </div>
        </div>

        <!-- Top Processes -->
        <div class="bg-gray-900 p-6 rounded-2xl border border-gray-800 shadow-xl">
            <h2 class="text-xl font-bold text-gray-200 mb-4">Top 5 Memory Consuming Processes</h2>
            <table class="w-full text-left">
                <thead>
                    <tr class="border-b border-gray-800 text-gray-400 text-sm">
                        <th class="pb-2">PID</th>
                        <th class="pb-2">Process Name</th>
                        <th class="pb-2 text-right">Memory (Working Set)</th>
                    </tr>
                </thead>
                <tbody>
                    $processesHtml
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"@

# Write output file
$tempPath = [System.IO.Path]::Combine($env:TEMP, "antigravity-dashboard.html")
$htmlContent | Out-File -FilePath $tempPath -Encoding utf8

Write-Host "Opening dashboard in default browser..." -ForegroundColor Green
Start-Process $tempPath
Write-Host "Done!" -ForegroundColor Green
# =========================================
