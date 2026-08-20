# Class-level skill: agent-project-diagnostic

Diagnose import failures, routing mismatches, and runtime breakage in local autonomous agent projects (Python, SQLite, Telegram, Playwright).

---

## When to use

- A local agent project (bot.py + agent/ + agents/ + tools/ + storage/) behaves unexpectedly: commands fail, agents don't respond, files aren't created, Telegram sends errors.
- After a code change, the bot stops responding or specific request types return generic failures.
- An agent that should handle a request is not being invoked.
- The model router (Hermes/Gemini) is unreachable or returning None.
- Files are created but not delivered to Telegram.
- Tasks are created but status is wrong (QUEUED forever, FAILED with no clear reason).

---

## Diagnose workflow

### Step 1: Isolate import errors (most common root cause)

The single most common cause of "everything is broken" in these projects is a missing or misconfigured dependency that breaks the import chain at module load time.

**The cascade pattern:**
```
tools/web_scraper.py imports trafilatura  →  ImportError
  → agent/agent_core.py imports tools.web_scraper  →  fails
    → EVERY agent inheriting AgentCore fails to import
      → registry.classify() fails (needs search_web → needs web_scraper)
      → orchestrator.py imports tools.web_scraper  →  fails
```

**Diagnostic command:**
```bash
cd /path/to/project
.venv/bin/python -c "import trafilatura; print('trafilatura OK')"  # or python.exe on Windows
.venv/bin/python -c "from agents.content import ContentAgent; print('ContentAgent OK')"
.venv/bin/python -c "from agent.orchestrator import Orchestrator; print('Orchestrator OK')"
```

If any of these fails, the error message tells you exactly which import chain is broken. Fix the missing package first.

**Check all required packages:**
```bash
cd /path/to/project
cat requirements.txt
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m pip check
```

### Step 2: Check model router status

The model router is the brain. If it's unreachable, content/research/analysis agents fail.

```bash
cd /path/to/project
.venv/bin/python -c "
from agent.model_router import ModelRouter
mr = ModelRouter()
print('hermes_available:', mr.hermes_available)
print('gemini_available:', mr.gemini_available)
print('active_provider:', mr.get_status()['active_provider'])
print('hermes_model:', mr.hermes_model)

# Test actual generation
result = mr.generate_text('Write 3 short posts about AI.')
print('generate_text result:', result[:100] if result else 'NONE')
"
```

**Common model router failures:**
- `hermes_available: False` → Ollama not running, wrong URL, or model not pulled
- `gemini_available: False` → GEMINI_API_KEY missing or invalid, or google-genai not installed
- `generate_text returns None` → both providers unreachable

**Hermes local setup (Ollama):**
- Default URL: `http://localhost:11434`
- Check: `ollama list` to see installed models
- Pull: `ollama pull hermes3:3b` (or the configured model)
- Env var: `HERMES_LOCAL_URL` (optional, default `http://localhost:11434`)
- Env var: `HERMES_LOCAL_MODEL` (optional, default `hermes3:3b`)

### Step 3: Check request routing

Verify that a request reaches the intended agent.

```bash
cd /path/to/project
.venv/bin/python -c "
from agent.registry import classify
result = classify('Create 3 AI posts for today')
print('classify result:', result)

from agent.planner import Planner
p = Planner()
plan = p.plan('Create 3 AI posts for today')
print('planner steps:', [s['tool'] for s in plan])
"
```

**Routing mismatch symptoms:**
- `classify()` returns empty list or wrong agent → check registry.py keyword matching
- Planner returns `CLARIFY` step → planner didn't match any intent keyword
- Request goes to wrong agent → check keyword priority in registry.py and planner.py

### Step 4: Check task engine state

```bash
cd /path/to/project
.venv/bin/python -c "
from agent.task_engine import TaskEngine
te = TaskEngine()
print('Tables:', [r[0] for r in te.db.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()])
tasks = te.list_all()
for t in tasks:
    print(f\"  {t['task_id'][:6]} [{t['status']}] {t['request'][:50]}\")
"
```

**Task state problems:**
- Tasks stuck in `QUEUED`/`RUNNING`/`RETRYING` → orchestrator isn't picking them up
- Task created but no result → orchestrator crashed mid-execution
- Duplicate tasks → something is creating tasks in multiple places

### Step 5: Check output file delivery

Files are created but not sent to Telegram. This is a common disconnect between the orchestrator (which records files) and the bot (which reads them).

```bash
cd /path/to/project
.venv/bin/python -c "
from agent.orchestrator import Orchestrator
o = Orchestrator()
tasks = o.list_tasks(10)
for t in tasks:
    print(f\"Task {t['task_id'][:6]}: status={t['status']}, files={t.get('output_files', '')}\")
    if t['status'] == 'COMPLETED':
        import json
        files = json.loads(t.get('output_files') or '[]')
        for f in files:
            import os
            print(f\"  File: {f}, exists={os.path.exists(f)}, size={os.path.getsize(f) if os.path.exists(f) else 'N/A'}\")
"
```

### Step 6: Check for circular imports

```bash
cd /path/to/project
.venv/bin/python -c "
# Try importing each module independently
import sys
sys.path.insert(0, '.')
for mod in ['agent.agent_core', 'agent.orchestrator', 'agent.registry',
            'agent.planner', 'agent.task_engine', 'agent.memory',
            'agent.verifier', 'agent.model_router', 'agent.master_agent',
            'agents.content', 'agents.hospital', 'agents.research',
            'agents.sales', 'agents.monitoring', 'agents.problem_solver',
            'tools.browser', 'tools.web_search', 'tools.web_scraper',
            'tools.pdf', 'tools.docx', 'tools.excel', 'tools.files',
            'tools.scheduler', 'tools.system', 'tools.research',
            'storage.database', 'storage.schemas', 'hospital']:
    try:
        __import__(mod)
        print(f'  OK {mod}')
    except Exception as e:
        print(f'  FAIL {mod}: {e}')
"
```

### Step 7: Check the specific agent for the failing request type

If content requests fail, check ContentAgent specifically:

```bash
cd /path/to/project
.venv/bin/python -c "
from agents.content import ContentAgent
c = ContentAgent()
result = c.handle_request('Create 3 AI posts for today')
print('Status:', result.status)
print('Summary:', result.summary)
print('Files:', result.files)
print('Errors:', result.errors)
"
```

---

## Common failures and fixes

### Import cascade failure

**Symptom:** Every agent fails to import, bot can't start, all requests return generic errors.

**Root cause:** A dependency listed in `requirements.txt` is not installed in the project venv. The most common culprits: `trafilatura`, `crawl4ai`, `playwright`, `google-genai`, `ddgs`.

**Fix:**
```bash
cd /path/to/project
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m pip check
```

**Windows note:** Use `.venv\\Scripts\\pip.exe` and `.venv\\Scripts\\python.exe`.

### Package missing __init__.py

**Symptom:** `ModuleNotFoundError: No module named 'earning'` when importing `earning.engine` or `agents.earning`.

**Root cause:** The `earning/` directory has Python modules but no `__init__.py` file. Python doesn't recognize it as a package.

**Fix:**
```bash
touch /path/to/project/earning/__init__.py
# Windows: type nul > C:\path\to\project\earning\__init__.py
```

### Model router unreachable

**Symptom:** ContentAgent returns FAILED with "Content generation unavailable", ResearchAgent returns empty reports.

**Root cause:** Hermes local (Ollama) not running or model not pulled.

**Fix:**
```bash
# Check Ollama is running
ollama list
# If no models, pull one
ollama pull hermes3:3b
# Check it's responding
curl http://localhost:11434/api/tags
```

### Registry routing to wrong agent

**Symptom:** "Create 3 AI posts" goes to ResearchAgent instead of ContentAgent.

**Root cause:** Keyword priority in `registry.py` or `planner.py` is wrong. Hospital keywords might match before content keywords.

**Fix:** Check the order of keyword checks in `registry.py` classify() function. Content keywords should be checked before generic research keywords.

### Task stuck in QUEUED/RUNNING

**Symptom:** Task created but never completes, status stays QUEUED or RUNNING forever.

**Root cause:** Orchestrator crashed during execution, or background thread died.

**Fix:**
```bash
# Check recoverable tasks
.venv/bin/python -c "
from agent.task_engine import TaskEngine
te = TaskEngine()
recovered = te.recover()
print(f'Recovered {recovered} tasks')
"
# Then retry
.venv/bin/python -c "
from agent.orchestrator import Orchestrator
o = Orchestrator()
# List tasks and retry the stuck one
for t in o.list_tasks():
    if t['status'] in ('QUEUED', 'RETRYING', 'RUNNING'):
        print(f'Retrying {t[\"task_id\"][:6]}...')
        o.retry_task(t['task_id'])
"
```

### File created but not delivered

**Symptom:** Orchestrator completes with files, but Telegram user receives no document.

**Root cause:** Bot reads files from wrong task ID, or file path in task record is wrong.

**Fix:** Verify the task record has correct output_files, and the bot reads from the same task_id that the orchestrator wrote to.

---

## Quick health check script

Run this after any code change to verify the system is functional:

```bash
cd /path/to/project
.venv/bin/python -m agent.self_test
```

Expected: all tests pass.

---

## References

- `references/import_cascade_failure.md` — Detailed breakdown of the trafilatura cascade pattern, how to diagnose it, and how to prevent it.
