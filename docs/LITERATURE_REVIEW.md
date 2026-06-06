# Related Work and Competitive Landscape

## 1. Purpose

This document provides context on the current state of virtual try-on research and industry solutions. Understanding existing approaches helps VPE-1.0 make informed architecture decisions and identify where to invest proprietary R&D effort.

## 2. Academic State of the Art

### Diffusion-Based Virtual Try-On

Recent virtual try-on research has converged on diffusion-based architectures, which generate high-quality images through iterative denoising. Key works include:

#### IDM-VTON (2024)
- **Approach:** Improves the cross-attention mechanism for garment-person composition by using an image-based dual encoding strategy. The garment is encoded at both high-level semantic and low-level detail levels.
- **Strengths:** Strong garment fidelity, preserves fine details like logos and textures. Achieves state-of-the-art results on VITON-HD and DressCode benchmarks.
- **Weaknesses:** Relatively high inference cost due to dual encoding. Pose-robustness on extreme poses is still limited.
- **VPE Relevance:** The dual garment encoding strategy is directly relevant to the enhanced cross-attention encoding planned for VPE.

#### OOTDiffusion (2024)
- **Approach:** Outfitting over a diffusion model with a learning-based feature fusion approach. Uses outfitting UNet to learn garment features independently.
- **Strengths:** Good generalization across garment types. Clean separation of garment and person encoding.
- **Weaknesses:** Struggles with complex poses and occluded garments. Multi-view consistency is not addressed.
- **VPE Relevance:** The independent garment feature learning approach aligns with VPE's garment encoder design.

#### StableVITON (2024)
- **Approach:** Extends Stable Diffusion with a zero cross-attention block for try-on. Avoids the need for paired training data by using a novel semantic correspondence module.
- **Strengths:** Generates realistic results with minimal paired data. Works with Stable Diffusion ecosystem.
- **Weaknesses:** Quality drops on non-standard body types and poses. Brand-specific adaptation is not explored.
- **VPE Relevance:** The zero cross-attention approach could inform VPE's cross-attention design. The unpaired training idea reduces dataset requirements.

#### GP-VTON (2023)
- **Approach:** Focuses on garment preservation through a warping module and a generation module. Uses DensePose for body representation.
- **Strengths:** Strong garment shape preservation. DensePose conditioning improves body-garment alignment.
- **Weaknesses:** Warping artifacts can appear on garments with complex patterns. Two-stage pipeline adds latency.
- **VPE Relevance:** DensePose conditioning is part of VPE's preprocessing plan. The warping module approach should be evaluated against direct diffusion generation.

#### CatVTON (2024)
- **Approach:** A simple yet effective concatenation-based approach that avoids complex cross-attention or warping. Uses lightweight adaptation to a pre-trained diffusion model.
- **Strengths:** Simple architecture with competitive quality. Lower training and inference cost.
- **Weaknesses:** Less control over fine-grained garment details. Limited pose handling.
- **VPE Relevance:** Shows that simpler architectures can be competitive. Useful as a baseline comparison for VPE.

### Pose Estimation and Body Representation

| Method | Use in VTON | Pros | Cons |
| --- | --- | --- | --- |
| OpenPose | Keypoint conditioning | Well-established, fast | Missing body shape detail |
| DensePose | Dense body surface map | Rich body information | Heavier compute |
| Human parsing | Semantic body segments | Useful for occlusion handling | Annotation-dependent |
| SMPL/SMPL-X | 3D body mesh | Enables multi-view | Complex, out of scope for V1 |

### Garment Representation Learning

Key techniques relevant to VPE:

- **CLIP-based garment encoding:** Captures high-level garment semantics but may lose texture details
- **VAE-based garment features:** Better texture preservation but may lose category semantics
- **Dual encoding (semantic + detail):** Best quality but higher cost — this is the VPE direction
- **LoRA adaptation:** Enables brand/style-specific tuning without full model retraining

## 3. Industry Solutions

### Fashn.ai VTON-1.5 (Baseline Reference)

- **Role in VPE:** Launch acceleration and benchmark baseline
- **Strengths:** Production-ready API, reasonable quality for standard cases, fast integration
- **Limitations:** Limited control over model internals, vendor pricing at scale, no brand-specific adaptation, quality ceiling tied to provider roadmap
- **VPE Differentiation:** IP ownership, latency control, brand-level adaptation, quality iteration speed

### Google Virtual Try-On

- **Approach:** Uses a modified diffusion model with Shopping Graph data. Focuses on upper-body garments with product-quality outputs.
- **Quality Target:** High garment fidelity, clean composition, handles diverse body types
- **Limitations:** Not publicly available as an API. Requires massive internal datasets.
- **VPE Benchmark:** Represents the aspirational quality target. VPE should approach this quality level progressively, starting with priority categories.

### Other Commercial Solutions

| Provider | Focus | Pricing Model | Key Limitation for VPE |
| --- | --- | --- | --- |
| Zeekit (Walmart) | Consumer try-on | Internal | Not available externally |
| Vue.ai | E-commerce automation | Per-image API | Limited garment fidelity control |
| Revery.ai | B2B VTON API | Per-image API | Pose robustness gaps |
| Kolors (Kwai) | Open-source VTON | Self-hosted | Requires significant engineering |

## 4. Benchmark Datasets

| Dataset | Images | Categories | Notes |
| --- | --- | --- | --- |
| VITON-HD | ~13K pairs | Upper body | Standard academic benchmark |
| DressCode | ~48K pairs | Upper, lower, dress | Multi-category, larger scale |
| VITON | ~16K pairs | Upper body | Older, lower resolution |
| DeepFashion | ~800K images | Various | Broader fashion dataset, not VTON-specific |

VPE should evaluate on VITON-HD and DressCode for academic comparison, plus internal brand-specific benchmark sets for production quality assessment.

## 5. Key Architectural Insights for VPE

Based on the literature survey, VPE's architecture should prioritize:

1. **Dual garment encoding** (semantic + detail level) — proven to improve fidelity in IDM-VTON
2. **DensePose conditioning** — provides richer body information than keypoints alone
3. **Cross-attention over concatenation** — better control over garment-person composition
4. **LoRA for brand adaptation** — avoids full retraining while enabling specialization
5. **Multi-view consistency loss** — not well-addressed in current literature, a potential VPE differentiator
6. **Inference optimization** — critical for production but underexplored in academic work

## 6. VPE Differentiation Summary

| Dimension | Academic SOTA | Commercial Providers | VPE Target |
| --- | --- | --- | --- |
| Garment fidelity | High (IDM-VTON) | Medium-High | High, with brand tuning |
| Pose robustness | Medium | Medium | High, with pose-aware blocks |
| Multi-view consistency | Low | Low | Medium-High (differentiator) |
| Inference latency | Not optimized | Variable | <4-6s production target |
| Brand adaptation | Not addressed | Not addressed | LoRA per brand |
| IP ownership | Open-source | Vendor-owned | Fully proprietary |
