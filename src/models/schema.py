"""
================================================================================
Module: src.models.schema
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Pydantic schemas establishing the canonical extensible data model
             for comparative sutra analysis and the Udyoga Bhashya manuscript.
             Supports multilingual fields across English (en), Hindi (hi), and
             Marathi (mr).
================================================================================
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class MultilingualText(BaseModel):
    """
    ----------------------------------------------------------------------------
    Class: MultilingualText
    ----------------------------------------------------------------------------
    Purpose:
        Represents an extensible multilingual text node supporting English (en),
        Hindi (hi), and Marathi (mr). English is the primary default, while Hindi
        and Marathi can be populated progressively.

    Attributes:
        en (str): Primary English exposition / translation.
        hi (Optional[str]): Hindi translation or commentary (nullable).
        mr (Optional[str]): Marathi translation or commentary (nullable).
    ----------------------------------------------------------------------------
    """
    en: str = Field(
        ...,
        description="Primary English explanation or synthesis."
    )
    hi: Optional[str] = Field(
        default=None,
        description="Hindi explanation or synthesis (optional/progressive)."
    )
    mr: Optional[str] = Field(
        default=None,
        description="Marathi explanation or synthesis (optional/progressive)."
    )


class SutraItem(BaseModel):
    """
    ----------------------------------------------------------------------------
    Class: SutraItem
    ----------------------------------------------------------------------------
    Purpose:
        Represents an individual classical aphorism (from either Narada Bhakti
        Sutra or Shandilya Bhakti Sutra) with its canonical numbering, Devanagari
        verse, and multilingual vishleshan (analysis).

    Attributes:
        sutra_no (str): The aphorism identifier or number (e.g., '1', '1.1').
        sanskrit (str): Original Sanskrit verse in Devanagari script.
        vishleshan (MultilingualText): Detailed multilingual analytical commentary.
    ----------------------------------------------------------------------------
    """
    sutra_no: str = Field(
        ...,
        description="Sutra aphorism numbering string (e.g., '1', '2')."
    )
    sanskrit: str = Field(
        ...,
        description="Canonical Sanskrit verse in authentic Devanagari script."
    )
    vishleshan: MultilingualText = Field(
        ...,
        description="Multilingual analysis and contextual breakdown."
    )


class SutraPairManuscript(BaseModel):
    """
    ----------------------------------------------------------------------------
    Class: SutraPairManuscript
    ----------------------------------------------------------------------------
    Purpose:
        Adheres strictly to the specification schema for a single comparative
        unit pairing a Narada Bhakti Sutra with a corresponding Shandilya Bhakti
        Sutra, classified under a unifying philosophical theme, and crowned by
        the synthesized Udyoga Bhashya.

    Attributes:
        pair_id (str): Unique pairing identifier (e.g., 'PAIR-001').
        theme (str): Unifying philosophical theme (e.g., 'Definition of Bhakti').
        narada_sutra (SutraItem): Narada Bhakti Sutra entry.
        shandilya_sutra (SutraItem): Shandilya Bhakti Sutra entry.
        udyoga_bhashya_synthesis (MultilingualText): Comparative philosophical synthesis.
    ----------------------------------------------------------------------------
    """
    pair_id: str = Field(
        ...,
        description="Unique identifier for the comparative sutra pair."
    )
    theme: str = Field(
        ...,
        description="Central philosophical theme connecting both aphorisms."
    )
    narada_sutra: SutraItem = Field(
        ...,
        description="The Narada Bhakti Sutra entry with Devanagari text and vishleshan."
    )
    shandilya_sutra: SutraItem = Field(
        ...,
        description="The Shandilya Bhakti Sutra entry with Devanagari text and vishleshan."
    )
    udyoga_bhashya_synthesis: MultilingualText = Field(
        ...,
        description="The comprehensive comparative Udyoga Bhashya synthesis."
    )


class ManuscriptCollection(BaseModel):
    """
    ----------------------------------------------------------------------------
    Class: ManuscriptCollection
    ----------------------------------------------------------------------------
    Purpose:
        Container wrapping a sequence of SutraPairManuscript records representing
        the complete or partial draft of the compiled Udyoga Sutra treatise.

    Attributes:
        title (str): Title of the compilation.
        author (str): Technical or editorial author attribution.
        manuscript (List[SutraPairManuscript]): Sequence of paired sutra analyses.
    ----------------------------------------------------------------------------
    """
    title: str = Field(
        default="SK Sutras - by Shri Shripad Kulkarni: Udyoga Sutra",
        description="Formal title of the treatise compilation."
    )
    author: str = Field(
        default="Hiranyam AI Labs & Shri Shripad Kulkarni",
        description="Attribution of technical and spiritual authors."
    )
    manuscript: List[SutraPairManuscript] = Field(
        default_factory=list,
        description="Collection of comparative sutra manuscript records."
    )
