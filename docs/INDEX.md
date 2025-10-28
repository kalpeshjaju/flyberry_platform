# Flyberry Data System - Project Index

**Purpose**: Complete navigation guide to understand the project structure
**Last Updated**: 2025-10-23
**Status**: Production Ready

---

## 📁 Project Structure Overview

```
flyberry_oct_restart/
├── 📊 DATA LAYER (3 folders)
│   ├── raw_data/          → Original source files (PDFs + MD)
│   ├── llm_readable/      → LLM-optimized markdown
│   └── extracted_data/    → Structured JSON (API-ready)
│
├── 🧠 INTELLIGENCE LAYER (1 folder)
│   └── brand_intel/       → Brand strategy & AI prompts
│
├── 🔧 CODE LAYER (5 files)
│   ├── flyberry_data_loader.py  → Main data loader
│   ├── build.py                 → HTML generator
│   ├── example_usage.py         → Usage examples
│   ├── validate-data.js         → JSON validator
│   └── data-lineage.json        → Source tracking
│
├── 🧪 TESTING LAYER (5 files)
│   ├── test_two_source_prompting.py
│   ├── test_with_claude_api.py
│   ├── test_prompt_1_missing_data.txt
│   ├── test_prompt_2_available_data.txt
│   └── TEST_GUIDE.md
│
├── 📖 DOCUMENTATION LAYER (3 files)
│   ├── README.md
│   ├── USAGE_TWO_SOURCE_PROMPTING.md
│   └── INDEX.md (this file)
│
├── 🎨 PRESENTATION LAYER (1 folder)
│   └── templates/         → HTML templates for output
│
└── ⚙️ CONFIGURATION
    └── requirements.txt   → Python dependencies
```

---

## 1️⃣ DATA LAYER - The Foundation

### 1.1 📦 `raw_data/` - Original Source Files
**Purpose**: Untouched original documents (source of truth)
**Format**: PDF files + Markdown notes
**Do NOT modify**: These are reference files only

```
raw_data/
├── Brand Guidelines (The Art of Snacking - Past Work) (1)_compressed.pdf
├── DESIGN GUIDELINES (1)_compressed.pdf
├── E-COMM PRIMARY CARDS_11zon.pdf
├── GIFTING CATALOUGE_11zon.pdf
├── HOPE GIFT BOX.pdf
├── INVESTOR UPDATE - Q4  FY25_compressed.pdf
├── INVESTOR UPDATE Q1 _ FY 26_compressed.pdf
├── RETAIL CATALOGUE_11zon.pdf
├── TRAINING CATALOUGE_11zon.pdf
└── customer_intelligence/
    ├── 09-current-customers.md
    ├── 14-what-customers-really-say.md
    ├── 18-ideal-customer-segments.md
    └── 37-customer-experience-journey.md
```

**Size**: 9 PDFs + 4 MD files = 13 source documents
**Used by**: Humans for reference, LLM extraction pipelines

---

### 1.2 📝 `llm_readable/` - LLM-Optimized Markdown
**Purpose**: Markdown versions of PDFs optimized for LLM consumption
**Format**: `.md` files with preserved structure + context
**Generation**: Converted from `raw_data/` PDFs using extraction tools

```
llm_readable/
├── Brand Guidelines (The Art of Snacking - Past Work) (1)_compressed.md
├── COMPETITIVE-LANDSCAPE-WEB-RESEARCH-2025-10.md  ← Web research
├── DESIGN GUIDELINES (1)_compressed.md
├── E-COMM PRIMARY CARDS_11zon.md
├── GIFTING CATALOUGE_11zon.md
├── HOPE GIFT BOX.md
├── INVESTOR UPDATE - Q4  FY25_compressed.md
├── INVESTOR UPDATE Q1 _ FY 26_compressed.md
├── RETAIL CATALOGUE_11zon.md
├── TRAINING CATALOUGE_11zon.md
├── claims-registry.json  ← Imported from extracted_data
└── customer_intelligence/
    ├── 09-current-customers.md
    ├── 14-what-customers-really-say.md
    ├── 18-ideal-customer-segments.md
    └── 37-customer-experience-journey.md
```

**Size**: 10 MD files + 1 JSON + 4 customer intelligence MD = 15 files
**Used by**: `to_two_source_prompt()` for context (narrative/storytelling)
**Key Feature**: Used as "Markdown Context" in two-source prompting

---

### 1.3 📊 `extracted_data/` - Structured JSON (API-Ready)
**Purpose**: Machine-readable structured data extracted from markdown
**Format**: JSON files with strict schemas
**Generation**: Extracted from `llm_readable/` using LLM pipelines

```
extracted_data/
├── claims-registry.json             → Health/nutrition claims
├── customer-insights.json           → Customer feedback analysis
├── customer-segments.json           → 5 customer personas
├── gifting-catalogue.json           → Corporate gift products
├── investor-updates.json            → Q4 FY25 + Q1 FY26 metrics
├── retail-catalogue.json            → Retail product listings
│
├── products/                        → 13 product files
│   ├── index.json                   → Product index
│   ├── medjoul-dates.json          → Full product data
│   ├── ajwa-dates.json
│   ├── ameri-dates.json
│   ├── brazil-nuts.json
│   ├── deglet-nour-dates.json
│   ├── deri-dates.json
│   ├── halawi-dates.json
│   ├── hazelnuts.json
│   ├── kalmi-dates.json
│   ├── mabroom-dates.json
│   ├── macadamia-nuts.json
│   ├── pecan-nuts.json
│   └── pine-nuts.json
│
├── recipes/                         → 11 recipe files
│   ├── index.json                   → Recipe index
│   ├── ajwa-kalakand.json
│   ├── caramely-date-sundae.json
│   ├── dark-chocolate-fondue.json
│   ├── date-bark.json
│   ├── date-bars.json
│   ├── hazelnut-katli.json
│   ├── natural-caramel.json
│   ├── nut-pulao.json
│   ├── pine-nut-candy.json
│   ├── roasted-spiced-pecan-nuts.json
│   └── vegan-parmesan.json
│
├── design/                          → Design system
│   └── brand-design-system.json    → Colors, typography, spacing
│
└── schemas/                         → JSON schemas for validation
    ├── claims-registry-schema.json
    ├── design-schema.json
    ├── gifting-catalogue-schema.json
    ├── investor-updates-schema.json
    ├── product-schema.json
    ├── recipe-schema.json
    └── retail-catalogue-schema.json
```

**Size**: 31 JSON data files + 7 schema files = 38 files
**Used by**: `flyberry_data_loader.py` (primary data source)
**Key Feature**: Used as "JSON Data" in two-source prompting (source of truth)

---

## 2️⃣ INTELLIGENCE LAYER - Brand Strategy

### 2.1 🧠 `brand_intel/` - Strategic Intelligence
**Purpose**: AI prompts, brand strategy frameworks, usage guides
**Format**: Markdown documentation + PDF references

```
brand_intel/
├── how-i-design-brand.md           → Brand design methodology
├── how-i-design-brand.pdf          → PDF version
├── LLM_SYSTEM_PROMPT.md            → System prompts for AI
├── README.md                       → Brand intel overview
└── USAGE_INSTRUCTIONS.md           → How to use brand intel
```

**Used by**: AI systems for brand-aligned content generation
**Key Feature**: Contains strategic frameworks and prompt templates

---

## 3️⃣ CODE LAYER - Data Access & Processing

### 3.1 🔧 Core Python Files

#### `flyberry_data_loader.py` ⭐ MAIN LOADER
**Purpose**: Load, verify, and query Flyberry data
**Size**: ~700 lines
**Key Features**:
- Lazy loading with caching
- Two-source prompt generation (JSON + Markdown)
- Data verification against sources
- Source lineage tracking

**Main Methods**:
```python
data = FlyberryData()
data.products                           # List all products
data.get_product("medjoul-dates")       # Get one product
data.verify_product("medjoul-dates")    # Verify against sources
data.to_two_source_prompt(              # Generate Claude prompt
    product_id="medjoul-dates",
    question="What are the benefits?"
)
```

**Dependencies**: `extracted_data/`, `llm_readable/`, `data-lineage.json`

---

#### `build.py` - HTML Generator
**Purpose**: Convert brand strategy markdown → branded HTML pages
**Size**: ~150 lines
**Usage**: `python build.py` (not currently used in main workflow)

**Dependencies**: `templates/act-template.html`

---

#### `example_usage.py` - Usage Examples
**Purpose**: 13 working examples demonstrating data loader features
**Size**: ~400 lines
**Usage**: `python example_usage.py`

**Examples included**:
1. Load all products
2. Load all recipes
3. Search products
4. Get product details
5. Get recipe details
6. Get customer segments
7. Load investor updates
8. Get design tokens
9. **Get product with sources** (NEW)
10. **Verify product data** (NEW)
11. **Load markdown context** (NEW)
12. **Check data lineage** (NEW)
13. **Two-source prompting** (NEW)

---

#### `validate-data.js` - JSON Validator
**Purpose**: Validate JSON files against schemas
**Size**: ~50 lines
**Usage**: `node validate-data.js`
**Language**: JavaScript (Node.js)

**Validates**: All JSON files in `extracted_data/` against `schemas/`

---

#### `data-lineage.json` ⭐ SOURCE TRACKING
**Purpose**: Map every JSON file back to source markdown and raw PDF
**Size**: 31 entries (100% coverage)
**Format**:
```json
{
  "products/medjoul-dates.json": {
    "sourceMarkdown": "llm_readable/GIFTING CATALOUGE_11zon.md",
    "sourceRaw": "raw_data/GIFTING CATALOUGE_11zon.pdf",
    "extractionMethod": "structured-extraction",
    "confidence": "high",
    "lastVerified": "2025-10-23"
  }
}
```

**Used by**: `flyberry_data_loader.py` for verification and source tracking

---

## 4️⃣ TESTING LAYER - Quality Assurance

### 4.1 🧪 Test Files

```
testing/
├── test_two_source_prompting.py          → Test prompt generator
├── test_with_claude_api.py               → API integration tests
├── test_prompt_1_missing_data.txt        → Test case 1 output
├── test_prompt_2_available_data.txt      → Test case 2 output
└── TEST_GUIDE.md                         → Testing instructions
```

**Test Cases**:
1. **Missing Data Test**: Ask for data that doesn't exist (sales info)
   - **Expected**: Claude says "information not available"
   - **Result**: ✅ PASSED

2. **Available Data Test**: Ask about data that exists (taste profile)
   - **Expected**: Claude cites JSON and answers accurately
   - **Result**: ✅ PASSED

**Run Tests**:
```bash
# Generate test prompts
python3 test_two_source_prompting.py

# Test with Claude API (requires ANTHROPIC_API_KEY)
python3 test_with_claude_api.py
```

---

## 5️⃣ DOCUMENTATION LAYER - Knowledge Base

### 5.1 📖 Documentation Files

```
docs/
├── README.md                              → Main project documentation
├── USAGE_TWO_SOURCE_PROMPTING.md          → Two-source tutorial
├── TEST_GUIDE.md                          → Testing instructions
└── INDEX.md                               → This file (structure guide)
```

**README.md** (11KB):
- Quick start guide
- Feature documentation
- Architecture overview
- Performance metrics
- Use cases

**USAGE_TWO_SOURCE_PROMPTING.md** (7.5KB):
- Two-source prompting tutorial
- 4 real-world examples
- Anti-hallucination rules
- Best practices

**TEST_GUIDE.md** (6.3KB):
- Test case documentation
- 3 testing methods
- Expected results
- Troubleshooting

**INDEX.md** (this file):
- Complete project navigation
- Folder structure
- File purposes
- Dependencies

---

## 6️⃣ PRESENTATION LAYER - Output Templates

### 6.1 🎨 `templates/` - HTML Templates

```
templates/
└── act-template.html    → Jinja2 template for brand strategy docs
```

**Variables**:
- `{{ act_number }}` - Act number (1-6)
- `{{ act_title }}` - Act title
- `{{ content }}` - Main content (markdown → HTML)
- `{{ generation_date }}` - Timestamp

**Used by**: `build.py` (not in main workflow currently)

---

## 7️⃣ CONFIGURATION - Dependencies

### 7.1 ⚙️ `requirements.txt`
**Purpose**: Python package dependencies
**Packages**:
- `anthropic` - Claude API integration (for testing)

**Install**: `pip3 install -r requirements.txt`

---

## 📊 Data Flow Diagram

```
┌──────────────┐
│  raw_data/   │  Original PDFs (source of truth)
│  (13 files)  │
└──────┬───────┘
       │ [PDF → Markdown Conversion]
       ↓
┌──────────────┐
│llm_readable/ │  LLM-optimized markdown (context)
│  (15 files)  │
└──────┬───────┘
       │ [LLM Extraction → JSON]
       ↓
┌──────────────┐
│extracted_data│  Structured JSON (facts)
│  (31 files)  │
└──────┬───────┘
       │
       ↓
┌─────────────────────────────────┐
│ flyberry_data_loader.py         │
│ + data-lineage.json             │
│                                 │
│ to_two_source_prompt():         │
│   JSON (facts) + MD (context)   │
│   ↓                             │
│   Claude Sonnet 4.5 Prompt      │
└─────────────────────────────────┘
```

---

## 🔍 Quick Navigation Guide

### "I want to..."

**...see raw source documents**
→ Go to `raw_data/`

**...read LLM-optimized content**
→ Go to `llm_readable/`

**...access product data**
→ Go to `extracted_data/products/`

**...access recipe data**
→ Go to `extracted_data/recipes/`

**...load data in Python**
→ Use `flyberry_data_loader.py`

**...create Claude prompts**
→ Use `data.to_two_source_prompt()`

**...verify data accuracy**
→ Use `data.verify_product()`

**...check data sources**
→ See `data-lineage.json`

**...run examples**
→ Run `python example_usage.py`

**...test the system**
→ Run `python test_two_source_prompting.py`

**...understand two-source prompting**
→ Read `USAGE_TWO_SOURCE_PROMPTING.md`

**...understand brand strategy**
→ Go to `brand_intel/`

**...validate JSON schemas**
→ Run `node validate-data.js`

---

## 🚫 DO NOT MODIFY

**These folders contain reference data only:**
- ❌ `raw_data/` - Original source files (backup/reference)
- ❌ `llm_readable/` - Generated from raw_data (regenerate if needed)

**Safe to modify:**
- ✅ `extracted_data/` - Update JSON as needed
- ✅ `brand_intel/` - Update strategies/prompts
- ✅ Python/JS files - Code improvements
- ✅ Documentation - Keep up to date

---

## 📈 Project Statistics

| Category | Count |
|----------|-------|
| **Source Documents** | 13 (9 PDFs + 4 MD) |
| **LLM Markdown** | 15 files |
| **JSON Data Files** | 31 files |
| **JSON Schemas** | 7 files |
| **Products** | 13 |
| **Recipes** | 11 |
| **Python Files** | 5 |
| **Test Files** | 5 |
| **Documentation** | 4 |
| **Templates** | 1 |
| **Total Files** | ~90 files |

---

## 🔗 Key Dependencies

```
raw_data/ → llm_readable/ → extracted_data/ → flyberry_data_loader.py
                                            ↘
                                             data-lineage.json
                                            ↗
                              llm_readable/ → to_two_source_prompt()
```

**Critical Path**:
1. `extracted_data/` provides JSON (facts)
2. `llm_readable/` provides Markdown (context)
3. `data-lineage.json` maps JSON → Markdown → PDF
4. `flyberry_data_loader.py` loads all data
5. `to_two_source_prompt()` generates Claude prompts

---

## ✅ System Status

| Component | Status | Coverage |
|-----------|--------|----------|
| Data Lineage | ✅ Complete | 100% (31/31 files) |
| JSON Schemas | ✅ Complete | 7 schemas |
| Product Data | ✅ Complete | 13 products |
| Recipe Data | ✅ Complete | 11 recipes |
| Documentation | ✅ Complete | 4 docs |
| Testing | ✅ Complete | 2 test cases passed |
| Git Status | ✅ Pushed | Commit 5c8f621 |

---

## 📝 Version History

- **v1.0** (2025-10-23): Initial index structure created
- Two-source prompting system implemented
- Data lineage tracking complete
- All documentation updated

---

**Last Updated**: 2025-10-23
**Maintained by**: Kalpesh + Claude Code
**Project**: Flyberry Data System (flyberry_oct_restart)
