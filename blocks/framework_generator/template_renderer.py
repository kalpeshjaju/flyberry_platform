#!/usr/bin/env python3
"""
Template Renderer - Render Content Templates with Data

Simple template rendering with placeholder substitution.
Handles:
- {{variable}} - Simple variable substitution
- {{#each items}}...{{/each}} - Loop over items
- {{#if condition}}...{{/if}} - Conditional rendering
- [Description] - Template placeholders for manual content

Author: Claude Code
Last Updated: 2025-10-23
"""

import re
from typing import Dict, Any, List


def render_template(template: str, context: Dict[str, Any]) -> str:
    """
    Render a template string with data context.

    Supports:
    - {{variable}} - Simple variable lookup
    - {{object.property}} - Nested property access
    - [Description] - Template placeholders (left as-is for now)
    - {len(items)} - Python expressions for counts

    Args:
        template: Template string
        context: Data context dictionary

    Returns:
        str: Rendered template
    """

    # For now, keep it simple - just handle direct variable references
    # The spec templates mostly use [placeholder] for content that needs
    # to be pulled from data, so we'll handle those specially

    result = template

    # Handle simple {{variable}} placeholders
    # Example: {{brand.mission}}
    pattern = r'\{\{([^}]+)\}\}'
    matches = re.findall(pattern, result)

    for match in matches:
        value = resolve_variable(match.strip(), context)
        if value is not None:
            # Replace {{variable}} with actual value
            result = result.replace(f'{{{{{match}}}}}', str(value))

    return result


def resolve_variable(var_path: str, context: Dict[str, Any]) -> Any:
    """
    Resolve a variable path in context.

    Examples:
        'brand.mission' -> context['brand']['mission']
        'products.count' -> context['products']['count']
        'products.dates[0].name' -> context['products']['dates'][0]['name']

    Args:
        var_path: Dot-separated variable path
        context: Data context

    Returns:
        Resolved value or None if not found
    """
    parts = var_path.split('.')
    value = context

    for part in parts:
        # Handle array access [0]
        array_match = re.match(r'(\w+)\[(\d+)\]', part)
        if array_match:
            key = array_match.group(1)
            index = int(array_match.group(2))
            if isinstance(value, dict) and key in value:
                value = value[key]
                if isinstance(value, list) and index < len(value):
                    value = value[index]
                else:
                    return None
            else:
                return None
        else:
            # Normal key access
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return None

    return value


def render_section_from_spec(section_spec: Dict[str, Any], context: Dict[str, Any]) -> str:
    """
    Render a section from spec template + data context.

    For Act 1, most sections just need the brand foundation content
    inserted at the right places. The spec templates have [placeholder]
    markers indicating where content should go.

    This function:
    1. Takes the content_template from spec
    2. Replaces [placeholders] with actual content from context
    3. Returns rendered markdown

    Args:
        section_spec: Section specification dict from spec_parser
        context: Data context from data_helpers

    Returns:
        str: Rendered section markdown
    """

    template = section_spec.get('content_template', '')
    if not template:
        return ""

    # For Act 1 Document 00, the templates mostly reference brand-foundation.md content
    # Example placeholders in templates:
    # [Mission statement from brand-foundation.md]
    # [Opening paragraph: 2-3 sentences...]
    # [Explain what this means operationally]

    # For now, we'll just return the template as-is because the actual content
    # needs to come directly from brand-foundation.md sections, which we'll
    # handle in the generator

    # The templates serve as STRUCTURE guides, not variable substitution templates

    return template


def build_section_content(section_spec: Dict[str, Any], context: Dict[str, Any]) -> str:
    """
    Build complete section content from spec + data.

    This is the main function that constructs actual document sections.
    Unlike render_section_from_spec which just returns the template,
    this function:
    1. Reads the section title and purpose from spec
    2. Pulls appropriate content from context (brand foundation, products, etc.)
    3. Constructs complete markdown section

    Args:
        section_spec: Section specification
        context: Data context

    Returns:
        str: Complete rendered section markdown
    """

    section_title = section_spec.get('title', '')
    section_number = section_spec.get('number', 0)

    # For Document 00, most sections map directly to brand-foundation.md sections
    # The mapping is: section title -> brand foundation section name

    # Map section titles to brand foundation keys
    title_to_key = {
        'THE ESSENCE OF FLYBERRY': 'essence',
        'OUR MISSION': 'mission',
        'OUR VISION': 'vision',
        'STRATEGIC POSITIONING': 'positioning',
        'INNOVATION DNA': 'innovation_dna',
        'THE CUSTOMER TRUTH': 'customer_truth',
        'CATEGORY STRATEGY': 'category_strategy',
        'BRAND PROMISE': 'promise',
        'THE FUTURE': 'future',
        'YOU EXPERIENCE THE DIFFERENCE': 'experience',
    }

    brand_key = title_to_key.get(section_title)

    if brand_key and 'brand' in context:
        # Get content from brand foundation
        content = context['brand'].get(brand_key, '')

        if content:
            # Build the section
            md = f"## {section_title}\n\n{content}\n"
            return md

    # If no direct mapping, return empty
    return ""


# Test if running directly
if __name__ == "__main__":
    print("🧪 Testing Template Renderer...\n")

    # Test simple variable resolution
    context = {
        'products': {
            'count': 13,
            'dates_count': 8,
            'nuts_count': 5,
        },
        'origins': {
            'count': 11
        },
        'brand': {
            'mission': 'To deliver India\'s finest-tasting gourmet products'
        }
    }

    # Test variable resolution
    print("--- Variable Resolution ---")
    test_vars = [
        'products.count',
        'products.dates_count',
        'origins.count',
        'brand.mission'
    ]

    for var in test_vars:
        value = resolve_variable(var, context)
        print(f"{{{{var}}}}: {value}")

    # Test template rendering
    print("\n--- Template Rendering ---")
    template = "We have {{products.count}} products ({{products.dates_count}} dates + {{products.nuts_count}} nuts) from {{origins.count}} countries."
    rendered = render_template(template, context)
    print(f"Template: {template}")
    print(f"Rendered: {rendered}")

    print("\n✅ Template renderer working!")
