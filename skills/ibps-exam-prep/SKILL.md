---
name: ibps-exam-prep
description: "Generate IBPS PO/Clerk practice questions using local Ollama models. Zero-cost unlimited question bank with topic prioritization."
version: 1.0.0
author: Hermes Agent Session
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ibps, po, clerk, banking, exam, ollama, practice-questions, local-models]
    homepage: https://hermes-agent.nousresearch.com/docs/
-->

# IBPS PO/CLERK Exam Preparation Skill

Generate practice questions for IBPS PO and Clerk examinations using local Ollama models.
Runs entirely on CPU with no API keys, no rate limits, no subscriptions.

## Quick Start

```bash
ollama serve
ollama pull hermes3:3b
python3 generate-ibps-questions.py
# Output: "Generated 300 questions for 2026-08-16"
```

## Exam Pattern Analysis (2016-2025)

### IBPS PO EXAM

**Quantitative Aptitude (35 questions = 35 marks)**
- 60-70% marks target: 21-25 marks from 35 questions
- **Priority topics:** speed_distance (20) + profit_loss (14) = 34 questions = 63% marks ✓
- Alternative: speed_distance (20) + number_series (9) = 29 questions = 54%

**Reasoning Ability (35 questions = 35 marks)**
- 60-70% marks target: 21-24 marks from 35 questions
- **Core combination:** seating_arrangement (20) + puzzles (20) = 40 questions
- Analysis: seating (20) = 57%, add puzzles (20) = 71% = 60-70% range ✓
- Strategy: Pick 21-24 best questions from these 40 for 60-70% marks

**English Language (30 questions)**
- 100% marks from Error Detection
- Focus: Grammar rules, subject-verb agreement, preposition usage, article errors

### CLERK EXAM

**Quantitative Aptitude (40 questions = 40 marks)**
- 80% marks target: 32 marks from 40 questions
- **Priority topics:** profit_loss (14) + work_time (11) + number_series (9) = 34 questions = 85%
- Strategy: Pick top 32 questions from these 34 for exactly 80% marks

**Reasoning Ability (40 questions = 40 marks)**
- 80% marks target: 32 marks from 40 questions
- **Core combination:** seating_arrangement (20) + puzzles (20) = 40 questions = 100%
- Strategy: Pick exactly 32 questions from these 40 for 80% marks

**English Language (40 questions)**
- 100% marks from Error Detection

## Generated Question Files

### CSV Files (created in Downloads folder)

- `ibps_po_english.csv` - 40 Error Detection questions
- `ibps_po_quant.csv` - 54 Quantitative questions
- `ibps_po_reasoning.csv` - 56 Reasoning questions

### PDF Output

- `IBPS_PO_Clerk_Practice_Questions.pdf` - 11-page practice set with all 150 questions

## Topic Priority Recommendations

### IBPS PO - Quantitative (60-70% marks)
- speed_distance (20) + profit_loss (14) = 63% marks ✓ BEST combo
- Recommended selection: Top 31 from these 43

### IBPS PO - Reasoning (60-70% marks)
- seating_arrangement (20) + puzzles (20) = 71% coverage
- Recommended selection: 21-24 best from these 40

### IBPS Clerk - Quantitative (80% marks)
- profit_loss (14) + work_time (11) + number_series (9) = 85% → pick 32 for 80%

### IBPS Clerk - Reasoning (80% marks)
- seating_arrangement (20) + puzzles (20) = 40 questions = 100% → pick 32 for 80%

## Usage Examples

### Generate 150 Questions
```bash
python3 generate-ibps-questions.py
```

### Generate Subject-Specific CSV
```bash
# English only (40 questions)
python3 - << 'PYEOF'
import csv
with open('ibps_po_daily_questions.csv', 'r') as f:
    reader = csv.DictReader(f)
    english = [r for r in reader if r['subject'] == 'English']
with open('ibps_po_english.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['id','subject','topic','questionText','options','correctAnswer'])
    writer.writeheader()
    for row in english:
        writer.writerow(row)
print(f"Wrote {len(english)} English questions")
PYEOF
```

### Generate Practice PDF
```bash
python3 - << 'PYEOF'
from fpdf import FPDF
import csv
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
base = "C:/Users/admin/Downloads/"
# ... generates IBPS_PO_Clerk_Practice_Questions.pdf
PYEOF
```

## Cost & Performance

| Metric | Value |
|--------|-------|
| **API cost** | $0.00 (free, unlimited) |
| **Rate limits** | None (local execution) |
| **API keys needed** | None |
| **Hardware requirement** | 4GB+ RAM for Q4_K_M, 8GB+ for Q5_K_M |
| **Max context length** | 128K (hermes3:3b) |
| **Concurrent queries** | Unlimited (single-process) |

## Support Files (Created in Skill Directory)

- `scripts/generate-ibps-questions.py` - Main generator script (300 questions)
- `references/exam-topic-analysis.md` - Topic breakdown & priority recommendations
- `references/quant-priority.md` - Quantitative priority topics by exam type
- `references/reasoning-priority.md` - Reasoning priority topics by exam type
- `templates/generate-ibps-csv.py` - CSV generation template
- `templates/generate-ibps-pdf.py` - PDF generation template

## Troubleshooting

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Model not found | Ollama not running or model not pulled | Run `ollama serve` then `ollama pull hermes3:3b` |
| Connection refused | Hermes using wrong base_url | Verify `model.base_url: http://localhost:11434/v1` |
| Slow response | Low RAM / high quant level | Lower quant (Q3_K_M) or increase n_threads |

## User Preference: Direct & Concise for Exam Prep

**When user wants exam preparation results directly:**
- Skip lengthy theoretical discussions
- Provide working files (CSV/PDF) over step-by-step guidance
- Focus on practical solutions and high-yield topic analysis
- Technical tools (Python, CLI) over GUI methods
- Local Ollama models over API-dependent solutions
- Hinglish (Hindi+English mix) acceptable
- Direct, practical help preferred over verbose explanations

**User communication style:** Hinglish is acceptable (Hindi+English mix). Direct, practical help is preferred over verbose explanations.