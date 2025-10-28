# Reference Data Sources

**Purpose**: Store external/additional data sources that enhance core product data

## Folder Structure

```
references/
├── llm-outputs/        # Claude/ChatGPT research outputs
├── web-sources/        # Saved web pages, competitor data
├── screenshots/        # Visual proof of data sources
└── documents/          # Reports, PDFs, external docs
```

## Naming Convention

All reference files should use this pattern:
`[source]-[topic]-[date].ext`

Examples:
- `claude-competitor-analysis-2025-10-24.md`
- `webresearch-market-size-2025-10.pdf`
- `screenshot-bateel-pricing-2025-10-24.png`

## Data Flow

```
1. Reference saved here (raw_data/references/)
    ↓
2. Processed to markdown (llm_readable/*-reference.md)
    ↓
3. Extracted to JSON (extracted_data/*-reference.json)
    ↓
4. Tracked in data-lineage.json
```

## Important Rules

1. **Always include source metadata** (URL, date, method)
2. **Use "-reference" suffix** for processed files
3. **Update data-lineage.json** after adding
4. **Include confidence level** (high/medium/low)
5. **Flag if verification needed**

---

Last Updated: 2025-10-24