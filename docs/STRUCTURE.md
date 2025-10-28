# Quick Reference - Folder Structure

**One-page visual guide to project organization**

---

## 📂 The 3-Layer Data System

```
DATA PIPELINE:
raw_data/ (PDFs) → llm_readable/ (MD) → extracted_data/ (JSON)
```

---

## 🗂️ Complete Structure (Simplified)

```
flyberry_oct_restart/
│
├── 📦 DATA (Where data lives)
│   ├── raw_data/              → 13 source PDFs/MD (DON'T MODIFY)
│   ├── llm_readable/          → 15 markdown files (for context)
│   └── extracted_data/        → 31 JSON files (for facts)
│       ├── products/          → 13 products
│       ├── recipes/           → 11 recipes
│       ├── design/            → 1 design system
│       └── schemas/           → 7 validation schemas
│
├── 🧠 INTELLIGENCE (Strategy & prompts)
│   └── brand_intel/           → 5 strategy documents
│
├── 🔧 CODE (Main tools)
│   ├── flyberry_data_loader.py     ⭐ Main loader
│   ├── data-lineage.json           ⭐ Source tracking
│   ├── build.py                    → HTML generator
│   ├── example_usage.py            → 13 examples
│   └── validate-data.js            → JSON validator
│
├── 🧪 TESTING (Quality checks)
│   ├── test_two_source_prompting.py
│   ├── test_with_claude_api.py
│   └── TEST_GUIDE.md
│
├── 📖 DOCS (Knowledge base)
│   ├── README.md                   → Main docs
│   ├── USAGE_TWO_SOURCE_PROMPTING.md
│   ├── INDEX.md                    → Detailed structure
│   └── STRUCTURE.md                → This file
│
└── 🎨 TEMPLATES (Output)
    └── templates/act-template.html
```

---

## 🎯 Common Tasks

| Task | File to Use |
|------|-------------|
| Load product data | `flyberry_data_loader.py` |
| Create Claude prompts | `data.to_two_source_prompt()` |
| Verify data sources | `data.verify_product()` |
| See examples | `example_usage.py` |
| Check structure | `INDEX.md` (detailed) |
| Run tests | `test_two_source_prompting.py` |

---

## 📊 Quick Stats

- **31** JSON data files (products + recipes + catalogs)
- **13** source PDFs
- **15** markdown files
- **100%** data lineage coverage
- **2/2** tests passing ✅

---

## 🚀 Quick Start

```bash
# Load data
from flyberry_data_loader import FlyberryData
data = FlyberryData()

# Get product
product = data.get_product("medjoul-dates")

# Create Claude prompt
prompt = data.to_two_source_prompt(
    product_id="medjoul-dates",
    question="What are the health benefits?"
)
```

---

For detailed documentation, see **INDEX.md**
