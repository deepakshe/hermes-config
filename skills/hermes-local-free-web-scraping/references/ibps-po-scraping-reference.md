# IBPS PO Web Scraping Techniques
Session Reference: August 15, 2026

## Sites Successfully Scraped

### High-Yield Sources (Best Content Quality)
1. **Adda247** (`https://www.adda247.com/ibps-po/expected-questions`)
   - Rich JSON data embedded in HTML (`<script type="application/ld+json">`)
   - Contains: course metadata, question counts, expected topics
   - Content: 500+ expected questions for Prelims
   - Extraction: `grep -oP '(?<=<script type="application/ld\\+json">).*?(?=</script>'`

2. **IndiaBIX** (`https://www.indiabix.com/ibps/po/`)
   - Well-structured navigation with clear sections
   - Topics: Arithmetic Aptitude, Reasoning, English, GK
   - Good for practice question categorization
   - Extraction: Focus on `div.nav-item` patterns

3. **YouTube Channels**
   - `@adda247` - Official IBPS PO content
   - `Study IQ` - Reasoning puzzles
   - `Byju's Exam Prep` - Mock tests
   - Video analysis: Parse channel descriptions for topic keywords

### Fallback Sources
- **BankingFaculty.com** - Returns 404 (site down)
- **CareerPower.in** - Login required
- **Testbook** - Requires subscription
- **Oliveboard** - Free content available

## Content Extraction Patterns

### 1. Expected Questions (70 Mark Target)
Priority order from examiner mindset analysis:

**HIGH (Must Master):**
- Error Detection: 12-14 questions
- Speed Distance Time: 8-10 questions
- Circular Seating Arrangement: 5-6 questions
- Profit Loss Discount: 5-6 questions
- Puzzles (Appointment type): 3-4 questions

**MEDIUM (Target for 70+ marks):**
- Number Series: 10-12 questions
- Data Interpretation: 15-20 questions
- Para Jumbles: 10-12 questions
- Blood Relations: 3-4 questions
- Syllogism: 3-4 questions

**PARSING STRATEGY:**
```python
# Key patterns to search for in scraped content
patterns = [
    r'70\s*(?:marks?|score)',
    r'expected\s*questions?',
    r'topic.*important|important.*topic',
    r'(?:arithmetic|quantitative|reasoning|english)\s*section',
    r'DI\s*(?:set|questions?)',
    r'(?:seating|puzzle|arrangement)\s*\d*\s*questions?'
]
```

### 2. Video Analysis Keywords
Search YouTube descriptions for:
- "IBPS PO Prelims 2026"
- "Expected questions"
- "Important topics"
- "70 marks strategy"
- "Cut-off strategy"

## Integration Pattern: Daily Question Generation

### Architecture
```
Input: Date (YYYY-MM-DD)
Output: 300 questions (100 each subject)

Pipeline:
1. Seed random with date
2. Generate English questions (Error detection, Grammar)
3. Generate Quant questions (Arithmetic patterns)
4. Generate Reasoning questions (Puzzles, Arrangements)
5. Shuffle and output CSV/JSON
```

### Formula-Based Generation
```python
# Speed Distance Time
time = distance / speed  # seconds
# Correct for km/h: time = distance * 18 / (speed * 5)

# Profit Loss
cp = sp * 100 / (100 + profit_percent)

# Work and Time
combined_days = (a_days * b_days) / (a_days + b_days)

# Number Series (Arithmetic)
next_term = last_term + common_difference
```

## Key Technical Insights

### 1. Browser Use Errors Encountered
- Chrome asking for remote debugging (click Allow)
- Timeout issues with complex pages
- JavaScript-heavy sites need different approach

### 2. curl/telnet Workarounds
```bash
# Direct fetch with specific headers
curl -sL -H "User-Agent: IBPS-PO-Scanner/1.0" \
  "https://example.com" | grep -iE "question|topic|concepts"

# Check multiple pages
curl -sL "https://site.com/page/{1..100}" > combined.html
```

### 3. Hybrid Approach
When browser tools failed:
1. Used terminal curl for raw HTML
2. Parsed with grep/sed/awk
3. Extracted JSON-LD for structured data
4. Generated questions procedurally from templates

## User Preferences Documented

1. **Hinglish Communication**: Mix of Hindi + English acceptable
2. **Direct Answers Preferred**: Skip lengthy explanations, give actionable data
3. **Practical Help**: Provide working files, not just theory
4. **Technical Tools**: Comfortable with Python, CLI tools
5. **Local Models**: Prefers Ollama over API-based solutions

## Next Steps for Web Scraping

### TODO:
- [ ] Scrape more banking sites (SBI, RBI portals)
- [ ] Parse PDF question papers
- [ ] Extract video transcripts for content analysis
- [ ] Build API for daily question delivery

### READY FILES:
- PDFDigestQuizModule.tsx - for question analysis
- IntelligenceCore.ts - for weakness detection
- QuestionBank.ts - procedural generator (50,000+ capacity)
- DailyQuestionBatch.ts - 300/day generator

## Integration Points with Existing App

### Components to Update:
1. **ExamDrillerView.tsx** - Add daily question import
2. **QuestionBankExplorerView.tsx** - Add filter for daily batches
3. **WarRoomView.tsx** - Show daily weak topics

### Services to Extend:
1. **questionBank.ts** - Already has 50K capacity
2. **dailyQuestionBatch.ts** - NEW: 300 questions/day generator
3. **dailyQuestionGenerator.ts** - NEW: Weakness analysis engine

## Error Recovery Patterns

When site unavailable:
```python
fallback_sources = [
    'archive.org/web/*',  # Wayback Machine
    'cached:/',  # Browser cache
    'local:/',  # Local copy
    'procedural:/'  # Generate from templates
]
```

## Success Metrics
- ✅ 1500+ practice questions generated
- ✅ Daily 300-question pipeline established
- ✅ Weakness analysis integration complete
- ✅ CSV/JSON export working
- ✅ Technical documentation captured