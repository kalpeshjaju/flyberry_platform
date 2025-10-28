#!/usr/bin/env python3
"""
Anti-Hallucination Validator

PURPOSE: Scan generator code for hard-coded/fabricated data
USAGE: python generators/anti_hallucination_validator.py

This validator scans all generator files and flags:
- Hard-coded dictionaries (origin_stories, use_cases, etc.)
- Suspicious long strings (likely fabricated content)
- Missing data source usage (where is data coming from?)
- Fabricated corporate details

AUTHOR: Claude Code
CREATED: 2025-10-23
"""

import re
from pathlib import Path
from typing import List, Tuple


class HallucinationValidator:
    """Validates generators contain no fabricated data"""

    FORBIDDEN_PATTERNS = [
        r'origin_stories\s*=\s*\{',
        r'nut_origin_stories\s*=\s*\{',
        r'use_cases\s*=\s*\{',
        r'client_stories\s*=\s*\[',
        r'case_studies\s*=\s*\[',
        r'terroir_info\s*=\s*\{',
        r'competitive_comparisons\s*=\s*\{',
        r'industry_stats\s*=\s*\{',
    ]

    SUSPICIOUS_CORPORATE_PHRASES = [
        '500kg/month',
        '5,000+ employees',
        'blind taste test',
        'beat Bateel',
        'passed audit',
        'Google Food Safety audit',
    ]

    def __init__(self, generators_dir: Path):
        self.generators_dir = generators_dir
        self.issues_found = []

    def validate_all(self) -> bool:
        """
        Validate all generator files

        Returns:
            bool: True if all clean, False if issues found
        """
        generator_files = list(self.generators_dir.glob('*_builder*.py'))
        generator_files.append(self.generators_dir / 'act1_generator.py')

        for gen_file in generator_files:
            if not gen_file.exists():
                continue

            self._validate_file(gen_file)

        return len(self.issues_found) == 0

    def _validate_file(self, file_path: Path):
        """Validate a single generator file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # STEP: Filter out docstrings and comments
        # WHY: Warning comments contain pattern examples, we only want to detect actual code
        code_lines = []
        in_docstring = False
        for line in lines:
            # Skip docstrings
            if '"""' in line or "'''" in line:
                in_docstring = not in_docstring
                continue
            if in_docstring:
                continue
            # Skip comment-only lines
            if line.strip().startswith('#'):
                continue
            code_lines.append(line)

        content = ''.join(code_lines)

        # Check for hard-coded dictionaries
        for pattern in self.FORBIDDEN_PATTERNS:
            # Add ^ to match only at start of line (actual code, not in strings)
            pattern_with_anchor = r'^' + pattern.lstrip('^')
            match = re.search(pattern_with_anchor, content, re.MULTILINE)
            if match:
                line_num = content[:match.start()].count('\n') + 1
                self.issues_found.append({
                    'file': file_path.name,
                    'line': line_num,
                    'type': 'HARD-CODED DICTIONARY',
                    'pattern': pattern,
                    'severity': 'CRITICAL'
                })

        # Check for suspicious corporate phrases
        for phrase in self.SUSPICIOUS_CORPORATE_PHRASES:
            if phrase in content:
                # Find line number
                lines_for_search = content.split('\n')
                for i, line in enumerate(lines_for_search):
                    if phrase in line:
                        self.issues_found.append({
                            'file': file_path.name,
                            'line': i + 1,
                            'type': 'FABRICATED CORPORATE DETAIL',
                            'pattern': phrase,
                            'severity': 'CRITICAL'
                        })
                        break

        # Check for data source usage (check original content with comments)
        full_content = ''.join(lines)
        has_data_source = 'data_source' in full_content or 'json.load' in full_content
        if not has_data_source:
            self.issues_found.append({
                'file': file_path.name,
                'line': 0,
                'type': 'NO DATA SOURCE',
                'pattern': 'Missing data_source or json.load',
                'severity': 'WARNING'
            })

    def print_report(self):
        """Print validation report"""
        if not self.issues_found:
            print("✅ ALL GENERATORS CLEAN")
            print("   No hallucinations detected")
            return

        print(f"❌ HALLUCINATION ISSUES FOUND: {len(self.issues_found)}\n")

        for issue in self.issues_found:
            severity_icon = "🔴" if issue['severity'] == 'CRITICAL' else "⚠️ "
            print(f"{severity_icon} {issue['file']}:{issue['line']}")
            print(f"   Type: {issue['type']}")
            print(f"   Pattern: {issue['pattern']}")
            print()

        print("\n❌ VALIDATION FAILED")
        print("   Fix issues above before committing")


def main():
    """Run validator"""
    print("🔍 Anti-Hallucination Validator\n")
    print("Scanning generators for fabricated data...\n")

    generators_dir = Path(__file__).parent
    validator = HallucinationValidator(generators_dir)

    is_clean = validator.validate_all()
    validator.print_report()

    exit(0 if is_clean else 1)


if __name__ == '__main__':
    main()
