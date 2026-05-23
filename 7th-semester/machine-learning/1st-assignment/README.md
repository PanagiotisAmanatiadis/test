# Assignment 1 — Corporate Bankruptcy Classification

**University of Macedonia | Applied Informatics | Machine Learning | 7th Semester 2022–2023**

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Dataset](#2-dataset)
3. [Pipeline Architecture](#3-pipeline-architecture)
4. [Installation](#4-installation)
5. [Usage](#5-usage)
6. [Methodology](#6-methodology)
7. [Results](#7-results)
8. [Excel & Pivot Table Analysis Guide](#8-excel--pivot-table-analysis-guide)
9. [Analytical Findings & Report Blueprint](#9-analytical-findings--report-blueprint)
10. [Output Structure](#10-output-structure)

---

## 1. Problem Statement

The goal is to identify which companies will declare **bankruptcy** using financial performance indicators. This is a **binary classification** problem with a heavily imbalanced dataset — the majority of companies are healthy (label 1), while a small minority have declared bankruptcy (label 2).

The pipeline evaluates **8 distinct classification algorithms** under a **Stratified 4-Fold cross-validation** scheme with **random undersampling** to enforce a 3:1 healthy-to-bankrupt training ratio, preventing the classifiers from simply predicting "healthy" for every instance.

---

## 2. Dataset

**File:** `data/Dataset2Use_Assignment1.xlsx`

| Column Group    | Columns | Description                                           |
|-----------------|---------|-------------------------------------------------------|
| Performance     | A–H     | 8 continuous financial performance indicators         |
| Activity        | I, J, K | 3 binary activity indicators (0 or 1)                 |
| Status (target) | L       | 1 = Healthy company, 2 = Bankrupt company             |
| Year            | M       | Fiscal year of the recorded figures                   |

**Actual class distribution (10,716 total samples):**

| Class    | Label | Count  | Percentage |
|----------|-------|--------|------------|
| Healthy  | 1     | 10,468 | 97.7%      |
| Bankrupt | 2     | 248    | 2.3%       |

The dataset exhibits **extreme class imbalance**: bankrupt companies represent only 2.3% of all samples (248 out of 10,716). This is the primary driver of all performance results and the reason no classifier reaches the Recall ≥ 60% threshold on the test set.

---

## 3. Pipeline Architecture

The project follows a modular `src` layout with dedicated packages for each concern:

```
1st-assignment/
├── data/
│   └── Dataset2Use_Assignment1.xlsx
├── configs/
│   └── config.yaml
├── src/
│   └── bankruptcy_clf/
│       ├── data/
│       │   └── dataset.py          — BankruptcyDataset: load, clean, normalize, auto-detect cols
│       ├── preprocessing/
│       │   └── balancer.py         — RandomUnderSampler: enforce 3:1 healthy-to-bankrupt ratio
│       ├── models/
│       │   └── factory.py          — ClassifierFactory.create_all() → dict of 8 estimators
│       ├── evaluation/
│       │   └── metrics.py          — @dataclass ClassificationResult + MetricsEvaluator
│       ├── visualization/
│       │   └── plotter.py          — Plotter: class distribution, indicator stats, confusion matrices
│       ├── pipeline/
│       │   └── experiment.py       — ExperimentRunner: orchestrates full CV loop, saves results
│       └── utils/
│           ├── logger.py            — setup_logger() via loguru
│           └── timer.py             — Timer() context manager
├── scripts/
│   └── run_pipeline.py              — click CLI entry point
├── tests/
│   ├── test_dataset.py
│   ├── test_balancer.py
│   └── test_metrics.py
├── reports/
│   ├── figures/                     — PNG outputs
│   └── results/
│       └── balancedDataOutcomes.csv
├── logs/
└── pyproject.toml
```

Configuration is managed via `configs/config.yaml` (OmegaConf). The entry point `run-pipeline` is defined in `pyproject.toml` and maps to `bankruptcy_clf.pipeline.experiment:main`.

### Class Label Encoding

| Original | Encoded | Meaning  |
|----------|---------|----------|
| 1        | 0       | Healthy  |
| 2        | 1       | Bankrupt (positive class) |

Bankrupt is the **positive class** because recall for bankrupt companies is the primary business concern.

---

## 4. Installation

Requires [uv](https://docs.astral.sh/uv/) and Python 3.11–3.12.

```bash
cd 1st-assignment
uv sync
```

This creates a virtual environment and installs all dependencies declared in `pyproject.toml`.

| Package      | Version (min) | Purpose                         |
|--------------|---------------|---------------------------------|
| pandas       | 2.1           | Data loading and manipulation   |
| numpy        | 1.26          | Numerical operations            |
| matplotlib   | 3.8           | Figure generation               |
| seaborn      | 0.13          | Confusion matrix heatmaps       |
| scikit-learn | 1.3           | All classifiers and CV tools    |
| openpyxl     | 3.1           | Reading .xlsx files             |
| omegaconf    | 2.3           | YAML configuration management   |
| loguru       | 0.7           | Structured logging              |
| click        | 8.1           | CLI entry point                 |

---

## 5. Usage

### Run the pipeline

```bash
cd 1st-assignment
uv run run-pipeline
```

This uses the default `configs/config.yaml`. To specify a custom config path:

```bash
uv run python scripts/run_pipeline.py --config configs/config.yaml
```

### Configuration

Edit `configs/config.yaml` to adjust folds, undersampling ratio, classifier hyperparameters, or output paths:

```yaml
seed: 42
data:
  path: data/Dataset2Use_Assignment1.xlsx
pipeline:
  n_folds: 4
  target_ratio: 3  # healthy:bankrupt ratio after undersampling
classifiers:
  lda: {}
  logistic_regression:
    max_iter: 1000
  decision_tree: {}
  random_forest:
    n_estimators: 100
  knn:
    n_neighbors: 5
  naive_bayes: {}
  svm:
    probability: true
  gradient_boosting:
    n_estimators: 100
    learning_rate: 0.1
visualization:
  dpi: 150
paths:
  logs_dir: logs
  figures_dir: reports/figures
  results_csv: reports/results/balancedDataOutcomes.csv
```

### Run tests

```bash
uv run pytest
```

---

## 6. Methodology

### 6.1 Stratified 4-Fold Cross-Validation

`StratifiedKFold(n_splits=4, shuffle=True, random_state=42)` preserves the class ratio across all folds. Given the actual dataset of 10,716 samples, each fold produces approximately:

| Split | Total  | Healthy | Bankrupt |
|-------|--------|---------|----------|
| Train | ~8,037 | ~7,851  | ~186     |
| Test  | ~2,679 | ~2,617  | ~62      |

### 6.2 Random Undersampling (3:1 Ratio)

Undersampling is applied to the **training fold only**. If `n_healthy / n_bankrupt > 3`:

```
target_healthy = 3 × n_bankrupt_train
```

Actual fold sizes after undersampling (from pipeline run):

| Split | Total | Healthy | Bankrupt |
|-------|-------|---------|----------|
| Train | 744   | 558     | 186      |
| Test  | 2,679 | 2,617   | 62       |

> **Critical:** Removed healthy companies are **discarded** — NOT transferred to the test set. The test set remains the original stratified split and therefore still reflects the full 97.7% / 2.3% imbalance. This is why only 62 bankrupt companies appear in each test fold, making high recall very difficult to achieve.

### 6.3 The 8 Classifiers

| # | Classifier              | Key Hyperparameters                        | Notes                        |
|---|-------------------------|--------------------------------------------|------------------------------|
| 1 | Linear Discriminant Analysis | solver='svd'                          | Linear boundaries            |
| 2 | Logistic Regression     | max_iter=1000, C=1.0                       | L2 regularized               |
| 3 | Decision Tree           | random_state=42                            | Fully grown by default       |
| 4 | Random Forest           | n_estimators=100, random_state=42          | Bagging ensemble             |
| 5 | k-Nearest Neighbors     | n_neighbors=5, metric='minkowski'          | Instance-based               |
| 6 | Naive Bayes (Gaussian)  | var_smoothing=1e-9                         | Probabilistic                |
| 7 | Support Vector Machine  | kernel='rbf', probability=True             | Kernel trick                 |
| 8 | **Gradient Boosting**   | n_estimators=100, learning_rate=0.1        | **Additional model (choice)**|

> The **8th model** chosen is **Gradient Boosting Classifier** (sklearn `GradientBoostingClassifier`). It was selected because boosting iteratively corrects residuals, making it effective on imbalanced tabular data.

### 6.4 Evaluation Metrics

| Metric      | Formula                          | Interpretation                               |
|-------------|----------------------------------|----------------------------------------------|
| Accuracy    | (TP+TN)/(TP+TN+FP+FN)           | Overall correctness                          |
| Precision   | TP/(TP+FP)                       | Of predicted bankrupt, how many truly are    |
| Recall      | TP/(TP+FN)                       | Of actual bankrupt, how many detected (≥60%) |
| F1 Score    | 2×(P×R)/(P+R)                   | Harmonic mean of Precision and Recall        |
| AUC-ROC     | Area under ROC curve             | Discrimination ability                       |
| Specificity | TN/(TN+FP)                       | Of actual healthy, how many correctly flagged (≥70%) |

**Business constraints to satisfy:**
- **Recall ≥ 60%** — correctly identify at least 60% of companies that will go bankrupt
- **Specificity ≥ 70%** — correctly identify at least 70% of healthy companies

---

## 7. Results

### 7.1 Mean Test-Set Performance (averaged across 4 folds)

Sorted by F1 Score descending.

| Classifier          | Accuracy | Precision | Recall | F1 Score | ROC-AUC | Specificity | Meets Recall≥60%? | Meets Spec≥70%? | Meets Both? |
|---------------------|----------|-----------|--------|----------|---------|-------------|-------------------|-----------------|-------------|
| Random Forest       | 0.9136   | 0.1296    | 0.4718 | 0.2031   | 0.8512  | 0.9242      | No                | Yes             | **No**      |
| SVM                 | 0.9283   | 0.1381    | 0.3790 | 0.2000   | 0.8356  | 0.9414      | No                | Yes             | **No**      |
| Gradient Boosting   | 0.9001   | 0.1207    | 0.5161 | 0.1952   | 0.8365  | 0.9093      | No                | Yes             | **No**      |
| Logistic Regression | 0.9244   | 0.1252    | 0.3670 | 0.1854   | 0.8328  | 0.9376      | No                | Yes             | **No**      |
| LDA                 | 0.9137   | 0.1192    | 0.4153 | 0.1844   | 0.8351  | 0.9255      | No                | Yes             | **No**      |
| kNN                 | 0.8827   | 0.0917    | 0.4597 | 0.1529   | 0.7990  | 0.8927      | No                | Yes             | **No**      |
| Naive Bayes         | 0.8637   | 0.0880    | 0.5242 | 0.1506   | 0.8216  | 0.8718      | No                | Yes             | **No**      |
| Decision Tree       | 0.8092   | 0.0630    | 0.5242 | 0.1124   | 0.6701  | 0.8160      | No                | Yes             | **No**      |

**Key result: No classifier meets both constraints simultaneously.** All classifiers clear Specificity ≥ 70% (range 0.816–0.941), but none reach Recall ≥ 60%. The highest recall achieved is 0.5242, shared by Naive Bayes and Decision Tree.

### 7.2 Per-Fold Results — Random Forest (Best by F1)

| Fold | TP | TN   | FP  | FN | Recall | Specificity | F1   | ROC-AUC |
|------|----|------|-----|----|--------|-------------|------|---------|
| 1    | 32 | 2391 | 226 | 30 | 0.5161 | 0.9136      | 0.20 | 0.8558  |
| 2    | 32 | 2449 | 168 | 30 | 0.5161 | 0.9358      | 0.24 | 0.8896  |
| 3    | 24 | 2410 | 207 | 38 | 0.3871 | 0.9209      | 0.16 | 0.7956  |
| 4    | 29 | 2424 | 193 | 33 | 0.4677 | 0.9263      | 0.20 | 0.8636  |

### 7.3 Per-Fold Results — Gradient Boosting (Highest Recall)

| Fold | TP | TN   | FP  | FN | Recall | Specificity | F1   | ROC-AUC |
|------|----|------|-----|----|--------|-------------|------|---------|
| 1    | 37 | 2345 | 272 | 25 | 0.5968 | 0.8961      | 0.20 | 0.8458  |
| 2    | 34 | 2427 | 190 | 28 | 0.5484 | 0.9274      | 0.24 | 0.8540  |
| 3    | 22 | 2356 | 261 | 40 | 0.3548 | 0.9003      | 0.13 | 0.7743  |
| 4    | 35 | 2390 | 227 | 27 | 0.5645 | 0.9133      | 0.22 | 0.8720  |

Note that Fold 1 of Gradient Boosting comes closest to the recall threshold at 0.5968, but still falls short of 0.60.

### 7.4 Train vs Test Gap — Gradient Boosting (Overfitting Analysis)

| Fold | Train Acc | Train Recall | Train F1 | Train AUC | Test Recall | Test F1 |
|------|-----------|--------------|----------|-----------|-------------|---------|
| 1    | 0.96      | 0.89         | 0.92     | 0.99      | 0.5968      | 0.20    |
| 2    | 0.93      | 0.77         | 0.85     | 0.99      | 0.5484      | 0.24    |
| 3    | 0.97      | 0.87         | 0.93     | 0.99      | 0.3548      | 0.13    |
| 4    | 0.95      | 0.84         | 0.90     | 0.99      | 0.5645      | 0.22    |

The train-to-test F1 gap for Gradient Boosting is approximately 0.68–0.80 points, indicating substantial overfitting to the balanced training set.

---

## 8. Excel & Pivot Table Analysis Guide

After running the pipeline, convert `reports/results/balancedDataOutcomes.csv` to Excel and follow these steps:

### Step 1: Add Derived Metric Columns

Using the Wikipedia Confusion Matrix formulas, add these Excel columns:

| Column | Formula (Excel, row 2) | Description |
|--------|------------------------|-------------|
| Accuracy    | `=(F2+G2)/(F2+G2+H2+I2)` | Overall correctness |
| Precision   | `=F2/(F2+H2)` | Positive predictive value |
| Recall (Sensitivity) | `=F2/(F2+I2)` | True positive rate |
| F1 Score    | `=2*(M2*N2)/(M2+N2)` | Harmonic mean |
| Specificity | `=G2/(G2+H2)` | True negative rate (Metric 1) |
| MCC         | `=(F2*G2-H2*I2)/SQRT((F2+H2)*(F2+I2)*(G2+H2)*(G2+I2))` | Matthews Correlation Coeff. (Metric 2) |

> Metrics 1 and 2 chosen: **Specificity** and **Matthews Correlation Coefficient (MCC)**. Both are robust to class imbalance — MCC in particular gives a single balanced measure even when classes are very unequal in size.

### Step 2: Create Pivot Tables

**Pivot Table 1 — Best Model by F1 Score**
- Rows: `Classifier Name`
- Columns: `Training or Test Set`
- Values: Average of `F1 Score`
- Filter: `Balanced or Unbalanced = Balanced`

**Pivot Table 2 — Constraint Check (Recall & Specificity)**
- Rows: `Classifier Name`
- Columns: `Training or Test Set`
- Values: Average of `Recall`, Average of `Specificity`
- Add conditional formatting: green if Recall ≥ 0.60, yellow if Specificity ≥ 0.70

**Pivot Table 3 — Overfitting Analysis**
- Rows: `Classifier Name`
- Columns: `Training or Test Set`
- Values: Average of `F1 Score`
- Create a Clustered Bar Chart from this table

**Pivot Table 4 — AUC-ROC Ranking**
- Rows: `Classifier Name`
- Values: Average of `ROC-AUC` (filter: Test Set only)
- Sort descending → insert Bar Chart

### Step 3: Recommended Excel Charts

1. **Clustered Bar Chart** — Mean F1 Score per classifier (Train vs Test), highlight gap to illustrate overfitting.
2. **Grouped Bar Chart** — Recall and Specificity per classifier on test set, draw reference lines at 0.60 and 0.70.
3. **Scatter Plot** — Precision vs Recall per classifier (bubble size = F1 score).
4. **Line Chart** — F1 score per fold per classifier (stability analysis).

---

## 9. Analytical Findings & Report Blueprint

### 9.1 No Classifier Satisfies Both Constraints

**Constraint 1:** Recall ≥ 60% (find at least 60% of bankrupt companies)
**Constraint 2:** Specificity ≥ 70% (find at least 70% of healthy companies)

| Classifier          | Mean Recall | Meets C1? | Mean Specificity | Meets C2? | Meets Both? |
|---------------------|-------------|-----------|-----------------|-----------|-------------|
| Random Forest       | 0.4718      | No        | 0.9242          | Yes       | No          |
| SVM                 | 0.3790      | No        | 0.9414          | Yes       | No          |
| Gradient Boosting   | 0.5161      | No        | 0.9093          | Yes       | No          |
| Logistic Regression | 0.3670      | No        | 0.9376          | Yes       | No          |
| LDA                 | 0.4153      | No        | 0.9255          | Yes       | No          |
| kNN                 | 0.4597      | No        | 0.8927          | Yes       | No          |
| Naive Bayes         | 0.5242      | No        | 0.8718          | Yes       | No          |
| Decision Tree       | 0.5242      | No        | 0.8160          | Yes       | No          |

**Answer to the assignment question:** No model satisfies both constraints simultaneously. The failure is structural: the test set reflects the full 97.7% / 2.3% class split (approximately 62 bankrupt companies per fold out of 2,679). Even with a balanced training set at 3:1, classifiers learn from only 186 bankrupt training examples, and must then detect bankrupt companies in a sea of healthy ones. The threshold between "enough true positives" and "too many false positives" cannot simultaneously meet Recall ≥ 60% and Specificity ≥ 70% at default decision boundaries for any of the 8 models evaluated.

### 9.2 Best Model by F1 Score

**Random Forest** achieves the highest mean test F1 of **0.2031** alongside the best AUC-ROC of **0.8512**. Despite not meeting the recall threshold, it strikes the best precision–recall balance overall and discriminates between classes more reliably than any other model.

### 9.3 Closest to Recall Constraint

**Gradient Boosting** (mean recall 0.5161) and jointly **Naive Bayes** and **Decision Tree** (mean recall 0.5242 each) come closest to the 60% recall target. Among these three, Gradient Boosting is preferred because it achieves similar recall with substantially better F1 (0.1952 vs 0.1506 and 0.1124) and AUC-ROC (0.8365 vs 0.8216 and 0.6701). In Fold 1, Gradient Boosting reaches a single-fold recall of 0.5968, the closest any model comes to the threshold across all 32 test evaluations.

### 9.4 Overfitting Analysis

Decision Tree and Random Forest show severe train-to-test F1 gaps:

| Classifier        | Train F1 (approx.) | Test F1 | Overfitting Severity |
|-------------------|--------------------|---------|----------------------|
| Decision Tree     | ~1.00              | 0.1124  | Severe               |
| Random Forest     | ~1.00              | 0.2031  | Severe               |
| Gradient Boosting | 0.85–0.93          | 0.1952  | Moderate-to-severe   |

Decision Tree overfits completely to the balanced training set (F1 ≈ 1.00) while delivering the worst test F1 of all models. Random Forest overfits equally on training but recovers partially on the test set due to variance reduction from bagging. Gradient Boosting trains to F1 in the range 0.85–0.93 (AUC 0.99 on train) but drops to 0.13–0.24 on test, confirming that the boosting ensemble also memorises training patterns that do not generalise to the imbalanced test distribution.

Linear models (LDA, Logistic Regression) and Naive Bayes exhibit far smaller train–test gaps, as expected from lower-capacity models.

### 9.5 Effect of Class Balancing

Without undersampling, tree-based models tend to achieve near-100% specificity by classifying almost everything as healthy — leading to near-zero recall for bankrupt companies. The 3:1 undersampling forces classifiers to learn bankrupt patterns at the cost of some specificity, which is the correct trade-off for this business problem. However, the extreme original imbalance (2.3% bankrupt) means that even after training on a balanced set, the test-time prior is dominated by healthy companies, suppressing recall regardless of the classifier chosen.

### 9.6 Model Interpretability Notes

- **LDA & Logistic Regression**: Fully interpretable via coefficients. Coefficients on financial indicators directly indicate which ratios are most predictive of bankruptcy.
- **Decision Tree**: High interpretability via tree visualization; severe overfitting observed in practice.
- **Random Forest / Gradient Boosting**: Feature importances available via `feature_importances_` attribute but predictions are not directly interpretable.
- **SVM**: Non-interpretable kernel model; strong generalization via margin maximization.
- **Naive Bayes**: Fast and interpretable, but the feature-independence assumption is unrealistic for correlated financial ratios.

---

## 10. Output Structure

```
1st-assignment/
├── data/
│   └── Dataset2Use_Assignment1.xlsx
├── configs/
│   └── config.yaml
├── src/bankruptcy_clf/            — main package (see §3)
├── scripts/
│   └── run_pipeline.py            — click CLI entry point
├── tests/
│   ├── test_dataset.py
│   ├── test_balancer.py
│   └── test_metrics.py
├── reports/
│   ├── figures/
│   │   ├── figure1_class_distribution_by_year.png
│   │   ├── figure2_indicator_statistics.png
│   │   ├── cm_fold0_LDA_Train_balanced.png
│   │   ├── cm_fold0_LDA_Test_balanced.png
│   │   └── ... (8 classifiers × 4 folds × 2 splits = 64 confusion matrix figures)
│   └── results/
│       └── balancedDataOutcomes.csv
└── logs/
    └── pipeline.log
```

### balancedDataOutcomes.csv Schema

| Column | Type | Description |
|--------|------|-------------|
| Classifier Name | str | Algorithm identifier |
| Training or Test Set | str | "Train" or "Test" |
| Balanced or Unbalanced | str | "Balanced" or "Unbalanced" |
| Fold | int | 1–4 |
| Number of Training Samples | int | Size of training set for this fold |
| Number of Non-Healthy Companies | int | Bankrupt count in training set |
| True Positives (TP) | int | Correctly predicted bankrupt |
| True Negatives (TN) | int | Correctly predicted healthy |
| False Positives (FP) | int | Healthy predicted as bankrupt |
| False Negatives (FN) | int | Bankrupt predicted as healthy |
| ROC-AUC | float | Area under ROC curve |
| Accuracy | float | Overall accuracy |
| Precision | float | Positive predictive value |
| Recall | float | Sensitivity / true positive rate |
| F1 Score | float | Harmonic mean of precision and recall |
| Specificity | float | True negative rate |

The CSV contains **64 rows** (8 classifiers × 4 folds × 2 splits: Train and Test).

---

*University of Macedonia — Machine Learning Assignment 1 | Academic Year 2022–2023*
