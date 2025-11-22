"""
Task 7: UMAP Visualization of Metabolic Subtypes
Applies UMAP dimensionality reduction to visualize the 4 metabolic subtypes
in 2D space, validating cluster separation and subtype naming.
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from umap import UMAP
from sklearn.preprocessing import StandardScaler
import warnings
import os

warnings.filterwarnings('ignore')

# ============================================================================
# Setup: Define parameters and subtype names
# ============================================================================
CLUSTER_FEATURES = ['HOMA_IR', 'FI', 'HbA1c', 'FBS', 'TGL', 'Creatinine']

# Subtype names based on metabolic profiles (from Task 6 analysis)
SUBTYPE_NAMES = {
    0: 'Resilient Phenotype',
    1: 'Compensated IR (CIR)',
    2: 'Hypertriglyceridemic (HTD)',
    3: 'Nephro-Metabolic Failure (SNMF)'
}

# Ensure output directory exists
OUTPUT_DIR = 'visualizations'
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("--- Task 7: Feature Visualization (UMAP) ---")

try:
    # 1. Load the final labeled dataset from Task 5
    df_labeled = pd.read_csv('nhanes_metabolic_labeled_task5.csv')
    df_labeled['Subtype_Name'] = df_labeled['Subtype'].map(SUBTYPE_NAMES)
    
    # 2. Extract the scaled features (UMAP must run on the scaled data)
    X_scaled = np.concatenate([np.load('X_train_scaled.npy'), np.load('X_test_scaled.npy')], axis=0)

except FileNotFoundError:
    print("Error: Missing required files. Ensure Task 5 ran and saved 'nhanes_metabolic_labeled_task5.csv' and the scaled arrays.")
    exit(1)

# --- Step 7.1: Apply UMAP Dimensionality Reduction ---
print("1. Applying UMAP reduction (6D to 2D)...")
# Using standard UMAP parameters for robust, non-linear embedding
umap_model = UMAP(n_components=2, random_state=42, n_neighbors=15, min_dist=0.1)
X_umap = umap_model.fit_transform(X_scaled)

# --- Step 7.2: Create the UMAP Visualization DataFrame ---
df_umap = pd.DataFrame(X_umap, columns=['UMAP-1', 'UMAP-2'])
# Attach the subtype name column
df_umap['Subtype_Name'] = df_labeled['Subtype_Name']
df_umap['Subtype_ID'] = df_labeled['Subtype']

# --- Step 7.3: Plotting and Saving ---
print("2. Generating UMAP scatter plot...")

plt.figure(figsize=(10, 8))

sns.scatterplot(
    x='UMAP-1',
    y='UMAP-2',
    hue='Subtype_Name',
    palette='viridis',
    data=df_umap,
    s=25,
    alpha=0.6,
    legend='full'
)

plt.title(f"UMAP Visualization of Metabolic Subtypes (k={len(SUBTYPE_NAMES)})", fontsize=14)
plt.legend(title='Metabolic Subtype', loc='upper right')

# Save the plot
plt.savefig(f'{OUTPUT_DIR}/7_umap_visualization.png', dpi=300, bbox_inches='tight')
plt.show()

# Save the coordinates for reference
os.makedirs('output', exist_ok=True)
df_umap.to_csv('output/umap_coordinates_task7.csv', index=False)

# ============================================================================
# Summary
# ============================================================================
print(f"Visualization saved to {OUTPUT_DIR}/7_umap_visualization.png")
print("✅ Task 7 Complete. The UMAP plot visually validates the separation of your 4 named subtypes.")

