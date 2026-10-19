"""
================================================================================
Package: src.database
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Relational persistence and repository layer for the SK Sutras platform.
             Provides robust SQLite storage for manuscript versions, human-in-the-loop
             review logs, and accessibility preferences.
================================================================================
"""

from src.database.repository import ManuscriptRepository

__all__ = ["ManuscriptRepository"]
