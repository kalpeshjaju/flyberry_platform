"""
Hallucination Guard - Runtime Anti-Hallucination System

PURPOSE: Enforce 3-checkpoint verification protocol during content generation
CONTEXT: Prevents fabricated data by requiring explicit data verification
DEPENDENCIES: data_integration.py, reference_data_validator.py

INTEGRATION: Called by build.py before each Act generation

AUTHOR: Claude Code
LAST UPDATED: 2025-10-28
"""

import json
import os
from typing import Dict, List, Tuple, Any
from datetime import datetime


class HallucinationGuard:
    """
    3-Checkpoint verification system to prevent hallucinations.

    WHY: Ensure all generated content is grounded in verifiable data
    HOW: CHECKPOINT 1 (verify data) → CHECKPOINT 2 (cite sources) → CHECKPOINT 3 (audit output)

    CHECKPOINTS:
    1. BEFORE: Verify data availability, show sources, state confidence
    2. DURING: Enforce citation of sources for all claims
    3. AFTER: Audit generated content for unsourced claims
    """

    def __init__(self, data_integration, data_dir: str):
        """
        Initialize guard with data integration instance.

        @param data_integration: FlyberryData instance
        @param data_dir: Path to extracted_data directory
        """
        self.data = data_integration
        self.data_dir = data_dir
        self.checkpoint1_passed = False
        self.checkpoint2_enabled = False
        self.checkpoint3_log = []

    def checkpoint1_verify_data(self, act_name: str, required_data: List[str]) -> Dict[str, Any]:
        """
        CHECKPOINT 1: Verify data availability BEFORE generation.

        WHY: Prevent hallucinations by confirming data exists
        HOW: Check all required data fields, report availability, state confidence

        @param act_name: Name of Act being generated (e.g., "Act 3: Discoveries")
        @param required_data: List of required data categories (e.g., ["products", "testimonials"])
        @returns: Verification report dictionary

        EXAMPLE:
        ```python
        report = guard.checkpoint1_verify_data("Act 1", ["products", "recipes", "brand"])
        if not report["can_proceed"]:
            raise ValueError(f"Missing data: {report['missing_data']}")
        ```
        """
        print(f"\n{'='*80}")
        print(f"CHECKPOINT 1: DATA VERIFICATION (BEFORE {act_name})")
        print(f"{'='*80}\n")

        report = {
            "act": act_name,
            "timestamp": datetime.now().isoformat(),
            "required_data": required_data,
            "available_data": {},
            "missing_data": [],
            "data_sources": [],
            "confidence_score": 0.0,
            "can_proceed": False,
            "warnings": []
        }

        # Check each required data category
        for category in required_data:
            availability = self._check_data_availability(category)
            report["available_data"][category] = availability

            if not availability["exists"]:
                report["missing_data"].append(category)
            else:
                report["data_sources"].extend(availability["sources"])

        # Calculate confidence score
        available_count = len([v for v in report["available_data"].values() if v["exists"]])
        total_count = len(required_data)
        report["confidence_score"] = available_count / total_count if total_count > 0 else 0.0

        # Determine if we can proceed
        if len(report["missing_data"]) == 0:
            report["can_proceed"] = True
        elif len(report["missing_data"]) <= len(required_data) * 0.3:  # Allow up to 30% missing
            report["can_proceed"] = True
            report["warnings"].append(
                f"⚠️  Proceeding with {len(report['missing_data'])} missing data categories - "
                "generated content will have gaps"
            )
        else:
            report["can_proceed"] = False
            report["warnings"].append(
                f"🔴 BLOCKED: Too much missing data ({len(report['missing_data'])}/{total_count}) - "
                "cannot generate quality content"
            )

        # Print report
        self._print_checkpoint1_report(report)

        # Update state
        self.checkpoint1_passed = report["can_proceed"]
        self.checkpoint2_enabled = report["can_proceed"]

        return report

    def _check_data_availability(self, category: str) -> Dict[str, Any]:
        """
        Check if data exists for a specific category.

        @param category: Data category to check
        @returns: Availability dictionary
        """
        availability = {
            "category": category,
            "exists": False,
            "count": 0,
            "sources": [],
            "completeness": 0.0
        }

        # Check different data categories
        if category == "products":
            if hasattr(self.data, 'products') and self.data.products:
                availability["exists"] = True
                availability["count"] = len(self.data.products)
                availability["sources"].append(f"extracted_data/products/*.json ({availability['count']} files)")
                availability["completeness"] = 1.0

        elif category == "recipes":
            if hasattr(self.data, 'recipes') and self.data.recipes:
                availability["exists"] = True
                availability["count"] = len(self.data.recipes)
                availability["sources"].append(f"extracted_data/recipes/*.json ({availability['count']} files)")
                availability["completeness"] = 1.0

        elif category == "claims":
            if hasattr(self.data, 'claims_registry') and self.data.claims_registry:
                availability["exists"] = True
                availability["count"] = len(self.data.claims_registry.get("claims", []))
                availability["sources"].append(f"extracted_data/claims-registry.json ({availability['count']} claims)")
                availability["completeness"] = 1.0

        elif category == "design":
            if hasattr(self.data, 'brand_design') and self.data.brand_design:
                availability["exists"] = True
                availability["count"] = 1
                availability["sources"].append("extracted_data/design/brand-design-system.json")
                availability["completeness"] = 1.0

        elif category == "testimonials":
            # Check reference data
            testimonials_file = os.path.join(self.data_dir, "customer-testimonials-reference.json")
            if os.path.exists(testimonials_file):
                with open(testimonials_file, 'r') as f:
                    data = json.load(f)
                    if data.get("metadata", {}).get("confidence") in ["high", "medium"]:
                        availability["exists"] = True
                        availability["sources"].append("customer-testimonials-reference.json")
                        availability["completeness"] = 0.7 if data["metadata"]["confidence"] == "medium" else 1.0
            else:
                availability["exists"] = False
                availability["sources"].append("⚠️  customer-testimonials-reference.json (MISSING)")

        elif category == "market_trends":
            trends_file = os.path.join(self.data_dir, "market-trends-reference.json")
            if os.path.exists(trends_file):
                with open(trends_file, 'r') as f:
                    data = json.load(f)
                    if data.get("metadata", {}).get("confidence") in ["high", "medium"]:
                        availability["exists"] = True
                        availability["sources"].append("market-trends-reference.json")
                        availability["completeness"] = 0.7 if data["metadata"]["confidence"] == "medium" else 1.0
            else:
                availability["exists"] = False

        elif category == "market_size":
            size_file = os.path.join(self.data_dir, "market-size-reference.json")
            if os.path.exists(size_file):
                with open(size_file, 'r') as f:
                    data = json.load(f)
                    if data.get("metadata", {}).get("confidence") in ["high", "medium"]:
                        availability["exists"] = True
                        availability["sources"].append("market-size-reference.json")
                        availability["completeness"] = 0.7 if data["metadata"]["confidence"] == "medium" else 1.0

        elif category == "competitors":
            comp_file = os.path.join(self.data_dir, "competitors-reference.json")
            if os.path.exists(comp_file):
                with open(comp_file, 'r') as f:
                    data = json.load(f)
                    if data.get("metadata", {}).get("confidence") in ["high", "medium"]:
                        availability["exists"] = True
                        availability["sources"].append("competitors-reference.json")
                        availability["completeness"] = 0.7 if data["metadata"]["confidence"] == "medium" else 1.0

        return availability

    def _print_checkpoint1_report(self, report: Dict):
        """
        Print human-readable Checkpoint 1 report.

        @param report: Verification report dictionary
        """
        print("📂 DATA SOURCES FOUND:")
        for source in report["data_sources"]:
            print(f"   ✅ {source}")

        if not report["data_sources"]:
            print("   ⚠️  No data sources found")

        print(f"\n📊 DATA AVAILABILITY: {len(report['available_data'])} categories checked")
        for category, availability in report["available_data"].items():
            status = "✅" if availability["exists"] else "❌"
            count_str = f"({availability['count']} items)" if availability["count"] > 0 else ""
            completeness_str = f"{availability['completeness']*100:.0f}% complete" if availability["exists"] else ""
            print(f"   {status} {category}: {count_str} {completeness_str}")

        if report["missing_data"]:
            print(f"\n❌ MISSING DATA ({len(report['missing_data'])} categories):")
            for missing in report["missing_data"]:
                print(f"   ⚠️  {missing} - Content will have gaps or use fallback data")

        print(f"\n🎯 CONFIDENCE SCORE: {report['confidence_score']:.0%}")
        print(f"   Reason: {len(report['available_data']) - len(report['missing_data'])}/{len(report['available_data'])} data categories available")

        if report["warnings"]:
            print(f"\n⚠️  WARNINGS:")
            for warning in report["warnings"]:
                print(f"   {warning}")

        if report["can_proceed"]:
            print(f"\n✅ CAN PROCEED: Sufficient data available for generation")
        else:
            print(f"\n🔴 CANNOT PROCEED: Insufficient data - fix missing data before generation")

        print(f"\n{'='*80}\n")

    def checkpoint2_citation_enforcer(self) -> str:
        """
        CHECKPOINT 2: Enforce citations during generation.

        WHY: Ensure all claims are sourced
        HOW: Return citation template for generators to use

        @returns: Citation template string
        """
        if not self.checkpoint1_passed:
            raise ValueError("Cannot enable Checkpoint 2 - Checkpoint 1 not passed")

        citation_template = """
        CITATION REQUIREMENTS:
        ----------------------
        For EVERY claim, fact, or data point, you MUST cite the source:

        ✅ GOOD:
        "Medjoul dates are known as the 'king of dates' (Source: medjoul-dates.json:description)"
        "67% of consumers prefer makhanas and dry fruits (Source: market-trends-reference.json:consumerData)"

        ❌ BAD:
        "Medjoul dates are popular" [No source]
        "Most customers love our products" [Vague, no data]

        MANDATORY CITATION FORMAT:
        - Product data: (Source: {product-name}.json:{field})
        - Market data: (Source: {reference-file}.json:{section})
        - Claims: (Source: claims-registry.json:claim_{id})

        IF DATA NOT AVAILABLE:
        - State explicitly: "Data not available"
        - DO NOT guess or infer
        - DO NOT use placeholder text like "research shows" without source
        """

        return citation_template

    def checkpoint3_audit_output(self, generated_content: str, act_name: str) -> Dict[str, Any]:
        """
        CHECKPOINT 3: Audit generated content for unsourced claims.

        WHY: Catch any hallucinations that slipped through
        HOW: Scan for claims without citations, flag suspicious patterns

        @param generated_content: The generated HTML or markdown content
        @param act_name: Name of Act that was generated
        @returns: Audit report dictionary

        EDGE CASES:
        - Content has valid citations → pass
        - Content has unsourced claims → fail with details
        - Content uses placeholder text → fail
        """
        print(f"\n{'='*80}")
        print(f"CHECKPOINT 3: OUTPUT AUDIT (AFTER {act_name})")
        print(f"{'='*80}\n")

        audit = {
            "act": act_name,
            "timestamp": datetime.now().isoformat(),
            "content_length": len(generated_content),
            "issues": [],
            "warnings": [],
            "citation_count": 0,
            "unsourced_claims_detected": 0,
            "passed": False
        }

        # Count citations
        citation_patterns = ["(Source:", "Source:", "According to"]
        for pattern in citation_patterns:
            audit["citation_count"] += generated_content.count(pattern)

        # Detect placeholder/hallucination indicators
        hallucination_indicators = [
            ("Based on industry reports", "Generic claim without specific source"),
            ("Studies show", "Vague research reference"),
            ("Research indicates", "Unspecified research"),
            ("Experts say", "Undefined experts"),
            ("[To be added]", "Placeholder text"),
            ("[TBD]", "Placeholder text"),
            ("PLACEHOLDER", "Placeholder text"),
        ]

        for indicator, reason in hallucination_indicators:
            if indicator in generated_content:
                audit["issues"].append({
                    "type": "UNSOURCED_CLAIM",
                    "indicator": indicator,
                    "reason": reason
                })
                audit["unsourced_claims_detected"] += 1

        # Check citation density (should have citations for data-heavy content)
        words = len(generated_content.split())
        if words > 500:  # Substantial content
            expected_citations = words // 200  # Rough heuristic: 1 citation per 200 words
            if audit["citation_count"] < expected_citations:
                audit["warnings"].append(
                    f"Low citation density: {audit['citation_count']} citations for {words} words "
                    f"(expected ~{expected_citations})"
                )

        # Determine if audit passed
        audit["passed"] = audit["unsourced_claims_detected"] == 0

        # Print audit report
        self._print_checkpoint3_report(audit)

        # Store for logging
        self.checkpoint3_log.append(audit)

        return audit

    def _print_checkpoint3_report(self, audit: Dict):
        """
        Print human-readable Checkpoint 3 audit report.

        @param audit: Audit report dictionary
        """
        print(f"📄 CONTENT LENGTH: {audit['content_length']} characters")
        print(f"📌 CITATIONS FOUND: {audit['citation_count']}")

        if audit["issues"]:
            print(f"\n🔴 ISSUES DETECTED ({len(audit['issues'])}):")
            for issue in audit["issues"]:
                print(f"   ⚠️  {issue['type']}: '{issue['indicator']}' - {issue['reason']}")

        if audit["warnings"]:
            print(f"\n⚠️  WARNINGS ({len(audit['warnings'])}):")
            for warning in audit["warnings"]:
                print(f"   {warning}")

        if audit["passed"]:
            print(f"\n✅ AUDIT PASSED: No hallucinations detected")
        else:
            print(f"\n🔴 AUDIT FAILED: {audit['unsourced_claims_detected']} unsourced claims detected")
            print(f"   → Review and add proper citations for all claims")

        print(f"\n{'='*80}\n")

    def generate_full_report(self) -> str:
        """
        Generate comprehensive report of all 3 checkpoints.

        @returns: Formatted report string
        """
        lines = []
        lines.append("="*80)
        lines.append("HALLUCINATION GUARD - FULL SESSION REPORT")
        lines.append("="*80)
        lines.append(f"Generated: {datetime.now().isoformat()}")
        lines.append("")

        lines.append("CHECKPOINT 1: Data Verification")
        if self.checkpoint1_passed:
            lines.append("  ✅ PASSED - Sufficient data available")
        else:
            lines.append("  ❌ FAILED - Insufficient data")

        lines.append("\nCHECKPOINT 2: Citation Enforcement")
        if self.checkpoint2_enabled:
            lines.append("  ✅ ENABLED - Citation template provided to generators")
        else:
            lines.append("  ❌ DISABLED - Checkpoint 1 not passed")

        lines.append(f"\nCHECKPOINT 3: Output Audits ({len(self.checkpoint3_log)} audits)")
        for audit in self.checkpoint3_log:
            status = "✅ PASSED" if audit["passed"] else "🔴 FAILED"
            lines.append(f"  {status} - {audit['act']}: {audit['citation_count']} citations, "
                        f"{audit['unsourced_claims_detected']} issues")

        lines.append("\n" + "="*80)
        return "\n".join(lines)


if __name__ == "__main__":
    """
    Test the hallucination guard.

    USAGE:
      python3 validators/hallucination_guard.py
    """
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'flyberry_oct_restart'))

    try:
        from flyberry_data_loader import FlyberryData
    except ImportError:
        print("❌ ERROR: Cannot import flyberry_data_loader.py")
        print("   Make sure flyberry_oct_restart is accessible")
        sys.exit(1)

    # Initialize
    data = FlyberryData()
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'flyberry_oct_restart', 'extracted_data')
    guard = HallucinationGuard(data, data_dir)

    # Test Checkpoint 1
    print("\n🧪 TESTING CHECKPOINT 1: Data Verification\n")
    report1 = guard.checkpoint1_verify_data(
        "Test Act",
        ["products", "recipes", "claims", "design", "testimonials", "market_trends"]
    )

    if report1["can_proceed"]:
        # Test Checkpoint 2
        print("\n🧪 TESTING CHECKPOINT 2: Citation Enforcer\n")
        citation_template = guard.checkpoint2_citation_enforcer()
        print(citation_template)

        # Test Checkpoint 3
        print("\n🧪 TESTING CHECKPOINT 3: Output Audit\n")
        sample_content = """
        Medjoul dates are known as the king of dates (Source: medjoul-dates.json:tagline).
        Our products are sourced from premium origins (Source: products/*.json:origin).
        Studies show that customers love dates. [This is hallucinated - no source]
        """
        audit = guard.checkpoint3_audit_output(sample_content, "Test Act")

    # Generate full report
    print(guard.generate_full_report())
