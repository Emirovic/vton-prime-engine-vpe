"""Engine adapters for baseline and proprietary VTON generation."""

from dataclasses import dataclass
from typing import Optional

from .schemas import QualityMode, TryOnRequest


@dataclass(frozen=True)
class EngineResult:
    engine_name: str
    output_image_uri: str
    provider_reference: Optional[str] = None


class BaselineProviderAdapter:
    """Adapter boundary for a Fashn.ai VTON-1.5-style baseline provider.

    The starter implementation is deterministic. In production, this class would
    own authentication, provider request formatting, retries, and response parsing.
    """

    engine_name = "baseline-fashn-vton-1.5"

    def generate(self, request: TryOnRequest) -> EngineResult:
        return EngineResult(
            engine_name=self.engine_name,
            output_image_uri=f"baseline://fashn-vton-1.5/{request.request_id}.jpg",
            provider_reference=f"baseline_job_{request.request_id}",
        )


class ProprietaryVPEAdapter:
    """Adapter boundary for the proprietary VPE model path."""

    engine_name = "vpe-proprietary"

    def generate(self, request: TryOnRequest) -> EngineResult:
        suffix = "preview" if request.quality_mode == QualityMode.PREVIEW else "production"
        return EngineResult(
            engine_name=self.engine_name,
            output_image_uri=f"vpe://generated/{request.request_id}_{suffix}.jpg",
        )
