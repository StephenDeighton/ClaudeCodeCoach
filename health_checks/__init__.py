"""Health check detector registry."""

from typing import List, Type
from .base import BaseDetector

# Registry of all detector classes
_detectors: List[Type[BaseDetector]] = []


def register(detector_class: Type[BaseDetector]) -> Type[BaseDetector]:
    """Decorator to register a health check detector."""
    _detectors.append(detector_class)
    return detector_class


def get_all_detectors() -> List[BaseDetector]:
    """Return instances of all registered detectors."""
    return [cls() for cls in _detectors]
