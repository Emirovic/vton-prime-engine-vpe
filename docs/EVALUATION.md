# Evaluation Framework

## 1. Why Evaluation Matters

Virtual try-on quality cannot be judged only by standard image metrics. A model may score well numerically while still failing for fashion use cases, such as distorted logos, changed fabric texture, or broken anatomy.

VPE-1.0 therefore uses a mixed evaluation framework:

- Human preference
- Fashion-specific QA
- Automated image checks
- Latency and reliability metrics

## 2. Quality Metrics

### Human Preference Rate

Blind side-by-side tests compare baseline output against VPE output. The main question is:

> Which output would be more acceptable for a real fashion e-commerce experience?

Target: 20-30% preference lift over baseline in priority categories.

### Garment Fidelity Score

Measures whether the generated output preserves:

- Color
- Silhouette
- Fabric texture
- Logos
- Patterns
- Product-specific details

Target: 90% QA pass rate for top categories.

### Pose Robustness Score

Evaluates hard cases:

- Bent arms
- Crossed arms
- Seated poses
- Side poses
- Occlusions from hands, hair, bags, or jackets

Target: measurable improvement over baseline on difficult-pose benchmark.

### Multi-View Consistency Score

Checks whether the same person-garment pair remains visually stable across multiple pose or view variants.

Target: fewer identity, garment, and silhouette changes across generated views.

### Latency

Measures total request time from accepted input to generated output.

Target: under 4-6 seconds for production-quality single-image try-on.

### Severe Artifact Rate

Tracks production outputs with major failures:

- Missing limbs
- Broken hands
- Unnatural body shape
- Incorrect garment category
- Destroyed logos or text
- Large segmentation failure

Target: under 2% severe artifact rate.

## 3. Evaluation Dataset

The benchmark set should include:

- Gender and body-shape diversity
- Different skin tones
- Different camera angles
- Product categories by priority
- Hard poses and occlusions
- Multiple brands and garment styles

The evaluation set must be versioned and kept separate from training data.

## 4. Human QA Rubric

Each output receives scores from 1 to 5:

- Realism
- Garment fidelity
- Pose correctness
- Identity preservation
- Commercial usability

Suggested labels:

- 5: Production-ready
- 4: Minor issue, usable
- 3: Noticeable issue, needs review
- 2: Major issue
- 1: Failure

## 5. Release Gate

A model version can move to production only if:

- It beats baseline in human preference tests
- It passes category-specific QA thresholds
- It meets latency requirements
- It does not increase severe artifact rate
- It has rollback support

