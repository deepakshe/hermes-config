# Import Cascade Failure Pattern

## The pattern

In local autonomous agent projects with a shared `AgentCore` base class, a single missing or broken dependency can cascade into a total system failure. This happens because:

1. `tools/web_scraper.py` (or similar) imports a package at module level
2. `agent/agent_core.py` imports `tools.web_scraper` (to expose `scrape` as a tool)
3. Every agent (`agents/content.py`, `agents/research.py`, etc.) inherits `AgentCore`
4. When any agent module is imported, Python loads `AgentCore`, which loads `tools.web_scraper`, which fails on the missing package

The result: **the entire agent system becomes unimportable**, even though the missing package is only used by one tool.

## Why the try/except fallback often doesn't help

`agent/agent_core.py` typically has a pattern like:

```python
try:
    from tools.web_scraper import scrape
except Exception:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from tools.web_scraper import scrape  # ← same import, same failure
```

The fallback path repeats the same import. If the package is genuinely missing, both paths fail identically. The fallback only helps when the failure is a `sys.path` issue (wrong Python environment), not a missing package.

## How to diagnose

### Quick check

```bash
cd /path/to/project
.venv/bin/python -c "import trafilatura; print('OK')"  # Windows: .venv\Scripts\python.exe
.venv/bin/python -c "from agents.content import ContentAgent; print('OK')"
.venv/bin/python -c "from agent.orchestrator import Orchestrator; print('OK')"
```

If the first command fails, you've found the root cause. If the second or third fails, it's a cascade from the first.

### Full import audit

```bash
cd /path/to/project
.venv/bin/python -c "
import sys
sys.path.insert(0, '.')
for mod in ['tools.web_scraper', 'tools.browser', 'agent.agent_core',
            'agent.orchestrator', 'agent.registry',
            'agents.content', 'agents.research', 'agents.sales',
            'agents.hospital', 'agents.monitoring', 'agents.problem_solver']:
    try:
        __import__(mod)
        print(f'  OK: {mod}')
    except Exception as e:
        print(f'  FAIL: {mod} → {type(e).__name__}: {e}')
"
```

### Reading the traceback

When an agent import fails, the traceback shows the chain:

```
ImportError: No module named 'trafilatura'
  → tools/web_scraper.py line 1: import trafilatura
  → agent/agent_core.py line 47: from tools.web_scraper import scrape
  → agents/content.py line 18: from agent.agent_core import AgentCore
  → (any code that imports ContentAgent)
```

The fix is always at the TOP of the chain: install the missing package.

## Common packages that trigger this

| Package | Used by | Symptom if missing |
|---------|---------|-------------------|
| `trafilatura` | `tools/web_scraper.py` | ImportError on any agent import |
| `crawl4ai` | `tools/web_scraper.py` | ImportError on any agent import |
| `playwright` | `tools/browser.py` | Browser tool unavailable (but doesn't cascade if browser import is lazy) |
| `google-genai` | `agent/model_router.py` | Gemini fallback unavailable (but doesn't cascade — router handles gracefully) |
| `ddgs` | `tools/web_search.py` | Search tool unavailable (may cascade if web_search is imported by core) |
| `reportlab` | `tools/pdf.py` | PDF generation fails, but doesn't cascade |
| `openpyxl` | `tools/excel.py` | Excel generation fails, but doesn't cascade |
| `python-docx` | `tools/docx.py` | DOCX generation fails, but doesn't cascade |

**Packages that DO NOT cascade** (because they're imported lazily or only in specific tools):
- `reportlab`, `openpyxl`, `python-docx` — these are imported in their respective tool modules, not in the shared core. Missing them breaks file generation but NOT agent imports.

**Packages that DO cascade** (because they're imported at the core level or in a module that the core imports):
- `trafilatura`, `crawl4ai` — imported in `tools/web_scraper.py`, which is imported by `agent_core.py`
- `ddgs` — imported in `tools/web_search.py`, which may be imported by `agent_core.py` or `research.py`

## Prevention

### 1. Install all requirements at project setup

```bash
cd /path/to/project
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m pip check
```

### 2. Verify critical imports after install

```bash
.venv/bin/python -c "
import trafilatura
import crawl4ai
import playwright
import ddgs
print('All critical imports OK')
"
```

### 3. Use lazy imports for non-critical tools

If a tool is not needed for the agent to start (e.g., browser automation), import it lazily inside the function that uses it, not at module level:

```python
# GOOD: lazy import
def browser_task(instructions):
    from playwright.sync_api import sync_playwright
    ...

# BAD: eager import at module level (breaks everything if missing)
from playwright.sync_api import sync_playwright
```

### 4. Check the runtime environment matches

On Windows with Hermes, the global `PYTHONPATH` may leak Hermes venv paths into the project venv. Clear it before running:

```powershell
# PowerShell
$env:PYTHONPATH = ""
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

```bash
# Bash
export PYTHONPATH=""
.venv/bin/pip install -r requirements.txt
```

### 5. Use the project's run script

If the project has a `run_project.ps1` or similar launcher, use it. It should handle PYTHONPATH clearing and venv activation correctly.

## One diagnostic command

After any code change or environment change, run:

```bash
cd /path/to/project
.venv/bin/python -m agent.self_test
```

If this passes, the import chain is intact and all tools are available.

## When this pattern is NOT the issue

If `agent.self_test` passes (all 13 tests) but a specific request still fails:
- The import chain is fine
- The issue is in the agent's logic, routing, or the specific tool it's trying to use
- Check the agent's `handle_request` method, the planner/registry classification, and the model router status

If `agent.self_test` fails on specific tests:
- `test_web_search` fails → `ddgs` issue or network problem
- `test_scraper` fails → `trafilatura` or `crawl4ai` issue (the cascade culprit)
- `test_browser` fails → Playwright not installed or Chromium not found
- `test_pdf`/`test_docx`/`test_excel` fails → respective package missing (non-cascading)
- `test_telegram` fails → token invalid or network issue
- `test_gemini` fails → GEMINI_API_KEY missing or google-genai not installed
