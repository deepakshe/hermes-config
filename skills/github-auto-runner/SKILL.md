---
name: github-auto-runner
description: Autonomous GitHub Trending Scout & Runner. Discovers #1 trending repositories of the day/hour, verifies open-source licenses, autoruns web demos in Chrome, and generates live integration wrappers for Antigravity and Hermes.
---

# GitHub Auto Runner Skill

This skill allows Antigravity and Hermes to autonomously discover, inspect, verify, and autorun trending GitHub repositories in real-time.

## Capabilities

1. **Scout #1 Trending Repositories**:
   Scans GitHub for top trending AI, developer, and video tools, checks their open-source license, stars, and release health.
   ```bash
   python "C:/Users/admin/.gemini/config/skills/github-auto-runner/scripts/fetch-trending.py" --topic "ai" --limit 5
   ```

2. **Auto-Run & Launch in Chrome**:
   Inspects any repository, verifies it is 100% free, and automatically launches Chrome to the repository / live web console demo.
   ```bash
   python "C:/Users/admin/.gemini/config/skills/github-auto-runner/scripts/autorun-repo.py" --repo "NousResearch/hermes-agent" --open-browser
   ```

3. **Auto-Integrate as Skill**:
   Clones the repository, inspects its entry point CLI/scripts, and registers an automated wrapper skill for Antigravity and Hermes.
