# Risks and Mitigations

## 1. Data Licensing Risk

Risk: Training data may include images without proper consent or commercial usage rights.

Mitigation:

- Track consent and license metadata
- Separate research-only and production-approved datasets
- Review data sources with legal support

## 2. Quality Risk

Risk: Outputs may look realistic but damage brand-critical details like logos, patterns, or fabric texture.

Mitigation:

- Use fashion-specific QA rubric
- Add garment fidelity metrics
- Create brand review workflow

## 3. Pose Robustness Risk

Risk: The model may fail on seated poses, crossed arms, occlusions, or side views.

Mitigation:

- Include hard-pose benchmark set
- Add pose-aware conditioning
- Track failure modes by pose type

## 4. Vendor Dependency Risk

Risk: The product may remain dependent on a third-party provider if proprietary development is delayed.

Mitigation:

- Keep provider behind an adapter interface
- Build comparable internal model endpoints early
- Track traffic percentage by engine

## 5. Latency and Cost Risk

Risk: Production-quality generation may be too slow or expensive.

Mitigation:

- Separate preview and production modes
- Optimize model serving
- Use batching, caching, and GPU scheduling
- Monitor cost per successful generation

## 6. Brand Trust Risk

Risk: Bad outputs may reduce trust from partner brands or users.

Mitigation:

- Add automated safety and artifact checks
- Use staged rollout
- Include manual QA for pilot brands
- Keep rollback available

