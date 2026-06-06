"""Preprocessing stubs for person, garment, and pose preparation.

In production, each preprocessing step would call a real segmentation model,
pose estimation model, or image processing pipeline. This module defines the
interface and returns deterministic placeholder results so the pipeline
contract is testable without GPU dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class PersonSegmentation:
    """Segmentation mask for a person image."""

    mask_uri: Optional[str] = None
    body_visibility: float = 1.0
    occlusion_type: str = "none"


@dataclass(frozen=True)
class GarmentSegmentation:
    """Segmentation mask for a garment image."""

    mask_uri: Optional[str] = None
    garment_area_ratio: float = 0.0


@dataclass(frozen=True)
class PoseEstimation:
    """Pose keypoints and body representation for a person image."""

    keypoints: list[tuple[float, float]] = field(default_factory=list)
    pose_type: str = "standing"
    confidence: float = 0.0
    densepose_uri: Optional[str] = None


@dataclass(frozen=True)
class PreprocessedInputs:
    """All preprocessing outputs bundled for the generation engine."""

    person_segmentation: PersonSegmentation
    garment_segmentation: GarmentSegmentation
    pose_estimation: PoseEstimation
    normalized_person_uri: Optional[str] = None
    normalized_garment_uri: Optional[str] = None


class PersonSegmenter:
    """Stub for person segmentation model.

    Production implementation would use a human parsing model such as
    SCHP, CDGNet, or a custom segmentation network.
    """

    def segment(self, person_image_uri: str) -> PersonSegmentation:
        return PersonSegmentation(
            mask_uri=f"seg://person/{person_image_uri}",
            body_visibility=1.0,
            occlusion_type="none",
        )


class GarmentSegmenter:
    """Stub for garment segmentation model.

    Production implementation would extract the garment mask and compute
    garment area for quality checks.
    """

    def segment(self, garment_image_uri: str) -> GarmentSegmentation:
        return GarmentSegmentation(
            mask_uri=f"seg://garment/{garment_image_uri}",
            garment_area_ratio=0.35,
        )


class PoseEstimator:
    """Stub for pose estimation model.

    Production implementation would use OpenPose, DensePose, or a custom
    pose estimation network to extract body keypoints and dense body maps.
    """

    def estimate(self, person_image_uri: str) -> PoseEstimation:
        return PoseEstimation(
            keypoints=[(0.5, 0.1)] * 17,  # 17-keypoint placeholder
            pose_type="standing",
            confidence=0.95,
            densepose_uri=f"densepose://person/{person_image_uri}",
        )


class PreprocessingPipeline:
    """Orchestrates all preprocessing steps before generation.

    This separates preprocessing from the main pipeline so each step
    can be tested, monitored, and optimized independently.
    """

    def __init__(self) -> None:
        self.person_segmenter = PersonSegmenter()
        self.garment_segmenter = GarmentSegmenter()
        self.pose_estimator = PoseEstimator()

    def run(
        self,
        person_image_uri: str,
        garment_image_uri: str,
    ) -> PreprocessedInputs:
        person_seg = self.person_segmenter.segment(person_image_uri)
        garment_seg = self.garment_segmenter.segment(garment_image_uri)
        pose = self.pose_estimator.estimate(person_image_uri)

        return PreprocessedInputs(
            person_segmentation=person_seg,
            garment_segmentation=garment_seg,
            pose_estimation=pose,
            normalized_person_uri=person_image_uri,
            normalized_garment_uri=garment_image_uri,
        )
