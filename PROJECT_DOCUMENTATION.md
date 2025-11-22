# Metabolic Profiling Project - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Task-by-Task Documentation](#task-by-task-documentation)
4. [Code Structure](#code-structure)
5. [Data Flow](#data-flow)
6. [Output Files](#output-files)
7. [Clinical Context](#clinical-context)

---

## Project Overview

This project implements a complete machine learning pipeline to identify distinct metabolic subtypes in the NHANES 2013-2014 dataset. The workflow processes raw survey data through imputation, feature engineering, normalization, and unsupervised clustering to reveal metabolic phenotypes.

### Objectives
- Download and prepare NHANES 2013-2014 data for participants aged 35+
- Handle missing values using robust imputation methods
- Engineer clinically relevant features (HOMA-IR)
- Identify optimal number of metabolic subtypes
- Cluster participants into distinct metabolic profiles
- Provide interpretable results for clinical application

---

## Architecture

### Pipeline Flow

```
Raw NHANES Data
    ↓
[Task 1] Data Acquisition & Filtering (Age 35+)
    ↓
[Task 1] MICE Imputation
    ↓
[Task 2] Feature Engineering (HOMA-IR)
    ↓
[Task 3] StandardScaler Normalization
    ↓
[Task 3] Train/Test Split (70/30)
    ↓
[Task 4] Optimal Cluster Determination (k=2 to 10)
    ↓
[Task 5] K-Means Clustering (k=4)
    ↓
Metabolic Subtype Profiles
```

---

## Task-by-Task Documentation

### Task 1: Data Acquisition and Preparation

**Script**: `123.py` (Lines 37-95)

**Purpose**: Download NHANES data, filter by age, and impute missing values

**Process**:
1. Initialize NHANES downloader for 2013-2014 cycle
2. Download demographic and laboratory variables:
   - Demographics: Age (RIDAGEYR)
   - Laboratory: Fasting Glucose (LBDGLU), Insulin (LBDIN), HbA1c (LBXGH), Triglycerides (LBXTR), Creatinine (LBXSC)
3. Merge datasets using participant ID (SEQN)
4. Filter to participants aged 35 years and older
5. Apply MICE imputation using `IterativeImputer`:
   - Max iterations: 10
   - Random state: 42
   - Models each feature as function of other features

**Key Variables**:
```python
NHANES_VARS = {
    'DEMO': ['SEQN', 'RIDAGEYR'],
    'GLU': ['SEQN', 'LBDGLU'],
    'INS': ['SEQN', 'LBDIN'],
    'GHB': ['SEQN', 'LBXGH'],
    'TGL_HDL': ['SEQN', 'LBXTR'],
    'CKD': ['SEQN', 'LBXSC']
}
```

**Output**: `nhanes_metabolic_imputed_task1.csv`

---

### Task 2: Feature Engineering

**Script**: `123.py` (Lines 97-119)

**Purpose**: Calculate HOMA-IR and prepare final feature set

**Process**:
1. Calculate HOMA-IR using formula:
   ```
   HOMA_IR = (Fasting Insulin × Fasting Blood Sugar) / 405
   ```
2. Define final 6-feature dataset:
   - HOMA_IR (calculated)
   - FI (Fasting Insulin)
   - HbA1c
   - FBS (Fasting Blood Sugar)
   - TGL (Triglycerides)
   - Creatinine

**Clinical Significance**:
- HOMA-IR is a key indicator of insulin resistance
- Higher values indicate greater insulin resistance
- Normal range: < 1.0, Borderline: 1.0-2.5, Insulin Resistant: > 2.5

**Output**: Updated `nhanes_metabolic_imputed_task1.csv` with HOMA_IR column

---

### Task 3: Data Normalization and Train-Test Split

**Script**: `123.py` (Lines 121-189)

**Purpose**: Normalize features and split data for model validation

**Process**:
1. Extract 6-feature dataset
2. Apply StandardScaler (Z-score normalization):
   - Transforms each feature to mean=0, std=1
   - Ensures equal feature contribution to clustering
3. Split data:
   - 70% training set
   - 30% test set
   - Random state: 42 (reproducibility)
   - Shuffle: True

**Why Normalization?**
- Features have different scales (e.g., FI: 2-25, FBS: 70-126)
- Without normalization, features with larger values dominate clustering
- Z-score normalization ensures all features contribute equally

**Output Files**:
- `X_train_scaled.npy` / `X_train_scaled.csv`
- `X_test_scaled.npy` / `X_test_scaled.csv`
- `scaler_params.npy` (for inverse transformation)

---

### Task 4: Optimal Cluster Determination

**Script**: `task4_cluster_determination.py`

**Purpose**: Determine optimal number of metabolic subtypes (k)

**Methods**:

#### 1. Elbow Method
- **Metric**: Inertia (Within-Cluster Sum of Squares)
- **Principle**: Look for "elbow" where rate of decrease slows
- **Interpretation**: Point of diminishing returns in cluster compactness

#### 2. Silhouette Score
- **Metric**: Average silhouette coefficient
- **Range**: -1 (poor) to +1 (excellent)
- **Interpretation**: Higher scores indicate better-defined clusters

**Process**:
1. Test k values from 2 to 10
2. For each k:
   - Train K-Means model
   - Calculate inertia
   - Calculate silhouette score
3. Visualize both metrics
4. Identify optimal k

**Typical Results**:
- Clinical relevance suggests 4-5 subtypes
- Statistical metrics may suggest different k
- Consider both for final decision

**Output**: `visualizations/4_optimal_clusters.png`

---

### Task 5: Core Clustering

**Script**: `task5_clustering.py`

**Purpose**: Apply K-Means clustering with optimal k to identify metabolic subtypes

**Process**:
1. Load scaled training data
2. Load original unscaled data (for inverse transformation)
3. Train K-Means model:
   - k = 4 (from Task 4)
   - Random state: 42
   - Max iterations: 300
4. Assign cluster labels to all data (train + test)
5. Unscale cluster centers:
   - Transform centers back to original units
   - Enables clinical interpretation
6. Display and save results

**Key Output**: Cluster Centers Table
```
            HOMA_IR    FI  HbA1c    FBS    TGL  Creatinine
Subtype ID                                                
Subtype 0      2.15   8.5    5.2   95.0   85.0        0.85
Subtype 1      4.80  18.2    5.8  108.0  145.0        0.92
Subtype 2      8.50  32.5    6.5  118.0  220.0        0.98
Subtype 3      1.80   6.8    4.9   88.0   65.0        0.78
```

**Output Files**:
- `output/nhanes_metabolic_labeled_task5.csv` - Full dataset with subtype labels
- `output/metabolic_subtype_centers_task5.csv` - Cluster centers (unscaled)

---

## Code Structure

### Main Scripts

#### `123.py` - Main Data Pipeline
- **Lines 1-16**: Imports and setup
- **Lines 18-35**: Variable definitions
- **Lines 37-95**: Task 1 (Data acquisition and imputation)
- **Lines 97-119**: Task 2 (Feature engineering)
- **Lines 121-189**: Task 3 (Normalization and splitting)

#### `eda.py` - Exploratory Data Analysis
- Distribution plots (KDE)
- Correlation heatmap
- Pair plots

#### `visualize.py` - Comprehensive Visualization
- Multiple visualization types
- Works with sample data if real data unavailable
- Saves all plots to `visualizations/` directory

#### `task4_cluster_determination.py` - Cluster Optimization
- Elbow method implementation
- Silhouette score calculation
- Visualization of both metrics

#### `task5_clustering.py` - Final Clustering
- K-Means implementation
- Cluster center unscaling
- Results export

---

## Data Flow

### Input Data
- **Source**: NHANES 2013-2014
- **Format**: XPT files (SAS transport format)
- **Download**: Automated via `nhanes-dl` library

### Processing Steps
1. **Raw Data** → Merged DataFrame
2. **Merged Data** → Age-filtered (35+)
3. **Filtered Data** → Imputed (MICE)
4. **Imputed Data** → Feature-engineered (HOMA-IR)
5. **Engineered Data** → Normalized (StandardScaler)
6. **Normalized Data** → Split (Train/Test)
7. **Scaled Data** → Clustered (K-Means)
8. **Clusters** → Unscaled centers

### Output Data
- **Intermediate**: CSV and NumPy files
- **Final**: Labeled dataset and cluster centers
- **Visualizations**: PNG files

---

## Output Files

### Data Files

| File | Description | Format |
|------|-------------|--------|
| `nhanes_metabolic_imputed_task1.csv` | Imputed data with all features | CSV |
| `X_train_scaled.npy` | Scaled training data | NumPy |
| `X_test_scaled.npy` | Scaled test data | NumPy |
| `X_train_scaled.csv` | Scaled training data | CSV |
| `X_test_scaled.csv` | Scaled test data | CSV |
| `scaler_params.npy` | Scaler parameters | NumPy |
| `nhanes_metabolic_labeled_task5.csv` | Full dataset with subtype labels | CSV |
| `metabolic_subtype_centers_task5.csv` | Cluster centers (unscaled) | CSV |

### Visualization Files

| File | Description |
|------|-------------|
| `1_distributions.png` | Feature distribution plots (KDE) |
| `2_correlation_heatmap.png` | Correlation matrix visualization |
| `3_pairplot.png` | Pairwise feature relationships |
| `4_boxplots.png` | Box plots for all features |
| `5_homa_relationships.png` | HOMA-IR vs FBS and FI |
| `4_optimal_clusters.png` | Elbow and silhouette plots |

---

## Clinical Context

### Metabolic Syndrome Components

The features analyzed represent key components of metabolic health:

1. **Insulin Resistance (HOMA-IR, FI, FBS)**
   - Central to metabolic syndrome
   - Predicts type 2 diabetes risk

2. **Glycemic Control (HbA1c, FBS)**
   - Long-term and short-term glucose levels
   - Diabetes diagnosis and monitoring

3. **Lipid Metabolism (TGL)**
   - Cardiovascular risk factor
   - Part of metabolic syndrome criteria

4. **Kidney Function (Creatinine)**
   - Metabolic health indicator
   - Diabetes complication marker

### Metabolic Subtype Interpretation

Each cluster center represents a distinct metabolic phenotype:

- **Healthy Profile**: Low values across all features
- **Moderate Risk**: Borderline values, early metabolic changes
- **High Risk**: Elevated insulin resistance, prediabetes range
- **Very High Risk**: Diabetes range values, high triglycerides

### Clinical Applications

1. **Risk Stratification**: Identify high-risk individuals
2. **Personalized Medicine**: Tailor interventions to subtype
3. **Prevention**: Target early metabolic changes
4. **Research**: Understand metabolic heterogeneity

---

## Technical Details

### Imputation Strategy

**MICE (Multiple Imputation by Chained Equations)**
- Iterative process
- Models each feature with missing values
- Uses other features as predictors
- Converges to stable imputations

**Why MICE?**
- Handles missing data in real-world surveys
- Preserves relationships between features
- More robust than simple imputation methods

### Clustering Algorithm

**K-Means Clustering**
- Partitioning method
- Minimizes within-cluster sum of squares
- Requires pre-specified k
- Sensitive to initialization (mitigated with random_state=42)

**Why K-Means?**
- Interpretable results
- Fast and scalable
- Works well with normalized data
- Produces distinct, non-overlapping clusters

### Validation Strategy

**Train-Test Split**
- 70% training: Model development
- 30% test: Validation (future use)
- Ensures generalizability

**Reproducibility**
- Random state: 42 (all scripts)
- Ensures consistent results across runs

---

## Future Enhancements

### Potential Improvements

1. **Alternative Clustering Methods**
   - Hierarchical clustering
   - DBSCAN (density-based)
   - Gaussian Mixture Models

2. **Feature Selection**
   - Identify most discriminative features
   - Reduce dimensionality if needed

3. **Cluster Validation**
   - Additional metrics (Davies-Bouldin index)
   - Stability analysis
   - Clinical validation

4. **Subtype Naming (Task 6)**
   - Clinical interpretation of each subtype
   - Assign meaningful names
   - Characterize subtype characteristics

5. **Predictive Modeling**
   - Predict subtype membership
   - Identify risk factors
   - Longitudinal analysis

---

## References

1. **NHANES**: Centers for Disease Control and Prevention. National Health and Nutrition Examination Survey Data. https://www.cdc.gov/nchs/nhanes/

2. **HOMA-IR**: Matthews DR, et al. Homeostasis model assessment: insulin resistance and beta-cell function from fasting plasma glucose and insulin concentrations in man. Diabetologia. 1985;28(7):412-9.

3. **MICE**: Van Buuren S, Groothuis-Oudshoorn K. mice: Multivariate Imputation by Chained Equations in R. Journal of Statistical Software. 2011;45(3):1-67.

4. **K-Means**: MacQueen J. Some methods for classification and analysis of multivariate observations. Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability. 1967;1:281-297.

---

## Version History

- **v1.0**: Initial implementation
  - Tasks 1-3: Data acquisition and preparation
  - Task 4: Cluster determination
  - Task 5: K-Means clustering
  - EDA and visualization tools

---

## Contact and Support

For questions, issues, or contributions:
- Review code comments in each script
- Check README.md for usage instructions
- Refer to this documentation for detailed explanations

