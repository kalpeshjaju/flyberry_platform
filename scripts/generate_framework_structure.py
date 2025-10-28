#!/usr/bin/env python3
"""
Generate a "Complete Framework Structure with Filenames" manifest and scaffold files.

Scope (Phase 1):
- Scaffold Act 1 (Discovery & Foundation) exactly as per requested format.
- Create minimal JSON/MD placeholders linking back to current HTML anchors.
- Emit FRAMEWORK_STRUCTURE_COMPLETE.md with the exact list style.

Non-destructive: writes to flyberry_brand_package/framework_export/
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = ROOT / "framework_export"
DOCS_DIR = ROOT / "docs"
MANIFEST = ROOT / "FRAMEWORK_STRUCTURE_COMPLETE.md"


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def write_json(p: Path, obj: dict):
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_md(p: Path, text: str):
    p.write_text(text.strip() + "\n", encoding="utf-8")


def scaffold_act1():
    base = EXPORT_DIR / "act-1-discovery-foundation"
    ensure_dir(base)

    sections = [
        (
            "1.1-business-foundation",
            "Business Foundation",
            [
                ("index.json", "Business Foundation Index", "docs/act-1-who-we-are.html#document-00-brand-foundation"),
                ("company-vision-mission.json", "Company Vision & Mission", "docs/act-1-who-we-are.html#document-00-brand-foundation"),
                ("business-model-analysis.json", "Business Model Analysis", "docs/act-2-where-we-are.html#document-00-current-reality"),
                ("value-proposition-architecture.json", "Value Proposition Architecture", "docs/act-1-who-we-are.html#document-01-product-portfolio"),
                ("organizational-values-culture.json", "Values & Culture", "docs/act-1-who-we-are.html#document-00-brand-foundation"),
                ("leadership-vision-stakeholder-alignment.json", "Leadership Vision & Alignment", "docs/act-1-who-we-are.html#document-00-brand-foundation"),
            ],
        ),
        (
            "1.2-market-intelligence",
            "Market Intelligence",
            [
                ("index.json", "Market Intelligence Index", "docs/act-3-discoveries.html#document-02-market-opportunities"),
                ("industry-landscape-trends.json", "Industry Landscape & Trends", "docs/act-3-discoveries.html#document-02-market-opportunities"),
                ("competitive-analysis-direct-indirect.json", "Competitive Analysis (Direct/Indirect)", "docs/act-3-discoveries.html#document-03-competitive-gaps"),
                ("market-segmentation.json", "Market Segmentation", "docs/act-3-discoveries.html#document-01-customer-deep-dive"),
                ("category-dynamics.json", "Category Dynamics", "docs/act-2-where-we-are.html#document-04-competitive-reality"),
                ("white-space-identification.json", "White Space Identification", "docs/act-3-discoveries.html#document-02-market-opportunities"),
            ],
        ),
        (
            "1.3-customer-understanding",
            "Customer Understanding",
            [
                ("index.json", "Customer Understanding Index", "docs/act-3-discoveries.html#document-01-customer-deep-dive"),
                ("target-audience-definition.json", "Target Audience Definition", "docs/act-3-discoveries.html#document-01-customer-deep-dive"),
                ("customer-personas-behavioral.json", "Customer Personas (Behavioral)", "docs/act-3-discoveries.html#document-01-customer-deep-dive"),
                ("customer-personas-psychographic.json", "Customer Personas (Psychographic)", "docs/act-3-discoveries.html#document-01-customer-deep-dive"),
                ("customer-personas-demographic.json", "Customer Personas (Demographic)", "docs/act-3-discoveries.html#document-01-customer-deep-dive"),
                ("customer-journey-mapping.json", "Customer Journey Mapping", "docs/act-3-discoveries.html#customer-journey-insights"),
                ("pain-points-jobs-to-be-done.json", "Pain Points & JTBD", "docs/act-3-discoveries.html#key-customer-quotes"),
                ("customer-sentiment-analysis.json", "Customer Sentiment Analysis", "docs/act-3-discoveries.html#key-customer-quotes"),
            ],
        ),
        (
            "1.4-brand-audit",
            "Brand Audit",
            [
                ("index.json", "Brand Audit Index", "docs/act-2-where-we-are.html#document-03-whats-broken"),
                ("current-brand-perception-internal.json", "Brand Perception (Internal)", "docs/act-2-where-we-are.html#document-01-brand-positioning-gap"),
                ("current-brand-perception-external.json", "Brand Perception (External)", "docs/act-2-where-we-are.html#document-01-brand-positioning-gap"),
                ("brand-equity-assessment.json", "Brand Equity Assessment", "docs/act-4-market-proof.html#document-01-premium-positioning-proof"),
                ("visual-identity-audit.json", "Visual Identity Audit", "docs/act-1-who-we-are.html#document-00-brand-foundation"),
                ("messaging-consistency-review.json", "Messaging Consistency Review", "docs/act-2-where-we-are.html#document-03-whats-broken"),
                ("competitive-positioning-analysis.json", "Competitive Positioning Analysis", "docs/act-3-discoveries.html#document-03-competitive-gaps"),
                ("brand-touchpoint-inventory.json", "Brand Touchpoint Inventory", "docs/index.html"),
            ],
        ),
        (
            "1.5-strategic-insights",
            "Strategic Insights",
            [
                ("index.json", "Strategic Insights Index", "docs/act-3-discoveries.html#document-05-key-insights-summary"),
                ("swot-analysis.json", "SWOT Analysis", "docs/act-3-discoveries.html#document-05-key-insights-summary"),
                ("market-opportunities-threats.json", "Market Opportunities & Threats", "docs/act-3-discoveries.html#document-02-market-opportunities"),
                ("competitive-advantages-moats.json", "Competitive Advantages & Moats", "docs/act-5-where-to-go.html#document-03-revenue-model-projections"),
                ("growth-barriers-constraints.json", "Growth Barriers & Constraints", "docs/act-2-where-we-are.html#document-05-the-100-cr-blockers"),
            ],
        ),
    ]

    created_files = []
    for folder_slug, section_title, files in sections:
        section_dir = base / folder_slug
        ensure_dir(section_dir)
        for fname, title, src_hint in files:
            p = section_dir / fname
            if fname.endswith(".json"):
                write_json(
                    p,
                    {
                        "title": title,
                        "source_hint": str(src_hint),
                        "status": "draft",
                        "notes": "Scaffolded from flyberry_brand_package; populate from referenced anchor.",
                    },
                )
            else:
                write_md(p, f"# {title}\n\nSource: {src_hint}")
            created_files.append(p)

    return created_files


def generate_manifest(created_act1_files_count: int):
    # Write only Act 1 exact format; note others pending
    content = f"""---
  Complete Framework Structure with Filenames

  Act 1: Discovery & Foundation ({created_act1_files_count} files)

  1.1 Business Foundation (6 files)

  1.1.1 index.json
  1.1.2 company-vision-mission.json
  1.1.3 business-model-analysis.json
  1.1.4 value-proposition-architecture.json
  1.1.5 organizational-values-culture.json
  1.1.6 leadership-vision-stakeholder-alignment.json

  1.2 Market Intelligence (6 files)

  1.2.1 index.json
  1.2.2 industry-landscape-trends.json
  1.2.3 competitive-analysis-direct-indirect.json
  1.2.4 market-segmentation.json
  1.2.5 category-dynamics.json
  1.2.6 white-space-identification.json

  1.3 Customer Understanding (8 files)

  1.3.1 index.json
  1.3.2 target-audience-definition.json
  1.3.3 customer-personas-behavioral.json
  1.3.4 customer-personas-psychographic.json
  1.3.5 customer-personas-demographic.json
  1.3.6 customer-journey-mapping.json
  1.3.7 pain-points-jobs-to-be-done.json
  1.3.8 customer-sentiment-analysis.json

  1.4 Brand Audit (8 files) (For Refresh/Revamp/Rebuild/Transition only)

  1.4.1 index.json
  1.4.2 current-brand-perception-internal.json
  1.4.3 current-brand-perception-external.json
  1.4.4 brand-equity-assessment.json
  1.4.5 visual-identity-audit.json
  1.4.6 messaging-consistency-review.json
  1.4.7 competitive-positioning-analysis.json
  1.4.8 brand-touchpoint-inventory.json

  1.5 Strategic Insights (5 files)

  1.5.1 index.json
  1.5.2 swot-analysis.json
  1.5.3 market-opportunities-threats.json
  1.5.4 competitive-advantages-moats.json
  1.5.5 growth-barriers-constraints.json

  ---
  Note: Act 1 scaffolded ({created_act1_files_count} files written). Acts 2–8 pending scaffold; ready to generate on approval.
"""
    MANIFEST.write_text(content, encoding="utf-8")


def main():
    ensure_dir(EXPORT_DIR)
    created = scaffold_act1()
    generate_manifest(len(created))
    print(f"✅ Wrote {len(created)} Act 1 files to {EXPORT_DIR}")
    print(f"✅ Manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
