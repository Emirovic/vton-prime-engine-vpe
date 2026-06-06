"""Pipeline interfaces for baseline and proprietary virtual try-on engines."""

from __future__ import annotations

from dataclasses import asdict
from time import perf_counter
from typing import Optional

from .config import EngineConfig
from .schemas import QualityMode, TryOnRequest, TryOnResponse


class VTONPipeline:
    """A small, testable pipeline contract for VTON engine development.

    The starter implementation returns a deterministic placeholder URI. In a
    production implementation, the private methods would call preprocessing,
    baseline provider inference, proprietary model inference, and postprocessing.
    """

    def __init__(self, config: Optional[EngineConfig] = None) -> None:
        self.config = config or EngineConfig()

    def run(self, request: TryOnRequest) -> TryOnResponse:
        self._validate_request(request)
        started = perf_counter()

        prepared = self._preprocess(request)
        output_uri = self._generate(prepared)
        quality_flags = self._postprocess(prepared, output_uri)

        latency_ms = max(1, int((perf_counter() - started) * 1000))
        return TryOnResponse(
            request_id=request.request_id,
            status="completed",
            engine=self.config.default_engine,
            output_image_uri=output_uri,
            latency_ms=latency_ms,
            quality_flags=quality_flags,
            metadata={
                "brand_id": request.brand_id,
                "garment_category": request.garment_category.value,
                "quality_mode": request.quality_mode.value,
            },
        )

    def _validate_request(self, request: TryOnRequest) -> None:
        if not request.person_image_uri.strip():
            raise ValueError("person_image_uri is required")
        if not request.garment_image_uri.strip():
            raise ValueError("garment_image_uri is required")

    def _preprocess(self, request: TryOnRequest) -> dict[str, object]:
        payload = asdict(request)
        payload["preprocessing"] = {
            "person_segmentation": "pending-model",
            "garment_segmentation": "pending-model",
            "pose_keypoints": "pending-model",
        }
        return payload

    def _generate(self, prepared_request: dict[str, object]) -> str:
        request_id = str(prepared_request["request_id"])
        quality_mode = prepared_request["quality_mode"]
        suffix = "preview" if quality_mode == QualityMode.PREVIEW else "production"
        return f"vpe://generated/{request_id}_{suffix}.jpg"

    def _postprocess(
        self,
        prepared_request: dict[str, object],
        output_uri: str,
    ) -> list[str]:
        flags: list[str] = []
        if prepared_request.get("garment_category") == "unknown":
            flags.append("unknown_garment_category")
        if not output_uri:
            flags.append("missing_output")
        return flags
