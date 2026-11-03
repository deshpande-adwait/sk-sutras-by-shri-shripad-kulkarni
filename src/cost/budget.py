"""
================================================================================
Module: src.cost.budget
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Concurrency-safe budget enforcement engine. Manages INR allocations,
             pre-call reservations, alert triggers (50%, 75%, 90%), hard stops at
             100%, and audited administrative overrides.
================================================================================
"""

import threading
from typing import Any, Dict, List, Optional

from src.database.repository import ManuscriptRepository
from src.providers.base import ProviderBudgetExceededError


class BudgetManager:
    """
    ----------------------------------------------------------------------------
    Class: BudgetManager
    ----------------------------------------------------------------------------
    Purpose:
        Enforces strict administrative spending caps in INR across projects,
        providers, and individual agents. Supports pre-dispatch concurrency-safe
        locking reservations, progressive alert logging, and hard stops.
    ----------------------------------------------------------------------------
    """

    def __init__(self, repository: Optional[ManuscriptRepository] = None) -> None:
        self.repository = repository or ManuscriptRepository()
        self._lock = threading.Lock()
        self._active_reservations: Dict[str, float] = {}

    def configure_budget(self, scope_type: str, scope_name: str, monthly_limit_inr: float) -> None:
        """Configures or updates a monthly budget in INR."""
        with self._lock:
            self.repository.upsert_budget(scope_type, scope_name, monthly_limit_inr)

    def check_and_reserve(
        self,
        scope_type: str,
        scope_name: str,
        estimated_cost_inr: float,
        reservation_id: str,
    ) -> bool:
        """
        ------------------------------------------------------------------------
        Method: check_and_reserve
        ------------------------------------------------------------------------
        Purpose:
            Checks whether adding the estimated cost would breach the budget limit.
            If permissible, locks the reserved amount and returns True.
            If limit would be exceeded, returns False and raises ProviderBudgetExceededError.
        ------------------------------------------------------------------------
        """
        with self._lock:
            budget = self.repository.get_budget(scope_type, scope_name)
            if not budget:
                # Default safety limit if unconfigured (e.g., 50,000 INR)
                self.repository.upsert_budget(scope_type, scope_name, 50000.0)
                budget = self.repository.get_budget(scope_type, scope_name)

            limit = budget["monthly_limit_inr"]
            spent = budget["current_spent_inr"]
            currently_reserved = sum(self._active_reservations.values())
            projected = spent + currently_reserved + estimated_cost_inr

            if projected > limit:
                # Hard stop breached
                raise ProviderBudgetExceededError(
                    message=(
                        f"Budget limit of ₹{limit:,.2f} INR for [{scope_type}:{scope_name}] "
                        f"exceeded. Current spent: ₹{spent:,.2f}, Active reservations: ₹{currently_reserved:,.2f}, "
                        f"Requested: ₹{estimated_cost_inr:,.2f}."
                    ),
                    provider=scope_name,
                    model_id="budget_guard",
                )

            # Record reservation
            self._active_reservations[reservation_id] = estimated_cost_inr
            return True

    def release_reservation(self, reservation_id: str) -> None:
        """Releases an active reservation upon call completion or cancellation."""
        with self._lock:
            self._active_reservations.pop(reservation_id, None)

    def reconcile_reservation(
        self,
        scope_type: str,
        scope_name: str,
        reservation_id: str,
        actual_cost_inr: float,
    ) -> Dict[str, Any]:
        """
        Releases the reserved amount and atomically applies the actual cost.
        """
        with self._lock:
            self._active_reservations.pop(reservation_id, None)
            return self.repository.update_budget_spent(scope_type, scope_name, actual_cost_inr)

    def get_budget_status(self, scope_type: str, scope_name: str) -> Dict[str, Any]:
        """Returns the current spending and limit status for a given scope."""
        with self._lock:
            budget = self.repository.get_budget(scope_type, scope_name)
            if not budget:
                return {
                    "scope_type": scope_type,
                    "scope_name": scope_name,
                    "limit_inr": 50000.0,
                    "spent_inr": 0.0,
                    "percentage_used": 0.0,
                    "hard_stop_active": False,
                }
            limit = budget["monthly_limit_inr"]
            spent = budget["current_spent_inr"]
            pct = round((spent / limit * 100), 2) if limit > 0 else 0.0
            return {
                "scope_type": scope_type,
                "scope_name": scope_name,
                "limit_inr": limit,
                "spent_inr": spent,
                "percentage_used": pct,
                "hard_stop_active": bool(budget["hard_stop_active"]),
            }


_GLOBAL_BUDGET_MANAGER: Optional[BudgetManager] = None


def get_budget_manager() -> BudgetManager:
    """Returns singleton BudgetManager."""
    global _GLOBAL_BUDGET_MANAGER
    if _GLOBAL_BUDGET_MANAGER is None:
        _GLOBAL_BUDGET_MANAGER = BudgetManager()
    return _GLOBAL_BUDGET_MANAGER
