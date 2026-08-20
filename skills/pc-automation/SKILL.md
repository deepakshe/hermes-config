---
name: pc-automation
description: >-
  Use this skill to automate Windows OS tasks, run system-level scripts, query system status, 
  manage processes, control window apps, and perform bulk operations on the host computer.
---

# Windows PC Automation Skill

This skill enables the agent to interact directly with the Windows host system, manage running applications, query PC resources, search files globally, and automate repetitive tasks using PowerShell.

## Available Helper Scripts

You can execute the following pre-built PowerShell scripts located in the `scripts/` directory to quickly interact with the PC:

1.  **System Information**:
    Get current CPU, Memory, Disk, and network adapter details.
    [get-sys-info.ps1](./scripts/get-sys-info.ps1)
    *Command:* `powershell -ExecutionPolicy Bypass -File C:/Users/admin/.gemini/config/skills/pc-automation/scripts/get-sys-info.ps1`

2.  **Process Manager**:
    List running processes or terminate a specific application by name or ID.
    [manage-process.ps1](./scripts/manage-process.ps1)
    *Command:* `powershell -ExecutionPolicy Bypass -File C:/Users/admin/.gemini/config/skills/pc-automation/scripts/manage-process.ps1 -Action List`

3.  **Clipboard Utility**:
    Get or set text on the Windows clipboard.
    [clipboard.ps1](./scripts/clipboard.ps1)
    *Command (Get):* `powershell -ExecutionPolicy Bypass -File C:/Users/admin/.gemini/config/skills/pc-automation/scripts/clipboard.ps1 -Action Get`

4.  **Application Launcher**:
    Launch installed applications or open URLs in the default browser.
    [app-launcher.ps1](./scripts/app-launcher.ps1)
    *Command:* `powershell -ExecutionPolicy Bypass -File C:/Users/admin/.gemini/config/skills/pc-automation/scripts/app-launcher.ps1 -Target "chrome.exe"`

5.  **Disk Cleanup Utility**:
    Scan and delete temporary files and clear the Recycle Bin.
    [disk-cleanup.ps1](./scripts/disk-cleanup.ps1)
    *Command (Scan/Dry-Run):* `powershell -ExecutionPolicy Bypass -File C:/Users/admin/.gemini/config/skills/pc-automation/scripts/disk-cleanup.ps1 -DryRun`

6.  **Interactive System Dashboard**:
    Generate a modern dark-themed HTML monitoring dashboard and launch it in your default web browser.
    [sys-dashboard.ps1](./scripts/sys-dashboard.ps1)
    *Command:* `powershell -ExecutionPolicy Bypass -File C:/Users/admin/.gemini/config/skills/pc-automation/scripts/sys-dashboard.ps1`

## Common PowerShell Snippets


If you need to perform other ad-hoc tasks, run these commands directly in PowerShell:

### File Management
*   **Search for files containing a keyword:**
    `Get-ChildItem -Path C:\ -Filter "*keyword*" -Recurse -ErrorAction SilentlyContinue`
*   **Search inside files for text (grep equivalent):**
    `Select-String -Path "C:\path\to\files\*.txt" -Pattern "SearchPattern"`

### Network Details
*   **Active TCP Connections:**
    `Get-NetTCPConnection | Where-Object {$_.State -eq "Listen"}`
*   **Test connection latency:**
    `Test-Connection -ComputerName google.com -Count 3`
