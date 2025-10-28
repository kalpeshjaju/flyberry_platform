#!/usr/bin/env python3
"""
Spec Parser - Parse Document Spec Markdown Files

Parses Act 1 document specifications to extract structured data:
- Document metadata (title, read time, purpose)
- Data sources required
- Section templates and requirements
- Output format specifications

Author: Claude Code
Last Updated: 2025-10-23
"""

import re
from pathlib import Path
from typing import Dict, List, Any


def parse_document_spec(spec_path: Path) -> Dict[str, Any]:
    """
    Parse a document spec markdown file into structured data.

    Args:
        spec_path: Path to document spec markdown file

    Returns:
        dict: Structured document specification
        {
            "document_number": "00",
            "document_title": "Brand Foundation",
            "read_time": "8 minutes",
            "purpose": "...",
            "data_sources": ["brand-foundation.md"],
            "sections": [
                {
                    "number": 1,
                    "title": "THE ESSENCE OF FLYBERRY",
                    "purpose": "...",
                    "content_template": "...",
                    "requirements": [...]
                }
            ],
            "quality_requirements": {
                "must_have": [...],
                "must_avoid": [...]
            }
        }
    """

    if not spec_path.exists():
        raise FileNotFoundError(f"Spec file not found: {spec_path}")

    content = spec_path.read_text(encoding='utf-8')

    # Extract document number and title from filename
    # Format: doc-00-brand-foundation.md
    filename = spec_path.name
    match = re.match(r'doc-(\d+)-(.+)\.md', filename)
    if not match:
        raise ValueError(f"Invalid spec filename format: {filename}")

    doc_number = match.group(1)
    doc_title_slug = match.group(2)

    # Parse document metadata from header
    doc_title = extract_heading_text(content, "# DOCUMENT")
    read_time = extract_field_value(content, "**Read Time**:")
    purpose = extract_section_content(content, "## PURPOSE")

    # Parse data sources
    data_sources = extract_data_sources(content)

    # Parse section templates
    sections = extract_section_templates(content)

    # Parse quality requirements
    quality_requirements = extract_quality_requirements(content)

    # Generate anchor for navigation
    anchor = f"document-{doc_number}-{doc_title_slug}"

    return {
        "document_number": doc_number,
        "document_title": doc_title.replace(f"DOCUMENT {doc_number}: ", "").replace(" - SPECIFICATION", "").strip(),
        "read_time": read_time or "5 minutes",
        "purpose": purpose.strip() if purpose else "",
        "data_sources": data_sources,
        "sections": sections,
        "quality_requirements": quality_requirements,
        "anchor": anchor
    }


def extract_heading_text(content: str, prefix: str) -> str:
    """Extract text from heading that starts with prefix."""
    lines = content.split('\n')
    for line in lines:
        if line.startswith(prefix):
            return line.replace('#', '').strip()
    return ""


def extract_field_value(content: str, field_name: str) -> str:
    """Extract value after field name (e.g., '**Read Time**: 8 minutes')."""
    lines = content.split('\n')
    for line in lines:
        if field_name in line:
            # Extract text after field name
            parts = line.split(field_name)
            if len(parts) > 1:
                return parts[1].strip()
    return ""


def extract_section_content(content: str, section_heading: str) -> str:
    """
    Extract content between section heading and next heading of same/higher level.
    Ignores headings inside code blocks.
    """
    lines = content.split('\n')
    in_section = False
    in_code_block = False
    section_lines = []

    # Determine heading level from the heading marker
    heading_match = re.match(r'^(#+)', section_heading)
    if not heading_match:
        return ""

    heading_level = len(heading_match.group(1))

    for line in lines:
        # Track code block state
        if line.strip().startswith('```'):
            in_code_block = not in_code_block

        # Start capturing when we find the heading
        if line.strip() == section_heading or line.strip().startswith(section_heading):
            in_section = True
            continue

        if in_section:
            # Only check for section-ending headings when NOT in code block
            if not in_code_block:
                heading_match = re.match(r'^(#+)\s', line)
                if heading_match:
                    current_level = len(heading_match.group(1))
                    if current_level <= heading_level:
                        break

            section_lines.append(line)

    return '\n'.join(section_lines).strip()


def extract_data_sources(content: str) -> List[str]:
    """Extract data sources from DATA SOURCES section."""
    data_sources_section = extract_section_content(content, "## DATA SOURCES")

    sources = []
    lines = data_sources_section.split('\n')

    for line in lines:
        # Look for markdown file references or JSON references
        # Format: **Primary**: `brand-foundation.md`
        # Format: - `products/*.json`

        # Extract from backticks
        backtick_matches = re.findall(r'`([^`]+)`', line)
        for match in backtick_matches:
            if match.endswith('.md') or match.endswith('.json') or '*' in match:
                sources.append(match)

    return sources


def extract_section_templates(content: str) -> List[Dict[str, Any]]:
    """Extract section templates from SECTION STRUCTURE section."""
    section_structure = extract_section_content(content, "## SECTION STRUCTURE")

    sections = []

    # Split by ### **Section N: TITLE** pattern
    section_pattern = r'###\s+\*\*Section\s+(\d+):\s+([^*]+)\*\*'
    section_matches = list(re.finditer(section_pattern, section_structure))

    for i, match in enumerate(section_matches):
        section_num = int(match.group(1))
        section_title = match.group(2).strip()

        # Get content between this section and next section
        start_pos = match.end()
        end_pos = section_matches[i + 1].start() if i + 1 < len(section_matches) else len(section_structure)
        section_content = section_structure[start_pos:end_pos]

        # Extract purpose
        purpose = extract_field_value(section_content, "**Purpose**:")

        # Extract content template (from markdown code blocks)
        content_template = extract_code_block(section_content, "markdown")

        # Extract requirements
        requirements = extract_requirements(section_content)

        sections.append({
            "number": section_num,
            "title": section_title,
            "purpose": purpose,
            "content_template": content_template,
            "requirements": requirements
        })

    return sections


def extract_code_block(content: str, language: str = "") -> str:
    """Extract content from markdown code block."""
    # Pattern: ```language\n...\n```
    pattern = rf'```{language}\s*\n(.*?)\n```'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        return match.group(1).strip()

    return ""


def extract_requirements(section_content: str) -> List[str]:
    """Extract requirements list from **Requirements**: section."""
    requirements = []

    # Find **Requirements**: section
    lines = section_content.split('\n')
    in_requirements = False

    for line in lines:
        if '**Requirements**:' in line:
            in_requirements = True
            continue

        if in_requirements:
            # Stop if we hit another bold section or ---
            if line.strip().startswith('**') and line.strip().endswith('**'):
                break
            if line.strip() == '---':
                break

            # Extract bullet points
            if line.strip().startswith('-'):
                requirement = line.strip()[1:].strip()  # Remove leading -
                requirements.append(requirement)

    return requirements


def extract_quality_requirements(content: str) -> Dict[str, List[str]]:
    """Extract quality requirements from QUALITY REQUIREMENTS section."""
    quality_section = extract_section_content(content, "## QUALITY REQUIREMENTS")

    must_have = []
    must_avoid = []

    lines = quality_section.split('\n')
    current_list = None

    for line in lines:
        if '**Must Have**:' in line or '### **Must Have**' in line:
            current_list = 'must_have'
            continue

        if '**Must Avoid**:' in line or '### **Must Avoid**' in line:
            current_list = 'must_avoid'
            continue

        # Extract checkboxes and bullets
        if current_list:
            # Format: - [ ] Item or - ❌ Item
            checkbox_match = re.match(r'^\s*-\s+\[\s*\]\s+(.+)', line)
            emoji_match = re.match(r'^\s*-\s+[❌✅]\s+(.+)', line)
            bullet_match = re.match(r'^\s*-\s+(.+)', line)

            if checkbox_match:
                item = checkbox_match.group(1).strip()
                if current_list == 'must_have':
                    must_have.append(item)
            elif emoji_match:
                item = emoji_match.group(1).strip()
                if current_list == 'must_avoid':
                    must_avoid.append(item)
            elif bullet_match and current_list == 'must_avoid':
                item = bullet_match.group(1).strip()
                must_avoid.append(item)

    return {
        "must_have": must_have,
        "must_avoid": must_avoid
    }


def get_all_document_specs(spec_dir: Path) -> List[Dict[str, Any]]:
    """
    Load and parse all document specs from directory.

    Args:
        spec_dir: Path to act-1-document-specs/ directory

    Returns:
        List of parsed document specs, sorted by document number
    """
    spec_files = sorted(spec_dir.glob("doc-*.md"))
    specs = []

    for spec_file in spec_files:
        try:
            spec = parse_document_spec(spec_file)
            specs.append(spec)
        except Exception as e:
            print(f"Warning: Failed to parse {spec_file.name}: {e}")

    # Sort by document number
    specs.sort(key=lambda s: s['document_number'])

    return specs


# Test if running directly
if __name__ == "__main__":
    print("🧪 Testing Spec Parser...\n")

    spec_dir = Path("/Users/kalpeshjaju/Development/flyberry_oct_restart/extracted_data/act-1-document-specs")

    # Test parsing all specs
    specs = get_all_document_specs(spec_dir)

    print(f"✅ Parsed {len(specs)} document specs\n")

    for spec in specs:
        print(f"📄 Document {spec['document_number']}: {spec['document_title']}")
        print(f"   Read Time: {spec['read_time']}")
        print(f"   Sections: {len(spec['sections'])}")
        print(f"   Data Sources: {len(spec['data_sources'])}")
        print(f"   Quality Requirements: {len(spec['quality_requirements']['must_have'])} must-haves, {len(spec['quality_requirements']['must_avoid'])} must-avoids")
        print()

    # Show detailed example for Document 00
    if specs:
        print("\n--- Document 00 Detail ---")
        doc00 = specs[0]
        print(f"Title: {doc00['document_title']}")
        print(f"Purpose: {doc00['purpose'][:100]}...")
        print(f"\nSections:")
        for section in doc00['sections'][:2]:  # First 2 sections
            print(f"  {section['number']}. {section['title']}")
            print(f"     Purpose: {section['purpose']}")
            print(f"     Requirements: {len(section['requirements'])}")
            if section['content_template']:
                print(f"     Template: {len(section['content_template'])} chars")
