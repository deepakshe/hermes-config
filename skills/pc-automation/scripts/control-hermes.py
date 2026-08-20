import os
import sys
import json
import subprocess
import argparse

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def get_hermes_status():
    print("========================================")
    print(" 🚀 HERMES AGENT RUNTIME STATUS ")
    print("========================================")
    
    # Check processes via PowerShell
    cmd = "Get-Process *hermes* -ErrorAction SilentlyContinue | Select-Object Id, ProcessName, CPU, WorkingSet64"
    res = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
    if res.stdout.strip():
        print("\n[ACTIVE PROCESSES]")
        print(res.stdout.strip())
    else:
        print("\n[INFO] No active Hermes process found.")
        
    # Check Workspaces & Skills
    workspaces = [
        r"C:\Users\admin\Desktop\autopioletbot\hermes",
        r"C:\Users\admin\Desktop\auto web console\hermes"
    ]
    
    print("\n[INSTALLED HERMES SKILLS]")
    for ws in workspaces:
        skills_dir = os.path.join(ws, "skills")
        if os.path.exists(skills_dir):
            print(f"\n📂 Workspace: {ws}")
            for sk in os.listdir(skills_dir):
                print(f"  • ⚡ {sk}")
        else:
            print(f"\n📂 Workspace: {ws} (No skills directory)")

def restart_hermes():
    print("Stopping running Hermes processes...")
    subprocess.run(["powershell", "-Command", "Stop-Process -Name *hermes* -Force -ErrorAction SilentlyContinue"])
    print("Hermes stopped. Starting primary Hermes instance...")
    lnk_path = r"C:\Users\admin\Desktop\Hermes.lnk"
    if os.path.exists(lnk_path):
        subprocess.Popen(["powershell", "-Command", f"Start-Process '{lnk_path}'"])
        print("✅ Hermes Agent restarted successfully!")
    else:
        print("Desktop shortcut not found.")

def main():
    parser = argparse.ArgumentParser(description="Antigravity Hermes Controller Bridge")
    parser.add_argument("action", choices=["status", "restart", "skills"], default="status", nargs="?", help="Action to perform")
    args = parser.parse_args()
    
    if args.action in ["status", "skills"]:
        get_hermes_status()
    elif args.action == "restart":
        restart_hermes()

if __name__ == "__main__":
    main()
