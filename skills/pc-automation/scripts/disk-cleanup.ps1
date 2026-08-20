# disk-cleanup.ps1 - Scans temporary folders and recycle bin to calculate potential space savings

param (
    [Parameter(Mandatory=$false)]
    [bool]$DryRun = $true
)

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "         DISK CLEANUP UTILITY            " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

function Get-FolderSize ($path) {
    if (Test-Path $path) {
        $size = (Get-ChildItem $path -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        if ($size -eq $null) { $size = 0 }
        return $size
    }
    return 0
}

# 1. User Temp folder
$userTempPath = $env:TEMP
Write-Host "Scanning User Temp directory: $userTempPath..." -ForegroundColor DarkGray
$userTempSize = Get-FolderSize $userTempPath

# 2. System Temp folder
$sysTempPath = "C:\Windows\Temp"
Write-Host "Scanning System Temp directory: $sysTempPath..." -ForegroundColor DarkGray
$sysTempSize = Get-FolderSize $sysTempPath

# 3. Recycle Bin size
Write-Host "Scanning Recycle Bin..." -ForegroundColor DarkGray
$recycleBinSize = 0
try {
    $shell = New-Object -ComObject Shell.Application
    $bin = $shell.Namespace(0x0a) # 0x0a = Recycle Bin
    foreach ($item in $bin.Items()) {
        $recycleBinSize += $item.Size
    }
} catch {
    # Fallback if COM object fails
}

$totalBytes = $userTempSize + $sysTempSize + $recycleBinSize
$totalMB = [Math]::Round($totalBytes / 1MB, 2)
$totalGB = [Math]::Round($totalBytes / 1GB, 2)

Write-Host "`n--- Summary of Cleanable Items ---" -ForegroundColor Yellow
Write-Host "User Temp Size   : $([Math]::Round($userTempSize / 1MB, 2)) MB"
Write-Host "System Temp Size : $([Math]::Round($sysTempSize / 1MB, 2)) MB"
Write-Host "Recycle Bin Size : $([Math]::Round($recycleBinSize / 1MB, 2)) MB"
Write-Host "----------------------------------"
Write-Host "Total Cleanable  : $totalMB MB ($totalGB GB)" -ForegroundColor Green

if ($DryRun) {
    Write-Host "`n[DRY RUN] No files were deleted." -ForegroundColor Cyan
    Write-Host "To execute actual deletion, run the script with the: -DryRun:`$false parameter" -ForegroundColor Yellow
} else {
    Write-Host "`nStarting cleanup..." -ForegroundColor Red
    
    # Clean User Temp
    Get-ChildItem $userTempPath -Recurse -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    
    # Clean System Temp
    Get-ChildItem $sysTempPath -Recurse -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    
    # Clear Recycle Bin
    Clear-RecycleBin -Force -ErrorAction SilentlyContinue
    
    Write-Host "Cleanup completed successfully!" -ForegroundColor Green
}
Write-Host "=========================================" -ForegroundColor Cyan
