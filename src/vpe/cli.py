"""Command-line entry point for the VPE starter pipeline."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .pipeline import VTONPipeline
from .schemas import EngineMode, GarmentCategory, QualityMode, TryOnRequest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a VTON-Prime Engine try-on job")
    parser.add_argument("--person", required=True, help="Person image URI or path")
    parser.add_argument("--garment", required=True, help="Garment image URI or path")
    parser.add_argument(
        "--category",
        default=GarmentCategory.UNKNOWN.value,
        choices=[category.value for category in GarmentCategory],
        help="Garment category",
    )
    parser.add_argument("--brand", default=None, help="Optional brand identifier")
    parser.add_argument(
        "--quality",
        default=QualityMode.PREVIEW.value,
        choices=[mode.value for mode in QualityMode],
        help="Try-on quality mode",
    )
    parser.add_argument(
        "--engine",
        default=EngineMode.PROPRIETARY.value,
        choices=[engine.value for engine in EngineMode],
        help="Generation engine route",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    request = TryOnRequest(
        person_image_uri=args.person,
        garment_image_uri=args.garment,
        garment_category=GarmentCategory(args.category),
        brand_id=args.brand,
        quality_mode=QualityMode(args.quality),
        engine_mode=EngineMode(args.engine),
    )
    response = VTONPipeline().run(request)
    print(json.dumps(asdict(response), indent=2))


if __name__ == "__main__":
    main()
