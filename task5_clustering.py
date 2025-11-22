"""
Task 5: Core Clustering with K-Means
Applies K-Means clustering with the optimal k value determined in Task 4
to identify distinct metabolic subtypes in the NHANES dataset.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
import os

warnings.filterwarnings('ignore')

# ============================================================================
# Setup: Define parameters and load data
# ============================================================================
K_CLUSTERS = 4  # Based on optimal k=4 finding from Task 4
CLUSTER_FEATURES = ['HOMA_IR', 'FI', 'HbA1c', 'FBS', 'TGL', 'Creatinine']

print("=" * 70)
print(f"TASK 5: Core Clustering with K={K_CLUSTERS} Subtypes")
print("=" * 70)

try:
    # 1. Load the scaled data prepared in Tasks 1-3
    print("\n[Step 1] Loading scaled training and test data...")
    X_train_scaled = np.load('X_train_scaled.npy')
    X_test_scaled = np.load('X_test_scaled.npy')
    print(f"  [OK] Training set: {X_train_scaled.shape[0]} samples")
    print(f"  [OK] Test set: {X_test_scaled.shape[0]} samples")
    
    # 2. Load the original (unscaled) imputed data to correctly unscale centers
    print("\n[Step 2] Loading original unscaled data...")
    df_imputed = pd.read_csv('nhanes_metabolic_imputed_task1.csv')
    
    # Ensure HOMA_IR is calculated
    if 'HOMA_IR' not in df_imputed.columns:
        if 'FI' in df_imputed.columns and 'FBS' in df_imputed.columns:
            df_imputed['HOMA_IR'] = (df_imputed['FI'] * df_imputed['FBS']) / 405
            print("  [OK] HOMA_IR calculated from FI and FBS")
        else:
            raise ValueError("Missing FI or FBS columns needed for HOMA_IR calculation")
    else:
        print("  [OK] HOMA_IR column already present")
    
    # Extract the 6-feature dataset
    X_unscaled = df_imputed[CLUSTER_FEATURES].copy()
    print(f"  [OK] Unscaled data: {len(X_unscaled)} samples, {X_unscaled.shape[1]} features")
    
    # 3. Re-fit the StandardScaler (needed for inverse transform)
    print("\n[Step 3] Fitting StandardScaler for inverse transformation...")
    scaler = StandardScaler()
    scaler.fit(X_unscaled)
    print("  [OK] Scaler fitted and ready for inverse transformation")
    
except FileNotFoundError as e:
    print(f"\nERROR: Missing required file: {e}")
    print("Please ensure Tasks 1-3 (123.py) ran successfully and generated:")
    print("  - X_train_scaled.npy")
    print("  - X_test_scaled.npy")
    print("  - nhanes_metabolic_imputed_task1.csv")
    exit(1)
except Exception as e:
    print(f"\nERROR: {e}")
    exit(1)

# ============================================================================
# Step 5.1: Train the K-Means Model
# ============================================================================
print("\n" + "-" * 70)
print(f"[Step 4] Training K-Means model with k={K_CLUSTERS}...")
print("-" * 70)

try:
    kmeans = KMeans(n_clusters=K_CLUSTERS, random_state=42, n_init='auto', max_iter=300)
except TypeError:
    # Fallback for older scikit-learn versions
    kmeans = KMeans(n_clusters=K_CLUSTERS, random_state=42, n_init=10, max_iter=300)

kmeans.fit(X_train_scaled)

print(f"  [OK] K-Means model trained successfully")
print(f"  - Number of iterations: {kmeans.n_iter_}")
print(f"  - Final inertia: {kmeans.inertia_:.2f}")

# ============================================================================
# Step 5.2: Assign Labels to the Entire Dataset
# ============================================================================
print("\n" + "-" * 70)
print("[Step 5] Assigning cluster labels to all data points...")
print("-" * 70)

# Combine train and test sets to assign labels to all data points
X_all_scaled = np.concatenate([X_train_scaled, X_test_scaled], axis=0)
all_labels = kmeans.predict(X_all_scaled)

print(f"  [OK] Labels assigned to {len(all_labels)} data points")

# Verify the sizes match
if len(all_labels) != len(X_unscaled):
    print(f"  WARNING: Size mismatch! Labels: {len(all_labels)}, Data: {len(X_unscaled)}")
    # Take only the first N labels where N matches the data size
    min_size = min(len(all_labels), len(X_unscaled))
    all_labels = all_labels[:min_size]
    X_unscaled = X_unscaled.iloc[:min_size].copy()
    print(f"  Adjusted to use first {min_size} samples")

# Add the cluster label column to the original unscaled DataFrame
df_imputed = X_unscaled.copy()
df_imputed['Subtype'] = all_labels

# Create final labeled dataset
df_final = df_imputed.reset_index(drop=True)

# Display cluster distribution
print("\n  Cluster Distribution:")
cluster_counts = pd.Series(all_labels).value_counts().sort_index()
for subtype, count in cluster_counts.items():
    percentage = (count / len(all_labels)) * 100
    print(f"    Subtype {subtype}: {count:4d} samples ({percentage:5.2f}%)")

# ============================================================================
# Step 5.3: Unscale Cluster Centers (Key for Task 6)
# ============================================================================
print("\n" + "-" * 70)
print("[Step 6] Unscaling cluster centers for interpretation...")
print("-" * 70)

# Get the cluster centers from the scaled space
scaled_centers = kmeans.cluster_centers_

# Apply the inverse transform using the fitted scaler
unscaled_centers = scaler.inverse_transform(scaled_centers)

# Create a DataFrame for easy reading and profiling
df_centers = pd.DataFrame(unscaled_centers, columns=CLUSTER_FEATURES)
df_centers.index.name = 'Subtype ID'
df_centers.index = [f'Subtype {i}' for i in range(K_CLUSTERS)]
df_centers = df_centers.round(3)

print("  [OK] Cluster centers unscaled successfully")
print(f"\n  Unscaled Cluster Centers (Mean values for each subtype):")
print("  " + "-" * 70)

# ============================================================================
# Step 5.4: Display Results and Save Data
# ============================================================================
print("\n" + "=" * 70)
print("UNSCALED METABOLIC SUBTYPE PROFILES (Task 6 Input)")
print("=" * 70)
print("\nThese are the characteristic metabolic profiles for each subtype:")
print("(Values are in original units: FI in μU/mL, FBS in mg/dL, etc.)\n")

# Display with better formatting
print(df_centers.to_string())

# Calculate and display additional statistics per cluster
print("\n" + "=" * 70)
print("CLUSTER STATISTICS")
print("=" * 70)

for subtype_id in range(K_CLUSTERS):
    subtype_data = df_final[df_final['Subtype'] == subtype_id][CLUSTER_FEATURES]
    print(f"\nSubtype {subtype_id} (n={len(subtype_data)}):")
    print(f"  Mean values:")
    for feature in CLUSTER_FEATURES:
        mean_val = subtype_data[feature].mean()
        std_val = subtype_data[feature].std()
        center_val = df_centers.loc[f'Subtype {subtype_id}', feature]
        print(f"    {feature:12s}: {center_val:8.3f} (mean: {mean_val:8.3f} ± {std_val:6.3f})")

# Save the final labeled dataset and the cluster centers
print("\n" + "=" * 70)
print("SAVING RESULTS")
print("=" * 70)

os.makedirs('output', exist_ok=True)

# Save labeled dataset
output_file1 = 'output/nhanes_metabolic_labeled_task5.csv'
df_final.to_csv(output_file1, index=False)
print(f"  [OK] Labeled dataset saved: {output_file1}")

# Save cluster centers
output_file2 = 'output/metabolic_subtype_centers_task5.csv'
df_centers.to_csv(output_file2, index=True)
print(f"  [OK] Cluster centers saved: {output_file2}")

# Also save in the root directory for backward compatibility
df_final.to_csv('nhanes_metabolic_labeled_task5.csv', index=False)
df_centers.to_csv('metabolic_subtype_centers_task5.csv', index=True)
print(f"  [OK] Files also saved to root directory for compatibility")

print("\n" + "=" * 70)
print("[SUCCESS] TASK 5 COMPLETE")
print("=" * 70)
print("\nSummary:")
print(f"  • K-Means clustering applied with k={K_CLUSTERS}")
print(f"  • {len(df_final)} samples assigned to {K_CLUSTERS} metabolic subtypes")
print(f"  • Cluster centers unscaled and ready for interpretation")
print(f"  • Data saved for Subtype Profiling and Naming (Task 6)")
print("\nNext Steps:")
print("  - Review the cluster centers to understand each subtype's characteristics")
print("  - Proceed to Task 6: Subtype Profiling and Naming")

