# Technical Architecture

## 1. System Overview

VPE-1.0 is designed as a modular virtual try-on system. The architecture separates provider integrations, proprietary model inference, evaluation, and production serving.

```text
User / Product UI
       |
       v
VTON API Gateway
       |
       v
Request Validation and Asset Preprocessing
       |
       +-------------------+
       |                   |
       v                   v
Baseline Provider      Proprietary VPE Model
       |                   |
       +---------+---------+
                 |
                 v
Postprocessing and QA Checks
                 |
                 v
Storage, Monitoring, and Feedback Loop
```

## 2. Inputs

Each try-on request should include:

- Person image
- Garment image
- Garment category
- Optional brand ID
- Optional pose or view target
- Request quality mode, such as preview or production

## 3. Core Components

### API Gateway

Handles authentication, rate limits, request IDs, and response formatting.

### Preprocessing

Preprocessing creates the model-ready inputs:

- Person segmentation
- Garment segmentation
- Human pose keypoints
- Dense body representation
- Image normalization
- Garment metadata normalization

### Baseline Provider Adapter

The baseline adapter lets the product launch quickly while the proprietary model is trained. It also creates comparable outputs for benchmarking.

### Proprietary Model Path

The proprietary path should include:

- Garment encoder
- Person and pose encoder
- Enhanced cross-attention blocks
- Pose-aware transformer blocks
- Multi-view conditioning module
- Diffusion or image-generation backbone
- Brand-level LoRA modules

### Postprocessing

Postprocessing should handle:

- Face and identity preservation checks
- Garment boundary cleanup
- Artifact detection
- Resolution upscaling when required
- Output metadata creation

### Evaluation Service

The evaluation service compares baseline and VPE outputs using:

- Human preference
- Artifact taxonomy
- Garment fidelity scoring
- Pose robustness scoring
- Latency and cost tracking

## 4. Training Workflow

```text
Raw Assets
   |
   v
Licensing and Consent Filter
   |
   v
Dataset Versioning
   |
   v
Preprocessing Jobs
   |
   v
Training / Fine-Tuning
   |
   v
Offline Evaluation
   |
   v
Model Registry
   |
   v
Staging Deployment
   |
   v
Production Deployment
```

## 5. Model Strategy

### Stage 1: Baseline Comparison

Use the external baseline to collect comparable outputs and define quality gaps.

### Stage 2: Proprietary Prototype

Train an internal model for a narrow category such as tops or dresses. Focus on garment fidelity and pose robustness.

### Stage 3: Brand Adaptation

Add LoRA modules per pilot brand. This allows specialized behavior without retraining the full model.

### Stage 4: Serving Optimization

Apply model quantization, batching, caching, memory optimization, and deployment tuning.

## 6. API Contract Example

```json
{
  "person_image_uri": "s3://bucket/person.jpg",
  "garment_image_uri": "s3://bucket/garment.jpg",
  "garment_category": "top",
  "brand_id": "pilot-brand",
  "quality_mode": "production"
}
```

Example response:

```json
{
  "request_id": "vpe_20260606_001",
  "status": "completed",
  "engine": "vpe-proprietary",
  "output_image_uri": "s3://bucket/results/output.jpg",
  "latency_ms": 4300,
  "quality_flags": []
}
```

## 7. Production Notes

- Store every request with a traceable request ID
- Save model version and dataset version with each output
- Separate preview mode from production quality mode
- Keep baseline and proprietary outputs comparable during transition
- Use release gates before switching traffic to new model versions

