---
name: hermes-local-free-web-scraping
description: "Set up Hermes Agent with local Ollama models for zero-cost, unlimited web scraping. Runs entirely on your CPU with no API keys, no rate limits, no subscriptions. Covers model setup, Hermes configuration, working around model limitations, and web scraping workflows."
version: 1.1.0
author: Hermes Agent Session
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, local, ollama, free, unlimited, web-scraping, local-models]
    homepage: https://hermes-agent.nousresearch.com/docs/
---

# Hermes Local Free Web Scraping

Run Hermes Agent completely free using local Ollama models. No API keys, no subscription costs, no rate limits — unlimited queries on your own hardware.

## Quick Start

```bash
# 1. Install Ollama (if not already installed)
# macOS / Linux:
brew install ollama
# Windows: Download from https://ollama.com/download

# 2. Start Ollama server
ollama serve

# 3. Pull a local model (hermes3:3b included, or choose others)
ollama pull hermes3:3b
# Or: ollama pull llama3

# 4. Configure Hermes to use local models
hermes config set model.provider ollama
hermes config set model.base_url http://localhost:11434/v1
hermes config set model.default hermes3:3b

# 5. Start chatting
hermes chat -q "Your web scraping task here"
```

## 🎯 User Preference: Direct & Concise Responses

**When user wants results directly:** Skip lengthy explanations, provide actionable files and direct answers. Focus on:
- Working files over theoretical discussions
- Practical solutions over step-by-step guidance
- Technical tools (Python, CLI) over GUI methods
- Local Ollama models over API-dependent solutions

**User communication style:** Hinglish is acceptable (Hindi+English mix). Direct, practical help is preferred over verbose explanations.

## Model Selection

| Model | Size | Quant | Context | Best For |
|-------|------|-------|---------|----------|
| `hermes3:3b` | 2GB | Q4_K_M | 128K | General chat, code, web scraping |
| `llama3` | 4-8GB | Q4_K_M | 8K-100K | Code, technical tasks |
| `phi3` | 2-3GB | Q4_K_M | 4K-8K | Lightweight tasks |

### Choosing a quant:
- **Q4_K_M** (default for hermes3:3b): Good balance of speed/quality, works on 4GB+ RAM
- **Q5_K_M**: Better quality, needs 8GB+ RAM
- **Q3_K_M**: Tighter budgets, slightly less quality

## Web Scraping Workflows

### BeautifulSoup-based scraper generation

```bash
hermes chat -q "Write Python code to scrape article titles from example.com using BeautifulSoup"
```

**Output:** Complete Python script with `requests` + `beautifulsoup4`, responsible scraping guidance, and ToS compliance notes.

### Selenium for dynamic sites

```bash
hermes chat -q "Generate a Selenium script to scroll and extract product prices from an e-commerce site"
```

**Output:** Selenium script with explicit waits, scroll handling, and error recovery.

### Structured JSON output

```bash
hermes chat -q "Scrape all product names from category page and output as JSON array"
```

**Output:** Strictly formatted JSON array ready for piping to CSV/database.

### Shell-based scraping (when browser tools fail)

```bash
# Direct curl with specific headers
curl -sL -H "User-Agent: IBPS-PO-Scanner/1.0" "https://site.com/questions" | \
  grep -iE "question|topic|expected" > results.txt

# Check multiple pages efficiently
for i in {1..50}; do
  curl -sL "https://site.com/page/$i" >> combined.html
done
```

## Troubleshooting

### Common issues and fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| `HTTP 400: does not support thinking` | Using `hermes3:3b` with thinking enabled | Set `agent.reasoning_effort: none` or use a different model |
| Model not found | Ollama not running or model not pulled | Run `ollama serve` then `ollama pull <model>` |
| Connection refused | Hermes using wrong base_url | Verify `model.base_url: http://localhost:11434/v1` |
| Slow response | Low RAM / high quant level | Lower quant (Q3_K_M) or increase n_threads |


### When Browser Tools Fail
1. **Check Chrome permissions** - Allow remote debugging if prompted
2. **Use terminal curl** - Fallback for JavaScript-heavy sites
3. **Check robots.txt** - Respect site policies
4. **Use Wayback Machine** - `archive.org/web/*` for archived content
5. **Generate procedurally** - When sites unavailable, create from templates

## Technical Integration Patterns

### Daily Question Batch Generator
See: `scripts/daily-question-batch-generator.py`

Generates 300 questions daily (100 each: English, Quant, Reasoning).
Procedural generation using date-based seeding for variety.

### Weakness Analysis Engine
Integrated with AppContext state management:
- Reads from Error Notebook (wrong answers)
- Analyzes mock test sections
- Generates personalized improvement plans
- Suggests YouTube video recommendations

### Content Extraction Regex Patterns
```python
patterns = [
    r'70\s*(?:marks?|score)',        # Target score
    r'expected\s*questions?',          # Important keyword
    r'important\s*topics?',            # Priority areas
    r'(?:arithmetic|quantitative)',    # Subject categories
    r'(?:seating|puzzle|arrangement)', # Reasoning topics
]
```

## References

- **Ollama docs**: https://ollama.com/docs
- **Hermes Agent docs**: https://hermes-agent.nousresearch.com/docs/
- **Hermes3 GGUF repo**: https://huggingface.co/bartowski/hermes3-3b-gguf
- **Model quant guide**: https://huggingface.co/docs/hub/gguf-llamacpp

## Support Files

- `scripts/daily-question-batch-generator.py` - Generates 300 daily questions
- `scripts/verify-ollama-setup.py` - Verification script for checking Ollama+Hermes connectivity
- `references/model-quantization.md` - Detailed quant selection guidance
- `references/ibps-po-scraping-reference.md` - Session techniques for competitive exam prep
- `templates/hermes-config.yaml` - Starter config template

## Cost & Performance

| Metric | Value |
|--------|-------|
| **API cost** | $0.00 (free, unlimited) |
| **Rate limits** | None (local execution) |
| **API keys needed** | None |
| **Hardware requirement** | 4GB+ RAM for Q4_K_M, 8GB+ for Q5_K_M |
| **Max context length** | 128K (hermes3:3b) |
| **Concurrent queries** | Unlimited (single-process) |

## Integration with IBPS PO Command Center

### Files Created:
- `src/services/dailyQuestionBatch.ts` - Generates 300 daily questions
- `src/services/dailyQuestionGenerator.ts` - Weakness analysis engine
- `src/components/questions/DailyPracticeDashboard.tsx` - UI component
- `INTEGRATION_SUMMARY.md` - Complete documentation

### Usage:
```typescript
import { generateDailyQuestionBatch } from './services/dailyQuestionBatch';

// Generate 300 questions for today
const dailyBatch = generateDailyQuestionBatch();

// Get improvement recommendations
import { generateImprovementPlan } from './services/dailyQuestionGenerator';
const plan = generateImprovementPlan();
```