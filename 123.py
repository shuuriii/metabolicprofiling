"""
Metabolic Profiling Project - Data Acquisition and Preparation
Tasks 1, 2, 3, and 5: Download NHANES data, apply MICE imputation, calculate HOMA-IR, 
normalize data, split into train/test sets, and apply K-Means clustering.
"""

import numpy as np
import pandas as pd
import nhanes_dl as nhanes
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
import warnings
import os

warnings.filterwarnings('ignore')

# ============================================================================
# Setup for File Saving
# ============================================================================
OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

K_CLUSTERS = 4
CLUSTER_FEATURES = ['HOMA_IR', 'FI', 'HbA1c', 'FBS', 'TGL', 'Creatinine']

# ============================================================================
# Task 1: Data Acquisition, Filtering, and MICE Imputation
# ============================================================================
print("=" * 70)
print("TASK 1: Data Acquisition, Filtering, and Imputation")
print("=" * 70)
print("Downloading and merging NHANES 2013-2014 demographic and laboratory data...")

NHANES_VARS = {
    'DEMO': ['SEQN', 'RIDAGEYR'],
    'GLU': ['SEQN', 'LBDGLU'],
    'INS': ['SEQN', 'LBDIN'],
    'GHB': ['SEQN', 'LBXGH'],
    'TGL_HDL': ['SEQN', 'LBXTR'],
    'CKD': ['SEQN', 'LBXSC']
}

try:
    nhanes.download_data(NHANES_VARS)
    df_raw = nhanes.data.copy()
    
    print(f"[OK] Raw data downloaded: {len(df_raw)} participants")
    
    # Rename features for clarity
    df = df_raw.rename(columns={
        'RIDAGEYR': 'Age',
        'LBDGLU': 'FBS',
        'LBDIN': 'FI',
        'LBXGH': 'HbA1c',
        'LBXTR': 'TGL',
        'LBXSC': 'Creatinine'
    })
    
    # Filter to Age 35+
    df_filtered = df[df['Age'] >= 35].reset_index(drop=True)
    print(f"[OK] Filtered to participants aged 35+: {len(df_filtered)} individuals")
    
    # Check for missing values before imputation
    print("\nMissing values before imputation:")
    missing_counts = df_filtered[['FI', 'HbA1c', 'FBS', 'TGL', 'Creatinine']].isnull().sum()
    print(missing_counts)
    print(f"Total missing values: {missing_counts.sum()}")
    
    # Select features for imputation
    imputation_cols = ['FI', 'HbA1c', 'FBS', 'TGL', 'Creatinine']
    
    # Apply MICE Imputation
    print("\nApplying MICE imputation (IterativeImputer)...")
    imputer = IterativeImputer(random_state=42, max_iter=10)
    df_imputed_array = imputer.fit_transform(df_filtered[imputation_cols])
    df_imputed = df_filtered.copy()
    df_imputed[imputation_cols] = df_imputed_array
    
    # Verify imputation success
    missing_after = df_imputed[imputation_cols].isnull().sum().sum()
    print(f"[OK] MICE Imputation complete. Missing values remaining: {missing_after}")
    
    # Save intermediate imputed data (Required for unscaling later)
    df_imputed.to_csv('nhanes_metabolic_imputed_task1.csv', index=False)
    print(f"[OK] Imputed data saved to: nhanes_metabolic_imputed_task1.csv")
    print("✅ Task 1 Complete. Imputed data saved.")
    
except Exception as e:
    print(f"\nERROR: An error occurred during NHANES download or processing: {e}")
    print("You may need to manually download and merge the XPT files from the CDC website.")
    raise

# ============================================================================
# Task 2: Feature Engineering (HOMA-IR)
# ============================================================================
print("\n" + "=" * 70)
print("TASK 2: Feature Engineering (HOMA-IR)")
print("=" * 70)

# HOMA-IR = (Fasting Insulin * Fasting Glucose) / 405
# Note: FBS is in mg/dL, FI is in uU/mL, hence the 405 denominator
print("Calculating HOMA-IR from Fasting Insulin and Fasting Blood Sugar...")
df_imputed['HOMA_IR'] = (df_imputed['FI'] * df_imputed['FBS']) / 405

print(f"[OK] HOMA-IR calculated for {len(df_imputed)} samples")
print(f"     HOMA-IR range: {df_imputed['HOMA_IR'].min():.2f} to {df_imputed['HOMA_IR'].max():.2f}")
print("✅ Task 2 Complete. HOMA_IR calculated.")

# ============================================================================
# Task 3: Standardization and Train/Test Split
# ============================================================================
print("\n" + "=" * 70)
print("TASK 3: Standardization and Train/Test Split")
print("=" * 70)

# Extract the 6-feature dataset
X_unscaled = df_imputed[CLUSTER_FEATURES].copy()
print(f"Original dataset size: {len(X_unscaled)} samples, {X_unscaled.shape[1]} features")

# Apply StandardScaler (Z-score normalization)
print("\nApplying StandardScaler (Z-score normalization)...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_unscaled)
print("[OK] Normalization complete")

# Train/Test Split (70/30)
print("\nSplitting data into Training (70%) and Test (30%) sets...")
X_train_scaled, X_test_scaled, _, _ = train_test_split(
    X_scaled, X_unscaled, test_size=0.3, random_state=42
)

# Save scaled data files
np.save('X_train_scaled.npy', X_train_scaled)
np.save('X_test_scaled.npy', X_test_scaled)
print(f"[OK] Training set size (70%): {len(X_train_scaled)}")
print(f"[OK] Test set size (30%): {len(X_test_scaled)}")
print(f"[OK] Scaled data saved to: X_train_scaled.npy, X_test_scaled.npy")
print("✅ Task 3 Complete. Scaled data saved to .npy files.")

# ============================================================================
# Task 5: Core Clustering and Labeling (K=4)
# ============================================================================
print("\n" + "=" * 70)
print("TASK 5: Core Clustering with K=4 Subtypes")
print("=" * 70)

print("Training K-Means model with k=4...")
kmeans = KMeans(n_clusters=K_CLUSTERS, random_state=42, n_init='auto', max_iter=300)
kmeans.fit(X_train_scaled)
print(f"[OK] K-Means model trained")
print(f"     Number of iterations: {kmeans.n_iter_}")
print(f"     Final inertia: {kmeans.inertia_:.2f}")

# Assign labels to the entire dataset (Train + Test)
print("\nAssigning cluster labels to all data points...")
X_all_scaled = np.concatenate([X_train_scaled, X_test_scaled])
all_labels = kmeans.predict(X_all_scaled)
df_imputed['Subtype'] = all_labels

print(f"[OK] Labels assigned to {len(all_labels)} samples")

# Display cluster distribution
print("\nCluster Distribution:")
cluster_counts = pd.Series(all_labels).value_counts().sort_index()
for subtype_id, count in cluster_counts.items():
    percentage = (count / len(all_labels)) * 100
    print(f"  Subtype {subtype_id}: {count:4d} samples ({percentage:5.2f}%)")

# Unscale Cluster Centers (Needed for Subtype Profiling)
print("\nUnscaling cluster centers for interpretation...")
unscaled_centers = scaler.inverse_transform(kmeans.cluster_centers_)
df_centers = pd.DataFrame(unscaled_centers, columns=CLUSTER_FEATURES)
df_centers.index.name = 'Subtype ID'
df_centers.index = [f'Subtype {i}' for i in range(K_CLUSTERS)]
df_centers = df_centers.round(2)

print("[OK] Cluster centers unscaled successfully")

# Save final labeled dataset and the cluster centers to the output folder
df_imputed.to_csv(f'{OUTPUT_DIR}/nhanes_metabolic_labeled_task5.csv', index=False)
df_centers.to_csv(f'{OUTPUT_DIR}/metabolic_subtype_centers_task5.csv', index=True)

# Also save to root directory for compatibility
df_imputed.to_csv('nhanes_metabolic_labeled_task5.csv', index=False)
df_centers.to_csv('metabolic_subtype_centers_task5.csv', index=True)

print(f"\n[OK] Files saved to {OUTPUT_DIR}/ and root directory")

# ============================================================================
# Display Results
# ============================================================================
print("\n" + "=" * 70)
print("UNSCALED METABOLIC SUBTYPE PROFILES")
print("=" * 70)
print("\nThese are the characteristic metabolic profiles for each subtype:")
print("(Values are in original units: FI in uU/mL, FBS in mg/dL, etc.)\n")
print(df_centers.to_markdown())

print("\n" + "=" * 70)
print("✅ TASK 5 COMPLETE")
print("=" * 70)
print(f"\nSummary:")
print(f"  • K-Means clustering applied with k={K_CLUSTERS}")
print(f"  • {len(df_imputed)} samples assigned to {K_CLUSTERS} metabolic subtypes")
print(f"  • Cluster centers unscaled and ready for interpretation")
print(f"  • Final files saved to {OUTPUT_DIR}/ and root directory")
print("\nNext Steps:")
print("  - Review the cluster centers to understand each subtype's characteristics")
print("  - Run Task 7 (UMAP visualization) to visualize subtype separation")
print("  - Run Task 8 (Model validation) to validate clustering quality")
