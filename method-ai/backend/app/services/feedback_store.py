"""Feedback storage service.

Stores user feedback on generated procedures for future improvement.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from filelock import FileLock

from app.core.config import settings
from app.models.schemas import FeedbackOutcome

logger = logging.getLogger(__name__)


def store_feedback(
    request_id: str,
    edits: str,
    outcome: FeedbackOutcome,
    notes: str | None = None,
) -> None:
    """
    Store feedback to the feedback file.

    Uses file locking for safe concurrent access.

    Args:
        request_id: Original procedure request ID
        edits: Description of edits made
        outcome: Outcome of the procedure
        notes: Additional notes
    """
    feedback_path = Path(settings.feedback_storage_path)

    # Ensure directory exists
    feedback_path.parent.mkdir(parents=True, exist_ok=True)

    # Create feedback record
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": request_id,
        "edits": edits,
        "outcome": outcome.value,
        "notes": notes,
    }

    # Write with file lock
    lock_path = feedback_path.with_suffix(".lock")
    lock = FileLock(lock_path)

    try:
        with lock:
            with open(feedback_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
        logger.info(f"Stored feedback for request {request_id}")
    except Exception as e:
        logger.error(f"Failed to store feedback: {e}")
        raise


def get_feedback_count() -> int:
    """Get the count of stored feedback records."""
    feedback_path = Path(settings.feedback_storage_path)

    if not feedback_path.exists():
        return 0

    try:
        with open(feedback_path, encoding="utf-8") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0
