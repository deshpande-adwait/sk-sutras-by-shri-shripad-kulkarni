"""
================================================================================
Module: src.cost.batch
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Asynchronous Batch Job Management interface for eligible non-interactive
             scholarly processing (e.g. bulk semantic pre-indexing, off-peak analysis).
================================================================================
"""

import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class BatchJobRecord(BaseModel):
    """Container holding batch execution state."""
    job_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    provider: str
    model_id: str
    status: str = Field(default="submitted") # 'submitted', 'in_progress', 'completed', 'failed'
    input_items_count: int
    completed_items_count: int = 0
    estimated_cost_inr: float = 0.0
    actual_cost_inr: Optional[float] = None
    created_at: str = Field(default_factory=lambda: str(uuid.uuid4()))


class BatchJobManager:
    """
    ----------------------------------------------------------------------------
    Class: BatchJobManager
    ----------------------------------------------------------------------------
    Purpose:
        Oversees asynchronous batch requests for eligible bulk scholarly tasks.
        Guarantees that interactive author workflows and human decisions are never
        diverted into delayed batch queues.
    ----------------------------------------------------------------------------
    """

    def __init__(self) -> None:
        self._jobs: Dict[str, BatchJobRecord] = {}

    def create_batch_job(
        self,
        provider: str,
        model_id: str,
        items: List[Dict[str, Any]],
        estimated_cost_inr: float = 0.0,
    ) -> BatchJobRecord:
        """Submits a new batch job record."""
        job = BatchJobRecord(
            provider=provider,
            model_id=model_id,
            input_items_count=len(items),
            estimated_cost_inr=estimated_cost_inr,
        )
        self._jobs[job.job_id] = job
        return job

    def get_job_status(self, job_id: str) -> Optional[BatchJobRecord]:
        """Retrieves current batch status."""
        return self._jobs.get(job_id)

    def mark_completed(self, job_id: str, actual_cost_inr: float) -> None:
        """Updates batch job upon completion."""
        job = self._jobs.get(job_id)
        if job:
            job.status = "completed"
            job.completed_items_count = job.input_items_count
            job.actual_cost_inr = actual_cost_inr
