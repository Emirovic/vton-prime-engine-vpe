import unittest

from src.vpe.evaluation import QualityScores, is_release_candidate, severe_artifact_rate
from src.vpe.pipeline import VTONPipeline
from src.vpe.schemas import EngineMode, GarmentCategory, QualityMode, TryOnRequest


class VTONPipelineTests(unittest.TestCase):
    def test_pipeline_returns_completed_response(self) -> None:
        request = TryOnRequest(
            person_image_uri="sample_person.jpg",
            garment_image_uri="sample_garment.jpg",
            garment_category=GarmentCategory.TOP,
            brand_id="demo-brand",
            quality_mode=QualityMode.PRODUCTION,
            engine_mode=EngineMode.PROPRIETARY,
        )

        response = VTONPipeline().run(request)

        self.assertEqual(response.status, "completed")
        self.assertEqual(response.request_id, request.request_id)
        self.assertEqual(response.metadata["brand_id"], "demo-brand")
        self.assertEqual(response.engine, "vpe-proprietary")
        self.assertTrue(response.output_image_uri.startswith("vpe://generated/"))
        self.assertEqual(response.quality_flags, [])

    def test_pipeline_can_route_to_baseline_provider(self) -> None:
        request = TryOnRequest(
            person_image_uri="sample_person.jpg",
            garment_image_uri="sample_garment.jpg",
            garment_category=GarmentCategory.DRESS,
            engine_mode=EngineMode.BASELINE,
        )

        response = VTONPipeline().run(request)

        self.assertEqual(response.engine, "baseline-fashn-vton-1.5")
        self.assertTrue(response.output_image_uri.startswith("baseline://fashn-vton-1.5/"))
        self.assertIsNotNone(response.metadata["provider_reference"])

    def test_pipeline_rejects_missing_person_image(self) -> None:
        request = TryOnRequest(
            person_image_uri="",
            garment_image_uri="sample_garment.jpg",
        )

        with self.assertRaises(ValueError):
            VTONPipeline().run(request)

    def test_unknown_category_is_flagged(self) -> None:
        request = TryOnRequest(
            person_image_uri="sample_person.jpg",
            garment_image_uri="sample_garment.jpg",
        )

        response = VTONPipeline().run(request)

        self.assertIn("unknown_garment_category", response.quality_flags)


class EvaluationTests(unittest.TestCase):
    def test_severe_artifact_rate(self) -> None:
        self.assertEqual(severe_artifact_rate(100, 2), 0.02)

    def test_severe_artifact_rate_zero_total_raises(self) -> None:
        with self.assertRaises(ValueError):
            severe_artifact_rate(0, 0)

    def test_severe_artifact_rate_negative_failures_raises(self) -> None:
        with self.assertRaises(ValueError):
            severe_artifact_rate(100, -1)

    def test_severe_artifact_rate_failures_exceed_total_raises(self) -> None:
        with self.assertRaises(ValueError):
            severe_artifact_rate(10, 20)

    def test_release_candidate_gate(self) -> None:
        scores = QualityScores(
            realism=4.4,
            garment_fidelity=4.2,
            pose_correctness=4.1,
            identity_preservation=4.5,
            commercial_usability=4.3,
        )

        self.assertTrue(
            is_release_candidate(
                scores=scores,
                severe_rate=0.01,
                latency_ms=4300,
                latency_budget_ms=6000,
            )
        )

    def test_release_candidate_fails_on_low_scores(self) -> None:
        scores = QualityScores(
            realism=2.0,
            garment_fidelity=2.5,
            pose_correctness=3.0,
            identity_preservation=2.0,
            commercial_usability=2.5,
        )

        self.assertFalse(
            is_release_candidate(
                scores=scores,
                severe_rate=0.01,
                latency_ms=4000,
                latency_budget_ms=6000,
            )
        )

    def test_release_candidate_fails_on_high_artifact_rate(self) -> None:
        scores = QualityScores(
            realism=4.5,
            garment_fidelity=4.5,
            pose_correctness=4.5,
            identity_preservation=4.5,
            commercial_usability=4.5,
        )

        self.assertFalse(
            is_release_candidate(
                scores=scores,
                severe_rate=0.10,
                latency_ms=4000,
                latency_budget_ms=6000,
            )
        )

    def test_release_candidate_fails_on_latency_budget(self) -> None:
        scores = QualityScores(
            realism=4.5,
            garment_fidelity=4.5,
            pose_correctness=4.5,
            identity_preservation=4.5,
            commercial_usability=4.5,
        )

        self.assertFalse(
            is_release_candidate(
                scores=scores,
                severe_rate=0.01,
                latency_ms=8000,
                latency_budget_ms=6000,
            )
        )

    def test_quality_scores_average(self) -> None:
        scores = QualityScores(
            realism=5.0,
            garment_fidelity=4.0,
            pose_correctness=3.0,
            identity_preservation=4.0,
            commercial_usability=4.0,
        )
        self.assertAlmostEqual(scores.average, 4.0)


class PreprocessingTests(unittest.TestCase):
    def test_preprocessing_pipeline_returns_all_components(self) -> None:
        from src.vpe.preprocessing import PreprocessingPipeline

        pipeline = PreprocessingPipeline()
        result = pipeline.run("person.jpg", "garment.jpg")

        self.assertIsNotNone(result.person_segmentation.mask_uri)
        self.assertIsNotNone(result.garment_segmentation.mask_uri)
        self.assertIsNotNone(result.pose_estimation.densepose_uri)
        self.assertEqual(result.pose_estimation.pose_type, "standing")
        self.assertEqual(len(result.pose_estimation.keypoints), 17)
        self.assertGreater(result.pose_estimation.confidence, 0.0)

    def test_preprocessing_preserves_input_uris(self) -> None:
        from src.vpe.preprocessing import PreprocessingPipeline

        pipeline = PreprocessingPipeline()
        result = pipeline.run("test_person.jpg", "test_garment.jpg")

        self.assertEqual(result.normalized_person_uri, "test_person.jpg")
        self.assertEqual(result.normalized_garment_uri, "test_garment.jpg")


class PipelineEdgeCaseTests(unittest.TestCase):
    def test_whitespace_only_person_uri_raises(self) -> None:
        request = TryOnRequest(
            person_image_uri="   ",
            garment_image_uri="sample_garment.jpg",
        )
        with self.assertRaises(ValueError):
            VTONPipeline().run(request)

    def test_whitespace_only_garment_uri_raises(self) -> None:
        request = TryOnRequest(
            person_image_uri="sample_person.jpg",
            garment_image_uri="  ",
        )
        with self.assertRaises(ValueError):
            VTONPipeline().run(request)

    def test_response_contains_preprocessing_data(self) -> None:
        request = TryOnRequest(
            person_image_uri="sample_person.jpg",
            garment_image_uri="sample_garment.jpg",
            garment_category=GarmentCategory.DRESS,
            engine_mode=EngineMode.PROPRIETARY,
        )
        response = VTONPipeline().run(request)
        self.assertEqual(response.status, "completed")
        self.assertGreater(response.latency_ms, 0)

    def test_all_garment_categories_are_accepted(self) -> None:
        for category in GarmentCategory:
            request = TryOnRequest(
                person_image_uri="sample_person.jpg",
                garment_image_uri="sample_garment.jpg",
                garment_category=category,
            )
            response = VTONPipeline().run(request)
            self.assertEqual(response.status, "completed")


if __name__ == "__main__":
    unittest.main()

