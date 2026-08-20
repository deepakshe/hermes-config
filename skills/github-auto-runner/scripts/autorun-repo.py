import os
import sys
import json
import argparse
import subprocess
import requests

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def inspect_and_run(repo_name, open_browser=True, clone_repo=False, integrate_skill=False):
    clean_name = repo_name.replace("https://github.com/", "").strip().strip("/")
    api_url = f"https://api.github.com/repos/{clean_name}"
    
    print(f"\n=======================================================")
    print(f" 🔍 INSPECTING & AUTORUNNING: {clean_name}")
    print(f"=======================================================\n")
    
    try:
        r = requests.get(api_url, headers={"User-Agent": "AntigravityAutoRunner"}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            lic = data.get("license")
            lic_name = lic.get("name") if lic else "Not specified"
            is_free = lic and any(k in lic_name.lower() for k in ["mit", "apache", "gpl", "bsd", "free"])
            
            print(f"📦 Repository: {data.get('full_name')}")
            print(f"⭐ Stars: {data.get('stargazers_count'):,}")
            print(f"📜 License: {lic_name} {'(🟢 100% Free / Open Source)' if is_free else '(🟡 Review Terms)'}")
            print(f"📖 Description: {data.get('description')}")
            print(f"🌐 Homepage / Demo: {data.get('homepage') or 'GitHub Repo'}")
            
            target_url = data.get("homepage") if (data.get("homepage") and data.get("homepage").startswith("http")) else data.get("html_url")
            
            # 1. Autorun in Chrome
            if open_browser:
                print(f"\n🚀 Launching Chrome to inspect live repository/demo...")
                subprocess.Popen(["powershell", "-Command", f"Start-Process chrome '{target_url}'"])
                print(f"✅ Chrome opened: {target_url}")
                
            # 2. Clone to D: Drive
            if clone_repo:
                target_dir = os.path.join(r"D:\antigravity\repos", clean_name.replace("/", "_"))
                os.makedirs(target_dir, exist_ok=True)
                print(f"\n📥 Cloning repository to: {target_dir}...")
                subprocess.run(["git", "clone", data.get("clone_url"), target_dir])
                print(f"✅ Repository cloned successfully!")
                
            # 3. Auto-integrate as Antigravity & Hermes Skill
            if integrate_skill:
                skill_slug = clean_name.split("/")[-1].lower()
                skill_dir = os.path.join(r"C:\Users\admin\.gemini\config\skills", skill_slug)
                os.makedirs(skill_dir, exist_ok=True)
                
                skill_md_content = f"""---
name: {skill_slug}
description: Automated wrapper for {data.get('full_name')}. {data.get('description') or 'Open-source GitHub repository.'}
---

# {data.get('full_name')} Skill

- **Stars**: {data.get('stargazers_count'):,} ⭐
- **License**: {lic_name}
- **Repository URL**: {data.get('html_url')}

## Quick Start
```bash
git clone {data.get('clone_url')}
```
"""
                with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
                    f.write(skill_md_content)
                
                # Sync to Hermes workspaces
                hermes_workspaces = [
                    r"C:\Users\admin\Desktop\autopioletbot\hermes\skills",
                    r"C:\Users\admin\Desktop\auto web console\hermes\skills"
                ]
                for hw in hermes_workspaces:
                    if os.path.exists(hw):
                        dest_hw = os.path.join(hw, skill_slug)
                        os.makedirs(dest_hw, exist_ok=True)
                        with open(os.path.join(dest_hw, "SKILL.md"), "w", encoding="utf-8") as f:
                            f.write(skill_md_content)
                            
                print(f"⚡ Skill '{skill_slug}' created and synced to Antigravity and Hermes!")
                
        else:
            print(f"❌ Error {r.status_code}: Could not fetch repository info.")
    except Exception as e:
        print(f"❌ Execution error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autorun and Inspect GitHub Repository in Chrome")
    parser.add_argument("--repo", type=str, required=True, help="GitHub repository (e.g. NousResearch/hermes-agent or full URL)")
    parser.add_argument("--open-browser", action="store_true", default=True, help="Launch repository in Chrome")
    parser.add_argument("--clone", action="store_true", help="Clone repository locally to D: drive")
    parser.add_argument("--integrate-skill", action="store_true", help="Register as an Antigravity & Hermes skill")
    args = parser.parse_args()
    
    inspect_and_run(args.repo, open_browser=args.open_browser, clone_repo=args.clone, integrate_skill=args.integrate_skill)
