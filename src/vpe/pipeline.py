"""Pipeline interfaces for baseline and proprietary virtual try-on engines."""

from __future__ import annotations

from dataclasses import asdict
from time import perf_counter
from typing import Optional

from .config import EngineConfig
from .engines import BaselineProviderAdapter, EngineResult, ProprietaryVPEAdapter
from .preprocessing import PreprocessedInputs, PreprocessingPipeline
from .schemas import EngineMode, TryOnRequest, TryOnResponse


class VTONPipeline:
    """A small, testable pipeline contract for VTON engine development.

    The starter implementation returns a deterministic placeholder URI. In a
    production implementation, the private methods would call preprocessing,
    baseline provider inference, proprietary model inference, and postprocessing.
    """

    def __init__(self, config: Optional[EngineConfig] = None) -> None:
        self.config = config or EngineConfig()
        self.baseline_engine = BaselineProviderAdapter()
        self.proprietary_engine = ProprietaryVPEAdapter()
        self.preprocessing = PreprocessingPipeline()

    def run(self, request: TryOnRequest) -> TryOnResponse:
        self._validate_request(request)
        started = perf_counter()

        prepared = self._preprocess(request)
        engine_result = self._generate(request)
        quality_flags = self._postprocess(prepared, engine_result)

        latency_ms = max(1, int((perf_counter() - started) * 1000))
        return TryOnResponse(
            request_id=request.request_id,
            status="completed",
            engine=engine_result.engine_name,
            output_image_uri=engine_result.output_image_uri,
            latency_ms=latency_ms,
            quality_flags=quality_flags,
            metadata={
                "brand_id": request.brand_id,
                "garment_category": request.garment_category.value,
                "quality_mode": request.quality_mode.value,
                "engine_mode": request.engine_mode.value,
                "provider_reference": engine_result.provider_reference,
            },
        )

    def _validate_request(self, request: TryOnRequest) -> None:
        if not request.person_image_uri.strip():
            raise ValueError("person_image_uri is required")
        if not request.garment_image_uri.strip():
            raise ValueError("garment_image_uri is required")

    def _preprocess(self, request: TryOnRequest) -> dict[str, object]:
        preprocessed = self.preprocessing.run(
            person_image_uri=request.person_image_uri,
            garment_image_uri=request.garment_image_uri,
        )
        payload = asdict(request)
        payload["preprocessing"] = {
            "person_segmentation": preprocessed.person_segmentation.mask_uri,
            "garment_segmentation": preprocessed.garment_segmentation.mask_uri,
            "pose_keypoints": preprocessed.pose_estimation.pose_type,
            "densepose": preprocessed.pose_estimation.densepose_uri,
            "pose_confidence": preprocessed.pose_estimation.confidence,
        }
        return payload

    def _generate(self, request: TryOnRequest) -> EngineResult:
        if request.engine_mode == EngineMode.BASELINE:
            return self.baseline_engine.generate(request)
        return self.proprietary_engine.generate(request)

    def _postprocess(
        self,
        prepared_request: dict[str, object],
        engine_result: EngineResult,
    ) -> list[str]:
        flags: list[str] = []
        if prepared_request.get("garment_category") == "unknown":
            flags.append("unknown_garment_category")
        if not engine_result.output_image_uri:
            flags.append("missing_output")
        return flags
