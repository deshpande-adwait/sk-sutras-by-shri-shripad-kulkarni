"""
================================================================================
Module: src.orchestration.nodes
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: State machine execution nodes for the 3-agent orchestration system:
             - NaradaAgent Node: Expounds Narada Sutra & sends devotional thesis.
             - ShandilyaAgent Node: Matches Shandilya Sutra & sends analytical response.
             - SutrakarAgent Node: Synthesizes Udyoga Bhashya & accumulates.
             - Human Review Node: Interrupts for HitL evaluation.
             - Record Approval Node: Persists confirmed manuscript & generates PDF.
================================================================================
"""

from typing import Any, Dict, List, Optional

from src.agents.narada_agent import NaradaAgent
from src.agents.shandilya_agent import ShandilyaAgent
from src.agents.sutrakar_agent import SutrakarAgent
from src.database.repository import ManuscriptRepository
from src.models.schema import SutraPairManuscript
from src.models.state import SutraSynthesisState


def narada_agent_node(state: SutraSynthesisState) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: narada_agent_node
    ----------------------------------------------------------------------------
    Purpose:
        Executes the NaradaAgent node within the LangGraph DAG. Fetches the
        next Narada sutra candidate, produces its multilingual devotional
        exposition, and generates the message addressed to the Shandilya Agent.

    Parameters:
        state (SutraSynthesisState): The current LangGraph workflow state.

    Returns:
        Dict[str, Any]: State delta containing:
            - 'current_narada_sutra': Validated SutraItem dictionary.
            - 'theme': Inferred or configured theme.
            - 'narada_message': Message from NaradaAgent to ShandilyaAgent.
            - 'workflow_stage': Updated stage identifier.
    ----------------------------------------------------------------------------
    """
    agent = NaradaAgent()
    queue: List[Dict[str, Any]] = state.get("batch_queue", [])
    idx: int = state.get("current_index", 0)

    candidate = queue[idx] if idx < len(queue) else None
    if not candidate:
        # Default to first sutra in knowledge base if queue is unpopulated
        candidate = agent.knowledge_base[0] if agent.knowledge_base else {
            "sutra_no": "1",
            "sanskrit": "अथातो भक्तिं व्याख्यास्यामः॥",
            "theme": "Inaugural Definition of Bhakti",
        }

    expounded = agent.expound_sutra(candidate)

    return {
        "current_pair": {
            "pair_id": f"PAIR-{str(idx + 1).zfill(3)}",
            "theme": expounded["theme"],
            "narada_sutra": expounded["sutra_item"].model_dump(),
            "narada_statement": expounded["agent_message_to_shandilya"],
        },
        "workflow_stage": "shandilya_matching",
    }


def shandilya_agent_node(state: SutraSynthesisState) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: shandilya_agent_node
    ----------------------------------------------------------------------------
    Purpose:
        Executes the ShandilyaAgent node within the LangGraph DAG. Receives the
        Narada sutra and prompt, queries the ChromaDB vector store for the closest
        matching Shandilya aphorism, expounds it, and generates the response
        message addressed to the Sutrakar Agent.

    Parameters:
        state (SutraSynthesisState): Current state containing current_pair with
                                     Narada agent's analysis.

    Returns:
        Dict[str, Any]: State delta containing updated current_pair with
                        Shandilya's matched sutra and response statement.
    ----------------------------------------------------------------------------
    """
    agent = ShandilyaAgent()
    curr = dict(state.get("current_pair", {}))

    narada_dict = curr.get("narada_sutra", {})
    from src.models.schema import SutraItem
    narada_item = SutraItem(**narada_dict)

    theme = curr.get("theme", "Comparative Bhakti Inquiry")
    narada_stmt = curr.get("narada_statement", "")

    matched = agent.match_and_respond(
        narada_sutra=narada_item,
        theme=theme,
        narada_message=narada_stmt,
    )

    curr["shandilya_sutra"] = matched["shandilya_sutra"].model_dump()
    curr["shandilya_statement"] = matched["agent_message_to_sutrakar"]

    return {
        "current_pair": curr,
        "workflow_stage": "sutrakar_synthesizing",
    }


def sutrakar_agent_node(state: SutraSynthesisState) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: sutrakar_agent_node
    ----------------------------------------------------------------------------
    Purpose:
        Executes the SutrakarAgent node within the LangGraph DAG. Coordinates
        the inputs from NaradaAgent and ShandilyaAgent, produces the authoritative
        comparative Udyoga Bhashya, validates the schema, and saves to SQLite.

    Parameters:
        state (SutraSynthesisState): State containing both agent's outputs.

    Returns:
        Dict[str, Any]: State delta with completed SutraPairManuscript and
                        review_status set to 'pending_human_review'.
    ----------------------------------------------------------------------------
    """
    agent = SutrakarAgent()
    curr = dict(state.get("current_pair", {}))

    from src.models.schema import SutraItem
    narada_item = SutraItem(**curr["narada_sutra"])
    shandilya_item = SutraItem(**curr["shandilya_sutra"])
    pair_id = curr.get("pair_id", "PAIR-001")
    theme = curr.get("theme", "Synthesis")

    manuscript_pair = agent.synthesize_and_compile(
        pair_id=pair_id,
        theme=theme,
        narada_sutra=narada_item,
        shandilya_sutra=shandilya_item,
        narada_statement=curr.get("narada_statement", ""),
        shandilya_statement=curr.get("shandilya_statement", ""),
    )

    return {
        "current_pair": manuscript_pair.model_dump(),
        "workflow_stage": "awaiting_human_review",
        "review_status": "pending_human_review",
    }


def human_review_checkpoint_node(state: SutraSynthesisState) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: human_review_checkpoint_node
    ----------------------------------------------------------------------------
    Purpose:
        The Human-in-the-Loop (HitL) interrupt checkpoint node. Halts automated
        execution to yield control to the human reviewer in the Streamlit portal.

    Parameters:
        state (SutraSynthesisState): The current state under review.

    Returns:
        Dict[str, Any]: State delta indicating active review checkpoint.
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
        Commits the approved manuscript pair, appends to draft_manuscript,
        updates the SQLite database, increments current_index, and compiles
        the latest version of the Udyoga Sutra PDF.

    Parameters:
        state (SutraSynthesisState): The active state.
        repo (Optional[ManuscriptRepository]): Optional injected repository.

    Returns:
        Dict[str, Any]: State delta.
    ----------------------------------------------------------------------------
    """
    active_pair = state.get("current_pair")
    if not active_pair:
        return {"workflow_stage": "complete"}

    model = SutraPairManuscript(**active_pair)
    db_repo = repo or ManuscriptRepository()
    db_repo.save_pair(model, status="approved")

    drafts = list(state.get("draft_manuscript", []))
    drafts.append(model.model_dump())

    # Compile the updated PDF publication
    from src.pdf.generator import ManuscriptPDFGenerator
    pdf_gen = ManuscriptPDFGenerator()
    pdf_gen.generate_pdf(
        pairs=[SutraPairManuscript(**d) for d in drafts],
        output_filename="udyoga_sutra_compiled.pdf",
    )

    idx: int = state.get("current_index", 0) + 1

    return {
        "draft_manuscript": drafts,
        "current_index": idx,
        "current_pair": None,
        "workflow_stage": "approved_and_compiled",
        "review_status": "approved",
    }
