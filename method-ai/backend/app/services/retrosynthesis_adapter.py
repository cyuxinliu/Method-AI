"""Retrosynthesis adapter service.

Integrates with IBM RXN for Chemistry via rxn4chemistry package.
Falls back to deterministic placeholder when RXN is not available.
"""

import logging
from typing import Any

from app.core.config import settings

logger = logging.getLogger(__name__)

# Normalized plan schema:
# {
#     "source": "ibm_rxn" | "placeholder",
#     "target_smiles": str,
#     "steps": [
#         {"rxn_smiles": str, "confidence": float, "notes": str}
#     ]
# }


def get_retrosynthesis_plan(target_smiles: str) -> dict[str, Any]:
    """
    Get a retrosynthesis plan for the target molecule.

    Attempts to use IBM RXN if configured, otherwise returns a placeholder.

    Args:
        target_smiles: Target molecule in SMILES format

    Returns:
        Normalized retrosynthesis plan dictionary
    """
    if settings.rxn_api_key:
        try:
            return _get_rxn_plan(target_smiles)
        except Exception as e:
            logger.warning(f"RXN API call failed, using placeholder: {e}")
            return _get_placeholder_plan(target_smiles)
    else:
        logger.info("RXN API key not configured, using placeholder plan")
        return _get_placeholder_plan(target_smiles)


def _get_rxn_plan(target_smiles: str) -> dict[str, Any]:
    """
    Fetch retrosynthesis plan from IBM RXN.

    Args:
        target_smiles: Target molecule in SMILES format

    Returns:
        Normalized plan from RXN

    Raises:
        Exception: If RXN API call fails
    """
    # Import here to avoid import errors when rxn4chemistry is not needed
    from rxn4chemistry import RXN4ChemistryWrapper

    logger.info(f"Calling IBM RXN for target: {target_smiles[:50]}...")

    # Initialize RXN wrapper
    rxn = RXN4ChemistryWrapper(api_key=settings.rxn_api_key)

    # Set project if configured
    if settings.rxn_project_id:
        rxn.set_project(settings.rxn_project_id)
    else:
        # Create or use default project
        rxn.create_project("method-ai-default")

    # Request retrosynthesis prediction
    response = rxn.predict_automatic_retrosynthesis(product=target_smiles)

    # Wait for results (with timeout handling)
    results = rxn.get_predict_automatic_retrosynthesis_results(response["prediction_id"])

    # Normalize the response
    return _normalize_rxn_response(target_smiles, results)


def _normalize_rxn_response(target_smiles: str, rxn_results: dict[str, Any]) -> dict[str, Any]:
    """
    Normalize IBM RXN response to internal schema.

    Args:
        target_smiles: Original target SMILES
        rxn_results: Raw response from RXN API

    Returns:
        Normalized plan dictionary
    """
    steps = []

    # Extract retrosynthetic pathways
    retrosynthetic_paths = rxn_results.get("retrosynthetic_paths", [])

    if retrosynthetic_paths:
        # Use the first (typically best) pathway
        best_path = retrosynthetic_paths[0] if retrosynthetic_paths else {}
        reactions = best_path.get("reactions", [])

        for idx, reaction in enumerate(reactions):
            steps.append({
                "rxn_smiles": reaction.get("rxn_smiles", ""),
                "confidence": reaction.get("confidence", 0.0),
                "notes": f"Step {idx + 1} from IBM RXN",
            })

    return {
        "source": "ibm_rxn",
        "target_smiles": target_smiles,
        "steps": steps,
    }


def _get_placeholder_plan(target_smiles: str) -> dict[str, Any]:
    """
    Generate a deterministic placeholder plan.

    Used when RXN is not available or fails.

    Args:
        target_smiles: Target molecule in SMILES format

    Returns:
        Placeholder plan dictionary
    """
    return {
        "source": "placeholder",
        "target_smiles": target_smiles,
        "steps": [],
    }


def is_rxn_configured() -> bool:
    """Check if IBM RXN is configured."""
    return settings.rxn_api_key is not None
