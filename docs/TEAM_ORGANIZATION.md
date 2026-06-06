# Project Organization

## 1. Core Team

### Program Lead / Product Owner

Owns roadmap, budget, stakeholder alignment, launch scope, and business success criteria.

### Research Lead

Owns architecture direction, model research, baseline comparison strategy, and technical quality targets.

### ML Engineers

Own model development, training, fine-tuning, evaluation experiments, and model-quality improvements.

Recommended size: 2-4 engineers.

### Data Engineer

Owns ingestion, preprocessing, labeling pipeline, dataset validation, and dataset versioning.

### MLOps / Platform Engineer

Owns GPU orchestration, experiment tracking, model registry, CI/CD, deployment, monitoring, and rollback.

### Backend Engineer

Owns inference API, provider integration, routing, storage integration, authentication, and scaling.

### QA / Evaluation Lead

Owns benchmark design, human evaluation workflow, release gates, QA rubric, and quality reporting.

### Fashion Domain Specialist / Annotator Lead

Owns garment taxonomy, visual quality standards, brand-specific feedback, and annotation guidelines.

### Legal / Procurement Support

Owns provider contract review, data licensing review, user consent requirements, model usage restrictions, and vendor-risk review.

## 2. Operating Rhythm

- Weekly product and roadmap review
- Twice-weekly ML experiment review
- Weekly benchmark and failure-case review
- Biweekly stakeholder demo
- Release gate review before production rollout

## 3. Ownership Matrix

| Area | Owner | Supporting Roles |
| --- | --- | --- |
| Roadmap | Program Lead | Research Lead, Backend Engineer |
| Baseline integration | Backend Engineer | MLOps Engineer |
| Model architecture | Research Lead | ML Engineers |
| Dataset pipeline | Data Engineer | QA Lead, Legal |
| Evaluation | QA Lead | Research Lead, Fashion Specialist |
| Deployment | MLOps Engineer | Backend Engineer |
| Brand validation | Fashion Specialist | Program Lead, QA Lead |
| Legal and vendor review | Legal Support | Program Lead |

