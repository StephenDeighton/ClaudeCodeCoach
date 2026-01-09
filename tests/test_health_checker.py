"""
Tests for the health checker service.

Example tests demonstrating C3 testing patterns.
"""

import pytest
from pathlib import Path
from health_checks.base import Severity, HealthIssue
from health_checks.critical.no_gitignore import NoGitignoreDetector


class TestHealthDetectors:
    """Test health check detectors."""

    def test_no_gitignore_detector_finds_missing_gitignore(self, temp_project_dir, mock_config):
        """Test that NoGitignoreDetector detects missing .gitignore."""
        # Setup: temp_project_dir has no .gitignore
        detector = NoGitignoreDetector()

        # Execute
        result = detector.check(temp_project_dir, mock_config)

        # Assert
        assert result is not None
        assert result.severity == Severity.CRITICAL
        assert result.rule_id == "no-gitignore"
        assert ".gitignore" in result.message

    def test_no_gitignore_detector_passes_with_gitignore(self, temp_project_dir, mock_config):
        """Test that NoGitignoreDetector passes when .gitignore exists."""
        # Setup: create .gitignore
        (temp_project_dir / ".gitignore").write_text("*.pyc\n")
        detector = NoGitignoreDetector()

        # Execute
        result = detector.check(temp_project_dir, mock_config)

        # Assert
        assert result is None  # No issue detected

    def test_health_issue_has_fix_prompt(self):
        """Test that HealthIssue can contain fix prompts."""
        issue = HealthIssue(
            rule_id="test-rule",
            severity=Severity.WARNING,
            title="Test Issue",
            message="This is a test",
            suggestion="Fix it",
            fix_prompt="Step 1: Do this\nStep 2: Do that"
        )

        assert issue.fix_prompt is not None
        assert "Step 1" in issue.fix_prompt
        assert "Step 2" in issue.fix_prompt


class TestHealthCheckerService:
    """Test the health checker service orchestration."""

    def test_health_checker_discovers_detectors(self):
        """Test that health checker can discover registered detectors."""
        from health_checks.registry import get_all_detectors

        detectors = get_all_detectors()

        # Should have all 22 detectors registered
        assert len(detectors) >= 22

        # Should include our critical detectors
        rule_ids = [d.rule_id for d in detectors]
        assert "no-gitignore" in rule_ids
        assert "secrets-exposed" in rule_ids

    def test_detectors_have_fix_prompts(self):
        """Test that all detectors have fix prompts."""
        from health_checks.registry import get_all_detectors

        detectors = get_all_detectors()

        for detector in detectors:
            assert hasattr(detector, 'fix_prompt'), f"{detector.rule_id} missing fix_prompt"
            assert detector.fix_prompt is not None, f"{detector.rule_id} has None fix_prompt"
            assert len(detector.fix_prompt) > 0, f"{detector.rule_id} has empty fix_prompt"


# Example of how to run specific tests:
# pytest tests/test_health_checker.py::TestHealthDetectors::test_no_gitignore_detector_finds_missing_gitignore
# pytest tests/test_health_checker.py -v
# pytest tests/ -k "gitignore"
