# Consolidated Script Summary

## Main Script: `123.py`

This consolidated script executes **Tasks 1, 2, 3, and 5** in sequence, providing a complete pipeline from raw NHANES data to clustered metabolic subtypes.

## What It Does

### Task 1: Data Acquisition, Filtering, and MICE Imputation
- Downloads NHANES 2013-2014 demographic and laboratory data
- Filters participants to age 35+ years
- Applies MICE (Multiple Imputation by Chained Equations) imputation
- Handles missing values in laboratory measurements

### Task 2: Feature Engineering (HOMA-IR)
- Calculates HOMA-IR (Homeostatic Model Assessment for Insulin Resistance)
- Formula: `HOMA_IR = (Fasting Insulin × Fasting Blood Sugar) / 405`
- Creates the final 6-feature dataset

### Task 3: Standardization and Train/Test Split
- Applies StandardScaler (Z-score normalization)
- Ensures equal feature contribution to clustering
- Splits data into 70% training and 30% test sets
- Uses random_state=42 for reproducibility

### Task 5: Core Clustering (K-Means, k=4)
- Trains K-Means clustering model with k=4 subtypes
- Assigns cluster labels to all data points
- Unscales cluster centers for clinical interpretation
- Displays metabolic subtype profiles

## Generated Files

### Root Directory Files:
- `nhanes_metabolic_imputed_task1.csv` - Imputed data with all features (including HOMA-IR)
- `X_train_scaled.npy` - Scaled training data (NumPy array)
- `X_test_scaled.npy` - Scaled test data (NumPy array)
- `nhanes_metabolic_labeled_task5.csv` - Full dataset with subtype labels (for compatibility)
- `metabolic_subtype_centers_task5.csv` - Cluster centers table (for compatibility)

### Output Directory Files:
- `output/nhanes_metabolic_labeled_task5.csv` - Full dataset with subtype labels
- `output/metabolic_subtype_centers_task5.csv` - Unscaled cluster centers (for Task 6)

## Usage

```bash
# Run the consolidated script
python 123.py
```

## Expected Output

The script will:
1. Download and process NHANES data
2. Display progress for each task
3. Show missing value statistics
4. Display cluster distribution
5. Print the unscaled metabolic subtype profiles table
6. Save all required files

## Next Steps After Running

Once `123.py` completes successfully, you can run:

1. **Task 4** (Optional): `python task4_cluster_determination.py`
   - Validates the choice of k=4 clusters

2. **Task 7** (Recommended): `python task7_umap_visualization.py`
   - Visualizes subtype separation in 2D space

3. **Task 8** (Recommended): `python task8_model_validation.py`
   - Validates clustering quality with Random Forest classifier

## Key Features

- **MICE Imputation**: Robust handling of missing laboratory values
- **HOMA-IR Calculation**: Clinically relevant insulin resistance metric
- **StandardScaler Normalization**: Ensures equal feature contribution
- **K-Means Clustering**: Identifies 4 distinct metabolic subtypes
- **Reproducible**: Uses random_state=42 throughout
- **Comprehensive Output**: Saves files in multiple locations for compatibility

## Process Flow

```
Raw NHANES Data
    ↓
[Task 1] Download & Filter (Age 35+)
    ↓
[Task 1] MICE Imputation
    ↓
[Task 2] Calculate HOMA-IR
    ↓
[Task 3] StandardScaler Normalization
    ↓
[Task 3] Train/Test Split (70/30)
    ↓
[Task 5] K-Means Clustering (k=4)
    ↓
[Task 5] Unscale Cluster Centers
    ↓
Metabolic Subtype Profiles
```

## Notes

- The script includes error handling for NHANES download issues
- All intermediate steps are saved for debugging and verification
- Files are saved to both root and `output/` directory for compatibility
- The script can be run multiple times (will overwrite previous results)

