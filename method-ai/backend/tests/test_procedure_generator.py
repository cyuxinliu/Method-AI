"""Tests for procedure generator service."""

import pytest

from app.models.schemas import ExperienceLevel, LabContext
from app.services.procedure_generator import generate_procedure


@pytest.fixture
def sample_lab_context() -> LabContext:
    """Create a sample lab context for testing."""
    return LabContext(
        scale_mg=500,
        equipment=["rotovap", "heating_mantle", "magnetic_stirrer"],
        purification_methods=["recrystallization", "filtration"],
        safety_constraints=["no_open_flame"],
        experience_level=ExperienceLevel.GRAD,
        time_budget_hours=8,
    )


@pytest.fixture
def placeholder_plan() -> dict:
    """Create a placeholder retrosynthesis plan."""
    return {
        "source": "placeholder",
        "target_smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "steps": [],
    }


@pytest.fixture
def rxn_plan() -> dict:
    """Create an RXN-sourced retrosynthesis plan."""
    return {
        "source": "ibm_rxn",
        "target_smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "steps": [
            {
                "rxn_smiles": "CC(=O)OC1=CC=CC=C1C(=O)O>>OC1=CC=CC=C1C(=O)O.CC(=O)Cl",
                "confidence": 0.95,
                "notes": "Step 1",
            }
        ],
    }


class TestGenerateProcedure:
    """Tests for generate_procedure function."""

    def test_generates_procedure_from_placeholder(
        self, placeholder_plan: dict, sample_lab_context: LabContext
    ):
        """Test that procedure is generated from placeholder plan."""
        procedure = generate_procedure(
            plan=placeholder_plan,
            lab_context=sample_lab_context,
        )

        assert len(procedure) >= 6
        assert len(procedure) <= 10
        assert procedure[0].step_number == 1
        assert all(step.action for step in procedure)

    def test_generates_procedure_from_rxn_plan(
        self, rxn_plan: dict, sample_lab_context: LabContext
    ):
        """Test that procedure is generated from RXN plan."""
        procedure = generate_procedure(
            plan=rxn_plan,
            lab_context=sample_lab_context,
        )

        assert len(procedure) >= 6
        # Check that RXN source is noted in rationale
        first_step = procedure[0]
        assert "IBM RXN" in (first_step.rationale or "")

    def test_procedure_has_workup_step(
        self, placeholder_plan: dict, sample_lab_context: LabContext
    ):
        """Test that procedure includes workup step."""
        procedure = generate_procedure(
            plan=placeholder_plan,
            lab_context=sample_lab_context,
        )

        actions = [step.action.lower() for step in procedure]
        has_workup = any("workup" in action for action in actions)
        assert has_workup

    def test_procedure_has_purification_step(
        self, placeholder_plan: dict, sample_lab_context: LabContext
    ):
        """Test that procedure includes purification step."""
        procedure = generate_procedure(
            plan=placeholder_plan,
            lab_context=sample_lab_context,
        )

        actions = [step.action.lower() for step in procedure]
        has_purification = any("purif" in action for action in actions)
        assert has_purification

    def test_procedure_step_numbers_sequential(
        self, placeholder_plan: dict, sample_lab_context: LabContext
    ):
        """Test that step numbers are sequential."""
        procedure = generate_procedure(
            plan=placeholder_plan,
            lab_context=sample_lab_context,
        )

        for i, step in enumerate(procedure, start=1):
            assert step.step_number == i

    def test_procedure_respects_equipment_list(
        self, placeholder_plan: dict, sample_lab_context: LabContext
    ):
        """Test that equipment from lab context is referenced."""
        procedure = generate_procedure(
            plan=placeholder_plan,
            lab_context=sample_lab_context,
        )

        # Find the equipment setup step
        equipment_step = None
        for step in procedure:
            if "apparatus" in step.action.lower() or "equipment" in step.action.lower():
                equipment_step = step
                break

        assert equipment_step is not None
        assert "equipment" in equipment_step.parameters

    def test_procedure_with_notes(
        self, placeholder_plan: dict, sample_lab_context: LabContext
    ):
        """Test that notes parameter is accepted."""
        procedure = generate_procedure(
            plan=placeholder_plan,
            lab_context=sample_lab_context,
            notes="Test notes for procedure",
        )

        assert len(procedure) >= 6

    def test_procedure_for_undergrad_level(self, placeholder_plan: dict):
        """Test procedure generation for undergraduate experience level."""
        lab_context = LabContext(
            scale_mg=100,
            equipment=["basic_glassware"],
            purification_methods=["filtration"],
            safety_constraints=[],
            experience_level=ExperienceLevel.UNDERGRAD,
            time_budget_hours=4,
        )

        procedure = generate_procedure(
            plan=placeholder_plan,
            lab_context=lab_context,
        )

        # Check PPE includes supervisor notification for undergrads
        first_step = procedure[0]
        ppe = first_step.parameters.get("ppe", [])
        assert "supervisor_notification" in ppe

    def test_procedure_for_industry_level(self, placeholder_plan: dict):
        """Test procedure generation for industry experience level."""
        lab_context = LabContext(
            scale_mg=5000,
            equipment=["reactor", "rotovap", "hplc"],
            purification_methods=["column_chromatography", "hplc"],
            safety_constraints=[],
            experience_level=ExperienceLevel.INDUSTRY,
            time_budget_hours=24,
        )

        procedure = generate_procedure(
            plan=placeholder_plan,
            lab_context=lab_context,
        )

        # Industry level should not have supervisor notification
        first_step = procedure[0]
        ppe = first_step.parameters.get("ppe", [])
        assert "supervisor_notification" not in ppe
