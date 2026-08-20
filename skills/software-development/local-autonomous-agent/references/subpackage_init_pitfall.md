# Subpackage Missing __init__.py

## The pattern

In Python projects with nested packages, a directory containing Python modules but no `__init__.py` file is not recognized as a package. This causes `ModuleNotFoundError` when code tries to import from that directory as if it were a package.

## Example from this session

**Project**: `autopioletbot/`  
**Directory**: `earning/` contained `engine.py`, `database.py`, `discovery.py`, `workflows/`, etc.  
**Missing**: `earning/__init__.py`  
**Failure**: `agents/earning.py` line 14: `from earning.engine import EarningEngine` → `ModuleNotFoundError: No module named 'earning'`

The `earning/` directory had all the code but Python couldn't import it as a package because `__init__.py` was absent.

## How to diagnose

```bash
cd /path/to/project
.venv/bin/python -c "from earning.engine import EarningEngine; print('OK')"
```

If this fails with `ModuleNotFoundError: No module named 'earning'`, check whether `earning/__init__.py` exists:

```bash
ls earning/__init__.py  # Linux/Mac
dir earning\__init__.py  # Windows
```

If the file doesn't exist, that's the problem.

## Fix

```bash
# Linux/Mac
touch earning/__init__.py

# Windows
type nul > earning\__init__.py
```

The `__init__.py` file can be empty. Its presence tells Python to treat the directory as a package.

## When this is NOT the issue

If `earning/__init__.py` exists but the import still fails, the problem may be:

1. **sys.path doesn't include the project root** — Python can't find the `earning` package because the project root isn't on the path. Fix: add `sys.path.insert(0, str(PROJECT_ROOT))` before the import, or run from the project root.

2. **Circular import** — `earning.engine` imports something that imports `earning` again. Check the import chain.

3. **Wrong Python environment** — The code is being run with a Python that doesn't have access to the project files. Verify you're using the project's venv Python.

## Prevention

### 1. Always include __init__.py for packages

Every directory that should be importable as a package needs `__init__.py`. This includes:
- Top-level packages (`agent/`, `agents/`, `tools/`, `hospital/`, `storage/`, `earning/`)
- Nested subpackages (`agents/`, `earning/workflows/`)

### 2. Verify package imports at setup

```bash
cd /path/to/project
.venv/bin/python -c "
import agent
import agents
import tools
import hospital
import storage
import earning  # This will fail if earning/__init__.py is missing
print('All packages importable')
"
```

### 3. Check the project layout

Before adding code to a new directory, verify it has `__init__.py`:

```
project/
├── agent/
│   ├── __init__.py    ← MUST exist
│   └── agent_core.py
├── agents/
│   ├── __init__.py    ← MUST exist
│   ├── content.py
│   └── earning.py
├── earning/            ← NEW package
│   ├── __init__.py    ← MUST ADD (was missing)
│   ├── engine.py
│   └── workflows/
│       ├── __init__.py ← ALSO NEEDED if importing from workflows
│       └── b2b_leads.py
```

### 4. Use namespace packages carefully

Python 3.3+ supports implicit namespace packages (directories without `__init__.py` that can still be imported under certain conditions). However, this only works when:
- There's no `__init__.py` in ANY directory in the chain
- The package is installed in a specific way (pip install -e, etc.)

For a typical local project run from the project root, explicit `__init__.py` files are more reliable.

## Related

- `references/import_cascade_failure.md` — When a missing dependency breaks the entire import chain
- `references/venv_isolation_windows.md` — Windows PYTHONPATH leak issues
