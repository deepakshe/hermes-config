---
name: web-research-strategy
description: "Web research with fallback paths when tools fail."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Research, Web, Fallback, Strategy, Troubleshooting]
    related_skills: [grounded-citations, arxiv, systematic-debugging]
---

# Web Research Strategy

## Core Principle

**Always attempt primary research first, then have documented fallbacks when tools fail.**

Users expect research-driven answers with citations, not hallucinated content. When the primary web access method fails, gracefully degrade to alternative retrieval methods while maintaining quality standards.

## Common Web Research Failure Patterns

### 1. browser_use / browser_exec Failures

**Symptoms:**
- `ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'`
- `ImportError`, `AttributeError`, or any Python environment error
- Empty captures or missing elements
- JavaScript-rendered content not loading

**Root Causes:**
- Dependency conflicts in the virtual environment
- Security policies blocking browser automation
- Complex JavaScript sites with dynamic content
- Network issues or rate limiting

### 2. web_search / web_extract Limitations

**Symptoms:**
- Search results don't match user's specific need
- Content behind paywalls or CAPTCHAs
- Real-time information not indexed yet
- Rate limiting from search APIs

## Recovery Strategy: The 3-Tier Fallback Approach

### Tier 1: Structured Retrieval (Primary)
```
terminal > curl > grep > json_parser
```

**Action:** Use curl with appropriate headers to fetch HTML content
```bash
curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "URL"
```

**When to use:** When browser_use fails but content is mostly static HTML

### Tier 2: Direct API Access (Secondary)
```
api_endpoint > json_response > field_extraction
```

**Action:** Target the API endpoints directly, bypassing the web UI
```bash
# Example: arXiv API instead of webpage
curl -s "https://export.arxiv.org/api/query?search_query=all:topic"
```

**When to use:** When the site has a public API, or when content is consistently unavailable via browser

### Tier 3: Knowledge + Conservative Estimation (Last Resort)
```
existing_knowledge + pattern_matching + probability_assessment
```

**Action:** Use corpus knowledge with explicit uncertainty markers
- State confidence level clearly
- Avoid definitive claims without sources
- Recommend user verify critical information

## User Preference Signal: Research-First

When a user specifies:
- "Research before generating"
- "Do not hallucinate"
- "Cite sources"
- "Memory-based papers only"

**Apply:** Always fetch external sources first. For IBPS/IB content, use:
1. Official notification pages (ibps.in)
2. Verified coaching sites (adda247.com, bankersadda.com)
3. Aggregator pages with clear source attribution
4. GitHub repositories with recalled questions
5. Last resort: existing knowledge base with probability tags

## Quality Standards for Research Deliverables

### Minimum Requirements
1. **Source diversity:** At least 2 independent sources for claims
2. **Recency verification:** Prefer 2023-2025 materials for IBPS
3. **Pattern evidence:** Show repeated structures across years
4. **Probability tags:** Always label estimates (A/B/C tier)

### Documentation Format
```
[SOURCE]: Specific claim or pattern
[Pattern]: Repeated 3+ times in 2021-2024 shifts
[Evidence]: "Question X used this structure in Shift Y"
[Confidence]: Tier A/B/C with rationale
```

## Recovery Implementation Template

```bash
# Step 1: Attempt primary method
browser_exec(url="TARGET", action="extract")

# Step 2: If failure, try curl
if failed:
    terminal("curl -s 'TARGET_URL' | grep -oE 'pattern'")

# Step 3: Check for API alternative
if still_no_content:
    search_for_api_endpoint("service_name")

# Step 4: Fallback to knowledge
if all_fail:
    use_existing_knowledge(confidence_level, source_patterns)
```

## Common Research Sources by Domain

### Banking Exams (IBPS, SBI, RBI)
- **Primary:** ibps.in, sbi.co.in, rbi.org.in
- **Secondary:** adda247.com, bankersadda.com, careers360.com
- **Archive:** examrace.com, indiabix.com

### Technical Content
- **Documentation:** Official docs + GitHub
- **Research:** arXiv API, Semantic Scholar API
- **News:** Multiple tech news sources for corroboration

## Recovery Checklist

Before delivering research-heavy content:

- [ ] Attempted primary web method
- [ ] Identified specific failure mode
- [ ] Applied appropriate fallback tier
- [ ] Verified source reliability
- [ ] Documented recovery path in response
- [ ] Marked confidence levels for estimates
- [ ] Provided at least one verifiable source

## When to Escalate

Do NOT attempt browser use for:
- Content requiring complex JavaScript execution without API alternatives
- Sites known to block automation
- User explicitly stated time constraints (switch to knowledge approach)

Report recovery path to user:
> "Note: The primary browser tool had environment issues. I used curl-based retrieval and found the following sources..."