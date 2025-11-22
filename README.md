# Metabolic Profiling Project: NHANES Data Analysis

A comprehensive machine learning pipeline for identifying metabolic subtypes in the NHANES 2013-2014 dataset using K-Means clustering.

## Project Overview

This project implements a complete workflow for:
1. **Data Acquisition**: Downloading and merging NHANES 2013-2014 demographic and laboratory data
2. **Data Preparation**: Handling missing values with MICE imputation and feature engineering
3. **Exploratory Data Analysis**: Visualizing feature distributions and correlations
4. **Cluster Determination**: Finding optimal number of metabolic subtypes
5. **Clustering**: Applying K-Means to identify distinct metabolic profiles

## Project Structure

```
metabolicprofiling.py/
├── 123.py                          # Main script: Tasks 1-3 (Data Acquisition & Preparation)
├── eda.py                          # Exploratory Data Analysis
├── visualize.py                    # Comprehensive visualization suite
├── task4_cluster_determination.py  # Task 4: Optimal cluster determination
├── task5_clustering.py             # Task 5: K-Means clustering
├── task7_umap_visualization.py     # Task 7: UMAP visualization
├── task8_model_validation.py       # Task 8: Model validation
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── OUTPUT_TABLE.txt                # Sample output table format
└── visualizations/                 # Generated visualization plots
    ├── 1_distributions.png
    ├── 2_correlation_heatmap.png
    ├── 3_pairplot.png
    ├── 4_boxplots.png
    ├── 5_homa_relationships.png
    ├── 4_optimal_clusters.png
    ├── 7_umap_visualization.png
    └── 8_confusion_matrix.png
```

## Features Analyzed

The project uses 6 key metabolic features:
- **HOMA_IR**: Homeostatic Model Assessment for Insulin Resistance (calculated)
- **FI**: Fasting Insulin (μU/mL)
- **HbA1c**: Hemoglobin A1c (%)
- **FBS**: Fasting Blood Sugar (mg/dL)
- **TGL**: Triglycerides (mg/dL)
- **Creatinine**: Serum Creatinine (mg/dL)

## Installation

1. **Clone or download this repository**

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

   Required packages:
   - pandas >= 1.5.0
   - numpy >= 1.23.0
   - scikit-learn >= 1.2.0
   - nhanes-dl >= 0.1.0
   - seaborn >= 0.12.0
   - matplotlib >= 3.6.0

## Usage Guide

### Step 1: Data Acquisition, Preparation, and Clustering (Tasks 1, 2, 3, 5)

Run the consolidated main script to download NHANES data, apply imputation, calculate HOMA-IR, normalize data, and perform clustering:

```bash
python 123.py
```

**What it does:**
- Downloads NHANES 2013-2014 demographic and laboratory data
- Filters participants to age 35+ (Task 1)
- Applies MICE imputation to handle missing values (Task 1)
- Calculates HOMA-IR from Fasting Insulin and Fasting Blood Sugar (Task 2)
- Applies StandardScaler normalization (Z-score) (Task 3)
- Splits data into 70% training and 30% test sets (Task 3)
- Applies K-Means clustering with k=4 (Task 5)
- Unscales cluster centers for interpretation (Task 5)

**Output files:**
- `nhanes_metabolic_imputed_task1.csv` - Imputed data with all features (root)
- `X_train_scaled.npy` - Scaled training data (NumPy array, root)
- `X_test_scaled.npy` - Scaled test data (NumPy array, root)
- `output/nhanes_metabolic_labeled_task5.csv` - Full dataset with subtype labels
- `output/metabolic_subtype_centers_task5.csv` - Unscaled cluster centers
- `nhanes_metabolic_labeled_task5.csv` - Labeled dataset (root, for compatibility)
- `metabolic_subtype_centers_task5.csv` - Cluster centers (root, for compatibility)

### Step 2: Optimal Cluster Determination (Task 4) - Optional

Validate the choice of k=4 clusters:

```bash
python task4_cluster_determination.py
```

**What it does:**
- Tests k values from 2 to 10
- Calculates inertia (Elbow Method) and silhouette scores
- Visualizes both metrics
- Confirms k=4 is optimal

**Output files:**
- `visualizations/4_optimal_clusters.png` - Elbow and silhouette plots

### Step 3: Exploratory Data Analysis (Optional)

Generate comprehensive visualizations of your data:

```bash
python visualize.py
```

**What it does:**
- Creates distribution plots (KDE) for all features
- Generates correlation heatmap
- Creates box plots
- Shows HOMA-IR relationships with FBS and FI
- Generates pair plots

**Output files:**
- `visualizations/1_distributions.png`
- `visualizations/2_correlation_heatmap.png`
- `visualizations/3_pairplot.png`
- `visualizations/4_boxplots.png`
- `visualizations/5_homa_relationships.png`

**Alternative EDA script:**
```bash
python eda.py
```

**Note**: Tasks 1, 2, 3, and 5 are now consolidated in `123.py`. The separate `task5_clustering.py` script is still available for running Task 5 independently if needed.

**Output table format:**
```
            HOMA_IR    FI  HbA1c    FBS    TGL  Creatinine
Subtype ID                                                
Subtype 0      2.15   8.5    5.2   95.0   85.0        0.85
Subtype 1      4.80  18.2    5.8  108.0  145.0        0.92
Subtype 2      8.50  32.5    6.5  118.0  220.0        0.98
Subtype 3      1.80   6.8    4.9   88.0   65.0        0.78
```

### Step 4: UMAP Visualization (Task 7)

Visualize the metabolic subtypes in 2D space:

```bash
python task7_umap_visualization.py
```

**What it does:**
- Applies UMAP dimensionality reduction (6D → 2D)
- Creates scatter plot showing subtype separation
- Validates cluster quality visually
- Maps subtypes to meaningful names

**Output files:**
- `visualizations/7_umap_visualization.png` - UMAP scatter plot
- `output/umap_coordinates_task7.csv` - UMAP coordinates for further analysis

**Subtype Names:**
- Subtype 0: Resilient Phenotype
- Subtype 1: Compensated Insulin Resistance (CIR)
- Subtype 2: Hypertriglyceridemic-Dyslipidemic (HTD)
- Subtype 3: Severe Nephro-Metabolic Failure (SNMF)

### Step 5: Model Validation (Task 8)

Validate the clustering results using a Random Forest classifier:

```bash
python task8_model_validation.py
```

**What it does:**
- Trains Random Forest classifier to predict metabolic subtypes
- Evaluates model performance on test set
- Generates classification report and confusion matrix
- Shows feature importance for subtype discrimination

**Output files:**
- `visualizations/8_confusion_matrix.png` - Confusion matrix visualization
- Console output with accuracy, precision, recall, and F1-scores

**Interpretation:**
- High accuracy (>80%) indicates well-separated, distinct subtypes
- Confusion matrix shows which subtypes are most/least confused
- Feature importance reveals which metabolic markers are most discriminative

## Task Details

### Task 1: Data Acquisition and MICE Imputation
- **Library**: `nhanes-dl` for downloading NHANES data
- **Age Filter**: Participants aged 35 years and older
- **Imputation Method**: Multiple Imputation by Chained Equations (MICE) using `IterativeImputer`
- **Features**: Age, FI, HbA1c, FBS, TGL, Creatinine

### Task 2: Feature Engineering
- **HOMA-IR Calculation**: `(Fasting Insulin × Fasting Blood Sugar) / 405`
- **Final Features**: 6 features including HOMA_IR, FI, HbA1c, FBS, TGL, Creatinine

### Task 3: Data Normalization and Splitting
- **Normalization**: StandardScaler (Z-score normalization)
- **Train/Test Split**: 70% training, 30% test
- **Random State**: 42 (for reproducibility)

### Task 4: Optimal Cluster Determination
- **Methods**: Elbow Method (inertia) and Silhouette Score
- **K Range**: 2 to 10 clusters
- **Optimal K**: Typically 4-5 based on clinical relevance and statistical metrics

### Task 5: Core Clustering
- **Algorithm**: K-Means clustering
- **K Value**: 4 (determined from Task 4)
- **Output**: Unscaled cluster centers for clinical interpretation

### Task 7: UMAP Visualization
- **Method**: UMAP (Uniform Manifold Approximation and Projection)
- **Purpose**: Visualize 6D metabolic space in 2D
- **Parameters**: n_neighbors=15, min_dist=0.1
- **Output**: Scatter plot showing subtype separation

### Task 8: Model Validation
- **Algorithm**: Random Forest Classifier
- **Purpose**: Validate clustering quality by predicting subtypes
- **Parameters**: n_estimators=100, class_weight='balanced'
- **Metrics**: Accuracy, Precision, Recall, F1-Score, Confusion Matrix
- **Output**: Classification report and confusion matrix visualization

## Clinical Interpretation

### Feature Units and Normal Ranges

| Feature | Unit | Normal Range | Clinical Significance |
|---------|------|--------------|----------------------|
| HOMA_IR | Unitless | < 1.0 (normal)<br>1.0-2.5 (borderline)<br>> 2.5 (insulin resistant) | Insulin resistance index |
| FI | μU/mL | 2-25 | Fasting insulin level |
| HbA1c | % | < 5.7% (normal)<br>5.7-6.4% (prediabetes)<br>≥ 6.5% (diabetes) | Long-term glucose control |
| FBS | mg/dL | 70-100 (normal)<br>100-125 (prediabetes)<br>≥ 126 (diabetes) | Fasting blood glucose |
| TGL | mg/dL | < 150 (normal)<br>150-199 (borderline)<br>≥ 200 (high) | Triglyceride levels |
| Creatinine | mg/dL | 0.6-1.2 (varies by gender/age) | Kidney function marker |

### Metabolic Subtype Interpretation

The cluster centers represent characteristic metabolic profiles:
- **Subtype 0**: Moderate metabolic profile
- **Subtype 1**: Elevated insulin resistance
- **Subtype 2**: High-risk metabolic profile (diabetes range)
- **Subtype 3**: Healthy metabolic profile

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'nhanes_dl'**
   ```bash
   pip install nhanes-dl
   ```

2. **FileNotFoundError: Missing data files**
   - Ensure you run `123.py` first to generate required data files
   - Check that all previous tasks completed successfully

3. **Unicode encoding errors (Windows)**
   - The scripts use ASCII-compatible characters
   - If issues persist, set environment variable: `PYTHONIOENCODING=utf-8`

4. **NHANES download fails**
   - Check internet connection
   - The `nhanes-dl` library may require manual download of XPT files in some cases
   - See error messages for specific guidance

## Dependencies

See `requirements.txt` for complete list. Key dependencies:
- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **scikit-learn**: Machine learning (K-Means, imputation, scaling)
- **nhanes-dl**: NHANES data download
- **seaborn**: Statistical visualizations
- **matplotlib**: Plotting
- **umap-learn**: UMAP dimensionality reduction

## Data Sources

- **NHANES 2013-2014**: National Health and Nutrition Examination Survey
- **Demographics**: Age (RIDAGEYR)
- **Laboratory Data**: 
  - Fasting Glucose (LBDGLU)
  - Fasting Insulin (LBDIN)
  - HbA1c (LBXGH)
  - Triglycerides (LBXTR)
  - Creatinine (LBXSC)

## Next Steps

After completing Task 7, you can:
1. **Validate Clusters**: Use UMAP visualization to assess cluster separation
2. **Subtype Profiling**: Analyze each subtype's characteristics in detail
3. **Clinical Validation**: Compare subtypes with known metabolic phenotypes
4. **Predictive Modeling**: Use subtypes for downstream analysis
5. **Longitudinal Analysis**: Track subtype changes over time (if data available)

## License

This project is for educational and research purposes. NHANES data is publicly available from the CDC.

## References

- NHANES: https://www.cdc.gov/nchs/nhanes/
- HOMA-IR: Matthews et al. (1985) Diabetologia
- MICE Imputation: Van Buuren & Groothuis-Oudshoorn (2011) Journal of Statistical Software

## Contact

For questions or issues, please refer to the code comments or documentation within each script.

