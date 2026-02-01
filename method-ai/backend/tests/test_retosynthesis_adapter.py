"""Tests for retrosynthesis adapter service.

Note: These tests only test the fallback path unless RXN_API_KEY is set.
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from app.services.retrosynthesis_adapter import (
    _get_placeholder_plan,
    _normalize_rxn_response,
    get_retrosynthesis_plan,
    is_rxn_configured,
)


class TestGetPlaceholderPlan:
    """Tests for placeholder plan generation."""

    def test_placeholder_plan_structure(self):
        """Test that placeholder plan has correct structure."""
        smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"
        plan = _get_placeholder_plan(smiles)

        assert "source" in plan
        assert "target_smiles" in plan
        assert "steps" in plan

    def test_placeholder_plan_source(self):
        """Test that placeholder plan has correct source."""
        plan = _get_placeholder_plan("CCO")
        assert plan["source"] == "placeholder"

    def test_placeholder_plan_preserves_smiles(self):
        """Test that placeholder plan preserves target SMILES."""
        smiles = "C1=CC=CC=C1"
        plan = _get_placeholder_plan(smiles)
        assert plan["target_smiles"] == smiles

    def test_placeholder_plan_empty_steps(self):
        """Test that placeholder plan has empty steps."""
        plan = _get_placeholder_plan("CCO")
        assert plan["steps"] == []


class TestNormalizeRxnResponse:
    """Tests for RXN response normalization."""

    def test_normalize_empty_response(self):
        """Test normalization of empty RXN response."""
        result = _normalize_rxn_response("CCO", {})

        assert result["source"] == "ibm_rxn"
        assert result["target_smiles"] == "CCO"
        assert result["steps"] == []

    def test_normalize_with_paths(self):
        """Test normalization with retrosynthetic paths."""
        rxn_response = {
            "retrosynthetic_paths": [
                {
                    "reactions": [
                        {"rxn_smiles": "A>>B", "confidence": 0.9},
                        {"rxn_smiles": "B>>C", "confidence": 0.8},
                    ]
                }
            ]
        }

        result = _normalize_rxn_response("CCO", rxn_response)

        assert result["source"] == "ibm_rxn"
        assert len(result["steps"]) == 2
        assert result["steps"][0]["rxn_smiles"] == "A>>B"
        assert result["steps"][0]["confidence"] == 0.9

    def test_normalize_with_empty_paths(self):
        """Test normalization with empty paths list."""
        rxn_response = {"retrosynthetic_paths": []}

        result = _normalize_rxn_response("CCO", rxn_response)

        assert result["steps"] == []


class TestGetRetrosynthesisPlan:
    """Tests for get_retrosynthesis_plan function."""

    @patch("app.services.retrosynthesis_adapter.settings")
    def test_uses_placeholder_when_no_api_key(self, mock_settings):
        """Test that placeholder is used when API key not set."""
        mock_settings.rxn_api_key = None

        plan = get_retrosynthesis_plan("CCO")

        assert plan["source"] == "placeholder"

    @patch("app.services.retrosynthesis_adapter.settings")
    def test_returns_valid_structure_without_api_key(self, mock_settings):
        """Test that valid structure is returned without API key."""
        mock_settings.rxn_api_key = None

        plan = get_retrosynthesis_plan("C1=CC=CC=C1")

        assert "source" in plan
        assert "target_smiles" in plan
        assert "steps" in plan
        assert isinstance(plan["steps"], list)

    @patch("app.services.retrosynthesis_adapter._get_rxn_plan")
    @patch("app.services.retrosynthesis_adapter.settings")
    def test_falls_back_on_rxn_error(self, mock_settings, mock_get_rxn):
        """Test fallback to placeholder when RXN call fails."""
        mock_settings.rxn_api_key = "test-key"
        mock_get_rxn.side_effect = Exception("API Error")

        plan = get_retrosynthesis_plan("CCO")

        assert plan["source"] == "placeholder"

    @patch("app.services.retrosynthesis_adapter._get_rxn_plan")
    @patch("app.services.retrosynthesis_adapter.settings")
    def test_uses_rxn_when_configured(self, mock_settings, mock_get_rxn):
        """Test that RXN is used when API key is set."""
        mock_settings.rxn_api_key = "test-key"
        mock_get_rxn.return_value = {
            "source": "ibm_rxn",
            "target_smiles": "CCO",
            "steps": [],
        }

        plan = get_retrosynthesis_plan("CCO")

        assert plan["source"] == "ibm_rxn"
        mock_get_rxn.assert_called_once_with("CCO")


class TestIsRxnConfigured:
    """Tests for is_rxn_configured function."""

    @patch("app.services.retrosynthesis_adapter.settings")
    def test_returns_false_when_no_key(self, mock_settings):
        """Test returns False when API key not set."""
        mock_settings.rxn_api_key = None
        assert is_rxn_configured() is False

    @patch("app.services.retrosynthesis_adapter.settings")
    def test_returns_true_when_key_set(self, mock_settings):
        """Test returns True when API key is set."""
        mock_settings.rxn_api_key = "test-key"
        assert is_rxn_configured() is True


class TestRxnIntegration:
    """Integration tests for RXN (only run when API key is set)."""

    @pytest.mark.skipif(
        not os.getenv("RXN_API_KEY"),
        reason="RXN_API_KEY not set - skipping integration tests",
    )
    def test_real_rxn_call(self):
        """Test real RXN API call (requires API key)."""
        # This test only runs when RXN_API_KEY is set in environment
        plan = get_retrosynthesis_plan("CCO")

        assert plan["source"] == "ibm_rxn"
        assert "target_smiles" in plan
        assert "steps" in plan
