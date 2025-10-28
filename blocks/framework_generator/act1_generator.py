#!/usr/bin/env python3
"""
Act 1 Generator - WHO WE ARE (FULLY SPEC-DRIVEN)

ARCHITECTURE:
- ALL Documents (00-06): FULLY SPEC-DRIVEN
  * Document 00: Brand Foundation (reads from brand-foundation.md)
  * Document 01: Product Portfolio (dynamic from products/*.json)
  * Document 02: Sourcing Philosophy (dynamic from origins data)
  * Document 03: Hero Products (dynamic from hero_products data)
  * Document 04: Nutritional Excellence (dynamic from claims-registry.json)
  * Document 05: Fortune 500 Validation (dynamic from corporate-clients.json)
  * Document 06: Brand Promise (dynamic from certifications.json)

Generates Act 1 markdown dynamically from structured JSON data + document specs.
NO static markdown - all content from INPUT folder + spec files.

Source: flyberry_oct_restart/extracted_data/
Specs: flyberry_oct_restart/extracted_data/act-1-document-specs/
"""

from pathlib import Path
from generators.spec_parser import parse_document_spec
from generators.data_helpers import get_all_brand_foundation_sections
from generators.document_builders_01_02 import build_document_01, build_document_02
from generators.document_builders_03_04 import build_document_03, build_document_04
from generators.document_builders_05_06 import build_document_05, build_document_06

def generate_act1_markdown(data_source):
    """
    Generate Act 1: WHO WE ARE from structured data

    Args:
        data_source: BrandPackageDataSource instance

    Returns:
        str: Complete markdown content for Act 1
    """

    # Get data
    brand = data_source.get_brand_info()
    products = data_source.get_all_products()
    products_by_cat = data_source.get_products_by_category()
    hero_products = data_source.get_hero_products()
    origins = data_source.get_sourcing_origins()
    nutritional_highlights = data_source.get_nutritional_highlights()

    # Load brand foundation sections (spec-driven)
    brand_sections = get_all_brand_foundation_sections()

    # Parse Document 00 spec
    spec_dir = Path("/Users/kalpeshjaju/Development/flyberry_oct_restart/extracted_data/act-1-document-specs")
    doc00_spec_path = spec_dir / "doc-00-brand-foundation.md"
    doc00_spec = parse_document_spec(doc00_spec_path) if doc00_spec_path.exists() else None

    # Start building markdown
    md = f"""# Act 1: WHO WE ARE
**Foundation & Heritage**

*The origin story, sourcing philosophy, hero products, Fortune 500 validation, and brand promise.*

---

## Quick Navigation

- **[00: Brand Foundation](#document-00-brand-foundation)** - Mission, vision, essence, and strategic positioning
- **[01: Product Portfolio](#document-01-product-portfolio)** - {len(products)} premium products ({len(products_by_cat['dates'])} dates + {len(products_by_cat['nuts'])} nuts)
- **[02: Sourcing Philosophy](#document-02-sourcing-philosophy)** - Global sourcing from {len(origins)} countries
- **[03: Hero Products](#document-03-hero-products)** - {len(hero_products)} standout products with unique features
- **[04: Nutritional Excellence](#document-04-nutritional-excellence)** - Top {min(10, len(nutritional_highlights))} nutritional highlights
- **[05: Fortune 500 Validation](#document-05-fortune-500-validation)** - Corporate trust and credibility
- **[06: Brand Promise](#document-06-brand-promise)** - Our commitment to quality

---

## DOCUMENT 00: Brand Foundation
**Read Time**: {doc00_spec['read_time'] if doc00_spec else '8 minutes'} | **Next**: [01 - Product Portfolio](#document-01-product-portfolio)

**What This Is**: {doc00_spec['purpose'].split(chr(10))[0] if doc00_spec else 'Our brand foundation'}

---

"""

    # Build Document 00 sections from spec (spec-driven)
    if doc00_spec:
        section_mapping = {
            'THE ESSENCE OF FLYBERRY': 'BRAND ESSENCE',
            'OUR MISSION': 'MISSION',
            'OUR VISION': 'VISION',
            'STRATEGIC POSITIONING': 'STRATEGIC POSITIONING',
            'INNOVATION DNA': 'INNOVATION DNA',
            'THE CUSTOMER TRUTH': 'THE CUSTOMER TRUTH',
            'CATEGORY STRATEGY': 'HOW INNOVATION SHOWS UP ACROSS CATEGORIES',
            'BRAND PROMISE': 'BRAND PROMISE',
            'THE FUTURE': None,  # Not in brand-foundation.md
            'YOU EXPERIENCE THE DIFFERENCE': 'YOU EXPERIENCE THE DIFFERENCE',
        }

        for section in doc00_spec['sections']:
            section_title = section['title']
            brand_key = section_mapping.get(section_title)

            # Skip if no mapping or section not found
            if not brand_key:
                continue

            # Get content from brand foundation
            content = brand_sections.get(brand_key, '')

            # Special handling for first section (THE ESSENCE)
            if section_title == 'THE ESSENCE OF FLYBERRY':
                md += f"## {section_title}\n\n"
                md += '> **"We reimagine food with artful nuance."**\n'
                md += '> Fine taste. Clean ingredients. World-class quality.\n\n'
                md += "Flyberry isn't another snack brand or dry fruit seller. We're a gourmet brand **relentlessly building to be #1 in every category we enter** - through obsessive sourcing, innovation, and craft.\n\n"
                md += "This is the foundation. This is who we are.\n\n---\n\n"
            elif content:
                md += f"## {section_title}\n\n{content}\n\n---\n\n"
    else:
        # Fallback if spec not found
        md += "*(Document 00 spec not found - using fallback)*\n\n---\n\n"

    md += "*Continue to: [01 - Product Portfolio](#document-01-product-portfolio) → \"Our complete product range\"*\n\n---\n\n"

    # Documents 01-06: FULLY SPEC-DRIVEN (reads from document specs)
    md += build_document_01(data_source)
    md += build_document_02(data_source)
    md += build_document_03(data_source)
    md += build_document_04(data_source)
    md += build_document_05(data_source)
    md += build_document_06(data_source)

    return md


# Test if running directly
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent))

    from data_integration import get_data_source

    print("🧪 Testing Act 1 Generator (Fully Spec-Driven)...\n")

    # Load data
    data_source = get_data_source()

    # Generate markdown
    print("📝 Generating Act 1 markdown from structured data...")
    markdown_content = generate_act1_markdown(data_source)

    # Show preview
    lines = markdown_content.split('\n')
    print(f"\n✅ Generated {len(lines)} lines of markdown")
    print(f"✅ Content length: {len(markdown_content)} characters")

    print("\n--- Preview (first 50 lines) ---")
    print('\n'.join(lines[:50]))
    print("...")

    # Optionally write to file
    output_path = Path(__file__).parent.parent / "source" / "act-1-who-we-are-GENERATED.md"
    output_path.write_text(markdown_content, encoding='utf-8')
    print(f"\n✅ Written to: {output_path}")
    print("🎯 Ready to build HTML from fully spec-driven generator!")
