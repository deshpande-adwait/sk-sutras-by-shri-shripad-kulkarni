"""
================================================================================
Module: src.models.schema
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Pydantic schemas establishing the canonical extensible data model
             for comparative sutra analysis, full 6-section manuscript units
             (Sections A-F), Agent 4 validation reports, and author reviews.
================================================================================
"""

import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ==============================================================================
# Legacy & Multilingual Base Primitives (Maintained for Backward Compatibility)
# ==============================================================================

class MultilingualText(BaseModel):
    """
    ----------------------------------------------------------------------------
    Class: MultilingualText
    ----------------------------------------------------------------------------
    Purpose:
        Represents an extensible multilingual text node supporting English (en),
        Hindi (hi), and Marathi (mr).
    ----------------------------------------------------------------------------
    """
    en: str = Field(..., description="Primary English text")
    hi: Optional[str] = Field(default=None, description="Hindi text")
    mr: Optional[str] = Field(default=None, description="Marathi text")


class SutraItem(BaseModel):
    """
    ----------------------------------------------------------------------------
    Class: SutraItem
    ----------------------------------------------------------------------------
    Purpose:
        Represents an individual classical aphorism (from either Narada Bhakti
        Sutra or Shandilya Bhakti Sutra) with its canonical numbering, Devanagari
        verse, and multilingual vishleshan (analysis).
    ----------------------------------------------------------------------------
    """
    sutra_no: str = Field(..., description="Sutra aphorism numbering string (e.g., '1', '2')")
    sanskrit: str = Field(..., description="Canonical Sanskrit verse in authentic Devanagari script")
    vishleshan: MultilingualText = Field(..., description="Multilingual analysis and contextual breakdown")


class SutraPairManuscript(BaseModel):
    """
    ----------------------------------------------------------------------------
    Class: SutraPairManuscript
    ----------------------------------------------------------------------------
    Purpose:
        Legacy comparative unit pairing a Narada Bhakti Sutra with a corresponding
        Shandilya Bhakti Sutra, classified under a unifying philosophical theme.
    ----------------------------------------------------------------------------
    """
    pair_id: str = Field(..., description="Unique identifier for the comparative sutra pair")
    theme: str = Field(..., description="Central philosophical theme connecting both aphorisms")
    narada_sutra: SutraItem = Field(..., description="The Narada Bhakti Sutra entry")
    shandilya_sutra: SutraItem = Field(..., description="The Shandilya Bhakti Sutra entry")
    udyoga_bhashya_synthesis: MultilingualText = Field(..., description="The comprehensive comparative Udyoga Bhashya synthesis")


class ManuscriptCollection(BaseModel):
    """Container wrapping a collection of SutraPairManuscript records."""
    title: str = Field(
        default="SK Sutras - by Shri Shripad Kulkarni: Udyoga Sutra",
        description="Formal title of the treatise compilation",
    )
    author: str = Field(
        default="Hiranyam AI Labs & Shri Shripad Kulkarni",
        description="Attribution of technical and spiritual authors",
    )
    manuscript: List[SutraPairManuscript] = Field(
        default_factory=list,
        description="Collection of comparative sutra manuscript records",
    )


# ==============================================================================
# Complete Manuscript Unit Specification (Sections A through F)
# ==============================================================================

class SourceFoundation(BaseModel):
    """Section A: Source foundation preserving authenticated provenance."""
    narada_sutra_ref: str = Field(..., description="Narada sutra number or citation (e.g. 'NBS-2')")
    narada_sanskrit: str = Field(..., description="Canonical Sanskrit text from Narada Bhakti Sutra")
    narada_provenance: str = Field(default="Narada Bhakti Sutra, Canonical 84 Aphorisms", description="Edition and provenance")
    narada_translation_en: str = Field(..., description="Authenticated English translation of Narada sutra")
    shandilya_sutra_ref: str = Field(..., description="Shandilya sutra number or citation (e.g. 'SBS-2')")
    shandilya_sanskrit: str = Field(..., description="Canonical Sanskrit text from Shandilya Bhakti Sutra")
    shandilya_provenance: str = Field(default="Shandilya Bhakti Sutra, Canonical 100 Aphorisms", description="Edition and provenance")
    shandilya_translation_en: str = Field(..., description="Authenticated English translation of Shandilya sutra")
    philosophical_relationship: str = Field(..., description="Rigorous philosophical relationship and thesis")
    selection_justification: str = Field(..., description="Scholarly justification for why this pairing is defensible")
    limitations_notes: Optional[str] = Field(default=None, description="Known tensions, boundary conditions, or limitations")


class SanskritAnalysis(BaseModel):
    """Section C: Granular Sanskrit linguistic and metrical exposition."""
    padaccheda: str = Field(..., description="Word-by-word division with Sandhi resolution")
    anvaya: str = Field(..., description="Syntactical prose order connecting subject, verb, and modifiers")
    word_meanings: str = Field(..., description="Granular word-by-word Sanskrit to English/Marathi meanings")
    grammatical_explanation: str = Field(..., description="Paninian morphological and case analysis")
    sandhi_analysis: Optional[str] = Field(default=None, description="Identification of Sandhi transitions")
    dhatu_derivation: Optional[str] = Field(default=None, description="Root Dhatu etymological derivations")
    chandas_name: str = Field(default="Anushtubh", description="Metre designation (e.g. 'Anushtubh / Sloka')")
    chandas_analysis: str = Field(..., description="Syllable counting (8x4=32 syllables) and laghu/guru metrical evaluation")


class MultilingualTranslations(BaseModel):
    """Section D: Scholarly translations preserving philosophical nuance."""
    translation_en: str = Field(..., description="Philosophical English translation")
    translation_hi: str = Field(..., description="Rigorous Hindi translation")
    translation_mr: str = Field(..., description="Authentic Marathi translation")


class FourFoldCommentary(BaseModel):
    """Section E: Four-Fold Commentary on conduct, society, and modern enterprise."""
    nirukta: str = Field(..., description="1. Nirukta — terminology, linguistic nuance, and etymology")
    vyavahara_dharma: str = Field(..., description="2. Vyavahara-Dharma — practical conduct, ethics, and professional behaviour")
    lokasangraha: str = Field(..., description="3. Lokasangraha — collective societal welfare, trusteeship, and duty")
    modern_leadership_synthesis: str = Field(..., description="4. Modern Leadership Synthesis — management, corporate governance, enterprise")


class ManuscriptUnit(BaseModel):
    """
    ----------------------------------------------------------------------------
    Class: ManuscriptUnit
    ----------------------------------------------------------------------------
    Purpose:
        Represents the definitive, complete authoring unit for a synthesized
        Udyoga Sutra, containing all mandatory sections A through F, metrical
        analyses, multilingual commentaries, and governance state.
    ----------------------------------------------------------------------------
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Primary database UUID")
    unit_id: str = Field(..., description="Treatise unit identifier (e.g., 'UDYOGA-SUTRA-001')")
    version_number: int = Field(default=1, description="Version increment number")
    is_current: bool = Field(default=True, description="True if active latest version")
    parent_version_id: Optional[str] = Field(default=None, description="Pointer to prior version ID if revised")

    chapter_number: int = Field(default=1, description="Chapter index")
    sutra_number: str = Field(..., description="Formal Udyoga Sutra numbering (e.g., '1', '2')")
    theme: str = Field(..., description="Central philosophical and ethical theme")
    central_principle: str = Field(..., description="Key aphoristic principle")
    composition_label: str = Field(
        default="Original contemporary composition",
        description="Mandatory label explicitly distinguishing modern work from ancient canon",
    )

    # Section A
    source_foundation: SourceFoundation = Field(..., description="Section A: Source foundation")

    # Section B: The Original Sanskrit Composition
    original_sanskrit_verse: str = Field(..., description="Section B: New Sanskrit composition in Devanagari")
    intended_meaning: str = Field(..., description="Section B: Intended philosophical and spiritual essence")

    # Section C
    sanskrit_analysis: SanskritAnalysis = Field(..., description="Section C: Sanskrit grammatical & metrical analysis")

    # Section D
    translations: MultilingualTranslations = Field(..., description="Section D: English, Hindi, and Marathi translations")

    # Section E
    commentary: FourFoldCommentary = Field(..., description="Section E: Four-Fold Commentary")

    # Section F: Additional Info & Governance
    philosophical_significance: Optional[str] = Field(default=None, description="Scholarly background and relevance")
    contemporary_examples: Optional[str] = Field(default=None, description="Case examples from business and leadership")
    limitations_notes: Optional[str] = Field(default=None, description="Boundary conditions and philosophical cautions")
    cross_references: Optional[str] = Field(default=None, description="References to Gita, Upanishads, Arthashastra")

    validation_status: str = Field(default="PENDING_VALIDATION", description="'PASS', 'FAIL', 'NEEDS_REVISION', 'HUMAN_REVIEW_REQUIRED'")
    approval_status: str = Field(default="PENDING_REVIEW", description="'PENDING_REVIEW', 'APPROVED', 'REJECTED', 'REVISION_REQUESTED', 'SCHOLAR_REVIEW', 'ON_HOLD'")
    approved_by: Optional[str] = Field(default=None, description="Author approver name (Shri Shripad Kulkarni)")
    approved_at: Optional[str] = Field(default=None, description="Approval timestamp")


# ==============================================================================
# Agent 4 Independent Validator Data Contracts
# ==============================================================================

class ValidationFinding(BaseModel):
    """Specific location-targeted finding generated by Agent 4."""
    gate: str = Field(..., description="'source_authenticity', 'philosophical_integrity', 'sanskrit_grammar', 'chandas_metre', 'translations', 'commentary', 'originality'")
    severity: str = Field(..., description="'CRITICAL', 'MAJOR', 'MINOR', 'INFO'")
    location: str = Field(..., description="Specific section and line (e.g. 'Section C: Chandas Pada 2')")
    issue_description: str = Field(..., description="Description of the defect or deviation")
    suggested_correction: str = Field(..., description="Actionable recommendation for Agent 3 revision")


class ValidationReport(BaseModel):
    """
    ----------------------------------------------------------------------------
    Class: ValidationReport
    ----------------------------------------------------------------------------
    Purpose:
        Complete scholarly validation report issued by Agent 4 for a manuscript unit.
    ----------------------------------------------------------------------------
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    manuscript_unit_id: str = Field(..., description="Target manuscript unit ID")
    execution_id: str = Field(..., description="Execution trace identifier")
    validator_model_id: str = Field(default="gpt-4o", description="Validator LLM model ID")
    overall_status: str = Field(..., description="'PASS', 'FAIL', 'NEEDS_REVISION', 'HUMAN_REVIEW_REQUIRED'")
    revision_cycle: int = Field(default=0, description="Current revision iteration (0 to 3)")

    source_authenticity_check: str = Field(default="PASS")
    philosophical_integrity_check: str = Field(default="PASS")
    sanskrit_grammar_check: str = Field(default="PASS")
    chandas_metre_check: str = Field(default="PASS")
    translations_check: str = Field(default="PASS")
    commentary_check: str = Field(default="PASS")
    originality_repetition_check: str = Field(default="PASS")

    findings: List[ValidationFinding] = Field(default_factory=list)
    critical_issues_count: int = Field(default=0)
    major_issues_count: int = Field(default=0)
    minor_issues_count: int = Field(default=0)
    required_corrections: str = Field(default="")
