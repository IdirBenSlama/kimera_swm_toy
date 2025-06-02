"""
Linguistic analysis module for Kimera SWM

This module implements multi-language analysis capabilities including
the "1+3+1" rule from SWM methodology.
"""

from .multi_language_analyzer import (
    MultiLanguageAnalyzer, 
    LanguageFamily, 
    select_unrelated_languages
)

__all__ = [
    'MultiLanguageAnalyzer', 
    'LanguageFamily', 
    'select_unrelated_languages'
]