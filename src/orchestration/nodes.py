"""
================================================================================
Module: src.orchestration.nodes
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: State machine execution nodes for the LangGraph pipeline. Handles
             candidate preparation, semantic comparative synthesis via flexible LLM,
             human-in-the-loop review interrupts, and relational manuscript persistence.
================================================================================
"""

import json
from typing import Any, Dict, List, Optional

from src.config import get_chat_model
from src.database.repository import ManuscriptRepository
from src.models.schema import MultilingualText, SutraItem, SutraPairManuscript
from src.models.state import SutraSynthesisState


def prepare_candidate_pair_node(state: SutraSynthesisState) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: prepare_candidate_pair_node
    ----------------------------------------------------------------------------
    Purpose:
        Retrieves the next candidate sutra pairing from `batch_queue` using
        `current_index`, sets it as the active `current_pair`, and transitions
        the workflow stage.

    Parameters:
        state (SutraSynthesisState): The current LangGraph state dictionary.

    Returns:
        Dict[str, Any]: State delta containing updated current_pair and workflow_stage.

    Errors:
        IndexError: Handled gracefully if current_index exceeds batch_queue length.

    Manual Debugging Notes:
        - If `batch_queue` is empty, marks workflow_stage as 'complete'.
    ----------------------------------------------------------------------------
    """
    queue: List[Dict[str, Any]] = state.get("batch_queue", [])
    idx: int = state.get("current_index", 0)

    if idx < len(queue):
        candidate = queue[idx]
        return {
            "current_pair": candidate,
            "workflow_stage": "synthesizing",
            "review_status": "in_progress",
        }
    else:
        return {
            "current_pair": None,
            "workflow_stage": "complete",
            "review_status": "completed",
        }


def synthesize_bhashya_node(state: SutraSynthesisState) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: synthesize_bhashya_node
    ----------------------------------------------------------------------------
    Purpose:
        Executes philosophical comparative synthesis between the Narada Bhakti
        Sutra and Shandilya Bhakti Sutra. Invokes the dynamic LLM provider
        (OpenAI/Anthropic/Gemini/Ollama) to produce the comparative Udyoga Bhashya
        in English, Hindi, and Marathi.

    Parameters:
        state (SutraSynthesisState): Current LangGraph state containing current_pair.

    Returns:
        Dict[str, Any]: State delta containing the synthesized current_pair with
                        the completed Udyoga Bhashya.

    Errors:
        RuntimeError: If LLM invocation or JSON parsing fails. A fallback synthesis
                      is injected to prevent catastrophic DAG failure.

    Manual Debugging Notes:
        - When testing offline without API keys, this node falls back to a structured
          deterministic synthesis template.
    ----------------------------------------------------------------------------
    """
    current_pair = state.get("current_pair")
    if not current_pair:
        return {"workflow_stage": "complete"}

    theme = current_pair.get("theme", "Philosophical Synthesis of Bhakti")
    narada = current_pair.get("narada_sutra", {})
    shandilya = current_pair.get("shandilya_sutra", {})

    prompt = f"""You are a master Sanskrit scholar and philosopher synthesizing the Narada Bhakti Sutra and Shandilya Bhakti Sutra into the comparative treatise 'Udyoga Sutra'.

Theme: {theme}

Narada Bhakti Sutra #{narada.get('sutra_no')}:
Sanskrit: {narada.get('sanskrit')}
Initial Vishleshan: {narada.get('vishleshan', {}).get('en', '')}

Shandilya Bhakti Sutra #{shandilya.get('sutra_no')}:
Sanskrit: {shandilya.get('sanskrit')}
Initial Vishleshan: {shandilya.get('vishleshan', {}).get('en', '')}

Task:
Produce a comparative 'Udyoga Bhashya' synthesis connecting the experiential devotional insight of Narada with the formal epistemological inquiry of Shandilya.
Provide the output strictly in this valid JSON format:
{{
  "en": "Comprehensive English comparative synthesis...",
  "hi": "हिंदी में तुलनात्मक उद्योग भाष्य...",
  "mr": "मराठीतील तुलनात्मक उद्योग भाष्य..."
}}
Return ONLY raw JSON, with no markdown fences, no code blocks, and no extra preamble.
"""

    synthesis_result: Dict[str, Any]
    try:
        llm = get_chat_model()
        response = llm.invoke(prompt)
        content_str = response.content.strip()
        # Clean potential markdown wrapping
        if content_str.startswith("```json"):
            content_str = content_str[7:]
        if content_str.startswith("```"):
            content_str = content_str[3:]
        if content_str.endswith("```"):
            content_str = content_str[:-3]
        synthesis_result = json.loads(content_str.strip())
    except Exception as exc:
        # Graceful fallback synthesis for testing and offline modes
        err_msg = f"LLM synthesis fallback triggered: {str(exc)}"
        errors = state.get("error_log", [])
        errors.append(err_msg)
        synthesis_result = {
            "en": (
                f"Comparative Udyoga Bhashya on '{theme}': Narada emphasizes supreme loving devotion "
                f"(Sutra {narada.get('sutra_no')}: {narada.get('sanskrit')}) as direct divine love, while "
                f"Shandilya approaches Bhakti (Sutra {shandilya.get('sutra_no')}: {shandilya.get('sanskrit')}) "
                f"as rational epistemological inquiry and profound attachment to Ishvara leading to liberation."
            ),
            "hi": (
                f"उद्योग भाष्य ('{theme}'): देवर्षि नारद भक्ति को परम प्रेम रूपा मानते हैं, "
                f"जबकि महर्षि शांडिल्य इसे ईश्वर के प्रति परम अनुराग और ज्ञाननिष्ठ जिज्ञासा के रूप में प्रस्तुत करते हैं।"
            ),
            "mr": (
                f"उद्योग भाष्य ('{theme}'): देवर्षी नारद भक्तीला परम प्रेमरूप मानतात, "
                f"तर महर्षी शांडिल्य ईश्वराच्या ठिकाणी असलेली परम अनुरक्ती आणि ज्ञानात्मक जिज्ञासा या रूपाने तिची मांडणी करतात."
            ),
        }

    # Update active pair structure
    updated_pair = dict(current_pair)
    updated_pair["udyoga_bhashya_synthesis"] = synthesis_result

    return {
        "current_pair": updated_pair,
        "workflow_stage": "awaiting_human_review",
        "review_status": "pending_human_review",
    }


def human_review_checkpoint_node(state: SutraSynthesisState) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: human_review_checkpoint_node
    ----------------------------------------------------------------------------
    Purpose:
        Represents the explicit Human-in-the-Loop (HitL) interrupt node.
        Halts automated graph progression until a human reviewer (e.g.,
        Shri Shripad Kulkarni) evaluates, edits, or approves the synthesis.

    Parameters:
        state (SutraSynthesisState): State containing active pair under review.

    Returns:
        Dict[str, Any]: State delta with review_status set to 'pending_human_review'.

    Manual Debugging Notes:
        - LangGraph compilation uses `interrupt_before=["human_review"]` or this
          checkpoint node to yield control to the Streamlit UI.
    ----------------------------------------------------------------------------
    """
    return {
        "workflow_stage": "in_human_review",
        "review_status": state.get("review_status", "pending_human_review"),
    }


def record_approval_node(
    state: SutraSynthesisState,
    repo: Optional[ManuscriptRepository] = None,
) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: record_approval_node
    ----------------------------------------------------------------------------
    Purpose:
        Once human approval is confirmed, converts the active pair into a fully
        validated SutraPairManuscript Pydantic model, persists it into the SQLite
        relational database, appends it to `draft_manuscript`, and increments
        `current_index` to advance the batch queue.

    Parameters:
        state (SutraSynthesisState): The current LangGraph state.
        repo (Optional[ManuscriptRepository]): Optional injected repository.

    Returns:
        Dict[str, Any]: State delta updating draft_manuscript, current_index,
                        and resetting current_pair.

    Errors:
        pydantic.ValidationError: If synthesized data fails schema constraints.
    ----------------------------------------------------------------------------
    """
    active_pair = state.get("current_pair")
    if not active_pair:
        return {"workflow_stage": "complete"}

    # Validate against strict specification schema
    manuscript_model = SutraPairManuscript(**active_pair)

    # Persist in SQLite relational database
    db_repo = repo or ManuscriptRepository()
    db_repo.save_pair(manuscript_model, status="approved")

    # Append to state manuscript list
    drafts: List[Dict[str, Any]] = list(state.get("draft_manuscript", []))
    drafts.append(manuscript_model.model_dump())

    idx: int = state.get("current_index", 0) + 1

    return {
        "draft_manuscript": drafts,
        "current_index": idx,
        "current_pair": None,
        "workflow_stage": "preparing_next",
        "review_status": "approved",
    }
