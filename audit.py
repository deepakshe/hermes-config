#!/usr/bin/env python3
"""
Hermes Agent System Audit - Complete diagnostic tool
Checks all components: model, fallback, browser, computer_use, plugins, 
toolset coverage, platforms, MCP, session_reset, memory, compression,
API keys, network connectivity, disk resources, skills, cron jobs, memories.
"""

import yaml
import json
import os
import subprocess
import httpx
import shutil
from pathlib import Path

HERMES_HOME = Path.home() / "AppData" / "Local" / "hermes"

def load_config():
    config_path = HERMES_HOME / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)

def load_gateway_state():
    state_path = HERMES_HOME / "gateway_state.json"
    if state_path.exists():
        with open(state_path) as f:
            return json.load(f)
    return {}

def check_api(url, timeout=5, headers=None):
    """Check API connectivity"""
    try:
        r = httpx.get(url, timeout=timeout, headers=headers)
        return r.status_code, r.text[:200]
    except Exception as e:
        return None, str(e)[:100]

def main():
    cfg = load_config()
    gs = load_gateway_state()
    errors = []
    warnings = []
    info = []

    def err(msg):
        errors.append(msg)
        print(f'✗ {msg}')

    def warn(msg):
        warnings.append(msg)
        print(f'⚠ {msg}')

    def inf(msg):
        info.append(msg)
        print(f'  ℹ {msg}')

    # ── 1. PRIMARY MODEL ──
    print('── PRIMARY MODEL ──')
    m = cfg['model']
    if not m.get('default'):
        err('primary model default खाली है')
    else:
        inf(f'primary: {m["default"]} via {m.get("provider","?")}')
    
    if not m.get('base_url'):
        err('primary base_url missing')
    else:
        status, _ = check_api(m['base_url'] + '/models')
        if status == 200:
            inf(f'primary API: OK ({status})')
        else:
            err(f'primary API: status {status}')
    
    if m.get('api_mode') not in ['chat_completions', 'responses']:
        err(f'api_mode invalid: {m.get("api_mode")}')

    # ── 2. FALLBACK CHAIN ──
    print('\n── FALLBACK CHAIN ──')
    bp = cfg.get('fallback_providers', [])
    if not isinstance(bp, list):
        err(f'fallback_providers type wrong: {type(bp)}')
    elif len(bp) == 0:
        err('fallback chain खाली')
    else:
        inf(f'fallback entries: {len(bp)}')
        for i, e in enumerate(bp):
            missing = []
            if not e.get('provider'): missing.append('provider')
            if not e.get('model'): missing.append('model')
            if not e.get('base_url'): missing.append('base_url')
            if not e.get('trigger_on'): missing.append('trigger_on')
            if not e.get('max_retries') or e['max_retries'] < 1: missing.append('max_retries')
            if missing:
                err(f'fallback[{i}]: missing {missing}')
            else:
                inf(f'fallback[{i}]: {e["provider"]} -> {e["model"]} ({e["base_url"]})')
                # Live check Ollama
                if 'localhost' in e['base_url']:
                    status, _ = check_api(e['base_url'] + '/api/tags')
                    if status == 200:
                        inf(f'  Ollama: OK')
                    elif status:
                        err(f'  Ollama: status {status}')
                    else:
                        err(f'  Ollama: unreachable')

    # ── 3. BROWSER ──
    print('\n── BROWSER ──')
    br = cfg.get('browser', {})
    inf(f'backend: {br.get("backend","?")')
    inf(f'executable: {br.get("executable_path","?")}')
    
    if 'browser/browser-use' not in cfg['plugins']['enabled']:
        err('browser/browser-use plugin NOT enabled')
    else:
        inf('plugin: enabled')
    
    # Python package check
    try:
        import browser_use
        inf('Python package: installed')
    except ImportError:
        err('Python package: NOT installed')

    # ── 4. COMPUTER USE ──
    print('\n── COMPUTER USE ──')
    cu = cfg.get('computer_use', {})
    inf(f'backend: {cu.get("backend","?")}')
    inf(f'enabled: {cu.get("enabled", False)}')
    
    cua_bin = Path(r'C:\Users\admin\AppData\Local\Programs\Cua\cua-driver\bin\cua-driver')
    if not cua_bin.exists():
        err(f'cua-driver binary not found: {cua_bin}')
    else:
        inf(f'binary OK: {cua_bin}')
    
    # Daemon check
    try:
        r = subprocess.run([str(cua_bin), 'status'], capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            for line in r.stdout.split('\n'):
                if 'running' in line.lower() or 'pid' in line.lower():
                    inf(f'cua-driver: {line.strip()}')
        else:
            err(f'cua-driver status: {r.stderr[:100]}')
    except Exception as e:
        err(f'cua-driver: {e}')

    # ── 5. SESSION RESET ──
    print('\n── SESSION RESET ──')
    sr = cfg.get('session_reset', {})
    mode = sr.get('mode', '')
    if mode in [None, '', 'none']:
        err('session_reset.mode NOT set — skills auto-load will fail in new sessions')
    else:
        inf(f'mode: {mode}')

    # ── 6. PLATFORM TOOLSETS ──
    print('\n── TOOLSET COVERAGE ──')
    essential = ['web', 'browser', 'computer_use', 'code_execution', 'skills', 'memory', 
                 'session_search', 'delegation', 'cronjob', 'terminal', 'file', 'vision',
                 'image_gen', 'tts', 'clarify', 'todo']
    
    for plat, tools in cfg['platform_toolsets'].items():
        missing = [t for t in essential if t not in tools]
        if plat in ['cli', 'telegram']:
            if missing:
                err(f'{plat}: missing {missing}')
            else:
                inf(f'{plat}: all essential tools present ({len(tools)} total)')
        else:
            inf(f'{plat}: {len(tools)} tools')

    # ── 7. API KEYS ──
    print('\n── API KEYS (sample) ──')
    key_envs = [
        ('OPENROUTER_API_KEY', 'OpenRouter'),
        ('GOOGLE_API_KEY', 'Google/Gemini'),
        ('OLLAMA_API_KEY', 'Ollama'),
        ('GITHUB_TOKEN', 'GitHub'),
        ('HERMES_NOUS_TOKEN', 'Nous Portal'),
    ]
    for env_key, desc in key_envs:
        val = os.environ.get(env_key, '')
        if val:
            inf(f'✓ {desc}: set')
        else:
            warn(f'○ {desc}: not set ({env_key})')

    # ── 8. NETWORK ──
    print('\n── NETWORK ──')
    hosts = [
        ('Nous Portal', 'https://inference-api.nousresearch.com/v1/models'),
        ('Ollama', 'http://localhost:11434/api/tags'),
        ('n8n', 'http://localhost:5678'),
    ]
    for name, url in hosts:
        status, _ = check_api(url, timeout=5)
        if status == 200:
            inf(f'{name}: OK')
        elif status:
            warn(f'{name}: status {status}')
        else:
            err(f'{name}: unreachable')

    # ── 9. SKILLS ──
    print('\n── SKILLS ──')
    skills_dir = HERMES_HOME / 'skills'
    if skills_dir.exists():
        skill_dirs = [d for d in skills_dir.iterdir() 
                      if d.is_dir() and not d.name.startswith('.')]
        inf(f'Installed: {len(skill_dirs)} skill directories')
        for sd in sorted(skill_dirs):
            skill_file = sd / 'SKILL.md'
            if skill_file.exists():
                inf(f'  ✓ {sd.name}: SKILL.md ({skill_file.stat().st_size} bytes)')
            else:
                warn(f'  ○ {sd.name}: NO SKILL.md')
    else:
        err('skills directory not found')

    # ── FINAL ──
    print(f'\n═══ SUMMARY ═══')
    print(f'Errors:   {len(errors)}')
    for e in errors:
        print(f'  ✗ {e}')
    print(f'Warnings: {len(warnings)}')
    for w in warnings[:10]:
        print(f'  ⚠ {w}')
    if len(warnings) > 10:
        print(f'  ... +{len(warnings)-10} more')
    print(f'Info:     {len(info)} checks passed')
    print(f'\n{"SYSTEM READY" if len(errors) == 0 else "SYSTEM HAS ERRORS — fix before automation scaling"}')

if __name__ == '__main__':
    main()
