# Roadmap

## Timeline Summary

Total estimated duration: **6–9 months** from project kickoff to production launch.

```text
Month:  1     2     3     4     5     6     7     8     9
        |-----|-----|-----|-----|-----|-----|-----|-----|
Ph 0:   █                                               (1 week)
Ph 1:   ████████                                         (2-4 weeks)
Ph 2:        ██████████████                              (4-6 weeks, overlaps Ph1 tail)
Ph 3:                  ████████████████████████           (8-12 weeks, starts after Ph2 data ready)
Ph 4:                              ████████████████      (6-8 weeks, overlaps Ph3 tail)
Ph 5:                                        ████████████(4-8 weeks, starts after Ph4 LoRA)
```

**Phase dependencies:**
- Phase 1 (baseline) can start immediately
- Phase 2 (data pipeline) can begin during Phase 1 tail, needs benchmark set from Phase 1
- Phase 3 (proprietary model) requires Phase 2 dataset pipeline operational
- Phase 4 (brand adaptation) requires Phase 3 base model checkpoint
- Phase 5 (production optimization) can begin during Phase 4, requires a candidate model

---

## Phase 0: Case Submission Starter

Duration: 1 week

Deliverables:

- Project plan
- Architecture proposal
- Evaluation framework
- Minimal pipeline scaffold
- Testable CLI contract

## Phase 1: Baseline Integration and Benchmarking

Duration: 2-4 weeks

Goals:

- Integrate baseline virtual try-on provider
- Create unified request/response interface
- Build initial benchmark dataset
- Run baseline quality and latency tests

Exit Criteria:

- Baseline outputs can be generated through the internal API
- Benchmark report exists for priority categories
- Failure cases are categorized

## Phase 2: Data and Evaluation Pipeline

Duration: 4-6 weeks

Goals:

- Build dataset ingestion and validation
- Add pose, mask, and garment metadata pipelines
- Create human evaluation workflow
- Version train, validation, and benchmark sets

Exit Criteria:

- Dataset versioning is active
- Human QA rubric is used consistently
- Model candidates can be compared against baseline

## Phase 3: Proprietary Model Prototype

Duration: 8-12 weeks

Goals:

- Train first internal model for limited categories
- Add garment-aware and pose-aware conditioning
- Compare against baseline on quality and latency
- Identify architecture improvements

Exit Criteria:

- Prototype beats baseline in at least one priority category
- Major failure modes are documented
- Training and evaluation are reproducible

## Phase 4: Brand Adaptation and Multi-View Consistency

Duration: 6-8 weeks

Goals:

- Add brand-level LoRA modules
- Improve consistency across multiple views
- Expand supported categories
- Run pilot brand validation

Exit Criteria:

- 3 pilot brands have adaptation modules
- Brand QA approval workflow is defined
- Multi-view benchmark shows measurable improvement

## Phase 5: Production Optimization

Duration: 4-8 weeks

Goals:

- Optimize inference latency
- Add autoscaling and monitoring
- Implement rollback and model registry
- Prepare controlled production launch

Exit Criteria:

- Production latency target is met
- Monitoring dashboard is active
- Rollback strategy is tested
- Release gate is approved

