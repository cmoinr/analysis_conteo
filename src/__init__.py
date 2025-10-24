"""Analysis Conteo - Event data analysis and visualization package."""

__version__ = '2.0.0'
__author__ = 'Analysis Team'

from .data import load_events_data
from .stats import descriptive, advanced
from .viz import basic, advanced as viz_advanced

__all__ = [
    'load_events_data',
    'descriptive',
    'advanced',
    'basic',
    'viz_advanced',
]
