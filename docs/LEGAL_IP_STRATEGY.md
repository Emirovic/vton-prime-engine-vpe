# Legal and IP Strategy

## 1. Purpose

VPE aims to create a proprietary, defensible AI asset. This requires careful management of intellectual property, data rights, open-source license compliance, and user privacy obligations.

## 2. Model IP Ownership

### Proprietary Model Path

The proprietary VPE model should be developed such that the company has full ownership of:

- Model architecture design
- Trained model weights
- Fine-tuned LoRA modules per brand
- Training configurations and hyperparameters
- Evaluation datasets and quality benchmarks
- Inference optimization techniques

### Open-Source Foundation Risks

If VPE uses a pre-trained foundation model (e.g., Stable Diffusion, SDXL) as a starting point, the license terms of that model govern what can be done with derived works:

| Foundation Model | License | Commercial Use | Key Restrictions |
| --- | --- | --- | --- |
| Stable Diffusion 1.x/2.x | CreativeML Open RAIL-M | Yes, with conditions | Cannot use to harm, must include license notice |
| SDXL | SDXL 1.0 License | Yes, with conditions | Same RAIL-M family restrictions |
| Stable Diffusion 3.x | Stability Community License | Limited | Revenue threshold restrictions |
| Custom from scratch | Full ownership | Unrestricted | Highest cost, highest control |

**Recommendation:** Start with a permissive foundation model (SD 1.x/2.x or SDXL) for prototyping. Track foundation model license requirements. Plan for a clean-room architecture for production release if full IP independence is required.

### Patent Landscape

- Monitor patent filings from Google, Amazon, and major fashion-tech companies in the VTON space
- Document novel architectural contributions for potential patent protection
- Keep design decision logs that demonstrate independent development

## 3. Data Rights and Licensing

### Dataset Licensing Requirements

Every image used for training must have one of the following:

- Internal ownership (company-produced studio images)
- Explicit commercial license from dataset provider
- Brand partner agreement allowing usage for model training
- User consent for user-generated content

### License Tracking

Each data asset in the pipeline must include:

- License type (owned, licensed, consented)
- License expiration date if applicable
- Geographic usage restrictions if any
- Permitted use cases (training, evaluation, production output generation)
- Attribution requirements if any

### Prohibited Data Sources

- Scraped images without consent
- Images from platforms that prohibit commercial AI training
- User-uploaded content without explicit opt-in consent
- Images with unresolved copyright claims

## 4. Privacy and Compliance

### GDPR (EU) Compliance

If VPE processes images of EU residents:

- Must have legal basis for processing (consent or legitimate interest)
- Must support right to erasure (model retraining or machine unlearning strategy)
- Must document data processing activities
- Must assess and mitigate privacy risks (DPIA if needed)
- Must not use biometric data without explicit consent

### KVKK (Turkey) Compliance

If operating in or serving Turkish users:

- Similar consent requirements as GDPR
- Must register with VERBİS (Data Controllers Registry) if applicable
- Must appoint a data controller representative
- Cross-border data transfer restrictions apply

### Practical Requirements

- Person images must be stored with consent metadata
- Outputs must not expose private identity without authorization
- A mechanism to remove specific person data from training sets must exist
- Production logs should not retain person-identifiable information beyond retention policy

## 5. Brand Partner Agreements

When onboarding pilot brands for LoRA adaptation modules:

- Define data ownership: brand provides product images, model weights are company-owned
- Specify output usage rights: who can use generated try-on images, for what purpose
- Include quality and brand safety commitments
- Define review and approval workflow
- Include termination and data deletion clauses

## 6. Vendor Contracts (Baseline Provider)

The baseline provider (Fashn.ai VTON-1.5-style) contract should be reviewed for:

| Clause | Risk | Mitigation |
| --- | --- | --- |
| Data retention | Provider may retain input images | Negotiate zero-retention or review retention policy |
| Output ownership | Unclear who owns generated images | Ensure contract assigns output rights to company |
| Usage restrictions | Provider may restrict commercial usage | Confirm commercial terms before launch |
| Rate limits / SLAs | Provider may throttle at scale | Negotiate minimum SLA and burst capacity |
| Termination | Lock-in risk if proprietary model delays | Ensure termination clause with reasonable notice |
| Price escalation | Provider may increase pricing | Lock in pricing for initial term, plan proprietary transition |

## 7. Summary of Obligations

| Area | Owner | Key Action |
| --- | --- | --- |
| Model IP tracking | Research Lead | Document architecture decisions, track foundation model licenses |
| Dataset licensing | Data Engineer + Legal | Maintain license metadata, review before production training |
| Privacy compliance | Legal + Data Engineer | GDPR/KVKK assessment, consent tracking, retention policy |
| Brand agreements | Program Lead + Legal | Draft template agreement, review with each pilot brand |
| Vendor contract | Legal + Program Lead | Review baseline provider terms before production integration |
| Open-source compliance | Research Lead + Legal | Track foundation model license obligations |
