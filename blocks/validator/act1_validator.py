#!/usr/bin/env python3
"""
ACT 1 VALIDATION SCRIPT

Purpose: Validates Act 1 HTML output against master blueprint requirements
Author: Claude Code (AI Collaboration Standards)
Last Updated: 2025-10-23

What This Does:
- Reads master blueprint to extract quality standards
- Reads generated HTML output
- Validates against 25-point quality checklist
- Checks specificity standard (generic vs specific claims)
- Scores depth across 5 dimensions (0-100 scale)
- Generates comprehensive validation report

How to Run:
    python3 validators/act1_validator.py

Output:
    - Console summary
    - Detailed report: validators/reports/act1-validation-YYYY-MM-DD.md
"""

import re
import os
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Dict, List, Tuple


class Act1Validator:
    """
    Validates Act 1 HTML against master blueprint requirements.

    WHY: Ensures HTML meets McKinsey/BCG-level quality standards before delivery
    HOW: Systematic checks across content, structure, writing, expertise dimensions

    ATTRIBUTES:
        blueprint_path (str): Path to master blueprint markdown
        html_path (str): Path to generated HTML file
        report_dir (str): Directory for validation reports

    EDGE CASES:
        - Missing files: Returns error message if paths invalid
        - Malformed HTML: BeautifulSoup handles gracefully
        - Empty sections: Counted as missing required content
    """

    def __init__(self):
        """Initialize validator with file paths"""
        # INPUT files
        self.blueprint_path = "/Users/kalpeshjaju/Development/flyberry_oct_restart/extracted_data/act-1-master-blueprint.md"
        self.html_path = "/Users/kalpeshjaju/Development/flyberry_brand_package/docs/act-1-who-we-are.html"

        # OUTPUT directory
        self.report_dir = "/Users/kalpeshjaju/Development/flyberry_brand_package/validators/reports"

        # Data containers
        self.html_content = None
        self.html_text = None
        self.soup = None
        self.word_count = 0
        self.line_count = 0

        # Validation results
        self.results = {
            'content_quality': {},
            'structure_quality': {},
            'writing_quality': {},
            'expertise_signals': {},
            'specificity': {},
            'depth_score': {}
        }

    def load_files(self) -> bool:
        """
        Load blueprint and HTML files for validation.

        RETURNS:
            bool: True if both files loaded successfully, False otherwise
        """
        try:
            # Load HTML
            with open(self.html_path, 'r', encoding='utf-8') as f:
                self.html_content = f.read()

            # Parse HTML
            self.soup = BeautifulSoup(self.html_content, 'html.parser')

            # Extract text content (remove HTML tags)
            self.html_text = self.soup.get_text(separator=' ', strip=True)

            # Calculate metrics
            self.word_count = len(self.html_text.split())
            self.line_count = len(self.html_content.split('\n'))

            print(f"✅ Loaded HTML: {self.html_path}")
            print(f"   Lines: {self.line_count}, Words: {self.word_count}")
            return True

        except FileNotFoundError as e:
            print(f"❌ ERROR: File not found - {e}")
            return False
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False

    def validate_content_quality(self) -> Dict[str, bool]:
        """
        Validate Content Quality (7 checks from blueprint lines 228-236)

        CHECKS:
            1. Core insight in first 2 sentences (Pyramid Principle)
            2. Every fact has "why this matters" explanation (SO WHAT test)
            3. Specific data provided (254.5%, not "high in")
            4. Third-party validation (Fortune 500, lab-tested, FSSAI)
            5. Customer benefit clearly stated
            6. Competitive differentiation shown
            7. Sources cited, confidence stated

        RETURNS:
            Dict mapping check name to pass/fail boolean
        """
        checks = {}

        # Check 1: Core insight in first 2 sentences
        # Look for substantive opening paragraphs in document sections
        doc_sections = self.soup.find_all('div', class_=re.compile('doc-'))
        has_pyramid_structure = False
        for section in doc_sections[:3]:  # Check first 3 documents
            paragraphs = section.find_all('p', limit=2)
            if len(paragraphs) >= 1:
                first_p = paragraphs[0].get_text()
                # Check if substantial (>50 chars) and not metadata
                if len(first_p) > 50 and not first_p.startswith('Read Time'):
                    has_pyramid_structure = True
                    break
        checks['core_insight_first'] = has_pyramid_structure

        # Check 2: "Why this matters" / "What this means" sections present
        why_matters_patterns = [
            r'why this matters',
            r'what this means',
            r'what you experience',
            r'what you taste',
            r'why \w+',
            r'this reveals'
        ]
        why_matters_count = sum(
            len(re.findall(pattern, self.html_text, re.IGNORECASE))
            for pattern in why_matters_patterns
        )
        # Expect at least 5 "why this matters" explanations across 7 documents
        checks['why_matters_present'] = why_matters_count >= 5

        # Check 3: Specific data provided (numbers with %, RDA, ×, ₹)
        specific_data_patterns = [
            r'\d+\.?\d*%',  # Percentages: 254.5%
            r'\d+×',         # Multipliers: 20×
            r'₹\d+',         # Prices: ₹899
            r'\d+\s*RDA',    # RDA values
            r'\d+\+?\s*(countries|companies|varieties|products)',  # Counts
        ]
        specific_data_count = sum(
            len(re.findall(pattern, self.html_text))
            for pattern in specific_data_patterns
        )
        # Expect at least 20 specific data points across full document
        checks['specific_data_provided'] = specific_data_count >= 20

        # Check 4: Third-party validation present
        validation_terms = [
            'fortune 500', 'lab-tested', 'fssai', 'haccp',
            'certified', 'verified', 'validated'
        ]
        has_validation = any(
            term in self.html_text.lower()
            for term in validation_terms
        )
        checks['third_party_validation'] = has_validation

        # Check 5: Customer benefit clearly stated
        benefit_patterns = [
            r'you taste',
            r'you experience',
            r'customer benefit',
            r'what you get',
            r'supports? \w+ (health|function)',
            r'benefits?:'
        ]
        benefit_count = sum(
            len(re.findall(pattern, self.html_text, re.IGNORECASE))
            for pattern in benefit_patterns
        )
        checks['customer_benefit_stated'] = benefit_count >= 5

        # Check 6: Competitive differentiation shown
        differentiation_patterns = [
            r'competitors',
            r'vs\s+competitors',
            r'20× fewer',
            r'india\'s only',
            r'while others',
            r'unlike'
        ]
        diff_count = sum(
            len(re.findall(pattern, self.html_text, re.IGNORECASE))
            for pattern in differentiation_patterns
        )
        checks['competitive_differentiation'] = diff_count >= 3

        # Check 7: Sources cited
        # Look for "Data Sources" section at end
        has_sources = 'data sources' in self.html_text.lower()
        checks['sources_cited'] = has_sources

        self.results['content_quality'] = checks
        return checks

    def validate_structure_quality(self) -> Dict[str, bool]:
        """
        Validate Structure Quality (5 checks from blueprint lines 238-243)

        CHECKS:
            1. MECE organization (7 distinct documents, no overlap)
            2. Pyramid structure (answer first, evidence follows)
            3. Progressive disclosure (H2 → H3 → bullets)
            4. Clear hierarchy (proper heading structure)
            5. Smooth transitions (bridge sentences between sections)

        RETURNS:
            Dict mapping check name to pass/fail boolean
        """
        checks = {}

        # Check 1: MECE - 7 distinct document sections present
        doc_sections = self.soup.find_all('div', class_=re.compile('doc-'))
        checks['mece_organization'] = len(doc_sections) >= 6  # Expect 7, accept 6+

        # Check 2: Pyramid structure - substantive opening paragraphs
        pyramid_count = 0
        for section in doc_sections:
            first_p = section.find('p')
            if first_p and len(first_p.get_text()) > 100:
                pyramid_count += 1
        checks['pyramid_structure'] = pyramid_count >= 5

        # Check 3: Progressive disclosure - H2, H3, bullets present
        h2_count = len(self.soup.find_all('h2'))
        h3_count = len(self.soup.find_all('h3'))
        h4_count = len(self.soup.find_all('h4'))
        ul_count = len(self.soup.find_all('ul'))
        checks['progressive_disclosure'] = (h2_count >= 5 and h3_count >= 10 and ul_count >= 5)

        # Check 4: Clear hierarchy - proper heading order
        headings = self.soup.find_all(['h1', 'h2', 'h3', 'h4'])
        heading_order_valid = True
        prev_level = 0
        for heading in headings:
            level = int(heading.name[1])
            # Check we don't skip levels (H2 → H4 without H3)
            if level > prev_level + 1 and prev_level > 0:
                heading_order_valid = False
                break
            prev_level = level
        checks['clear_hierarchy'] = heading_order_valid

        # Check 5: Smooth transitions - "Continue to" links present
        transition_patterns = [
            r'continue to:',
            r'next:',
            r'now let\'s',
            r'this reveals',
            r'building on'
        ]
        transition_count = sum(
            len(re.findall(pattern, self.html_text, re.IGNORECASE))
            for pattern in transition_patterns
        )
        checks['smooth_transitions'] = transition_count >= 5

        self.results['structure_quality'] = checks
        return checks

    def validate_writing_quality(self) -> Dict[str, bool]:
        """
        Validate Writing Quality (5 checks from blueprint lines 244-250)

        CHECKS:
            1. Active voice predominates
            2. Mix of sentence lengths (rhythm)
            3. Strategic bold emphasis
            4. Quotable brand philosophy statements
            5. Headers tell story (not generic labels)

        RETURNS:
            Dict mapping check name to pass/fail boolean
        """
        checks = {}

        # Check 1: Active voice - look for "we", "you" vs passive "is", "are"
        active_patterns = [r'\bwe\s+\w+', r'\byou\s+\w+']
        passive_patterns = [r'\bis\s+\w+ed\b', r'\bare\s+\w+ed\b', r'\bwas\s+\w+ed\b']

        active_count = sum(len(re.findall(p, self.html_text, re.IGNORECASE)) for p in active_patterns)
        passive_count = sum(len(re.findall(p, self.html_text, re.IGNORECASE)) for p in passive_patterns)

        # Active should be at least 2× passive
        checks['active_voice_predominates'] = active_count >= (passive_count * 2)

        # Check 2: Sentence length variety
        # Extract sentences from main content
        sentences = re.split(r'[.!?]+', self.html_text)
        sentence_lengths = [len(s.split()) for s in sentences if len(s.strip()) > 10]

        if len(sentence_lengths) > 20:
            avg_length = sum(sentence_lengths) / len(sentence_lengths)
            # Good rhythm: mix of short (<10), medium (10-20), long (>20)
            short = sum(1 for l in sentence_lengths if l < 10)
            medium = sum(1 for l in sentence_lengths if 10 <= l <= 20)
            long_s = sum(1 for l in sentence_lengths if l > 20)

            # All three types should be present
            checks['sentence_length_variety'] = (short > 5 and medium > 5 and long_s > 3)
        else:
            checks['sentence_length_variety'] = False

        # Check 3: Strategic bold emphasis - <strong> tags present
        strong_tags = self.soup.find_all('strong')
        checks['strategic_bold_emphasis'] = len(strong_tags) >= 20

        # Check 4: Quotable brand philosophy - blockquotes present
        blockquotes = self.soup.find_all('blockquote')
        checks['quotable_philosophy'] = len(blockquotes) >= 1

        # Check 5: Headers tell story - check if headers have meaningful words
        headers = self.soup.find_all(['h2', 'h3', 'h4'])
        generic_headers = ['overview', 'introduction', 'summary', 'conclusion', 'background']

        total_headers = len(headers)
        non_generic = 0
        for header in headers:
            header_text = header.get_text().lower()
            # Check if header is NOT just generic
            is_generic = any(g in header_text for g in generic_headers)
            if not is_generic and len(header_text) > 10:
                non_generic += 1

        # At least 80% of headers should be non-generic
        checks['headers_tell_story'] = (non_generic / max(total_headers, 1)) >= 0.8

        self.results['writing_quality'] = checks
        return checks

    def validate_expertise_signals(self) -> Dict[str, bool]:
        """
        Validate Expertise Signals (5 checks from blueprint lines 252-258)

        CHECKS:
            1. Technical terminology used correctly
            2. Non-obvious insights revealed
            3. "Why behind what" explained
            4. Category dynamics understood
            5. Market positioning clear

        RETURNS:
            Dict mapping check name to pass/fail boolean
        """
        checks = {}

        # Check 1: Technical terms present
        technical_terms = [
            'majestic', 'terroir', 'rda', 'fssai', 'haccp',
            'style 0', 'grade', 'classification', 'vacuum-frying',
            'cold chain', 'microclimate', 'export grade'
        ]
        tech_term_count = sum(
            self.html_text.lower().count(term)
            for term in technical_terms
        )
        checks['technical_terminology'] = tech_term_count >= 10

        # Check 2: Non-obvious insights (look for specific patterns)
        insight_patterns = [
            r'\d+-\d+\s+year',  # "7-8 year maturation"
            r'wild-harvested',
            r'dead sea microclimate',
            r'terroir',
            r'top export grade'
        ]
        insight_count = sum(
            len(re.findall(pattern, self.html_text, re.IGNORECASE))
            for pattern in insight_patterns
        )
        checks['non_obvious_insights'] = insight_count >= 3

        # Check 3: "Why" explanations present
        why_patterns = [
            r'why\s+\w+',
            r'because',
            r'the reason',
            r'this is why',
            r'this enables',
            r'this allows'
        ]
        why_count = sum(
            len(re.findall(pattern, self.html_text, re.IGNORECASE))
            for pattern in why_patterns
        )
        checks['why_explained'] = why_count >= 10

        # Check 4: Category dynamics (commodity trap, premium positioning)
        category_terms = [
            'commodity', 'category', 'market', 'positioning',
            'premium', 'differentiation', 'competition'
        ]
        category_count = sum(
            self.html_text.lower().count(term)
            for term in category_terms
        )
        checks['category_dynamics'] = category_count >= 5

        # Check 5: Market positioning clear (building to #1, leadership)
        positioning_terms = [
            '#1', 'number 1', 'leader', 'leadership',
            'building to', 'dominate', 'finest'
        ]
        positioning_count = sum(
            self.html_text.lower().count(term)
            for term in positioning_terms
        )
        checks['market_positioning_clear'] = positioning_count >= 5

        self.results['expertise_signals'] = checks
        return checks

    def check_specificity_standard(self) -> Dict[str, any]:
        """
        Check Specificity Standard (blueprint lines 183-204)

        CHECKS:
            - Generic claims: "premium quality", "trusted by corporates", "healthy"
            - Specific claims: "254.5% RDA", "50+ Fortune 500", "20× fewer"
            - Ratio: specific / total

        RETURNS:
            Dict with generic_claims, specific_claims, ratio, examples
        """
        # Generic claim patterns (from blueprint)
        generic_patterns = [
            (r'\bpremium quality\b', 'premium quality'),
            (r'\btrusted by corporates\b', 'trusted by corporates'),
            (r'\bindustry-leading\b', 'industry-leading'),
            (r'\bhealthy nuts\b', 'healthy nuts'),
            (r'\bhigh quality\b', 'high quality'),
            (r'\bworld-class\b(?!\s+quality)', 'world-class (without specifics)'),
            (r'\bexceptional\b(?!\s+\w+)', 'exceptional (vague)'),
            (r'\bfinest\b(?!\s+\w+)', 'finest (without context)')
        ]

        # Specific claim patterns
        specific_patterns = [
            (r'\d+\.?\d*%\s*RDA', 'RDA percentage'),
            (r'\d+×', 'multiplier comparison'),
            (r'₹\d+', 'specific price'),
            (r'\d+\+?\s*(countries|companies|varieties)', 'specific count'),
            (r'jordan valley', 'specific origin'),
            (r'majestic\s+grade', 'specific grade'),
            (r'style\s+0', 'specific classification'),
            (r'5-10°c', 'specific temperature'),
            (r'fortune 500', 'third-party validation'),
        ]

        # Find generic claims
        generic_claims = []
        for pattern, name in generic_patterns:
            matches = re.finditer(pattern, self.html_text, re.IGNORECASE)
            for match in matches:
                # Get surrounding context (50 chars before/after)
                start = max(0, match.start() - 50)
                end = min(len(self.html_text), match.end() + 50)
                context = self.html_text[start:end].replace('\n', ' ')
                generic_claims.append({
                    'term': name,
                    'context': f"...{context}..."
                })

        # Find specific claims
        specific_claims = []
        for pattern, name in specific_patterns:
            matches = re.finditer(pattern, self.html_text, re.IGNORECASE)
            for match in matches:
                specific_claims.append({
                    'term': name,
                    'value': match.group()
                })

        # Calculate ratio
        total = len(generic_claims) + len(specific_claims)
        if total > 0:
            specific_ratio = len(specific_claims) / total
        else:
            specific_ratio = 0.0

        self.results['specificity'] = {
            'generic_count': len(generic_claims),
            'specific_count': len(specific_claims),
            'ratio': specific_ratio,
            'target': 0.90,  # 90% specific claims target
            'generic_examples': generic_claims[:5],  # First 5 examples
            'specific_examples': specific_claims[:10]  # First 10 examples
        }

        return self.results['specificity']

    def calculate_depth_score(self) -> Dict[str, int]:
        """
        Calculate Depth Score (blueprint lines 268-289)

        DIMENSIONS:
            1. Data Specificity (20 points) - specific numbers vs generic
            2. Evidence Hierarchy (20 points) - fact + validation + implication
            3. Customer Translation (20 points) - features → benefits with sensory
            4. Structural Integrity (20 points) - MECE, hierarchy, transitions
            5. Expertise Demonstration (20 points) - technical depth, insights

        TARGET: 100/100

        RETURNS:
            Dict with scores for each dimension and total
        """
        scores = {}

        # 1. Data Specificity (20 points)
        # Based on specificity ratio
        specificity = self.results['specificity']
        if specificity['ratio'] >= 0.90:
            scores['data_specificity'] = 20
        elif specificity['ratio'] >= 0.75:
            scores['data_specificity'] = 15
        elif specificity['ratio'] >= 0.60:
            scores['data_specificity'] = 10
        else:
            scores['data_specificity'] = int(specificity['ratio'] * 20)

        # 2. Evidence Hierarchy (20 points)
        # Check if claims have fact + validation + implication structure
        # Sample: Fortune 500 mention + specific count + "what this means"
        has_full_hierarchy = (
            'fortune 500' in self.html_text.lower() and
            '50+' in self.html_text and
            ('trust' in self.html_text.lower() or 'validation' in self.html_text.lower())
        )

        validation_count = len(re.findall(r'(lab-tested|fssai|haccp|certified|verified)', self.html_text, re.IGNORECASE))
        implication_count = len(re.findall(r'(what this means|why this matters|you taste|you experience)', self.html_text, re.IGNORECASE))

        evidence_score = 0
        if has_full_hierarchy:
            evidence_score += 8
        evidence_score += min(6, validation_count * 2)  # Up to 6 points
        evidence_score += min(6, implication_count)      # Up to 6 points
        scores['evidence_hierarchy'] = min(20, evidence_score)

        # 3. Customer Translation (20 points)
        # Look for sensory language and benefit mapping
        sensory_terms = [
            'taste', 'flavor', 'texture', 'soft', 'crunchy', 'creamy',
            'buttery', 'sweet', 'caramel', 'honey', 'rich', 'notes'
        ]
        sensory_count = sum(self.html_text.lower().count(term) for term in sensory_terms)

        benefit_patterns = [
            r'you taste', r'you experience', r'what you get',
            r'supports \w+ (health|function)', r'benefits:'
        ]
        benefit_count = sum(len(re.findall(p, self.html_text, re.IGNORECASE)) for p in benefit_patterns)

        translation_score = 0
        translation_score += min(10, sensory_count // 2)  # 1 point per 2 sensory terms, max 10
        translation_score += min(10, benefit_count * 2)   # 2 points per benefit section, max 10
        scores['customer_translation'] = min(20, translation_score)

        # 4. Structural Integrity (20 points)
        # Based on structure quality checks
        structure_checks = self.results['structure_quality']
        structure_passed = sum(1 for v in structure_checks.values() if v)
        scores['structural_integrity'] = int((structure_passed / 5) * 20)

        # 5. Expertise Demonstration (20 points)
        # Based on expertise signals checks
        expertise_checks = self.results['expertise_signals']
        expertise_passed = sum(1 for v in expertise_checks.values() if v)
        scores['expertise_demonstration'] = int((expertise_passed / 5) * 20)

        # Total score
        scores['total'] = sum(scores.values())
        scores['target'] = 100

        self.results['depth_score'] = scores
        return scores

    def identify_critical_issues(self) -> List[str]:
        """
        Identify critical issues that must be fixed.

        CRITICAL = fails core quality requirements from blueprint

        RETURNS:
            List of critical issue descriptions
        """
        issues = []

        # Content Quality issues
        if not self.results['content_quality'].get('specific_data_provided'):
            issues.append("Missing sufficient specific data points (need 20+, found fewer)")

        if not self.results['content_quality'].get('why_matters_present'):
            issues.append("Missing 'What This Means' / 'Why This Matters' sections (need 5+)")

        if not self.results['content_quality'].get('third_party_validation'):
            issues.append("Missing third-party validation (Fortune 500, lab-tested, FSSAI)")

        # Structure Quality issues
        if not self.results['structure_quality'].get('mece_organization'):
            issues.append("Missing MECE structure (need 7 distinct documents)")

        # Specificity issues
        specificity = self.results['specificity']
        if specificity['ratio'] < 0.90:
            issues.append(f"Specificity ratio below target (found {specificity['ratio']:.1%}, need 90%+)")

        if specificity['generic_count'] > 5:
            issues.append(f"Too many generic claims (found {specificity['generic_count']}, should be <5)")

        # Depth Score issues
        depth = self.results['depth_score']
        if depth['total'] < 80:
            issues.append(f"Depth score below passing threshold (scored {depth['total']}/100, need 80+)")

        # Expertise issues
        if not self.results['expertise_signals'].get('technical_terminology'):
            issues.append("Insufficient technical terminology (need 10+ uses)")

        return issues

    def generate_recommendations(self) -> List[str]:
        """
        Generate actionable recommendations for improvement.

        RETURNS:
            List of specific recommendations
        """
        recommendations = []

        # Based on failed checks
        content = self.results['content_quality']
        structure = self.results['structure_quality']
        writing = self.results['writing_quality']
        expertise = self.results['expertise_signals']

        if not content.get('why_matters_present'):
            recommendations.append(
                "Add 'What This Means' sections after major claims (target: 5+ across document)"
            )

        if not content.get('competitive_differentiation'):
            recommendations.append(
                "Strengthen competitive differentiation (add 'vs competitors', '20× fewer', 'India's only')"
            )

        if not structure.get('smooth_transitions'):
            recommendations.append(
                "Add transition sentences between sections ('Continue to:', 'This reveals:', 'Building on')"
            )

        if not writing.get('active_voice_predominates'):
            recommendations.append(
                "Increase active voice usage (convert passive 'is done' to active 'we do')"
            )

        if not expertise.get('why_explained'):
            recommendations.append(
                "Add more 'why' explanations (why this origin? why this process? why this matters?)"
            )

        # Specificity recommendations
        specificity = self.results['specificity']
        if specificity['generic_count'] > 0:
            recommendations.append(
                f"Replace {specificity['generic_count']} generic claims with specific data (see examples in report)"
            )

        # Depth score recommendations
        depth = self.results['depth_score']
        if depth['data_specificity'] < 18:
            recommendations.append(
                "Increase data specificity (add more RDA%, specific origins, exact counts)"
            )

        if depth['customer_translation'] < 18:
            recommendations.append(
                "Strengthen customer translation (add sensory language: buttery, caramel notes, soft texture)"
            )

        return recommendations

    def generate_report(self) -> str:
        """
        Generate comprehensive validation report in markdown format.

        RETURNS:
            str: Formatted markdown report
        """
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')

        # Calculate summary stats
        content_passed = sum(1 for v in self.results['content_quality'].values() if v)
        content_total = len(self.results['content_quality'])

        structure_passed = sum(1 for v in self.results['structure_quality'].values() if v)
        structure_total = len(self.results['structure_quality'])

        writing_passed = sum(1 for v in self.results['writing_quality'].values() if v)
        writing_total = len(self.results['writing_quality'])

        expertise_passed = sum(1 for v in self.results['expertise_signals'].values() if v)
        expertise_total = len(self.results['expertise_signals'])

        specificity = self.results['specificity']
        depth = self.results['depth_score']

        # Determine pass/fail
        overall_pass = (
            depth['total'] >= 80 and
            specificity['ratio'] >= 0.80 and
            content_passed >= 5 and
            structure_passed >= 4
        )

        # Build report
        report = f"""# ACT 1 VALIDATION REPORT

**Date**: {date_str}
**HTML File**: act-1-who-we-are.html
**Lines**: {self.line_count}
**Word Count**: {self.word_count:,}

---

## QUALITY CHECKLIST

### Content Quality ({content_passed}/{content_total} checks passed)

"""

        # Content Quality details
        for check, passed in self.results['content_quality'].items():
            status = "✅" if passed else "❌"
            check_name = check.replace('_', ' ').title()
            report += f"{status} {check_name}\n"

        report += f"\n**Score**: {content_passed}/{content_total} passed\n\n---\n\n"

        # Structure Quality
        report += f"### Structure Quality ({structure_passed}/{structure_total} checks passed)\n\n"
        for check, passed in self.results['structure_quality'].items():
            status = "✅" if passed else "❌"
            check_name = check.replace('_', ' ').title()
            report += f"{status} {check_name}\n"

        report += f"\n**Score**: {structure_passed}/{structure_total} passed\n\n---\n\n"

        # Writing Quality
        report += f"### Writing Quality ({writing_passed}/{writing_total} checks passed)\n\n"
        for check, passed in self.results['writing_quality'].items():
            status = "✅" if passed else "❌"
            check_name = check.replace('_', ' ').title()
            report += f"{status} {check_name}\n"

        report += f"\n**Score**: {writing_passed}/{writing_total} passed\n\n---\n\n"

        # Expertise Signals
        report += f"### Expertise Signals ({expertise_passed}/{expertise_total} checks passed)\n\n"
        for check, passed in self.results['expertise_signals'].items():
            status = "✅" if passed else "❌"
            check_name = check.replace('_', ' ').title()
            report += f"{status} {check_name}\n"

        report += f"\n**Score**: {expertise_passed}/{expertise_total} passed\n\n---\n\n"

        # Specificity Standard
        report += f"""## SPECIFICITY STANDARD

**Generic claims found**: {specificity['generic_count']} instances
"""

        if specificity['generic_examples']:
            report += "\nExamples:\n"
            for example in specificity['generic_examples']:
                report += f"- \"{example['term']}\"\n"
                report += f"  Context: {example['context']}\n"

        report += f"""
**Specific claims found**: {specificity['specific_count']} instances

Examples:
"""

        for example in specificity['specific_examples'][:5]:
            report += f"- {example['value']} ({example['term']}) ✅\n"

        ratio_pct = specificity['ratio'] * 100
        target_pct = specificity['target'] * 100

        report += f"""
**Ratio**: {specificity['specific_count']} specific / {specificity['generic_count'] + specificity['specific_count']} total = {ratio_pct:.1f}%
**Target**: >{target_pct:.0f}% specific

"""

        if specificity['ratio'] >= specificity['target']:
            report += "✅ **PASS** - Meets specificity standard\n\n"
        else:
            report += f"❌ **FAIL** - Below target by {target_pct - ratio_pct:.1f} percentage points\n\n"

        report += "---\n\n"

        # Depth Score
        report += f"""## DEPTH SCORE

1. **Data Specificity**: {depth['data_specificity']}/20
2. **Evidence Hierarchy**: {depth['evidence_hierarchy']}/20
3. **Customer Translation**: {depth['customer_translation']}/20
4. **Structural Integrity**: {depth['structural_integrity']}/20
5. **Expertise Demonstration**: {depth['expertise_demonstration']}/20

**TOTAL**: {depth['total']}/100
**Target**: {depth['target']}/100

"""

        if depth['total'] >= 80:
            report += "✅ **PASS** - Meets depth standard\n\n"
        else:
            report += f"❌ **FAIL** - Below passing threshold by {80 - depth['total']} points\n\n"

        report += "---\n\n"

        # Critical Issues
        issues = self.identify_critical_issues()
        report += f"## CRITICAL ISSUES ({len(issues)})\n\n"

        if issues:
            for i, issue in enumerate(issues, 1):
                report += f"{i}. {issue}\n"
        else:
            report += "✅ No critical issues found\n"

        report += "\n---\n\n"

        # Recommendations
        recommendations = self.generate_recommendations()
        report += f"## RECOMMENDATIONS ({len(recommendations)})\n\n"

        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                report += f"{i}. {rec}\n"
        else:
            report += "✅ No recommendations - excellent quality\n"

        report += "\n---\n\n"

        # Final Verdict
        report += "## FINAL VERDICT\n\n"

        if overall_pass:
            report += "✅ **PASS** - HTML meets master blueprint requirements\n\n"
            report += "**Quality Level**: Production-ready\n"
        else:
            report += "❌ **FAIL** - HTML requires revision before approval\n\n"
            report += "**Required Actions**:\n"
            report += "1. Address all critical issues listed above\n"
            report += "2. Implement recommendations\n"
            report += "3. Re-run validation\n"
            report += "4. Target: 80/100 depth score + 90% specificity ratio\n"

        report += "\n---\n\n"
        report += f"**Validation completed**: {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"**Validator**: act1_validator.py v1.0\n"

        return report

    def save_report(self, report: str) -> str:
        """
        Save validation report to file.

        PARAMS:
            report (str): Formatted markdown report

        RETURNS:
            str: Path to saved report file
        """
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        filename = f"act1-validation-{date_str}.md"
        filepath = os.path.join(self.report_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)

        return filepath

    def print_summary(self):
        """Print concise summary to console"""
        depth = self.results['depth_score']
        specificity = self.results['specificity']
        issues = self.identify_critical_issues()

        content_passed = sum(1 for v in self.results['content_quality'].values() if v)
        structure_passed = sum(1 for v in self.results['structure_quality'].values() if v)
        writing_passed = sum(1 for v in self.results['writing_quality'].values() if v)
        expertise_passed = sum(1 for v in self.results['expertise_signals'].values() if v)

        print("\n" + "="*60)
        print("ACT 1 VALIDATION SUMMARY")
        print("="*60)
        print(f"\n📊 DEPTH SCORE: {depth['total']}/100 (target: 80+)")
        print(f"   - Data Specificity: {depth['data_specificity']}/20")
        print(f"   - Evidence Hierarchy: {depth['evidence_hierarchy']}/20")
        print(f"   - Customer Translation: {depth['customer_translation']}/20")
        print(f"   - Structural Integrity: {depth['structural_integrity']}/20")
        print(f"   - Expertise Demonstration: {depth['expertise_demonstration']}/20")

        print(f"\n📈 SPECIFICITY RATIO: {specificity['ratio']:.1%} (target: 90%+)")
        print(f"   - Generic claims: {specificity['generic_count']}")
        print(f"   - Specific claims: {specificity['specific_count']}")

        print(f"\n✅ QUALITY CHECKS:")
        print(f"   - Content Quality: {content_passed}/7")
        print(f"   - Structure Quality: {structure_passed}/5")
        print(f"   - Writing Quality: {writing_passed}/5")
        print(f"   - Expertise Signals: {expertise_passed}/5")

        print(f"\n⚠️  CRITICAL ISSUES: {len(issues)}")
        if issues:
            for issue in issues[:3]:  # Show first 3
                print(f"   - {issue}")
            if len(issues) > 3:
                print(f"   ... and {len(issues) - 3} more (see report)")

        # Final verdict
        overall_pass = (
            depth['total'] >= 80 and
            specificity['ratio'] >= 0.80 and
            content_passed >= 5 and
            structure_passed >= 4
        )

        print("\n" + "="*60)
        if overall_pass:
            print("✅ PASS - HTML meets blueprint requirements")
        else:
            print("❌ FAIL - HTML requires revision")
        print("="*60 + "\n")

    def run_validation(self) -> bool:
        """
        Run complete validation workflow.

        WORKFLOW:
            1. Load files
            2. Run all validation checks
            3. Calculate scores
            4. Generate report
            5. Save report
            6. Print summary

        RETURNS:
            bool: True if validation passed, False otherwise
        """
        print("\n🔍 ACT 1 VALIDATOR - Starting validation...\n")

        # Load files
        if not self.load_files():
            return False

        print("\n📋 Running quality checks...")

        # Run validations
        self.validate_content_quality()
        print("   ✓ Content quality checks complete")

        self.validate_structure_quality()
        print("   ✓ Structure quality checks complete")

        self.validate_writing_quality()
        print("   ✓ Writing quality checks complete")

        self.validate_expertise_signals()
        print("   ✓ Expertise signals checks complete")

        self.check_specificity_standard()
        print("   ✓ Specificity standard checks complete")

        self.calculate_depth_score()
        print("   ✓ Depth score calculation complete")

        # Generate and save report
        print("\n📝 Generating validation report...")
        report = self.generate_report()
        report_path = self.save_report(report)
        print(f"   ✓ Report saved: {report_path}")

        # Print summary
        self.print_summary()

        # Determine pass/fail
        depth = self.results['depth_score']
        specificity = self.results['specificity']
        content_passed = sum(1 for v in self.results['content_quality'].values() if v)
        structure_passed = sum(1 for v in self.results['structure_quality'].values() if v)

        return (
            depth['total'] >= 80 and
            specificity['ratio'] >= 0.80 and
            content_passed >= 5 and
            structure_passed >= 4
        )


def main():
    """
    Main execution function.

    HOW TO USE:
        python3 validators/act1_validator.py
    """
    validator = Act1Validator()
    passed = validator.run_validation()

    # Exit code: 0 if passed, 1 if failed
    exit(0 if passed else 1)


if __name__ == "__main__":
    main()
