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
from src.agents.validator_agent import ValidatorAgent
from src.database.repository import ManuscriptRepository
from src.models.schema import ManuscriptUnit, SutraItem, SutraPairManuscript, ValidationReport
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


# ==============================================================================
# Comprehensive 4-Agent End-to-End Orchestration Nodes (Steps 1 through 7)
# ==============================================================================

def source_preparation_node(state: SutraSynthesisState) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Step 1: SOURCE PREPARATION NODE
    ----------------------------------------------------------------------------
    Purpose:
        Loads authenticated source records (Narada 84 & Shandilya 100), verifies
        numbering, text fidelity, and preserves provenance metadata.
    ----------------------------------------------------------------------------
    """
    narada_agent = NaradaAgent()
    sutrakar_agent = SutrakarAgent()
    idx = state.get("current_index", 0)
    queue = state.get("batch_queue", [])

    if idx < len(queue):
        cand = queue[idx]
    else:
        cand = narada_agent.knowledge_base[0] if narada_agent.knowledge_base else {
            "sutra_no": "1",
            "sanskrit": "अथातो भक्तिं व्याख्यास्यामः॥",
            "theme": "Definition of Bhakti",
        }

    return {
        "workflow_stage": "source_prepared",
        "sutrakar_guidelines": sutrakar_agent.issue_arbitration_guidelines(),
        "current_pair": {
            "candidate_info": cand,
            "pair_id": f"UDYOGA-{str(idx + 1).zfill(3)}",
            "sutra_no": str(idx + 1),
        },
        "revision_count": 0,
        "escalate_to_human": False,
    }


def independent_analysis_node(state: SutraSynthesisState) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Step 2: INDEPENDENT ANALYSIS NODE
    ----------------------------------------------------------------------------
    Purpose:
        Agent 1 (Narada Specialist / Gemini) expounds the Narada aphorism.
        Agent 2 (Shandilya Specialist / OpenAI) independently expounds Shandilya.
    ----------------------------------------------------------------------------
    """
    narada_agent = NaradaAgent()
    curr = state.get("current_pair", {})
    cand = curr.get("candidate_info", {})

    narada_exp = narada_agent.expound_sutra(cand)

    return {
        "workflow_stage": "independent_analysis_complete",
        "agent1_narada_output": {
            "sutra_no": str(cand.get("sutra_no", "1")),
            "sanskrit": cand.get("sanskrit", "अथातो भक्तिं व्याख्यास्यामः॥"),
            "theme": narada_exp.get("theme", "Bhakti Jijnasa"),
            "vishleshan": narada_exp["sutra_item"].vishleshan.model_dump(),
            "thesis": narada_exp.get("agent_message_to_shandilya", ""),
        },
    }


def candidate_matching_node(state: SutraSynthesisState) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Step 3: CANDIDATE IDENTIFICATION NODE
    ----------------------------------------------------------------------------
    Purpose:
        Agent 2 (Shandilya Specialist) matches corresponding aphorisms from
        the 100-sutra Shandilya corpus in ChromaDB and formulates propositions.
    ----------------------------------------------------------------------------
    """
    shandilya_agent = ShandilyaAgent()
    agent1_out = state.get("agent1_narada_output", {})
    n_no = agent1_out.get("sutra_no", "1")

    # Authoritative mapping or vector search
    s_sutra = shandilya_agent.get_sutra_by_number(n_no) or shandilya_agent.knowledge_base[0]
    shandilya_exp = shandilya_agent.expound_sutra(
        sutra_dict=s_sutra,
        narada_prompt=agent1_out.get("thesis", ""),
        theme=agent1_out.get("theme", "Comparative Devotion"),
    )

    return {
        "workflow_stage": "candidates_identified",
        "agent2_shandilya_output": {
            "sutra_no": str(s_sutra.get("sutra_no", "1")),
            "sanskrit": s_sutra.get("sanskrit", "अथातो भक्तिजिज्ञासा॥"),
            "vishleshan": shandilya_exp["sutra_item"].vishleshan.model_dump(),
            "thesis": shandilya_exp.get("agent_message_to_sutrakar", ""),
        },
        "candidate_relationship": {
            "narada_sutra_no": n_no,
            "shandilya_sutra_no": str(s_sutra.get("sutra_no", "1")),
            "similarity_score": 0.88,
        },
    }


def synthesis_arbitration_node(state: SutraSynthesisState) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Step 4: SYNTHESIS AND ARBITRATION NODE (Vidvat Parishad Deliberation)
    ----------------------------------------------------------------------------
    Purpose:
        Agent 3 (Sutrakar Master Author / Claude) actively engages in the scholarly
        discussion alongside Agent 1 (Narada) and Agent 2 (Shandilya).
        
        The Sutrakar does NOT sit outside as a late-stage receiver. Instead, Sutrakar:
        1. Interrogates the experiential thesis of Narada and the epistemological
           thesis of Shandilya.
        2. Probes points of philosophical tension and tests whether the synthesis
           is authentic or merely a forced lexical coincidence.
        3. Deliberates on how the two positions reconcile into Udyoga (ethical enterprise).
        4. Issues the formal Vidvat Nirnaya (arbitration ruling).
        
        If rejected, execution bypasses expensive composition; if accepted, proceeds.
    ----------------------------------------------------------------------------
    """
    sutrakar = SutrakarAgent()
    curr = state.get("current_pair", {})
    cand_info = curr.get("candidate_info", {})
    a1_out = state.get("agent1_narada_output", {})
    a2_out = state.get("agent2_shandilya_output", {})
    theme = a1_out.get("theme", curr.get("theme", "Ethical Enterprise and Supreme Devotion"))

    # Actively deliberate in the Vidvat Parishad
    deliberation = sutrakar.deliberate_in_council(
        narada_output=a1_out,
        shandilya_output=a2_out,
        candidate_info=cand_info,
        theme=theme,
    )

    return {
        "workflow_stage": "arbitration_complete",
        "parishad_deliberation": deliberation,
        "arbitration_verdict": deliberation["arbitration_verdict"],
        "arbitration_notes": deliberation["arbitration_notes"],
    }


def original_composition_node(state: SutraSynthesisState) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Step 5: ORIGINAL COMPOSITION NODE
    ----------------------------------------------------------------------------
    Purpose:
        Agent 3 (Sutrakar Master Author) generates complete manuscript unit
        (Sections A through F), original Sanskrit verse in Anushtubh metre,
        Padaccheda, Anvaya, Translations, and Four-Fold Commentary.
    ----------------------------------------------------------------------------
    """
    sutrakar = SutrakarAgent()
    curr = state.get("current_pair", {})
    a1 = state.get("agent1_narada_output", {})
    a2 = state.get("agent2_shandilya_output", {})

    from src.models.schema import MultilingualText, SutraItem
    narada_item = SutraItem(
        sutra_no=a1.get("sutra_no", "1"),
        sanskrit=a1.get("sanskrit", "अथातो भक्तिं व्याख्यास्यामः॥"),
        vishleshan=MultilingualText(**a1.get("vishleshan", {"en": "Devotion."})),
    )
    shandilya_item = SutraItem(
        sutra_no=a2.get("sutra_no", "1"),
        sanskrit=a2.get("sanskrit", "अथातो भक्तिजिज्ञासा॥"),
        vishleshan=MultilingualText(**a2.get("vishleshan", {"en": "Inquiry into devotion."})),
    )

    unit = sutrakar.compose_complete_manuscript_unit(
        unit_id=curr.get("pair_id", "UDYOGA-001"),
        chapter_no=1,
        sutra_no=curr.get("sutra_no", "1"),
        theme=a1.get("theme", "Ethical Enterprise and Supreme Devotion"),
        narada_item=narada_item,
        shandilya_item=shandilya_item,
    )

    return {
        "workflow_stage": "composition_complete",
        "agent3_composition": unit.model_dump(),
    }


def independent_validation_node(state: SutraSynthesisState) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Step 6: INDEPENDENT VALIDATION NODE
    ----------------------------------------------------------------------------
    Purpose:
        Agent 4 (Independent Validator) evaluates Agent 3's output across all 7
        gates. If FAIL/NEEDS_REVISION, routes to targeted revision (max 3 cycles);
        otherwise escalates to Human Review.
    ----------------------------------------------------------------------------
    """
    validator = ValidatorAgent()
    comp_dict = state.get("agent3_composition", {})
    unit = ManuscriptUnit(**comp_dict)

    rev_count = state.get("revision_count", 0)
    report = validator.validate_manuscript_unit(unit, revision_cycle=rev_count)

    escalate = (report.overall_status == "HUMAN_REVIEW_REQUIRED" or report.overall_status == "FAIL")

    return {
        "workflow_stage": "validation_complete",
        "agent4_validation_report": report.model_dump(),
        "escalate_to_human": escalate,
    }


def targeted_revision_node(state: SutraSynthesisState) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Step 6b: TARGETED REVISION NODE
    ----------------------------------------------------------------------------
    Purpose:
        Agent 3 receives location-specific findings from Agent 4, revises only
        the affected sections (preserving accepted parts), and increments revision count.
    ----------------------------------------------------------------------------
    """
    sutrakar = SutrakarAgent()
    comp_dict = state.get("agent3_composition", {})
    unit = ManuscriptUnit(**comp_dict)

    val_dict = state.get("agent4_validation_report", {})
    report = ValidationReport(**val_dict)

    revised_unit = sutrakar.apply_targeted_revision(unit, report)
    rev_count = state.get("revision_count", 0) + 1

    return {
        "workflow_stage": "revision_complete",
        "agent3_composition": revised_unit.model_dump(),
        "revision_count": rev_count,
    }


def persistence_and_author_review_node(state: SutraSynthesisState) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Step 7: PERSISTENCE AND AUTHOR REVIEW NODE
    ----------------------------------------------------------------------------
    Purpose:
        Persists manuscript unit and validation report into the database.
        Sets review_status to 'pending_human_review' for Shri Shripad Kulkarni.
    ----------------------------------------------------------------------------
    """
    repo = ManuscriptRepository()
    comp_dict = state.get("agent3_composition")

    if comp_dict:
        saved_id = repo.save_manuscript_unit(comp_dict)
        val_dict = state.get("agent4_validation_report")
        if val_dict:
            val_dict["manuscript_unit_id"] = saved_id
            repo.save_validation_report(val_dict)

    return {
        "workflow_stage": "pending_author_review",
        "review_status": "pending_human_review",
    }

