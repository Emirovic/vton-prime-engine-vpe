"""Typed request and response objects for VTON jobs."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from uuid import uuid4


class GarmentCategory(str, Enum):
    TOP = "top"
    DRESS = "dress"
    JACKET = "jacket"
    OUTERWEAR = "outerwear"
    BOTTOM = "bottom"
    UNKNOWN = "unknown"


class QualityMode(str, Enum):
    PREVIEW = "preview"
    PRODUCTION = "production"


class EngineMode(str, Enum):
    BASELINE = "baseline"
    PROPRIETARY = "proprietary"


@dataclass(frozen=True)
class TryOnRequest:
    """Input contract for a virtual try-on request."""

    person_image_uri: str
    garment_image_uri: str
    garment_category: GarmentCategory = GarmentCategory.UNKNOWN
    brand_id: Optional[str] = None
    quality_mode: QualityMode = QualityMode.PREVIEW
    engine_mode: EngineMode = EngineMode.PROPRIETARY
    request_id: str = field(default_factory=lambda: f"vpe_{uuid4().hex[:12]}")


@dataclass(frozen=True)
class TryOnResponse:
    """Output contract returned by the pipeline."""

    request_id: str
    status: str
    engine: str
    output_image_uri: Optional[str]
    latency_ms: int
    quality_flags: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)
