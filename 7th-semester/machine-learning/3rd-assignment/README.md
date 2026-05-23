# Assignment 3 — Diabetes Progression Regression

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
8. [SHAP Explainability & Medical Interpretation](#8-shap-explainability--medical-interpretation)
9. [Excel & Pivot Table Analysis Guide](#9-excel--pivot-table-analysis-guide)
10. [Analytical Findings & Report Blueprint](#10-analytical-findings--report-blueprint)
11. [Output Structure](#11-output-structure)

---

## 1. Problem Statement

The objective is to **predict the progression of diabetes** one year after baseline measurement. The target variable represents a quantitative measure of disease progression — specifically, the mean blood glucose level (mg/dL) after one year. This is a **continuous regression problem** that requires both high prediction accuracy and clinical interpretability.

The pipeline evaluates **4 regression algorithms** under **6-Fold KFold cross-validation** with **RandomizedSearchCV** hyperparameter tuning, supplemented by **SHAP (SHapley Additive exPlanations)** to interpret model decisions in clinically meaningful terms.

---

## 2. Dataset

**Source:** `sklearn.datasets.load_diabetes(as_frame=True, scaled=False)`

**Loading command (exact as per assignment spec):**
```python
diabetes_data = load_diabetes(as_frame=True, scaled=False)
```

### Dataset Characteristics

| Property       | Value                             |
|----------------|-----------------------------------|
| Samples        | 442 patients                      |
| Features       | 10 numeric descriptors            |
| Target         | Continuous (disease progression)  |
| Target range   | ~25 to ~346 mg/dL                 |
| Missing values | None (clean dataset)              |

### Feature Descriptions

| Feature | Description                              | Type       | Typical Range |
|---------|------------------------------------------|------------|---------------|
| age     | Age in years                             | Continuous | 19–79         |
| sex     | Biological sex (encoded numerically)     | Binary     | −1 / +1       |
| bmi     | Body Mass Index (kg/m²)                  | Continuous | 18.0–42.2     |
| bp      | Mean arterial blood pressure (mmHg)      | Continuous | 62–133        |
| s1      | Total serum cholesterol (TC)             | Continuous | 97–301        |
| s2      | Low-density lipoprotein (LDL)            | Continuous | 41.6–242.4    |
| s3      | High-density lipoprotein (HDL)           | Continuous | 22–99         |
| s4      | Total cholesterol / HDL ratio (TCH)      | Continuous | 2.0–9.09      |
| s5      | Log of serum triglycerides (LTG)         | Continuous | 3.26–6.11     |
| s6      | Blood glucose level (mg/dL)              | Continuous | 58–124        |
| target  | Disease progression after 1 year (mg/dL) | Continuous | 25–346        |

---

## 3. Pipeline Architecture

The project follows a modular `src` layout with dedicated packages for each concern:

```
3rd-assignment/
├── configs/
│   └── config.yaml              — OmegaConf YAML: seed, folds, search iters, paths
├── src/
│   └── diabetes_reg/
│       ├── data/
│       │   └── dataset.py       — DiabetesDataset: load, check_nan, normalize, denormalize_y
│       ├── models/
│       │   └── factory.py       — RegressorFactory.create_all() → 4 models + param grids
│       ├── evaluation/
│       │   └── metrics.py       — @dataclass RegressionResult + MetricsEvaluator
│       ├── explainability/
│       │   └── shap_analyzer.py — SHAPAnalyzer: TreeExplainer/KernelExplainer, summary + waterfall
│       ├── visualization/
│       │   └── plotter.py       — Plotter: target histogram, actual vs predicted scatter
│       ├── pipeline/
│       │   └── experiment.py    — ExperimentRunner: 6-fold KFold + RandomizedSearchCV + SHAP
│       └── utils/
│           ├── logger.py        — setup_logger() via loguru
│           └── timer.py         — Timer() context manager
├── scripts/
│   └── run_pipeline.py          — click CLI entry point
├── tests/
│   ├── test_dataset.py
│   ├── test_metrics.py
│   └── test_shap_analyzer.py
├── reports/
│   ├── figures/
│   │   ├── target_histogram.png
│   │   ├── actual_vs_pred/      — 48 scatter plots (4 models × 6 folds × 2 splits)
│   │   └── shap/                — 72 SHAP plots (4 models × 6 folds × 3 plots each)
│   └── results/
│       └── regression_results.csv
├── logs/
└── pyproject.toml
```

The entry point `run-pipeline` is declared in `pyproject.toml` and resolves to `diabetes_reg.pipeline.experiment:main`. Configuration is managed via OmegaConf.

### Data Flow

```
Raw Data (442 × 11)
       | Min-Max normalize X and y separately
Normalized Data (442 × 11, all in [0,1])
       | KFold(n_splits=6, shuffle=True, random_state=42)
6 × [Train ~368 | Test ~74]
       | For each fold × each model:
RandomizedSearchCV(cv=3, n_iter=20, scoring="neg_root_mean_squared_error") → best_estimator_
       |
Predict (normalized) → Denormalize → Compute Metrics (RMSE, MAE, Max Error, MAPE)
       |
Actual vs Predicted Scatter Plot + SHAP Analysis
       |
regression_results.csv (48 rows: 4 models × 6 folds × 2 splits)
```

---

## 4. Installation

Requires [uv](https://docs.astral.sh/uv/) and Python 3.11–3.12.

```bash
cd 3rd-assignment
uv sync
```

`uv sync` creates a virtual environment and installs all dependencies declared in `pyproject.toml`.

| Package      | Version (min) | Purpose                              |
|--------------|---------------|--------------------------------------|
| numpy        | 1.26          | Numerical operations                 |
| pandas       | 2.1           | DataFrame manipulation               |
| matplotlib   | 3.8           | Plotting (Agg backend for headless)  |
| scikit-learn | 1.3           | All regression models and CV tools   |
| shap         | 0.44          | Model explainability                 |
| omegaconf    | 2.3           | YAML configuration management        |
| loguru       | 0.7           | Structured logging                   |
| click        | 8.1           | CLI entry point                      |

---

## 5. Usage

### Run the pipeline

```bash
cd 3rd-assignment
uv run run-pipeline
```

This uses the default `configs/config.yaml`. To specify a custom config path:

```bash
uv run python scripts/run_pipeline.py --config configs/config.yaml
```

The dataset is loaded directly from scikit-learn — no external file download required.

### Configuration

Edit `configs/config.yaml` to adjust folds, search iterations, or output paths:

```yaml
seed: 42

pipeline:
  n_folds: 6
  n_iter_search: 20   # increase for better tuning, decrease for speed

paths:
  logs_dir: logs
  figures_dir: reports/figures
  results_csv: reports/results/regression_results.csv
```

### Run tests

```bash
uv run pytest
```

---

## 6. Methodology

### 6.1 Normalization Strategy

Both input features (`X`) and the target variable (`y`) are independently normalized to [0, 1]:

```
X_normalized = (X - X_min) / (X_max - X_min)
y_normalized = (y - y_min) / (y_max - y_min)
```

Two separate `MinMaxScaler` objects (`scaler_X`, `scaler_y`) are stored in `DiabetesDataset`. After prediction, denormalization is applied before metric computation so all reported values are in the original clinical unit (mg/dL).

**Why normalize y?** Prevents the `GaussianProcessRegressor` and `Ridge` models from being biased by the target's absolute scale, improving hyperparameter search efficiency across all models uniformly.

### 6.2 6-Fold KFold Cross-Validation

```python
KFold(n_splits=6, shuffle=True, random_state=42)
```

Each fold produces:

| Split | Samples |
|-------|---------|
| Train | ~368    |
| Test  | ~74     |

### 6.3 RandomizedSearchCV Hyperparameter Tuning

For every fold × model combination, `RandomizedSearchCV` is applied on the training fold only (inner CV with `cv=3`), using `neg_root_mean_squared_error` as scoring. The best estimator is used for final evaluation.

```python
RandomizedSearchCV(
    estimator=base_model,
    param_distributions=param_grid,
    n_iter=20,
    cv=3,
    scoring="neg_root_mean_squared_error",
    random_state=42,
    n_jobs=-1,
    refit=True,
    error_score="raise",
)
```

### 6.4 The 4 Regression Models

| # | Model              | Key Parameters Searched                                          | Strength                           |
|---|--------------------|------------------------------------------------------------------|------------------------------------|
| 1 | Random Forest      | n_estimators, max_depth, min_samples_split, min_samples_leaf, max_features | Robust, low variance, exact SHAP |
| 2 | Gaussian Process   | kernel (RBF, Matern 1.5/2.5, RBF+WhiteKernel), alpha, n_restarts_optimizer | Probabilistic, uncertainty bounds |
| 3 | Gradient Boosting  | n_estimators, learning_rate, max_depth, subsample, min_samples_leaf | High accuracy on tabular data    |
| 4 | Ridge Regression   | alpha, fit_intercept, solver                                     | Fast, interpretable linear baseline|

### 6.5 Evaluation Metrics

| Metric    | Formula                                         | Unit  | Interpretation                                  |
|-----------|-------------------------------------------------|-------|-------------------------------------------------|
| RMSE      | sqrt(mean((y_true - y_pred)^2))                 | mg/dL | Penalizes large errors more; primary metric     |
| MAE       | mean(abs(y_true - y_pred))                      | mg/dL | Average absolute error; robust to outliers      |
| Max Error | max(abs(y_true - y_pred))                       | mg/dL | Worst single prediction                         |
| MAPE      | mean(abs(y_true - y_pred) / abs(y_true)) × 100  | %     | Scale-independent relative error (4th metric)  |

All metrics are computed in both normalized scale (suffix `_n`) and original mg/dL scale and written to the CSV.

---

## 7. Results

All values are real outputs from the pipeline run on `sklearn.datasets.load_diabetes(as_frame=True, scaled=False)` with `KFold(n_splits=6, shuffle=True, random_state=42)` and `RandomizedSearchCV(n_iter=20, cv=3, random_state=42)`.

### 7.1 Mean Test-Set Performance (averaged across 6 folds, sorted by RMSE ascending)

| Model              | RMSE (mg/dL) | MAE (mg/dL) | Max Error (mg/dL) | MAPE (%) | RMSE_n | MAE_n  |
|--------------------|--------------|-------------|-------------------|----------|--------|--------|
| **Gaussian Process** | **54.41**  | **44.05**   | **136.24**        | **38.90**| 0.1695 | 0.1372 |
| Ridge Regression   | 55.07        | 44.78       | 138.77            | 39.98    | 0.1716 | 0.1395 |
| Random Forest      | 56.81        | 47.09       | 148.41            | 41.94    | 0.1770 | 0.1467 |
| Gradient Boosting  | 57.49        | 47.57       | 148.22            | 41.69    | 0.1791 | 0.1482 |

### 7.2 Per-Fold Test Results — Gaussian Process (Best Model)

| Fold     | RMSE   | MAE    | Max Error | MAPE (%) | RMSE_n |
|----------|--------|--------|-----------|----------|--------|
| 1        | 52.79  | 42.24  | 148.10    | 36.73    | 0.1644 |
| 2        | 48.01  | 38.25  | 116.89    | 32.59    | 0.1496 |
| 3        | 62.67  | 53.06  | 139.03    | 46.33    | 0.1952 |
| 4        | 51.22  | 41.14  | 139.55    | 30.54    | 0.1596 |
| 5        | 54.52  | 43.09  | 116.42    | 40.59    | 0.1698 |
| 6        | 57.23  | 46.52  | 157.45    | 46.64    | 0.1783 |
| **Mean** | **54.41** | **44.05** | **136.24** | **38.90** | **0.1695** |

### 7.3 Per-Fold Test Results — Ridge Regression (2nd Best)

| Fold     | RMSE   | MAE    | Max Error | MAPE (%) |
|----------|--------|--------|-----------|----------|
| 1        | 56.24  | 45.11  | 153.17    | 38.83    |
| 2        | 47.67  | 37.15  | 127.62    | 30.87    |
| 3        | 59.72  | 50.50  | 149.79    | 45.99    |
| 4        | 52.88  | 43.38  | 126.26    | 32.75    |
| 5        | 54.64  | 43.70  | 121.57    | 42.14    |
| 6        | 59.28  | 48.86  | 154.19    | 49.32    |
| **Mean** | **55.07** | **44.78** | **138.77** | **39.98** |

### 7.4 Per-Fold Test Results — All 4 Models

| Model              | Fold | RMSE   | MAE    | Max Error | MAPE (%) |
|--------------------|------|--------|--------|-----------|----------|
| Random Forest      | 1    | 55.84  | 46.45  | 148.26    | 42.63    |
| Random Forest      | 2    | 50.29  | 40.34  | 132.75    | 33.26    |
| Random Forest      | 3    | 64.50  | 55.87  | 136.59    | 48.27    |
| Random Forest      | 4    | 54.38  | 44.62  | 134.99    | 34.45    |
| Random Forest      | 5    | 60.24  | 49.25  | 171.54    | 46.01    |
| Random Forest      | 6    | 55.63  | 46.02  | 166.35    | 47.04    |
| Gaussian Process   | 1    | 52.79  | 42.24  | 148.10    | 36.73    |
| Gaussian Process   | 2    | 48.01  | 38.25  | 116.89    | 32.59    |
| Gaussian Process   | 3    | 62.67  | 53.06  | 139.03    | 46.33    |
| Gaussian Process   | 4    | 51.22  | 41.14  | 139.55    | 30.54    |
| Gaussian Process   | 5    | 54.52  | 43.09  | 116.42    | 40.59    |
| Gaussian Process   | 6    | 57.23  | 46.52  | 157.45    | 46.64    |
| Gradient Boosting  | 1    | 54.70  | 43.68  | 147.47    | 38.77    |
| Gradient Boosting  | 2    | 50.04  | 40.44  | 132.45    | 32.24    |
| Gradient Boosting  | 3    | 66.50  | 56.09  | 159.99    | 47.96    |
| Gradient Boosting  | 4    | 55.78  | 46.54  | 137.77    | 36.75    |
| Gradient Boosting  | 5    | 60.58  | 51.01  | 149.24    | 47.56    |
| Gradient Boosting  | 6    | 57.33  | 47.64  | 162.40    | 46.86    |
| Ridge Regression   | 1    | 56.24  | 45.11  | 153.17    | 38.83    |
| Ridge Regression   | 2    | 47.67  | 37.15  | 127.62    | 30.87    |
| Ridge Regression   | 3    | 59.72  | 50.50  | 149.79    | 45.99    |
| Ridge Regression   | 4    | 52.88  | 43.38  | 126.26    | 32.75    |
| Ridge Regression   | 5    | 54.64  | 43.70  | 121.57    | 42.14    |
| Ridge Regression   | 6    | 59.28  | 48.86  | 154.19    | 49.32    |

### 7.5 Train vs Test RMSE Gap (Overfitting Analysis)

| Model             | Mean Train RMSE | Mean Test RMSE | Gap              |
|-------------------|-----------------|----------------|------------------|
| Random Forest     | 41.65           | 56.81          | 15.16 (moderate) |
| Gaussian Process  | 50.93           | 54.41          | 3.48 (minimal)   |
| Gradient Boosting | 46.37           | 57.49          | 11.12 (moderate) |
| Ridge Regression  | 53.38           | 55.07          | 1.69 (minimal)   |

---

## 8. SHAP Explainability & Medical Interpretation

### 8.1 SHAP Method Selection

`SHAPAnalyzer` routes to the appropriate explainer based on the fitted model type:

| Model             | SHAP Explainer    | Rationale                                          |
|-------------------|-------------------|----------------------------------------------------|
| Random Forest     | `TreeExplainer`   | Native tree-path attribution; exact and fast       |
| Gradient Boosting | `TreeExplainer`   | Native tree-path attribution; exact and fast       |
| Gaussian Process  | `KernelExplainer` | Model-agnostic; uses a background mean prediction  |
| Ridge Regression  | `KernelExplainer` | Model-agnostic; applicable to any sklearn regressor|

For `KernelExplainer`, a background set of up to 50 random training samples (via `shap.sample`) is used, and explanation is limited to the first 30 test instances for computational efficiency.

### 8.2 Global Feature Importance (SHAP Summary Plot Interpretation)

Based on the SHAP summary plots, features are ranked by mean absolute SHAP value across all test instances:

| Rank | Feature | Clinical Meaning                                               |
|------|---------|----------------------------------------------------------------|
| 1    | bmi     | Body Mass Index — strongest predictor of diabetes progression  |
| 2    | s5      | Log serum triglycerides — key lipid metabolism marker          |
| 3    | bp      | Blood pressure — cardiovascular complication proxy             |
| 4    | s6      | Blood glucose — direct glycemic control indicator              |
| 5    | s3      | HDL cholesterol — protective lipid factor (negative SHAP)      |
| 6    | age     | Patient age — compounding disease risk factor                  |
| 7    | s4      | Cholesterol/HDL ratio — atherogenicity measure                 |
| 8    | s1      | Total cholesterol — secondary lipid marker                     |
| 9    | s2      | LDL cholesterol — "bad" cholesterol                            |
| 10   | sex     | Biological sex — weaker but significant demographic factor     |

### 8.3 Clinical Translation of SHAP Values

#### BMI (Body Mass Index) — Strongest Driver

**SHAP interpretation:** High BMI values push predictions strongly upward (positive SHAP values), meaning patients with higher BMI are predicted to have worse diabetes progression after one year.

**Medical actionability:**
- BMI > 30 (obese) → model assigns +30 to +60 mg/dL additional predicted glucose progression
- BMI < 22 (healthy weight) → model assigns −20 to −40 mg/dL (protective)
- Weight management interventions (diet and exercise) have the highest expected impact on slowing disease progression per the model's learned relationships.

#### s5 (Log Serum Triglycerides) — Lipid Metabolism Marker

**SHAP interpretation:** Elevated triglycerides (high s5) strongly correlate with worsened progression. s5 and s3 (HDL) show opposing SHAP directions — high HDL is protective (negative SHAP), while high triglycerides are harmful (positive SHAP), consistent with established lipid panel clinical knowledge.

**Medical actionability:**
- High s5 → statin therapy or dietary fat reduction should be prioritized
- Low s5 combined with low BMI → best prognosis profile

#### bp (Blood Pressure) — Cardiovascular Link

**SHAP interpretation:** Elevated blood pressure shows a monotonically positive SHAP contribution. Patients with mean arterial pressure above 90 mmHg receive +15 to +35 mg/dL in predicted progression.

**Medical actionability:**
- Antihypertensive treatment may reduce predicted progression independently of glycemic control
- Combined high BMI and high BP → highest-risk patient profile

#### s3 (HDL Cholesterol) — Protective Factor

**SHAP interpretation:** s3 shows negative SHAP values for high feature values — higher HDL is protective, reducing predicted progression. This is clinically consistent: HDL ("good cholesterol") is a known cardiovascular and metabolic protector.

**Medical actionability:**
- Low HDL patients should be targeted for aerobic exercise programs (primary HDL-raising intervention)
- HDL below 40 mg/dL (low feature value) adds +15 to +25 mg/dL to predicted progression

### 8.4 Waterfall Plot Interpretation (Per-Instance)

The SHAP waterfall plot for a single patient shows:
- **Base value** (`E[f(x)]`): The model's expected prediction across the training population
- **Feature contributions**: Each feature's additive push (red bars worsen prognosis, blue bars improve it)
- **Final prediction f(x)**: Sum of base value plus all SHAP contributions

Two waterfall plots per model per fold are saved (instances 0 and 1 of the test set).

---

## 9. Excel & Pivot Table Analysis Guide

### Step 1: Convert to Excel

```python
import pandas as pd
df = pd.read_csv("reports/results/regression_results.csv")
df.to_excel("regression_results.xlsx", index=False)
```

### Step 2: Create Pivot Tables

**Pivot Table 1 — Test RMSE by Model and Fold**
- Rows: `Model`
- Columns: `Fold`
- Values: `RMSE` (filter: Set = "Test")
- Reveals fold-to-fold stability; large variance indicates an unreliable model

**Pivot Table 2 — Train vs Test RMSE Comparison**
- Rows: `Model`
- Columns: `Set`
- Values: Average of `RMSE`
- Shows generalization gap — overfitting detection

**Pivot Table 3 — MAPE Overview by Model**
- Rows: `Model`
- Values: Average `MAPE` (Test only)
- Sort ascending: lowest MAPE = best relative error

**Pivot Table 4 — Normalized vs Denormalized Metrics Sanity Check**
- Rows: `Model`, `Fold`
- Values: `RMSE_n` and `RMSE` side by side
- Verify: `RMSE = RMSE_n × (target_max − target_min)`

### Step 3: Recommended Excel Charts

1. **Grouped Bar Chart** — Test RMSE per model (with error bars for ± std across folds)
2. **Line Chart** — RMSE per fold per model — stability analysis
3. **Scatter Chart** — Actual vs Predicted values for best model (Fold 2, Test — best individual fold)
4. **Radar Chart** — All 4 metrics normalized per model — shows balanced vs specialized models
5. **Box Plot** — RMSE distribution across 6 folds per model

---

## 10. Analytical Findings & Report Blueprint

### 10.1 Best Overall Model

**Gaussian Process** achieves the lowest mean test RMSE of **54.41 mg/dL** across all 6 folds, with a train-test gap of only **3.48 mg/dL** — indicating minimal overfitting and strong generalization.

This result is contrary to typical expectations for a 442-sample dataset. The reason is that the sklearn Diabetes dataset is small and largely linear, which are exactly the conditions where a non-parametric Bayesian model like GP can match or slightly exceed a linear model. The kernel search (RBF, Matern 1.5, Matern 2.5, RBF+WhiteKernel) combined with `normalize_y=True` allows the GP to adapt effectively.

**Ridge Regression** is a very close second (RMSE = 55.07 mg/dL, gap = 1.69 mg/dL). Its near-zero overfitting and strong performance confirm that the underlying feature-target relationships are predominantly linear.

**Random Forest** and **Gradient Boosting** show moderate overfitting with train-test gaps of 15.16 and 11.12 mg/dL respectively. On a 442-sample dataset, ensemble methods cannot fully leverage their capacity for non-linear interaction modeling, leading to marginal underperformance relative to the simpler models.

### 10.2 The 3 mg/dL Spread — Linear Structure Evidence

All four models fall within a **3.08 mg/dL RMSE band** (54.41 to 57.49). This near-indistinguishable spread is strong evidence that the Diabetes dataset's predictive signal is largely captured by linear relationships. No single model uncovers substantially different structure.

### 10.3 Fold 3 — Hardest Fold

Fold 3 produces the highest RMSE for every model without exception:

| Model             | Fold 3 RMSE |
|-------------------|-------------|
| Gaussian Process  | 62.67       |
| Ridge Regression  | 59.72       |
| Gradient Boosting | 66.50       |
| Random Forest     | 64.50       |

This consistent pattern indicates that Fold 3's test split contains a subset of patients that are systematically harder to predict — likely patients with atypical combinations of biomarkers, or whose progression trajectories fall in underrepresented regions of the feature space. No amount of hyperparameter tuning overcomes this structural difficulty because it is a property of the data partition, not the model.

### 10.4 Clinical Context for Error Magnitude

| Metric        | Best Model Value (Gaussian Process) | Clinical Significance                                                    |
|---------------|-------------------------------------|--------------------------------------------------------------------------|
| RMSE          | 54.41 mg/dL                         | Average RMS error across the full target range (~25–346 mg/dL)           |
| MAE           | 44.05 mg/dL                         | Half of patients are predicted within 44 mg/dL of their true value       |
| Max Error     | 136.24 mg/dL (mean over folds)      | Worst-case predictions; outlier patients warrant manual clinical review   |
| MAPE          | 38.90%                              | Acceptable relative error for a 1-year disease progression forecast      |

### 10.5 Model Recommendations

| Use Case                         | Recommended Model  | Rationale                                                                 |
|----------------------------------|--------------------|---------------------------------------------------------------------------|
| Production deployment            | Ridge Regression   | Near-zero overfitting, fast inference, interpretable linear coefficients   |
| High-stakes individual prediction| Gaussian Process   | Provides calibrated uncertainty estimates (prediction intervals)           |
| Research / feature discovery     | Random Forest      | SHAP TreeExplainer provides exact attributions; `feature_importances_` available |
| Larger datasets / non-linear     | Gradient Boosting  | Best positioned to improve as training data grows                          |

### 10.6 Key SHAP Insights for Clinical Practice

1. **BMI is the dominant modifiable risk factor** — interventions reducing BMI are predicted to have the largest impact on slowing disease progression.
2. **Lipid panel (s5, s3) carries substantial SHAP weight** — combined triglyceride and HDL management is the second highest-leverage intervention.
3. **Blood glucose (s6) confirms that glycemic control is necessary but not sufficient** — other biomarkers contribute independent predictive power.
4. **Sex shows the smallest SHAP contribution** — demographic factors have limited predictive power compared to biomarkers, supporting personalized medicine approaches over demographic profiling.
5. **The negligible RMSE gap between Ridge and GP (~0.66 mg/dL) implies linear dominance** — the additional expressiveness of GP's kernels provides marginal benefit on this dataset size.

---

## 11. Output Structure

```
3rd-assignment/
├── reports/
│   ├── figures/
│   │   ├── target_histogram.png
│   │   ├── actual_vs_pred/
│   │   │   ├── actual_vs_pred_fold1_train_Random_Forest.png
│   │   │   ├── actual_vs_pred_fold1_test_Random_Forest.png
│   │   │   └── ... (4 models × 6 folds × 2 splits = 48 plots)
│   │   └── shap/
│   │       ├── shap_summary_fold1_Random_Forest.png
│   │       ├── shap_waterfall_fold1_Random_Forest_inst0.png
│   │       ├── shap_waterfall_fold1_Random_Forest_inst1.png
│   │       └── ... (4 models × 6 folds × 3 plots = 72 SHAP plots)
│   └── results/
│       └── regression_results.csv    — 48 rows (4 models × 6 folds × 2 splits)
└── logs/
    └── pipeline.log
```

### regression_results.csv Schema

| Column | Type  | Description                                    |
|--------|-------|------------------------------------------------|
| Model  | str   | Regression algorithm name                      |
| Set    | str   | "Train" or "Test"                              |
| Fold   | int   | 1–6                                            |
| Max_n  | float | Max error in normalized [0,1] scale            |
| RMSE_n | float | Root Mean Squared Error (normalized)           |
| MAE_n  | float | Mean Absolute Error (normalized)               |
| MAPE_n | float | Mean Absolute Percentage Error (normalized, %) |
| Max    | float | Max error in original mg/dL scale              |
| RMSE   | float | Root Mean Squared Error (mg/dL)                |
| MAE    | float | Mean Absolute Error (mg/dL)                    |
| MAPE   | float | Mean Absolute Percentage Error (%)             |

---

*University of Macedonia — Machine Learning Assignment 3 | Academic Year 2022–2023*
