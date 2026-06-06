"""Configuration values for the VPE starter pipeline."""

from dataclasses import dataclass


@dataclass(frozen=True)
class EngineConfig:
    """Runtime configuration for a try-on engine."""

    default_engine: str = "vpe-prototype"
    preview_latency_budget_ms: int = 2500
    production_latency_budget_ms: int = 6000
    severe_artifact_threshold: float = 0.02
    minimum_qa_score: float = 4.0

