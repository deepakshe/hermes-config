# Multi-Agent Architecture for Local Projects

## Overview
Turn a single-agent project into a multi-agent operating system by creating:
- A **shared Agent Core** (TaskEngine, Memory, Verifier, tools, browser, etc.)
- Specialized **agent classes** with role-specific capabilities
- A **Master Agent** that routes tasks to specialists
- **Hinglish NL parsing** for natural user queries

## Architecture

```
                    MASTER AGENT
                          |
        +-----------------+-------------------+
        |         |       |       |           |
    HOSPITAL  RESEARCH  CONTENT  SALES    MONITORING
        |         |       |       |        PROBLEM
        |         |       |       |          SOLVER
        +---------+-------+-------+-----------+
                          |
                    SHARED CORE
                    - task_engine.py
                    - orchestrator.py
                    - memory.py
                    - verifier.py
                    - tools/* (browser, web_search, scraper, files, pdf, docx, excel, scheduler)
                          |
                     SQLITE + APScheduler
```

## Agent Roles & Permissions

| Agent | Allowed Tools | Forbidden Tools | Memory Namespace |
|-------|---------------|-----------------|------------------|
| Hospital | hospital_db, excel, pdf, scheduler | shell, browser, search, scrape, publishing | hospital/ |
| Research | search, scraper, browser, excel, pdf | shell, payments, publishing, system_info | research/ |
| Content | research, browser, files, pdf, scheduler | shell, payments, scraping, publishing (unless auth) | content/ |
| Sales | research, files, pdf, excel | shell, browser, payments (no auto-claim), publishing | sales/ |
| Monitoring | browser, scraper, scheduler | shell, payments, publishing | monitoring/ |
| Problem Solver | all safe tools + delegation | shell, payments, system_info | problem_solver/ |
| Master | delegate, basic tools | shell (restricted), payments | master/ |

## Multi-Language (Hinglish) Intent Detection

Pattern match both English and Hindi keywords:

```python
HOSPITAL_KEYWORDS = [
    # Hindi
    "salary", "vyakti", "wage", "payslip", "payroll",
    "attendance", "leave", "overtime", "roster", "contract", "deadline",
    "bill", "vendor", "due", "payment", "inventory", "reorder",
    # English
    "salary", "staff", "employee", "payslip"
]
```

## Telegram Command Routing

Bot.py routes to Master Agent which classifies and delegates:

```
User: "Hospital ka August salary calculate karo"
    ↓
Master Agent
    ↓
classify() → ["hospital"]
    ↓
HospitalAgent.handle_request()
    ↓
Result: AgentResult(status="COMPLETED", summary="...", data=..., files=[...])
```

## File Structure

```
agent/
  agent_core.py       # Shared core class
  task_engine.py      # Persistent task queue
  orchestrator.py     # Task executor + recovery
  memory.py           # Persistent memory
  verifier.py         # Result verification
  model_router.py     # Local/gemini routing
  planner.py          # Request decomposition
  registry.py         # Agent definitions
  master_agent.py     # Central router

agents/
  __init__.py
  master.py           # Master Agent (can also be in agent/)
  hospital.py         # Hospital admin
  research.py         # Deep research
  content.py          # Content production
  sales.py            # Digital products
  monitoring.py       # Persistent alerts
  problem_solver.py   # General problem solving

tools/
  browser.py          # Playwright wrapper
  web_search.py       # ddgs search
  web_scraper.py      # Crawl4AI/trafilatura
  pdf.py, docx.py, excel.py
  scheduler.py        # APScheduler wrapper
  files.py            # File validation

hospital/              # Hospital domain module
  staff.py, salary.py, billing.py, attendance.py, reports.py, db.py

storage/               # SQLite stores
  database.py, schemas.py
```

## Task Persistence

Tasks survive process restarts. Each agent logs its work:

```python
from storage.database import get_db
from storage import schemas

# Task creation
task_id = TaskEngine.create("Calculate August salary", user_id="123")
# Status transitions: QUEUED → RUNNING → COMPLETED/FAILED
# Each subtask stores: parent_task_id, assigned_agent, result
```

## Background Worker Pattern

Long tasks run without blocking Telegram:

```python
def handle_request(self, request, progress_callback=None):
    if progress_callback:
        progress_callback("agent-name", "🔍 Step 1: researching...")
    # ... work ...
    if progress_callback:
        progress_callback("agent-name", "✅ Completed")
```

## Running the Multi-Agent System

```powershell
# PowerShell (clears PYTHONPATH)
powershell -ExecutionPolicy Bypass -File "run_project.ps1"

# Or bash with isolation
PYTHONPATH= .venv/Scripts/python.exe bot.py
```

## Verification Checklist

Before saying complete:
- [ ] `python -m pip check` → "No broken requirements found"
- [ ] All agent imports work
- [ ] Master classifier correctly routes test queries
- [ ] Task persistence works (restart + recover)
- [ ] Background tasks report via callback
- [ ] Hospital queries hit real SQLite
- [ ] File outputs (PDF/XLSX) validate
- [ ] Scheduler jobs persist