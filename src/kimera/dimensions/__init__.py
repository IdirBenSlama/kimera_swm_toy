"""
Kimera Dimensions Module - Multi-dimensional analysis for SWM Geoids
"""

from .geoid_v2 import GeoidV2, GeoidDimension, DimensionType, init_geoid_v2

__all__ = [
    'GeoidV2',
    'GeoidDimension',
    'DimensionType',
    'init_geoid_v2'
]