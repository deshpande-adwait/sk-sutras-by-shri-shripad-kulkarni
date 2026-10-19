"""
================================================================================
Package: src.orchestration
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: LangGraph multi-agent orchestration pipeline. Implements batch
             processing DAGs with bi-directional Human-in-the-Loop (HitL) interrupts.
================================================================================
"""

from src.orchestration.graph import build_sutra_synthesis_graph

__all__ = ["build_sutra_synthesis_graph"]
