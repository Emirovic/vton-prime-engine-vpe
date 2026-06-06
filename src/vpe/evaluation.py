"""Fashion-specific evaluation helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class QualityScores:
    realism: float
    garment_fidelity: float
    pose_correctness: float
    identity_preservation: float
    commercial_usability: float

    @property
    def average(self) -> float:
        values = [
            self.realism,
            self.garment_fidelity,
            self.pose_correctness,
            self.identity_preservation,
            self.commercial_usability,
        ]
        return sum(values) / len(values)


def severe_artifact_rate(total_outputs: int, severe_failures: int) -> float:
    if total_outputs <= 0:
        raise ValueError("total_outputs must be greater than zero")
    if severe_failures < 0:
        raise ValueError("severe_failures cannot be negative")
    if severe_failures > total_outputs:
        raise ValueError("severe_failures cannot exceed total_outputs")
    return severe_failures / total_outputs


def is_release_candidate(
    scores: QualityScores,
    severe_rate: float,
    latency_ms: int,
    latency_budget_ms: int,
    minimum_score: float = 4.0,
    max_severe_rate: float = 0.02,
) -> bool:
    return (
        scores.average >= minimum_score
        and severe_rate <= max_severe_rate
        and latency_ms <= latency_budget_ms
    )

