"""
Pattern abstraction module for Kimera SWM

This module implements deep pattern extraction according to SWM methodology,
including functional, structural, dynamic, and relational patterns.
"""

from .abstraction_engine import (
    PatternAbstractionEngine,
    PatternType,
    FunctionalPattern,
    StructuralPattern,
    DynamicPattern,
    RelationalPattern,
    AbstractedPatternSet
)

__all__ = [
    'PatternAbstractionEngine',
    'PatternType',
    'FunctionalPattern',
    'StructuralPattern',
    'DynamicPattern',
    'RelationalPattern',
    'AbstractedPatternSet'
]