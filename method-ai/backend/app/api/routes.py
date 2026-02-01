"""API Routes for Method.AI."""

import logging
import uuid

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    FeedbackRequest,
    FeedbackResponse,
    GenerateProcedureRequest,
    GenerateProcedureResponse,
)
from app.services.feedback_store import store_feedback
from app.services.procedure_generator import generate_procedure
from app.services.retrosynthesis_adapter import get_retrosynthesis_plan
from app.services.risk_annotator import annotate_risks

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/v1/generate-procedure", response_model=GenerateProcedureResponse)
async def generate_procedure_endpoint(
    request: GenerateProcedureRequest,
) -> GenerateProcedureResponse:
    """
    Generate a draft lab procedure from a target molecule and lab context.

    This endpoint produces DRAFT procedures intended for review by qualified
    professionals. Generated content is not validated and may contain errors.
    """
    request_id = str(uuid.uuid4())
    logger.info(f"Processing generate-procedure request: {request_id}")

    try:
        # Get retrosynthesis plan
        if request.retrosynthesis_plan is not None:
            plan = {
                "source": "user_provided",
                "target_smiles": request.target_smiles,
                "steps": request.retrosynthesis_plan.get("steps", []),
            }
            logger.info(f"Using user-provided retrosynthesis plan for {request_id}")
        else:
            plan = get_retrosynthesis_plan(request.target_smiles)
            logger.info(f"Retrieved retrosynthesis plan from {plan['source']} for {request_id}")

        # Generate procedure
        procedure = generate_procedure(
            plan=plan,
            lab_context=request.lab_context,
            notes=request.notes,
        )

        # Annotate risks
        risk_flags, fallback_options = annotate_risks(
            procedure=procedure,
            lab_context=request.lab_context,
        )

        return GenerateProcedureResponse(
            procedure=procedure,
            risk_flags=risk_flags,
            fallback_options=fallback_options,
            citations=[],
            disclaimer=(
                "DRAFT PROCEDURE - This is a computer-generated draft intended for "
                "review by qualified professionals. It has not been validated and may "
                "contain errors. Users must verify all steps, assess risks, and ensure "
                "compliance with applicable regulations before execution. No warranty "
                "of safety, accuracy, or fitness for purpose is provided."
            ),
            version="0.1.0",
            request_id=request_id,
        )

    except Exception as e:
        logger.error(f"Error processing request {request_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.post("/v1/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest) -> FeedbackResponse:
    """
    Submit feedback on a generated procedure.

    Feedback helps improve future procedure generation.
    """
    logger.info(f"Received feedback for request: {request.request_id}")

    try:
        store_feedback(
            request_id=request.request_id,
            edits=request.edits,
            outcome=request.outcome,
            notes=request.notes,
        )
        return FeedbackResponse(stored=True)

    except Exception as e:
        logger.error(f"Error storing feedback for {request.request_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to store feedback") from e
