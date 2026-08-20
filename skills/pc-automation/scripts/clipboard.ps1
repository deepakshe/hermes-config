param (
    [Parameter(Mandatory=$true)]
    [ValidateSet("Get", "Set")]
    [string]$Action,

    [Parameter(Mandatory=$false)]
    [string]$Text = ""
)

if ($Action -eq "Get") {
    $clipText = Get-Clipboard -Raw
    if ($clipText) {
        Write-Host "--- Clipboard Contents ---" -ForegroundColor Yellow
        Write-Output $clipText
    } else {
        Write-Host "Clipboard is empty or does not contain text." -ForegroundColor DarkGray
    }
}
elseif ($Action -eq "Set") {
    if ($Text -ne "") {
        Set-Clipboard -Value $Text
        Write-Host "Successfully copied text to the clipboard!" -ForegroundColor Green
    } else {
        Write-Warning "For Action='Set', you must provide a non-empty string in the -Text parameter."
    }
}
