# Roadmap

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

