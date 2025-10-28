#!/usr/bin/env python3
"""
Data Helpers - Load and Extract Brand Package Data

Helper functions to:
- Extract sections from brand-foundation.md
- Load new JSON data (claims, clients, certifications)
- Build data context for template rendering

Author: Claude Code
Last Updated: 2025-10-23
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional


# Base paths
EXTRACTED_DATA_DIR = Path("/Users/kalpeshjaju/Development/flyberry_oct_restart/extracted_data")
BRAND_FOUNDATION_PATH = EXTRACTED_DATA_DIR / "brand-foundation.md"
CLAIMS_REGISTRY_PATH = EXTRACTED_DATA_DIR / "claims-registry.json"
CORPORATE_CLIENTS_PATH = EXTRACTED_DATA_DIR / "corporate-clients.json"
CERTIFICATIONS_PATH = EXTRACTED_DATA_DIR / "certifications.json"


def get_brand_foundation_section(section_name: str) -> str:
    """
    Extract a specific section from brand-foundation.md.

    Args:
        section_name: Name of section (e.g., "MISSION", "VISION", "BRAND ESSENCE")

    Returns:
        str: Section content (without heading)
    """
    if not BRAND_FOUNDATION_PATH.exists():
        raise FileNotFoundError(f"Brand foundation file not found: {BRAND_FOUNDATION_PATH}")

    content = BRAND_FOUNDATION_PATH.read_text(encoding='utf-8')

    # Find section heading (## SECTION_NAME)
    # Extract content until next ## heading or end
    section_heading = f"## {section_name}"
    lines = content.split('\n')

    in_section = False
    section_lines = []

    for line in lines:
        # Start capturing when we find the heading
        if line.strip() == section_heading:
            in_section = True
            continue

        if in_section:
            # Stop if we hit another ## heading
            if line.startswith('## '):
                break

            section_lines.append(line)

    result = '\n'.join(section_lines).strip()

    # Remove any trailing --- separators
    if result.endswith('---'):
        result = result[:-3].strip()

    return result


def get_all_brand_foundation_sections() -> Dict[str, str]:
    """
    Extract all major sections from brand-foundation.md.

    Returns:
        dict: Section name -> content mapping
    """
    sections = {}

    # Known sections in brand-foundation.md
    section_names = [
        "MISSION",
        "VISION",
        "BRAND ESSENCE",
        "STRATEGIC POSITIONING",
        "INNOVATION DNA",
        "THE CUSTOMER TRUTH",
        "CATEGORY STRATEGY",
        "BRAND PROMISE",
        "THE FUTURE",
        "YOU EXPERIENCE THE DIFFERENCE"
    ]

    for section_name in section_names:
        try:
            content = get_brand_foundation_section(section_name)
            sections[section_name] = content
        except Exception as e:
            # Section might not exist, skip
            pass

    return sections


def get_brand_foundation_subsection(section_name: str, subsection_name: str) -> str:
    """
    Extract a subsection from within a section.

    Example:
        get_brand_foundation_subsection("STRATEGIC POSITIONING", "WHAT MAKES FLYBERRY DIFFERENT")

    Args:
        section_name: Parent section name
        subsection_name: Subsection heading

    Returns:
        str: Subsection content
    """
    section_content = get_brand_foundation_section(section_name)

    # Find subsection heading (### SUBSECTION_NAME)
    subsection_heading = f"### {subsection_name}"
    lines = section_content.split('\n')

    in_subsection = False
    subsection_lines = []

    for line in lines:
        if line.strip() == subsection_heading:
            in_subsection = True
            continue

        if in_subsection:
            # Stop if we hit another ### or ## heading
            if line.startswith('###') or line.startswith('##'):
                break

            subsection_lines.append(line)

    return '\n'.join(subsection_lines).strip()


def load_claims_registry() -> Dict[str, Any]:
    """Load claims-registry.json."""
    if not CLAIMS_REGISTRY_PATH.exists():
        return {"claims": [], "categories": {}}

    with open(CLAIMS_REGISTRY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_corporate_clients() -> Dict[str, Any]:
    """Load corporate-clients.json."""
    if not CORPORATE_CLIENTS_PATH.exists():
        return {"clients": [], "summary": {}}

    with open(CORPORATE_CLIENTS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_certifications() -> Dict[str, Any]:
    """Load certifications.json."""
    if not CERTIFICATIONS_PATH.exists():
        return {"certifications": [], "qualityMetrics": {}}

    with open(CERTIFICATIONS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_top_claims(n: int = 10) -> List[Dict[str, Any]]:
    """
    Get top N nutritional claims by RDA percentage.

    Args:
        n: Number of top claims to return

    Returns:
        List of claim dicts sorted by RDA% descending
    """
    claims_data = load_claims_registry()
    claims = claims_data.get('claims', [])

    # Sort by rdaPercent descending (handle None values)
    sorted_claims = sorted(
        claims,
        key=lambda c: float(c.get('rdaPercent', 0) or 0),
        reverse=True
    )

    return sorted_claims[:n]


def get_claims_by_product(product_name: str) -> List[Dict[str, Any]]:
    """
    Get all claims for a specific product.

    Args:
        product_name: Name of product

    Returns:
        List of claims for that product
    """
    claims_data = load_claims_registry()
    claims = claims_data.get('claims', [])

    return [
        claim for claim in claims
        if claim.get('product') == product_name
    ]


def get_fortune500_clients() -> List[Dict[str, Any]]:
    """Get list of Fortune 500 clients only."""
    clients_data = load_corporate_clients()
    clients = clients_data.get('clients', [])

    return [
        client for client in clients
        if client.get('fortune500', False)
    ]


def get_client_count_by_category() -> Dict[str, int]:
    """
    Get client count breakdown by category.

    Returns:
        dict: {category: count}
    """
    clients_data = load_corporate_clients()
    clients = clients_data.get('clients', [])

    categories = {}
    for client in clients:
        category = client.get('category', 'Other')
        categories[category] = categories.get(category, 0) + 1

    return categories


def build_data_context(data_source) -> Dict[str, Any]:
    """
    Build complete data context for template rendering.

    Args:
        data_source: BrandPackageDataSource instance

    Returns:
        dict: Complete data context with all available data
    """

    # Load brand foundation sections
    brand_sections = get_all_brand_foundation_sections()

    # Load new data sources
    claims = load_claims_registry()
    clients = load_corporate_clients()
    certifications = load_certifications()

    # Get product data
    products = data_source.get_all_products()
    products_by_cat = data_source.get_products_by_category()
    hero_products = data_source.get_hero_products()
    origins = data_source.get_sourcing_origins()
    nutritional_highlights = data_source.get_nutritional_highlights()

    # Count unique origin countries
    origin_countries = set()
    for product in products:
        origin = product.get('origin')
        if origin:
            origin_countries.add(origin)

    context = {
        # Brand foundation sections
        'brand': {
            'mission': brand_sections.get('MISSION', ''),
            'vision': brand_sections.get('VISION', ''),
            'essence': brand_sections.get('BRAND ESSENCE', ''),
            'positioning': brand_sections.get('STRATEGIC POSITIONING', ''),
            'innovation_dna': brand_sections.get('INNOVATION DNA', ''),
            'customer_truth': brand_sections.get('THE CUSTOMER TRUTH', ''),
            'category_strategy': brand_sections.get('CATEGORY STRATEGY', ''),
            'promise': brand_sections.get('BRAND PROMISE', ''),
            'future': brand_sections.get('THE FUTURE', ''),
            'experience': brand_sections.get('YOU EXPERIENCE THE DIFFERENCE', ''),
        },

        # Products
        'products': {
            'all': products,
            'count': len(products),
            'by_category': products_by_cat,
            'dates': products_by_cat.get('dates', []),
            'nuts': products_by_cat.get('nuts', []),
            'dates_count': len(products_by_cat.get('dates', [])),
            'nuts_count': len(products_by_cat.get('nuts', [])),
            'hero': hero_products,
        },

        # Origins
        'origins': {
            'all': origins,
            'count': len(origin_countries),
            'countries': sorted(origin_countries),
        },

        # Nutritional data
        'nutrition': {
            'highlights': nutritional_highlights,
            'top_10': nutritional_highlights[:10] if nutritional_highlights else [],
        },

        # Claims
        'claims': {
            'all': claims.get('claims', []),
            'count': len(claims.get('claims', [])),
            'top_11': get_top_claims(11),
            'by_category': claims.get('categories', {}),
        },

        # Corporate clients
        'clients': {
            'all': clients.get('clients', []),
            'count': clients.get('summary', {}).get('totalClients', 0),
            'fortune500': get_fortune500_clients(),
            'fortune500_count': clients.get('summary', {}).get('fortune500Count', 0),
            'by_category': get_client_count_by_category(),
        },

        # Certifications
        'certifications': {
            'all': certifications.get('certifications', []),
            'count': len(certifications.get('certifications', [])),
            'metrics': certifications.get('qualityMetrics', {}),
        },
    }

    return context


# Test if running directly
if __name__ == "__main__":
    print("🧪 Testing Data Helpers...\n")

    # Test brand foundation extraction
    print("--- Brand Foundation Sections ---")
    sections = get_all_brand_foundation_sections()
    for name, content in sections.items():
        print(f"✓ {name}: {len(content)} chars")

    print("\n--- Mission Statement ---")
    mission = get_brand_foundation_section("MISSION")
    print(mission[:200] + "..." if len(mission) > 200 else mission)

    # Test new data sources
    print("\n--- Claims Registry ---")
    claims = load_claims_registry()
    print(f"✓ Total claims: {len(claims.get('claims', []))}")
    print(f"✓ Categories: {len(claims.get('categories', {}))}")

    top_claims = get_top_claims(5)
    print("\nTop 5 Claims by RDA%:")
    for claim in top_claims:
        print(f"  - {claim.get('product')}: {claim.get('nutrient')} ({claim.get('rdaPercent')}%)")

    print("\n--- Corporate Clients ---")
    clients = load_corporate_clients()
    print(f"✓ Total clients: {clients.get('summary', {}).get('totalClients', 0)}")
    print(f"✓ Fortune 500: {clients.get('summary', {}).get('fortune500Count', 0)}")

    fortune500 = get_fortune500_clients()
    print(f"\nFortune 500 Clients: {', '.join([c.get('name') for c in fortune500[:5]])}")

    print("\n--- Certifications ---")
    certs = load_certifications()
    print(f"✓ Total certifications: {len(certs.get('certifications', []))}")
    if certs.get('certifications'):
        print("\nCertifications:")
        for cert in certs.get('certifications', [])[:3]:
            print(f"  - {cert.get('name')}: {cert.get('description', '')[:60]}...")

    print("\n✅ All data helpers working!")
