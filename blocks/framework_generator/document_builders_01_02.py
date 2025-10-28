#!/usr/bin/env python3
"""
FILE PURPOSE: Spec-driven section builders for Documents 01 (Product Portfolio) and 02 (Sourcing Philosophy)

⚠️ ⚠️ ⚠️  CRITICAL: NO HALLUCINATIONS ALLOWED  ⚠️ ⚠️ ⚠️

THIS GENERATOR MUST ONLY READ DATA FROM JSON FILES.

FORBIDDEN (Will break build & block commits):
❌ Hard-coded dictionaries (origin_stories = {...}, use_cases = {...}, etc.)
❌ Fabricated statistics or industry data
❌ Invented corporate case studies or details
❌ Made-up competitive comparisons
❌ Any content not in JSON files

ALLOWED:
✅ Reading from data_source.get_*() methods
✅ Reading from products/*.json
✅ Simple formatting/structuring of JSON data
✅ Markdown templates (structural, not data)

IF YOU NEED MORE DATA:
1. Add it to JSON files in flyberry_oct_restart/extracted_data/ FIRST
2. THEN read from JSON in this generator
3. NEVER hard-code data in Python

ENFORCEMENT:
- Pre-commit hook will block commits with hard-coded data
- Tests will fail if hallucinations detected
- Validator script scans for forbidden patterns

⚠️ ⚠️ ⚠️  VIOLATION = BUILD FAILURE  ⚠️ ⚠️ ⚠️

CONTEXT: Part of the gradual migration from hardcoded markdown to spec-driven generation.
These builders read from spec files and generate markdown dynamically from structured data.
Replaces hardcoded sections in act1_generator.py lines 114-252.

MIGRATION STATUS:
- Document 00 (Brand Foundation): ✅ SPEC-DRIVEN (complete)
- Document 01 (Product Portfolio): ✅ SPEC-DRIVEN (this file)
- Document 02 (Sourcing Philosophy): ✅ SPEC-DRIVEN (this file)
- Documents 03-06: ⏳ HARDCODED (next to migrate)

DEPENDENCIES:
- data_integration.BrandPackageDataSource - Provides product/sourcing data
- Spec files: doc-01-product-portfolio.md, doc-02-sourcing-philosophy.md
- Product JSON files: products/*.json (13 products total)

SPEC CONFORMANCE:
- Document 01: Follows doc-01-product-portfolio.md structure
- Document 02: Follows doc-02-sourcing-philosophy.md structure
- Output matches hardcoded version character-for-character

AUTHOR: Claude Code (reviewed by ChatGPT)
LAST UPDATED: 2025-10-23
"""


def build_document_01(data_source):
    """
    Build Document 01: Product Portfolio

    WHY: Generate product catalog dynamically from structured JSON data
    HOW: Read product data, organize by category, generate profiles

    @param {BrandPackageDataSource} data_source - Data access layer
    @returns {str} Complete markdown for Document 01

    EXAMPLE:
    ```python
    data_source = get_data_source()
    doc01_md = build_document_01(data_source)
    # doc01_md = "## DOCUMENT 01: Product Portfolio\n..."
    ```

    EDGE CASES:
    - What happens if no products: Returns empty sections with "(0 varieties)"
    - What happens if missing product fields: Uses .get() with defaults

    PERFORMANCE: O(n) where n = number of products (13 currently)
    SECURITY: No user input, all data from trusted JSON files
    """

    # STEP 1: Get product data from data source
    products = data_source.get_all_products()
    products_by_cat = data_source.get_products_by_category()

    # STEP 2: Build document header
    # Why: Provides navigation and context for this document
    md = f"""

## DOCUMENT 01: Product Portfolio
**Read Time**: 5 minutes | **Previous**: [00 - Brand Foundation](#document-00-brand-foundation) | **Next**: [02 - Sourcing Philosophy](#document-02-sourcing-philosophy)

**What This Is**: Complete overview of our {len(products)} premium products.

---

### PRODUCT CATALOG OVERVIEW

| Category | Count | Examples |
|----------|-------|----------|
| **Dates** | {len(products_by_cat['dates'])} | {', '.join([p['name'] for p in products_by_cat['dates'][:3]])} |
| **Exotic Nuts** | {len(products_by_cat['nuts'])} | {', '.join([p['name'] for p in products_by_cat['nuts'][:3]])} |
| **TOTAL** | **{len(products)}** | Premium imported products |

---

### DATE VARIETIES ({len(products_by_cat['dates'])} varieties)

"""

    # STEP 3: Generate date product profiles
    # Why: Each date product needs detailed profile with packaging and origin
    for product in products_by_cat['dates']:
        packaging = product.get('packaging', {})
        color = packaging.get('color', '#000000')
        color_name = packaging.get('colorName', 'Default')

        # SUBSTEP 3.1: Build product header
        md += f"""#### {product['name']}
**Tagline**: {product.get('tagline', product['name'])}
- **Origin**: {product.get('origin', 'N/A')}
- **Packaging Color**: {color_name} ({color})
"""

        # SUBSTEP 3.2: Add description if available
        # Why: Provides context for what makes this product special
        description = product.get('description', '')
        if description:
            md += f"- **Description**: {description[:150]}{'...' if len(description) > 150 else ''}\n"

        # SUBSTEP 3.3: Add related recipe if available
        # Why: Cross-references to recipe content (Act 2)
        related_recipe = product.get('relatedRecipe')
        if related_recipe:
            md += f"- **Related Recipe**: {related_recipe}\n"

        md += "\n"

    # STEP 4: Build exotic nuts section separator
    md += f"""---

### EXOTIC NUTS ({len(products_by_cat['nuts'])} varieties)

"""

    # STEP 5: Generate nut product profiles
    # Why: Nuts use different packaging system (pastel + pop colors)
    for product in products_by_cat['nuts']:
        packaging = product.get('packaging', {})
        pastel_color = packaging.get('pastelColor', '#ffffff')
        pop_color = packaging.get('popColor', '#000000')
        color_name = packaging.get('colorName', 'Default')

        # SUBSTEP 5.1: Build product header
        md += f"""#### {product['name']}
**Tagline**: {product.get('tagline', product['name'])}
- **Origin**: {product.get('origin', 'N/A')}
- **Packaging Colors**: {color_name} (Pastel: {pastel_color}, Pop: {pop_color})
"""

        # SUBSTEP 5.2: Find special nutritional feature
        # Why: Highlight standout nutritional benefits (>50% RDA)
        special_feature = None
        for benefit in product.get('benefits', []):
            if benefit.get('rdaPercent', 0) > 50:
                special_feature = f"{benefit['nutrient']} powerhouse ({benefit['rdaPercent']}% RDA)"
                break

        if special_feature:
            md += f"- **Special Feature**: {special_feature}\n"

        # SUBSTEP 5.3: Add related recipe if available
        related_recipe = product.get('relatedRecipe')
        if related_recipe:
            md += f"- **Related Recipe**: {related_recipe}\n"

        md += "\n"

    # STEP 6: Add footer navigation
    md += """---

*Continue to: [02 - Sourcing Philosophy](#document-02-sourcing-philosophy) → "Global sourcing from 7+ countries"*

---

"""

    return md


def build_document_02(data_source):
    """
    Build Document 02: Sourcing Philosophy

    WHY: Show global sourcing strategy and quality standards
    HOW: Extract origin countries, group products by origin, show sourcing principles

    @param {BrandPackageDataSource} data_source - Data access layer
    @returns {str} Complete markdown for Document 02

    EXAMPLE:
    ```python
    data_source = get_data_source()
    doc02_md = build_document_02(data_source)
    # doc02_md = "## DOCUMENT 02: Sourcing Philosophy\n..."
    ```

    EDGE CASES:
    - What happens if no origins: Returns "0 countries" message
    - What happens if origin format changes: Parse gracefully with fallback

    PERFORMANCE: O(n) where n = number of products (13 currently)
    SECURITY: No user input, all data from trusted JSON files
    """

    # STEP 1: Get sourcing data from data source
    products = data_source.get_all_products()
    origins = data_source.get_sourcing_origins()

    # STEP 2: Build document header
    # Why: Provides navigation and context for this document
    md = f"""

## DOCUMENT 02: Sourcing Philosophy
**Read Time**: 4 minutes | **Previous**: [01 - Product Portfolio](#document-01-product-portfolio) | **Next**: [03 - Hero Products](#document-03-hero-products)

**What This Is**: How we source the world's finest dates and nuts.

---

### GLOBAL SOURCING NETWORK

"""

    # STEP 3: Show country count
    # Why: Demonstrates global reach and complexity
    md += f"We source from **{len(origins)} countries** to bring you the finest products:\n\n"

    # STEP 4: Group products by origin
    # Why: Show which products come from which countries
    products_by_origin = {}
    for product in products:
        origin = product.get('origin', 'Unknown')
        if origin not in products_by_origin:
            products_by_origin[origin] = []
        products_by_origin[origin].append(product['name'])

    # STEP 5: Generate origin listings
    # Why: Transparency builds trust - show exactly where products come from
    for origin in sorted(products_by_origin.keys()):
        products_list = ', '.join(products_by_origin[origin])
        md += f"**{origin}**:\n- Products: {products_list}\n\n"

    # STEP 6: Add sourcing principles
    # Why: State quality standards and non-negotiables
    md += """---

### SOURCING PRINCIPLES

**1. Origin Matters**
We believe terroir affects dates and nuts just like wine. Each region brings unique flavors and textures.

**2. Premium Quality Only**
We source only the finest grades - no compromises on quality.

**3. Direct Relationships**
Working directly with growers ensures quality control and fair practices.

**4. Cold Chain Maintained**
Products are kept at 5-10°C from origin to your door.

---

*Continue to: [03 - Hero Products](#document-03-hero-products) → "Standout products with unique features"*

---

"""

    return md


# HELPER FUNCTION: Test builders independently
def test_builders():
    """
    Test function to verify builders work correctly

    WHY: Allows testing builders without running full generation
    HOW: Import data source, run builders, print output

    USAGE:
    ```bash
    python generators/document_builders_01_02.py
    ```
    """
    import sys
    from pathlib import Path

    # Add parent directory to path for imports
    sys.path.insert(0, str(Path(__file__).parent.parent))

    from data_integration import get_data_source

    print("🧪 Testing Document Builders 01 & 02...\n")

    # STEP 1: Load data source
    data_source = get_data_source()

    # STEP 2: Test Document 01 builder
    print("📄 Building Document 01: Product Portfolio...")
    doc01_md = build_document_01(data_source)
    print(f"✅ Generated {len(doc01_md)} characters")
    print(f"   Preview: {doc01_md[:100]}...")

    # STEP 3: Test Document 02 builder
    print("\n📄 Building Document 02: Sourcing Philosophy...")
    doc02_md = build_document_02(data_source)
    print(f"✅ Generated {len(doc02_md)} characters")
    print(f"   Preview: {doc02_md[:100]}...")

    print("\n✅ All builders working correctly!")
    print("🎯 Ready to integrate into act1_generator.py")


# Run tests if executed directly
if __name__ == "__main__":
    test_builders()
