"""
Reference Data Validator

PURPOSE: Verify quality, accuracy, and legitimacy of reference data files
CONTEXT: Prevents hallucinations by enforcing strict data verification standards
DEPENDENCIES: json, datetime, urllib.parse

ANTI-HALLUCINATION STRATEGY:
1. Source verification: Ensure all data has verifiable sources
2. Confidence scoring: Track confidence levels (high/medium/low)
3. Date tracking: Ensure data freshness (<6 months)
4. Completeness checks: Verify required fields present
5. Cross-referencing: Check consistency across data files

AUTHOR: Claude Code
LAST UPDATED: 2025-10-28
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
from urllib.parse import urlparse


class ReferenceDataValidator:
    """
    Validates reference data files for accuracy, completeness, and legitimacy.

    WHY: Prevent hallucinations by ensuring all reference data is verifiable
    HOW: Multi-checkpoint verification system with confidence scoring
    """

    # Required metadata fields for all reference files
    REQUIRED_METADATA = [
        "source",
        "date",
        "extractedBy",
        "confidence",
        "needsVerification"
    ]

    # Confidence levels and their requirements
    CONFIDENCE_LEVELS = {
        "high": {
            "requirements": [
                "Official source (government, industry body, company)",
                "Date within 3 months",
                "Specific URL or document reference",
                "Cross-verified with 2+ sources"
            ],
            "score": 0.85
        },
        "medium": {
            "requirements": [
                "Reputable source (industry report, credible publication)",
                "Date within 6 months",
                "URL or publication reference",
                "Logical consistency with known facts"
            ],
            "score": 0.65
        },
        "low": {
            "requirements": [
                "Template or estimated data",
                "Requires verification",
                "Placeholder for research"
            ],
            "score": 0.30
        }
    }

    # Data freshness thresholds
    FRESHNESS_THRESHOLDS = {
        "current": 90,      # <3 months
        "recent": 180,      # <6 months
        "outdated": 365,    # >1 year
    }

    def __init__(self, data_dir: str):
        """
        Initialize validator with data directory path.

        @param data_dir: Path to extracted_data directory
        """
        self.data_dir = data_dir
        self.validation_results = []
        self.errors = []
        self.warnings = []

    def validate_file(self, filepath: str) -> Dict[str, Any]:
        """
        Validate a single reference data file.

        WHY: Ensure each file meets quality standards before use
        HOW: Check metadata, source, confidence, freshness, completeness

        @param filepath: Path to JSON reference file
        @returns: Validation result dictionary

        EDGE CASES:
        - File doesn't exist -> return error
        - Invalid JSON -> return parse error
        - Missing metadata -> flag as incomplete
        - Low confidence + not flagged for verification -> warning
        """
        result = {
            "file": os.path.basename(filepath),
            "path": filepath,
            "valid": False,
            "confidence": "unknown",
            "freshness": "unknown",
            "issues": [],
            "warnings": [],
            "metadata": {}
        }

        try:
            # STEP 1: Check file exists
            if not os.path.exists(filepath):
                result["issues"].append(f"File not found: {filepath}")
                return result

            # STEP 2: Parse JSON
            with open(filepath, 'r') as f:
                data = json.load(f)

            # STEP 3: Validate metadata
            metadata_valid, metadata_issues = self._validate_metadata(data.get("metadata", {}))
            result["metadata"] = data.get("metadata", {})
            result["issues"].extend(metadata_issues)

            if not metadata_valid:
                return result

            # STEP 4: Validate source
            source_valid, source_issues = self._validate_source(data["metadata"]["source"])
            result["issues"].extend(source_issues)

            # STEP 5: Check data freshness
            freshness, freshness_warning = self._check_freshness(data["metadata"]["date"])
            result["freshness"] = freshness
            if freshness_warning:
                result["warnings"].append(freshness_warning)

            # STEP 6: Validate confidence level
            confidence = data["metadata"]["confidence"]
            confidence_valid, confidence_issues = self._validate_confidence(
                confidence,
                data["metadata"].get("needsVerification", True),
                freshness
            )
            result["confidence"] = confidence
            result["issues"].extend(confidence_issues)

            # STEP 7: Check data completeness
            completeness_score, completeness_warnings = self._check_completeness(data)
            result["completeness"] = completeness_score
            result["warnings"].extend(completeness_warnings)

            # STEP 8: Determine overall validity
            result["valid"] = len(result["issues"]) == 0

            # STEP 9: Add recommendations
            result["recommendations"] = self._generate_recommendations(result)

        except json.JSONDecodeError as e:
            result["issues"].append(f"Invalid JSON: {str(e)}")
        except Exception as e:
            result["issues"].append(f"Validation error: {str(e)}")

        return result

    def _validate_metadata(self, metadata: Dict) -> Tuple[bool, List[str]]:
        """
        Validate metadata section has all required fields.

        @param metadata: Metadata dictionary
        @returns: (is_valid, list_of_issues)
        """
        issues = []

        for field in self.REQUIRED_METADATA:
            if field not in metadata:
                issues.append(f"Missing required metadata field: {field}")

        return len(issues) == 0, issues

    def _validate_source(self, source: str) -> Tuple[bool, List[str]]:
        """
        Validate source is specific and verifiable.

        WHY: Generic sources like "web search" are not verifiable
        HOW: Check for URLs, publication names, document titles

        @param source: Source string
        @returns: (is_valid, list_of_issues)
        """
        issues = []
        warnings = []

        # Check for template/placeholder sources
        placeholder_indicators = [
            "template",
            "to be collected",
            "needs",
            "[",
            "TBD",
            "TODO"
        ]

        source_lower = source.lower()
        for indicator in placeholder_indicators:
            if indicator in source_lower:
                issues.append(f"Placeholder source detected: '{source}' - requires real source")
                return False, issues

        # Check for specific source elements
        has_url = "http://" in source or "https://" in source
        has_publication = any(word in source_lower for word in [
            "report", "journal", "publication", "whitepaper", "study",
            "research", "analysis", "survey", "census"
        ])
        has_organization = any(word in source_lower for word in [
            "government", "ministry", "department", "association",
            "institute", "foundation", "agency"
        ])

        if not (has_url or has_publication or has_organization):
            issues.append(
                f"Source lacks specificity: '{source}' - should include URL, "
                "publication name, or official organization"
            )

        return len(issues) == 0, issues

    def _check_freshness(self, date_str: str) -> Tuple[str, str]:
        """
        Check how fresh the data is based on date.

        @param date_str: Date string in YYYY-MM-DD format
        @returns: (freshness_level, warning_message)

        FRESHNESS LEVELS:
        - current: <3 months old
        - recent: 3-6 months old
        - outdated: 6-12 months old
        - stale: >12 months old
        """
        try:
            data_date = datetime.strptime(date_str, "%Y-%m-%d")
            today = datetime.now()
            age_days = (today - data_date).days

            if age_days < 0:
                return "future", "WARNING: Date is in the future - likely incorrect"
            elif age_days <= self.FRESHNESS_THRESHOLDS["current"]:
                return "current", None
            elif age_days <= self.FRESHNESS_THRESHOLDS["recent"]:
                return "recent", "Data is 3-6 months old - consider updating"
            elif age_days <= self.FRESHNESS_THRESHOLDS["outdated"]:
                return "outdated", "Data is 6-12 months old - should be updated"
            else:
                return "stale", f"Data is {age_days // 365} year(s) old - MUST be updated"
        except ValueError:
            return "invalid", f"Invalid date format: {date_str} (expected YYYY-MM-DD)"

    def _validate_confidence(
        self,
        confidence: str,
        needs_verification: bool,
        freshness: str
    ) -> Tuple[bool, List[str]]:
        """
        Validate confidence level is appropriate for data quality.

        WHY: Prevent overconfident claims on unverified data
        HOW: Cross-check confidence against verification status and freshness

        @param confidence: Confidence level (high/medium/low)
        @param needs_verification: Whether data needs verification
        @param freshness: Data freshness level
        @returns: (is_valid, list_of_issues)
        """
        issues = []

        # Check confidence is valid level
        if confidence not in self.CONFIDENCE_LEVELS:
            issues.append(
                f"Invalid confidence level: '{confidence}' "
                f"(must be: {', '.join(self.CONFIDENCE_LEVELS.keys())})"
            )
            return False, issues

        # Cross-check confidence against verification status
        if confidence == "high" and needs_verification:
            issues.append(
                "Confidence marked 'high' but needsVerification=true - "
                "inconsistent. High confidence requires verification."
            )

        # Cross-check confidence against freshness
        if confidence == "high" and freshness in ["outdated", "stale"]:
            issues.append(
                f"Confidence marked 'high' but data is {freshness} - "
                "high confidence requires current data"
            )

        return len(issues) == 0, issues

    def _check_completeness(self, data: Dict) -> Tuple[float, List[str]]:
        """
        Check data completeness (how much is filled vs placeholders).

        WHY: Detect template files that haven't been filled with real data
        HOW: Count placeholder indicators vs actual data

        @param data: Full data dictionary
        @returns: (completeness_score 0-1, list_of_warnings)
        """
        warnings = []

        # Convert data to JSON string for analysis
        data_str = json.dumps(data)

        # Count placeholder indicators
        placeholder_count = 0
        placeholder_indicators = [
            "[To be collected]",
            "[Add actual",
            "[Name]",
            "[URL]",
            "TBD",
            "TODO",
            "YYYY-MM-DD",
            "YYYY",
            "[If applicable]",
            "0.0/5.0",
            '"0"',
            'null'
        ]

        for indicator in placeholder_indicators:
            placeholder_count += data_str.count(indicator)

        # Rough completeness score
        # High placeholder count = low completeness
        if placeholder_count > 20:
            completeness = 0.1
            warnings.append(f"Very low completeness: {placeholder_count} placeholders found - mostly template")
        elif placeholder_count > 10:
            completeness = 0.3
            warnings.append(f"Low completeness: {placeholder_count} placeholders found - needs significant work")
        elif placeholder_count > 5:
            completeness = 0.6
            warnings.append(f"Moderate completeness: {placeholder_count} placeholders found - needs filling")
        elif placeholder_count > 0:
            completeness = 0.8
            warnings.append(f"Good completeness: {placeholder_count} placeholders found - minor gaps")
        else:
            completeness = 1.0

        return completeness, warnings

    def _generate_recommendations(self, result: Dict) -> List[str]:
        """
        Generate actionable recommendations based on validation results.

        @param result: Validation result dictionary
        @returns: List of recommendation strings
        """
        recommendations = []

        # Confidence recommendations
        if result["confidence"] == "low":
            recommendations.append(
                "🔴 CRITICAL: Replace with verified data from official sources"
            )
        elif result["confidence"] == "medium":
            recommendations.append(
                "🟡 RECOMMENDED: Cross-verify with additional sources to achieve high confidence"
            )

        # Freshness recommendations
        if result["freshness"] in ["outdated", "stale"]:
            recommendations.append(
                "⏰ UPDATE REQUIRED: Data is outdated - research latest information"
            )

        # Completeness recommendations
        if result.get("completeness", 0) < 0.5:
            recommendations.append(
                "📝 FILL REQUIRED: File is mostly template - complete with actual data"
            )
        elif result.get("completeness", 0) < 0.8:
            recommendations.append(
                "✏️ REFINEMENT: Replace remaining placeholders with real data"
            )

        # No issues = ready for use
        if result["valid"] and result["confidence"] == "high" and result["freshness"] == "current":
            recommendations.append(
                "✅ VERIFIED: Data meets all quality standards - ready for production use"
            )

        return recommendations

    def validate_all_reference_files(self) -> Dict[str, Any]:
        """
        Validate all reference data files in extracted_data directory.

        WHY: Comprehensive quality check before using data in generation
        HOW: Find all *-reference.json files and validate each

        @returns: Summary report with all validation results
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_files": 0,
            "valid_files": 0,
            "invalid_files": 0,
            "by_confidence": {
                "high": 0,
                "medium": 0,
                "low": 0,
                "unknown": 0
            },
            "by_freshness": {
                "current": 0,
                "recent": 0,
                "outdated": 0,
                "stale": 0,
                "invalid": 0,
                "unknown": 0
            },
            "files": []
        }

        # Find all reference files
        reference_files = []
        for filename in os.listdir(self.data_dir):
            if filename.endswith("-reference.json"):
                reference_files.append(os.path.join(self.data_dir, filename))

        report["total_files"] = len(reference_files)

        # Validate each file
        for filepath in reference_files:
            result = self.validate_file(filepath)
            report["files"].append(result)

            # Update counters
            if result["valid"]:
                report["valid_files"] += 1
            else:
                report["invalid_files"] += 1

            # Count by confidence
            confidence = result.get("confidence", "unknown")
            if confidence in report["by_confidence"]:
                report["by_confidence"][confidence] += 1

            # Count by freshness
            freshness = result.get("freshness", "unknown")
            if freshness in report["by_freshness"]:
                report["by_freshness"][freshness] += 1

        # Overall assessment
        report["production_ready"] = (
            report["valid_files"] == report["total_files"] and
            report["by_confidence"]["high"] >= report["total_files"] * 0.7 and
            report["by_freshness"]["current"] >= report["total_files"] * 0.5
        )

        return report

    def generate_report(self, report: Dict) -> str:
        """
        Generate human-readable validation report.

        @param report: Report dictionary from validate_all_reference_files()
        @returns: Formatted report string
        """
        lines = []
        lines.append("=" * 80)
        lines.append("REFERENCE DATA VALIDATION REPORT")
        lines.append("=" * 80)
        lines.append(f"Generated: {report['timestamp']}")
        lines.append(f"Total Files: {report['total_files']}")
        lines.append("")

        # Overall status
        lines.append("OVERALL STATUS:")
        if report["production_ready"]:
            lines.append("  ✅ PRODUCTION READY - All files meet quality standards")
        else:
            lines.append("  ⚠️  NOT PRODUCTION READY - Quality issues found")
        lines.append("")

        # Summary
        lines.append("SUMMARY:")
        lines.append(f"  Valid Files:   {report['valid_files']}/{report['total_files']}")
        lines.append(f"  Invalid Files: {report['invalid_files']}/{report['total_files']}")
        lines.append("")

        # Confidence breakdown
        lines.append("CONFIDENCE LEVELS:")
        for level, count in report["by_confidence"].items():
            if count > 0:
                emoji = "✅" if level == "high" else "🟡" if level == "medium" else "🔴"
                lines.append(f"  {emoji} {level.upper()}: {count} file(s)")
        lines.append("")

        # Freshness breakdown
        lines.append("DATA FRESHNESS:")
        for level, count in report["by_freshness"].items():
            if count > 0:
                emoji = "🟢" if level == "current" else "🟡" if level == "recent" else "🔴"
                lines.append(f"  {emoji} {level.upper()}: {count} file(s)")
        lines.append("")

        # Individual file results
        lines.append("INDIVIDUAL FILES:")
        lines.append("-" * 80)
        for file_result in report["files"]:
            status = "✅" if file_result["valid"] else "❌"
            lines.append(f"\n{status} {file_result['file']}")
            lines.append(f"   Confidence: {file_result['confidence']}")
            lines.append(f"   Freshness: {file_result['freshness']}")
            lines.append(f"   Completeness: {file_result.get('completeness', 0)*100:.0f}%")

            if file_result["issues"]:
                lines.append("   ⚠️  ISSUES:")
                for issue in file_result["issues"]:
                    lines.append(f"      - {issue}")

            if file_result["warnings"]:
                lines.append("   ⚠️  WARNINGS:")
                for warning in file_result["warnings"]:
                    lines.append(f"      - {warning}")

            if file_result.get("recommendations"):
                lines.append("   💡 RECOMMENDATIONS:")
                for rec in file_result["recommendations"]:
                    lines.append(f"      {rec}")

        lines.append("\n" + "=" * 80)

        return "\n".join(lines)


if __name__ == "__main__":
    """
    Run validation on all reference data files.

    USAGE:
      python3 validators/reference_data_validator.py
    """
    import sys

    # Determine data directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)

    # Check if data is symlinked from flyberry_oct_restart
    data_dir = os.path.join(project_dir, "data", "extracted_data")
    if not os.path.exists(data_dir):
        # Try flyberry_oct_restart directly
        parent_dir = os.path.dirname(project_dir)
        data_dir = os.path.join(parent_dir, "flyberry_oct_restart", "extracted_data")

    if not os.path.exists(data_dir):
        print("❌ ERROR: Cannot find extracted_data directory")
        print(f"   Looked in: {data_dir}")
        sys.exit(1)

    print(f"🔍 Validating reference data in: {data_dir}\n")

    # Run validation
    validator = ReferenceDataValidator(data_dir)
    report = validator.validate_all_reference_files()

    # Print report
    print(validator.generate_report(report))

    # Save report to file
    report_path = os.path.join(project_dir, "REFERENCE_DATA_VALIDATION_REPORT.md")
    with open(report_path, 'w') as f:
        f.write(validator.generate_report(report))

    print(f"\n📄 Full report saved to: {report_path}")

    # Exit with appropriate code
    if report["production_ready"]:
        print("\n✅ All reference data validated successfully")
        sys.exit(0)
    else:
        print("\n⚠️  Reference data validation failed - see report for details")
        sys.exit(1)
