# Gap Analysis Against Target Quality

## 1. Purpose

The first version of VPE should not start by assuming that the proprietary model is already better than the baseline. The correct approach is to integrate a Fashn.ai VTON-1.5-style baseline, measure it on the company's target use cases, and then improve the gaps with internal architecture, data, and serving work.

This document defines the gap-analysis framework for realism, garment fidelity, pose robustness, multi-view consistency, and latency.

## 2. Baseline Measurement

The baseline provider is used for:

- Fast market-entry experiments
- Reference output generation
- Latency and cost comparison
- Failure-case discovery
- Human preference comparisons

Each baseline output should be stored with:

- Request ID
- Person image reference
- Garment image reference
- Garment category
- Brand ID if available
- Provider version if available
- Latency
- Quality flags
- Human QA scores

## 3. Target Dimensions

### Realism and Texture Fidelity

Expected gap:

- Output may look plausible overall but lose fabric texture, small logos, product text, stitching, or pattern alignment.

Internal improvement path:

- Stronger garment encoder
- Garment-detail preservation loss
- High-resolution crop evaluation around logos and patterns
- Brand-specific adaptation modules

### Pose Robustness

Expected gap:

- Hard poses can cause broken arms, wrong sleeve placement, body-shape distortion, or garment leakage into the background.

Internal improvement path:

- Pose-aware transformer blocks
- Human parsing and dense-pose conditioning
- Hard-pose benchmark set
- Data balancing for seated, side, crossed-arm, and occluded poses

### Multi-View Consistency

Expected gap:

- The same garment-person pair may change shape, color, or fit across different views.

Internal improvement path:

- Multi-view conditioning module
- Shared garment identity embedding
- Consistency loss across generated variants
- Evaluation set with repeated person-garment pairs

### Inference Latency

Expected gap:

- High-quality generation may be too slow for product-detail-page usage.

Internal improvement path:

- Preview and production quality modes
- Model compilation and optimized kernels
- GPU batching and queueing
- Caching repeated garment embeddings
- Autoscaling based on queue depth and latency

## 4. Comparison Table

| Dimension | Baseline Role | VPE Target | Evidence Needed |
| --- | --- | --- | --- |
| Realism | Reference quality | Higher human preference | Blind A/B tests |
| Garment fidelity | Product-detail baseline | Better logo, texture, silhouette preservation | Fashion QA rubric |
| Pose robustness | Failure discovery | Higher pass rate on hard poses | Hard-pose benchmark |
| Multi-view consistency | Comparison output | Stable garment identity across views | Repeated-pair tests |
| Latency | Provider latency benchmark | 4-6 second production target | API timing logs |
| Cost/control | Vendor reference | Lower long-term dependency | Cost per successful generation |

## 5. Output of Gap Analysis

The gap analysis should produce:

- Baseline benchmark report
- Failure taxonomy
- Category-priority matrix
- Architecture backlog
- Dataset expansion backlog
- Latency optimization backlog

