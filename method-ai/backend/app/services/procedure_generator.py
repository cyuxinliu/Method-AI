"""Procedure generator service.

Generates draft lab procedures from retrosynthesis plans and lab context.
Uses deterministic, template-based generation.
"""

from typing import Any

from app.models.schemas import LabContext, ProcedureStep


def generate_procedure(
    plan: dict[str, Any],
    lab_context: LabContext,
    notes: str | None = None,
) -> list[ProcedureStep]:
    """
    Generate a draft procedure from a retrosynthesis plan and lab context.

    This generates DRAFT content for review by qualified professionals.
    The output is deterministic and template-based.

    Args:
        plan: Normalized retrosynthesis plan
        lab_context: Laboratory constraints and context
        notes: Optional additional notes

    Returns:
        List of procedure steps
    """
    steps: list[ProcedureStep] = []
    source = plan.get("source", "unknown")

    # Determine rationale suffix based on source
    source_note = ""
    if source == "ibm_rxn":
        source_note = " (Derived from IBM RXN plan - requires verification)"
    elif source == "placeholder":
        source_note = " (Placeholder procedure - requires full development)"

    # Step 1: Preparation
    steps.append(
        ProcedureStep(
            step_number=1,
            action="Prepare workspace and review safety requirements",
            parameters={
                "location": "appropriate_workspace",
                "ppe": _get_ppe_list(lab_context),
                "review": ["sds_sheets", "institutional_protocols"],
            },
            rationale=f"Ensure proper safety setup before beginning{source_note}",
        )
    )

    # Step 2: Materials
    steps.append(
        ProcedureStep(
            step_number=2,
            action="Gather and verify all materials",
            parameters={
                "verification": "check_labels_and_purity",
                "scale": f"{lab_context.scale_mg}mg",
            },
            rationale="Confirm all materials are available and appropriate",
        )
    )

    # Step 3: Equipment setup
    steps.append(
        ProcedureStep(
            step_number=3,
            action="Set up reaction apparatus",
            parameters={
                "equipment": lab_context.equipment[:5] if lab_context.equipment else ["standard_glassware"],
                "verification": "check_integrity",
            },
            rationale="Proper equipment setup ensures reproducibility",
        )
    )

    # Step 4: Weighing
    steps.append(
        ProcedureStep(
            step_number=4,
            action="Weigh starting materials accurately",
            parameters={
                "balance_type": "analytical" if lab_context.scale_mg < 100 else "standard",
                "record": "laboratory_notebook",
            },
            rationale="Accurate measurement is essential for stoichiometry",
        )
    )

    # Step 5: Reaction setup
    steps.append(
        ProcedureStep(
            step_number=5,
            action="Combine reagents according to protocol",
            parameters={
                "order": "as_specified",
                "mixing": "appropriate_method",
                "atmosphere": _get_atmosphere(lab_context),
            },
            rationale="Order and conditions of addition affect outcome",
        )
    )

    # Step 6: Reaction monitoring
    steps.append(
        ProcedureStep(
            step_number=6,
            action="Monitor reaction progress",
            parameters={
                "methods": ["visual_observation", "analytical_if_available"],
                "interval": "periodic",
                "documentation": "record_observations",
            },
            rationale="Monitoring ensures reaction proceeds as expected",
        )
    )

    # Step 7: Reaction completion
    steps.append(
        ProcedureStep(
            step_number=7,
            action="Confirm reaction completion and quench if needed",
            parameters={
                "confirmation": "appropriate_analytical_method",
                "quench": "as_required_by_reaction_type",
            },
            rationale="Proper quenching ensures safety and product stability",
        )
    )

    # Step 8: Workup
    steps.append(
        ProcedureStep(
            step_number=8,
            action="Perform workup procedure",
            parameters={
                "steps": ["cool_if_needed", "transfer", "separate_phases_if_applicable"],
                "waste_handling": "follow_institutional_guidelines",
            },
            rationale="Workup isolates crude product from reaction mixture",
        )
    )

    # Step 9: Purification
    purification = lab_context.purification_methods[0] if lab_context.purification_methods else "appropriate_method"
    steps.append(
        ProcedureStep(
            step_number=9,
            action="Purify product",
            parameters={
                "primary_method": purification,
                "alternatives": lab_context.purification_methods[1:3] if len(lab_context.purification_methods) > 1 else [],
            },
            rationale="Purification removes impurities to obtain clean product",
        )
    )

    # Step 10: Characterization and storage
    steps.append(
        ProcedureStep(
            step_number=10,
            action="Characterize and store product",
            parameters={
                "characterization": "available_analytical_methods",
                "storage": "appropriate_container_and_conditions",
                "labeling": "complete_information",
            },
            rationale="Proper characterization confirms identity; proper storage ensures stability",
        )
    )

    return steps


def _get_ppe_list(lab_context: LabContext) -> list[str]:
    """Determine appropriate PPE based on context."""
    base_ppe = ["lab_coat", "safety_glasses", "appropriate_gloves"]

    # Add based on experience level
    if lab_context.experience_level.value in ["undergrad", "grad"]:
        base_ppe.append("supervisor_notification")

    return base_ppe


def _get_atmosphere(lab_context: LabContext) -> str:
    """Determine atmosphere requirements."""
    constraints = lab_context.safety_constraints

    if "inert_atmosphere_required" in constraints:
        return "inert_gas"
    if "no_glovebox" in constraints:
        return "ambient_with_caution"

    return "as_specified_in_protocol"
