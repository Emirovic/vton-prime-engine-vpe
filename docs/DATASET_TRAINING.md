# Dataset and Training Workflow

## 1. Dataset Requirements

VPE requires a controlled, licensed, and versioned dataset. The dataset should cover person images, garment images, masks, pose signals, metadata, and evaluation labels.

## 2. Data Sources

Approved sources may include:

- Brand-provided product images
- Internally produced studio photos
- Licensed fashion datasets
- User-generated content only with explicit consent
- Synthetic or augmented data for controlled edge cases

Every asset must have usage-right metadata before it can be used for production training.

## 3. Required Data Fields

For person images:

- Person image URI
- Body visibility
- Pose type
- Occlusion type
- Consent and license status
- Split assignment

For garment images:

- Garment image URI
- Category
- Brand
- Color
- Pattern type
- Logo or text presence
- Product ID if available

For generated outputs:

- Request ID
- Model version
- Dataset version
- Output URI
- Latency
- QA scores
- Failure labels

## 4. Preprocessing Pipeline

```text
Raw Assets
   |
   v
License and Consent Validation
   |
   v
Image Quality Filtering
   |
   v
Person Segmentation / Human Parsing
   |
   v
Garment Masking
   |
   v
Pose Keypoint Extraction
   |
   v
Dataset Versioning
   |
   v
Training / Validation / Benchmark Splits
```

## 5. Training Strategy

### Stage 1: Narrow Category Prototype

Start with one or two high-value categories, such as tops and dresses. This reduces complexity and makes evaluation clearer.

### Stage 2: Garment Fidelity Improvements

Improve preservation of color, silhouette, logos, and fabric texture with stronger garment conditioning and targeted evaluation.

### Stage 3: Pose Robustness

Train with hard-pose examples and explicit pose conditioning.

### Stage 4: Brand-Level Adaptation

Use LoRA modules for pilot brands so the system can learn brand-specific visual details without retraining the whole model.

### Stage 5: Production Candidate Training

Freeze a dataset version, train a candidate model, evaluate it against baseline, and register the model only if it passes release gates.

## 6. Dataset Versioning Rules

- Training data, validation data, and benchmark data must be separated
- Benchmark data must not be used for training
- Every model must record dataset version
- Deleted or license-expired data must be traceable
- QA labels should be versioned with the images they evaluate

## 7. Training Deliverables

- Dataset schema
- Dataset validation report
- Training configuration
- Model checkpoint
- Evaluation report
- Failure analysis
- Release recommendation

