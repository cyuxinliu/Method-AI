"""Risk annotator service.

Analyzes lab context and procedures to identify potential risks and suggest fallbacks.
"""

from app.models.schemas import LabContext, ProcedureStep


def annotate_risks(
    procedure: list[ProcedureStep],
    lab_context: LabContext,
) -> tuple[list[str], list[str]]:
    """
    Annotate risks based on lab context and procedure.

    Args:
        procedure: Generated procedure steps
        lab_context: Laboratory constraints and context

    Returns:
        Tuple of (risk_flags, fallback_options)
    """
    risk_flags = []
    fallback_options = []

    # Analyze safety constraints
    risk_flags.extend(_analyze_safety_constraints(lab_context))

    # Analyze equipment limitations
    risk_flags.extend(_analyze_equipment(lab_context))

    # Analyze experience level
    risk_flags.extend(_analyze_experience(lab_context))

    # Analyze time constraints
    risk_flags.extend(_analyze_time(lab_context, procedure))

    # Analyze scale
    risk_flags.extend(_analyze_scale(lab_context))

    # Generate fallback options
    fallback_options = _generate_fallbacks(lab_context)

    # Always add verification reminder
    risk_flags.append(
        "All procedures require verification by qualified personnel before execution"
    )

    return risk_flags, fallback_options


def _analyze_safety_constraints(lab_context: LabContext) -> list[str]:
    """Analyze safety constraints for risks."""
    flags = []
    constraints = lab_context.safety_constraints

    if "no_glovebox" in constraints:
        flags.append("No glovebox available - verify air/moisture sensitivity requirements")

    if "no_fume_hood" in constraints:
        flags.append("No fume hood noted - ensure adequate ventilation for all operations")

    if "no_open_flame" in constraints:
        flags.append("Open flame restricted - use alternative heating methods")

    if "limited_ventilation" in constraints:
        flags.append("Limited ventilation - restrict use of volatile materials")

    return flags


def _analyze_equipment(lab_context: LabContext) -> list[str]:
    """Analyze equipment availability for risks."""
    flags = []
    equipment = lab_context.equipment
    purification = lab_context.purification_methods

    # Check for common analytical equipment
    has_analytical = any(
        eq in equipment
        for eq in ["nmr", "hplc", "gc", "mass_spec", "ir"]
    )
    if not has_analytical:
        flags.append("Limited analytical equipment - product verification may be constrained")

    # Check purification options
    if "column_chromatography" not in purification and "hplc" not in purification:
        flags.append("No chromatography available - ensure alternative purification is suitable")

    if "rotovap" not in equipment and "rotary_evaporator" not in equipment:
        flags.append("No rotary evaporator - solvent removal may require alternative approach")

    return flags


def _analyze_experience(lab_context: LabContext) -> list[str]:
    """Analyze experience level for appropriate flags."""
    flags = []
    level = lab_context.experience_level.value

    if level == "undergrad":
        flags.append("Undergraduate level - ensure appropriate supervision is arranged")
        flags.append("Review all steps with supervisor before beginning")

    if level in ["undergrad", "grad"]:
        flags.append("Ensure emergency procedures are reviewed and understood")

    return flags


def _analyze_time(lab_context: LabContext, procedure: list[ProcedureStep]) -> list[str]:
    """Analyze time constraints."""
    flags = []
    time_hours = lab_context.time_budget_hours

    if time_hours < 4:
        flags.append("Limited time budget - ensure procedure can be safely paused if needed")

    if time_hours < 2:
        flags.append("Very short time window - consider breaking into multiple sessions")

    return flags


def _analyze_scale(lab_context: LabContext) -> list[str]:
    """Analyze scale-related considerations."""
    flags = []
    scale_mg = lab_context.scale_mg

    if scale_mg > 10000:  # > 10g
        flags.append("Large scale operation - review heat dissipation and mixing efficiency")

    if scale_mg < 10:  # < 10mg
        flags.append("Small scale operation - ensure appropriate precision in measurements")

    return flags


def _generate_fallbacks(lab_context: LabContext) -> list[str]:
    """Generate fallback options based on context."""
    fallbacks = []

    # Solvent alternatives
    fallbacks.append("Alternative solvent systems may be considered if primary choice unavailable")

    # Temperature modifications
    fallbacks.append("Temperature profile can be adjusted based on reaction monitoring")

    # Purification alternatives
    if len(lab_context.purification_methods) > 1:
        methods = ", ".join(lab_context.purification_methods[:3])
        fallbacks.append(f"Alternative purification methods available: {methods}")
    else:
        fallbacks.append("Consider alternative purification approach if primary method insufficient")

    return fallbacks
