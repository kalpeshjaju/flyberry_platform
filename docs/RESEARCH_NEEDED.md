# 📋 Research Tasks Required

**Generated**: 2025-10-26 08:03
**Missing Files**: 6

---

## Quick Summary

- [ ] customer-testimonials-reference.json (ACT3)
- [ ] market-trends-reference.json (ACT3)
- [ ] market-size-reference.json (ACT4)
- [ ] market-validation-reference.json (ACT4)
- [ ] trend-analysis-reference.json (ACT5)
- [ ] expansion-opportunities-reference.json (ACT5)

---

## ACT3 Requirements

### 📁 customer-testimonials-reference.json

**Purpose**: Real customer testimonials and reviews

**Impact**: Incomplete ACT3 - missing Real customer testimonials and reviews


**Suggested Data Sources**:
- Google Reviews
- Social Media
- Customer Surveys

**Data Structure Template**:
```json
{
  "metadata": {
    "source": "[Source name/URL]",
    "date": "2025-10-26",
    "extractedBy": "[Your name/Claude/ChatGPT]",
    "confidence": "[high/medium/low]",
    "needsVerification": true/false
  },
  "data": {
    // Add structured data here
  }
}
```

**Collection Steps**:
1. Research from suggested sources
2. Save raw data to: `raw_data/references/`
3. Create markdown version: `llm_readable/*-reference.md`
4. Extract to JSON: `extracted_data/customer-testimonials-reference.json`
5. Update `data-lineage.json` with source tracking

---

### 📁 market-trends-reference.json

**Purpose**: Current market trends in premium snacking

**Impact**: Incomplete ACT3 - missing Current market trends in premium snacking


**Suggested Data Sources**:
- Industry Reports
- Market Research

**Data Structure Template**:
```json
{
  "metadata": {
    "source": "[Source name/URL]",
    "date": "2025-10-26",
    "extractedBy": "[Your name/Claude/ChatGPT]",
    "confidence": "[high/medium/low]",
    "needsVerification": true/false
  },
  "data": {
    // Add structured data here
  }
}
```

**Collection Steps**:
1. Research from suggested sources
2. Save raw data to: `raw_data/references/`
3. Create markdown version: `llm_readable/*-reference.md`
4. Extract to JSON: `extracted_data/market-trends-reference.json`
5. Update `data-lineage.json` with source tracking

---

## ACT4 Requirements

### 📁 market-size-reference.json

**Purpose**: Market size and growth data for premium dates/nuts

**Impact**: Incomplete ACT4 - missing Market size and growth data for premium dates/nuts


**Suggested Data Sources**:
- Industry Reports
- Government Data
- Trade Associations

**Data Structure Template**:
```json
{
  "metadata": {
    "source": "[Source name/URL]",
    "date": "2025-10-26",
    "extractedBy": "[Your name/Claude/ChatGPT]",
    "confidence": "[high/medium/low]",
    "needsVerification": true/false
  },
  "data": {
    // Add structured data here
  }
}
```

**Collection Steps**:
1. Research from suggested sources
2. Save raw data to: `raw_data/references/`
3. Create markdown version: `llm_readable/*-reference.md`
4. Extract to JSON: `extracted_data/market-size-reference.json`
5. Update `data-lineage.json` with source tracking

---

### 📁 market-validation-reference.json

**Purpose**: Third-party validation and certifications

**Impact**: Incomplete ACT4 - missing Third-party validation and certifications


**Suggested Data Sources**:
- Industry Awards
- Media Coverage
- Certifications

**Data Structure Template**:
```json
{
  "metadata": {
    "source": "[Source name/URL]",
    "date": "2025-10-26",
    "extractedBy": "[Your name/Claude/ChatGPT]",
    "confidence": "[high/medium/low]",
    "needsVerification": true/false
  },
  "data": {
    // Add structured data here
  }
}
```

**Collection Steps**:
1. Research from suggested sources
2. Save raw data to: `raw_data/references/`
3. Create markdown version: `llm_readable/*-reference.md`
4. Extract to JSON: `extracted_data/market-validation-reference.json`
5. Update `data-lineage.json` with source tracking

---

## ACT5 Requirements

### 📁 trend-analysis-reference.json

**Purpose**: Future trends and opportunities

**Impact**: Incomplete ACT5 - missing Future trends and opportunities


**Suggested Data Sources**:
- Trend Reports
- Consumer Research
- Industry Forecasts

**Data Structure Template**:
```json
{
  "metadata": {
    "source": "[Source name/URL]",
    "date": "2025-10-26",
    "extractedBy": "[Your name/Claude/ChatGPT]",
    "confidence": "[high/medium/low]",
    "needsVerification": true/false
  },
  "data": {
    // Add structured data here
  }
}
```

**Collection Steps**:
1. Research from suggested sources
2. Save raw data to: `raw_data/references/`
3. Create markdown version: `llm_readable/*-reference.md`
4. Extract to JSON: `extracted_data/trend-analysis-reference.json`
5. Update `data-lineage.json` with source tracking

---

### 📁 expansion-opportunities-reference.json

**Purpose**: Geographic and product expansion opportunities

**Impact**: Incomplete ACT5 - missing Geographic and product expansion opportunities


**Suggested Data Sources**:
- Market Analysis
- Distribution Opportunities

**Data Structure Template**:
```json
{
  "metadata": {
    "source": "[Source name/URL]",
    "date": "2025-10-26",
    "extractedBy": "[Your name/Claude/ChatGPT]",
    "confidence": "[high/medium/low]",
    "needsVerification": true/false
  },
  "data": {
    // Add structured data here
  }
}
```

**Collection Steps**:
1. Research from suggested sources
2. Save raw data to: `raw_data/references/`
3. Create markdown version: `llm_readable/*-reference.md`
4. Extract to JSON: `extracted_data/expansion-opportunities-reference.json`
5. Update `data-lineage.json` with source tracking

---

## 📝 How to Complete These Tasks

### Step 1: Gather Data
- Use web search, official sources, or LLM assistance
- Save screenshots/PDFs as proof in `raw_data/references/`

### Step 2: Process Data
```bash
# Example for competitor data
cd flyberry_oct_restart

# 1. Save raw source
echo 'Source data...' > raw_data/references/competitors-web-2025-10.md

# 2. Create readable version
cp raw_data/references/competitors-web-2025-10.md \
   llm_readable/competitors-reference.md

# 3. Extract to JSON
# Create extracted_data/competitors-reference.json with structure above
```

### Step 3: Update Tracking
Add to `data-lineage.json`:
```json
"competitors-reference.json": {
  "sourceMarkdown": "llm_readable/competitors-reference.md",
  "sourceRaw": "raw_data/references/competitors-web-2025-10.md",
  "extractionMethod": "manual/llm-assisted",
  "confidence": "medium",
  "isReference": true
}
```

### Step 4: Test
```bash
cd ../flyberry_brand_package
python3 build.py
# Should no longer show missing data warnings
```

---

*Generated by Flyberry Brand Package Builder*