# Cost Estimation and Budget Framework

## 1. Purpose

A virtual try-on project without cost visibility is a project without accountability. This document provides a planning-level cost model for each major budget category. The numbers below are directional estimates for planning, not procurement commitments.

## 2. GPU Training Costs

### Compute Requirements

Training a production-quality diffusion-based VTON model typically requires:

- Base model pre-training or fine-tuning: 200–500 A100 GPU-hours per experiment
- LoRA brand adaptation modules: 20–50 A100 GPU-hours per brand
- Evaluation and ablation runs: 50–100 A100 GPU-hours per cycle
- Hyperparameter search: 100–300 A100 GPU-hours per sweep

### Cost Estimates (Cloud GPU Pricing)

| Resource | Unit Cost (approx.) | Estimated Usage | Phase Cost |
| --- | --- | --- | --- |
| A100 80GB on-demand | $2.50–3.50/hr | 500–1000 hrs (Phase 3) | $1,250–3,500 |
| A100 spot/preemptible | $1.00–1.50/hr | 300–600 hrs (experiments) | $300–900 |
| LoRA fine-tuning (3 brands) | $1.50/hr avg | 60–150 hrs | $90–225 |
| Total training compute | | | **$1,640–4,625** |

### Cost Reduction Strategies

- Use spot/preemptible instances for non-critical experiments
- Checkpoint aggressively to recover from preemptions
- Start with smaller model variants for architecture validation
- Share base model weights across LoRA experiments

## 3. Inference Serving Costs

### Production Serving Estimates

| Scenario | GPU | Throughput | Cost per Image |
| --- | --- | --- | --- |
| Single A100 serving | A100 40GB | ~15–25 images/min | $0.008–0.015 |
| Optimized (TensorRT/compiled) | A100 40GB | ~30–50 images/min | $0.004–0.008 |
| Preview mode (fewer steps) | T4/A10 | ~40–80 images/min | $0.001–0.003 |

### Monthly Serving Cost Model

| Traffic Level | Daily Volume | Monthly GPU Hours | Monthly Cost |
| --- | --- | --- | --- |
| Pilot (low) | 1,000 images | ~30–50 hrs | $75–175 |
| Growth | 10,000 images | ~250–400 hrs | $625–1,400 |
| Scale | 100,000 images | ~2,000–3,500 hrs | $5,000–12,250 |

## 4. Baseline Provider Costs (Comparison)

### Third-Party API Pricing

External VTON providers typically charge per-image or per-API-call:

| Volume | Estimated Provider Cost/Image | Monthly Cost (10K images) |
| --- | --- | --- |
| Low volume | $0.05–0.15 | $500–1,500 |
| Medium volume (negotiated) | $0.03–0.08 | $300–800 |
| High volume (enterprise) | $0.02–0.05 | $200–500 |

### Break-Even Analysis

The proprietary engine has higher upfront investment but lower marginal cost:

```text
Break-even point (approximate):

  Upfront investment (training + infra setup): ~$10,000–20,000
  Monthly proprietary serving (10K images):     ~$625–1,400
  Monthly provider cost (10K images):           ~$300–1,500

  At 10K images/month with mid-range pricing:
    Provider: ~$800/month
    Proprietary: ~$1,000/month + amortized training

  At 50K images/month:
    Provider: ~$2,500–4,000/month
    Proprietary: ~$2,500–3,500/month (inference only)

  Break-even: ~30,000–80,000 cumulative images
              (approximately 3–8 months at growth-stage volume)
```

The proprietary path becomes cost-advantaged at scale, with the added benefit of IP ownership, latency control, and quality differentiation.

## 5. Data and Annotation Costs

| Item | Unit Cost | Estimated Volume | Total |
| --- | --- | --- | --- |
| Studio photography (if needed) | $5–15/image set | 500–2,000 sets | $2,500–30,000 |
| Licensed dataset acquisition | Varies | 1–3 datasets | $1,000–10,000 |
| Human QA annotation (per image) | $0.10–0.30 | 5,000–20,000 labels | $500–6,000 |
| Pose and segmentation annotation | $0.20–0.50 | 5,000–10,000 images | $1,000–5,000 |
| **Total data pipeline** | | | **$5,000–51,000** |

Most of this cost can be reduced significantly if brand partners provide existing product imagery.

## 6. Infrastructure and Tooling

| Tool | Monthly Cost | Notes |
| --- | --- | --- |
| Experiment tracking (W&B/MLflow) | $0–200 | Free tier may cover early stages |
| Object storage (S3/GCS) | $50–200 | Depends on dataset and output volume |
| Model registry | $0–100 | Can use open-source (MLflow) |
| CI/CD (GitHub Actions) | $0–50 | Free tier for public repos |
| Monitoring (Grafana/Datadog) | $0–200 | Basic tier |
| **Total infra/month** | | **$50–750** |

## 7. Team Cost (Not Budgeted Here)

Team compensation is the largest cost category but is outside the scope of this technical cost estimate. The team structure is defined in [TEAM_ORGANIZATION.md](TEAM_ORGANIZATION.md). For planning purposes:

- A 6–8 person team for 6–9 months represents the primary investment
- The technical costs above are incremental to team costs

## 8. Total Project Cost Summary

| Category | Low Estimate | High Estimate |
| --- | --- | --- |
| GPU training compute | $1,640 | $4,625 |
| GPU inference (6 months pilot) | $450 | $1,050 |
| Data and annotation | $5,000 | $51,000 |
| Infrastructure and tooling (6 months) | $300 | $4,500 |
| **Total (excl. team)** | **$7,390** | **$61,175** |

## 9. Key Takeaway

The proprietary engine requires meaningful upfront investment but creates long-term cost advantage at scale. The baseline provider strategy in Phase 1 allows the product to generate revenue while the proprietary system is built, which partially offsets development costs.
