# src package initialization
# This makes the src folder a proper Python package

from .data_loader import DataLoader
from .validators import DataValidator, Issue
from .risk_engine import RiskEngine, RiskScore
from .report_generator import ReportGenerator
from .main import AutomatedEDA

__all__ = [
    'DataLoader',
    'DataValidator',
    'Issue',
    'RiskEngine',
    'RiskScore',
    'ReportGenerator',
    'AutomatedEDA'
]

__version__ = '1.0.0'
