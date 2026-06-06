import unittest

from src.vpe.evaluation import QualityScores, is_release_candidate, severe_artifact_rate
from src.vpe.pipeline import VTONPipeline
from src.vpe.schemas import GarmentCategory, QualityMode, TryOnRequest


class VTONPipelineTests(unittest.TestCase):
    def test_pipeline_returns_completed_response(self) -> None:
        request = TryOnRequest(
            person_image_uri="sample_person.jpg",
            garment_image_uri="sample_garment.jpg",
            garment_category=GarmentCategory.TOP,
            brand_id="demo-brand",
            quality_mode=QualityMode.PRODUCTION,
        )

        response = VTONPipeline().run(request)

        self.assertEqual(response.status, "completed")
        self.assertEqual(response.request_id, request.request_id)
        self.assertEqual(response.metadata["brand_id"], "demo-brand")
        self.assertTrue(response.output_image_uri.startswith("vpe://generated/"))
        self.assertEqual(response.quality_flags, [])

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


if __name__ == "__main__":
    unittest.main()

