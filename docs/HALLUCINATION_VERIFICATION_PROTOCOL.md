# Hallucination Verification Protocol

**Purpose**: Ensure Claude provides PROVABLE, VERIFIABLE answers with NO hallucinations

**Version**: 1.0.0
**Date**: 2025-10-24
**Status**: MANDATORY for all content generation

---

## Protocol Overview

For EVERY content generation request (catalogue, positioning, analysis, etc.), Claude MUST complete these 3 checkpoints:

```
CHECKPOINT 1 (BEFORE) → CHECKPOINT 2 (DURING) → CHECKPOINT 3 (AFTER)
     ↓                        ↓                         ↓
  Verify Data          Use Only Verified       Audit Output
  Show Sources         Cite Everything         Prove No Hallucination
  Get Confirmation     No Assumptions          Provide Trail
```

---

## CHECKPOINT 1: BEFORE Generation (MANDATORY)

### What Claude MUST Do:

1. **Load Data from flyberry_data_loader.py**
   ```python
   from flyberry_data_loader import FlyberryData
   data = FlyberryData()
   ```

2. **Show EXACT Sources with Proof**
   ```
   📂 DATA SOURCES FOUND:
   ✅ extracted_data/products/medjoul-dates.json
      File exists: Yes
      Size: 2,154 bytes
      Sample: Line 5 → "name": "Medjoul Dates"

   ✅ llm_readable/GIFTING CATALOUGE_11zon.md
      File exists: Yes
      Size: 20,462 chars
      Sample: Line 47 → "King of Dates from Jordan Valley"
   ```

3. **List What Data IS Available**
   ```
   📊 VERIFIED DATA AVAILABLE:
   ✅ Product names (13/13) - Source: products/*.json
   ✅ Origins (13/13) - Source: products/*.json:origin field
   ✅ Nutritional data (13/13) - Source: products/*.json:benefits
   ✅ Taste profiles (13/13) - Source: products/*.json:tasteProfile
   ✅ Customer segments (2/2) - Source: customer-segments.json
   ```

4. **List What Data is MISSING**
   ```
   ❌ DATA NOT AVAILABLE:
   ⚠️  Product pricing (not in any JSON/MD files)
   ⚠️  Sales figures (not tracked)
   ⚠️  Inventory levels (not available)
   ⚠️  Customer reviews (only testimonials available)
   ```

5. **State Confidence Score**
   ```
   🎯 CONFIDENCE SCORE: 9/10

   **Reason**: All core product data verified in JSON files
   **Source**: flyberry_data_loader.py + data-lineage.json
   **Coverage**: 13/13 products with 100% data completeness
   **Last Verified**: 2025-10-24
   **Limitation**: Cannot include pricing (data unavailable)
   ```

6. **Get User Confirmation**
   ```
   ════════════════════════════════════════════
   PROCEED WITH GENERATION? (Y/N)
   ════════════════════════════════════════════
   ```

### Template for Checkpoint 1:

```markdown
═══════════════════════════════════════════
CHECKPOINT 1: DATA VERIFICATION (BEFORE)
═══════════════════════════════════════════

📂 DATA SOURCES FOUND:
[List all files with file:line samples]

📊 DATA AVAILABLE:
[List verified data categories with counts]

❌ DATA MISSING:
[List unavailable data - prevents hallucination]

🎯 CONFIDENCE SCORE: X/10
   Reason: [Why this score]
   Source: [Where data comes from]
   Coverage: [Completeness metric]
   Last Verified: [Date]
   Limitation: [What cannot be included]

════════════════════════════════════════════
PROCEED WITH GENERATION? (Y/N)
════════════════════════════════════════════
```

---

## CHECKPOINT 2: DURING Generation (MANDATORY)

### What Claude MUST Do:

1. **Use ONLY Verified Sources**
   - Every fact must come from Checkpoint 1 verified data
   - No assumptions
   - No external knowledge
   - No "common sense" additions

2. **Cite Everything**
   ```markdown
   According to the JSON data (medjoul-dates.json:8),
   the origin is "Imported Product of Jordan / Palestine".

   From the markdown context (GIFTING CATALOUGE_11zon.md:47),
   these dates are described as "King of Dates from the Jordan Valley."
   ```

3. **Use Two-Source Prompting**
   ```python
   prompt = data.to_two_source_prompt(
       product_id="medjoul-dates",
       question="Generate catalogue entry"
   )
   # This ensures JSON (facts) + Markdown (context) approach
   ```

4. **If Data Missing → State It Explicitly**
   ```markdown
   ⚠️  Pricing information is not available in the provided data.
   ```

---

## CHECKPOINT 3: AFTER Generation (MANDATORY)

### What Claude MUST Do:

1. **Create Citation Map**
   ```
   📋 CITATION MAP (Output → Source):

   "Medjoul Dates" → medjoul-dates.json:5
   "King of Dates" → medjoul-dates.json:6
   "Jordan/Palestine" → medjoul-dates.json:8
   "13.5% RDA fiber" → medjoul-dates.json:23 (benefits[0].rdaPercent)
   "Caramel-like sweetness" → medjoul-dates.json:45 (tasteProfile.flavor)
   "Orange packaging" → medjoul-dates.json:12 (packaging.colorName)
   ```

2. **Run Hallucination Check**
   ```
   🔍 HALLUCINATION CHECK:

   ✅ Product names: All verified in JSON (13/13)
   ✅ Origins: All verified in JSON (13/13)
   ✅ Nutritional claims: All verified in JSON (42/42 claims used)
   ✅ Taste profiles: All from JSON tasteProfile fields
   ✅ Descriptions: All from markdown context

   ❌ Pricing: NOT included (unavailable in data)
   ❌ Awards/certifications: NOT included (unavailable in data)
   ❌ Customer ratings: NOT included (only testimonials available)

   📊 FABRICATION COUNT: 0
   ```

3. **Provide Verification Score**
   ```
   📊 VERIFICATION SCORE: 10/10

   - Total facts stated: 156
   - Verified facts: 156 (100%)
   - Fabricated facts: 0 (0%)
   - Unverified claims: 0 (0%)
   - Citations provided: 156 (100%)

   ✅ HALLUCINATION-FREE GUARANTEE
   ```

4. **Save Audit Trail**
   ```json
   {
     "task": "Product Catalogue Generation",
     "date": "2025-10-24",
     "sources_used": [
       "extracted_data/products/*.json (13 files)",
       "llm_readable/GIFTING CATALOUGE_11zon.md"
     ],
     "data_verified": true,
     "hallucination_check": "passed",
     "fabrication_count": 0,
     "confidence_score": 10,
     "audit_file": "catalogue_audit_2025-10-24.json"
   }
   ```

### Template for Checkpoint 3:

```markdown
═══════════════════════════════════════════
CHECKPOINT 3: OUTPUT VERIFICATION (AFTER)
═══════════════════════════════════════════

📋 CITATION MAP:
[Every fact → source file:line]

🔍 HALLUCINATION CHECK:
✅ [Category]: Verified
✅ [Category]: Verified
❌ [Category]: NOT included (reason)

📊 VERIFICATION SCORE: X/10
   - Total facts: X
   - Verified: X (100%)
   - Fabricated: 0 (0%)
   - Citations: X (100%)

✅ HALLUCINATION-FREE GUARANTEE

════════════════════════════════════════════
AUDIT TRAIL: [filename]
════════════════════════════════════════════
```

---

## Enforcement Rules

### ✅ Claude MUST:

1. Complete ALL 3 checkpoints for content generation
2. Show PROOF of data existence (file:line samples)
3. State what data is MISSING (prevents false claims)
4. Provide confidence score with REASONING
5. Get user confirmation before generating
6. Cite EVERY fact with source
7. Create citation map after generation
8. Run hallucination check (show 0 fabrications)
9. Save audit trail

### ❌ Claude MUST NOT:

1. Skip checkpoints (even for "simple" requests)
2. Say "no hallucinations" without proving it
3. Use external knowledge or assumptions
4. Fabricate data for missing fields
5. Skip citation map
6. Claim 100% confidence without evidence
7. Generate content without user confirmation

---

## Integration with Existing Systems

### Works With:

1. **flyberry_data_loader.py** - Primary data source
2. **Two-Source Prompting** - JSON + Markdown verification
3. **data-lineage.json** - Source tracking (100% coverage)
4. **3-Checkpoint System** (CLAUDE.md) - Aligns with global standards

### Adds New Layer:

```
Before: User Ask → Claude Generates → Output
Now:    User Ask → Checkpoint 1 (Verify) → User Confirms →
        Checkpoint 2 (Generate) → Checkpoint 3 (Audit) → Output
```

---

## Examples

### Example 1: Product Catalogue

**User Request:** "Generate product catalogue"

**Checkpoint 1 Output:**
```
═══════════════════════════════════════════
CHECKPOINT 1: DATA VERIFICATION
═══════════════════════════════════════════

📂 SOURCES: 13 product JSON files + 3 markdown catalogs
📊 AVAILABLE: Names, origins, nutrition, taste (100%)
❌ MISSING: Pricing, sales data
🎯 CONFIDENCE: 9/10 (all product data verified)

PROCEED? (Y/N)
```

**Checkpoint 3 Output:**
```
═══════════════════════════════════════════
CHECKPOINT 3: OUTPUT VERIFICATION
═══════════════════════════════════════════

📋 CITATIONS: 156 facts → all mapped to sources
🔍 HALLUCINATION CHECK: 0 fabrications
📊 SCORE: 10/10 (100% verified)
✅ HALLUCINATION-FREE GUARANTEE
```

---

## User Benefits

1. **Trust**: Can verify Claude's claims independently
2. **Transparency**: See exactly what data is being used
3. **No Surprises**: Know what's missing BEFORE generation
4. **Auditable**: Full trail of sources → output
5. **Quality**: Confidence scores based on evidence
6. **Safety**: No fabricated data can slip through

---

## Quick Reference Card

```
┌─────────────────────────────────────────┐
│ 3-CHECKPOINT VERIFICATION PROTOCOL      │
├─────────────────────────────────────────┤
│                                         │
│ ✅ BEFORE: Verify + Show + Confirm     │
│    → Load data                          │
│    → Show sources (file:line)           │
│    → List available/missing             │
│    → Confidence score                   │
│    → User confirms                      │
│                                         │
│ ✅ DURING: Use Only Verified + Cite    │
│    → Two-source prompting               │
│    → Every fact cited                   │
│    → No assumptions                     │
│                                         │
│ ✅ AFTER: Audit + Verify + Prove       │
│    → Citation map                       │
│    → Hallucination check                │
│    → Verification score                 │
│    → Audit trail saved                  │
│                                         │
└─────────────────────────────────────────┘
```

---

**Last Updated**: 2025-10-24
**Version**: 1.0.0
**Status**: MANDATORY
**Applies To**: All content generation tasks (catalogues, positioning, analysis, etc.)
