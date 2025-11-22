"""
Exploratory Data Analysis (EDA) for Metabolic Profiling Project
Generates distribution plots, correlation heatmap, and pair plots
to understand feature relationships before clustering.
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')  # Suppress warnings

# Define the final 6 features for clustering
CLUSTER_FEATURES = ['HOMA_IR', 'FI', 'HbA1c', 'FBS', 'TGL', 'Creatinine']

# ============================================================================
# Step 0: Load the Imputed Data
# ============================================================================
print("=" * 70)
print("Starting Exploratory Data Analysis (EDA)")
print("=" * 70)

# Load the intermediate CSV file saved in Task 1-2
try:
    df_imputed = pd.read_csv('nhanes_metabolic_imputed_task1.csv')
    print(f"✓ Data loaded successfully with {len(df_imputed)} records.")
    print(f"✓ Features: {', '.join(df_imputed.columns.tolist())}")
except FileNotFoundError:
    print("ERROR: 'nhanes_metabolic_imputed_task1.csv' not found.")
    print("Please ensure the data acquisition script (Tasks 1-3) ran successfully and created this file.")
    exit(1)

# ============================================================================
# Step 1: Feature Engineering (Recalculate HOMA-IR to ensure column is present)
# ============================================================================
print("\nVerifying HOMA-IR calculation...")

# Check if HOMA-IR already exists, if not calculate it
if 'HOMA_IR' not in df_imputed.columns:
    if 'FI' in df_imputed.columns and 'FBS' in df_imputed.columns:
        df_imputed['HOMA_IR'] = (df_imputed['FI'] * df_imputed['FBS']) / 405
        print("✓ HOMA-IR calculated from FI and FBS")
    else:
        print("ERROR: Missing FI or FBS columns needed for HOMA-IR calculation")
        exit(1)
else:
    print("✓ HOMA-IR column already present")

# Extract the 6-feature dataset for EDA
df_eda = df_imputed[CLUSTER_FEATURES].copy()
print(f"✓ EDA dataset prepared: {df_eda.shape[0]} samples, {df_eda.shape[1]} features")

# ============================================================================
# Step 2: Distribution Plots (KDEs)
# ============================================================================
print("\n" + "-" * 70)
print("Step 2: Generating Distribution Plots (KDE)")
print("-" * 70)

# Reformat data for easier plotting
df_plot = df_eda.melt()

# Create distribution plots using FacetGrid
plt.figure(figsize=(15, 10))
g = sns.FacetGrid(
    df_plot, 
    col='variable', 
    col_wrap=3, 
    sharex=False, 
    sharey=False, 
    height=4, 
    aspect=1.2
)
g.map(sns.kdeplot, 'value', fill=True, color="darkblue")
g.set_titles("{col_name} Distribution")
g.set_axis_labels("", "Density")
plt.suptitle("Feature Distributions Before Clustering", y=1.02, fontsize=18)
plt.tight_layout(rect=[0, 0, 1, 0.98])
plt.savefig('feature_distributions.png', dpi=300, bbox_inches='tight')
print("✓ Distribution plots saved to 'feature_distributions.png'")
plt.show()

# ============================================================================
# Step 3: Correlation Heatmap
# ============================================================================
print("\n" + "-" * 70)
print("Step 3: Generating Correlation Heatmap")
print("-" * 70)

correlation_matrix = df_eda.corr()
print("\nCorrelation Matrix:")
print(correlation_matrix.round(3))

plt.figure(figsize=(9, 7))
sns.heatmap(
    correlation_matrix, 
    annot=True, 
    cmap='coolwarm', 
    center=0,
    fmt=".2f", 
    linewidths=.5, 
    linecolor='black',
    square=True,
    cbar_kws={"shrink": 0.8}
)
plt.title("Correlation Matrix of Metabolic Features", fontsize=16, pad=20)
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("✓ Correlation heatmap saved to 'correlation_heatmap.png'")
plt.show()

# Highlight HOMA-IR correlations
print("\nHOMA-IR Correlations:")
homa_correlations = correlation_matrix['HOMA_IR'].sort_values(ascending=False)
for feature, corr in homa_correlations.items():
    if feature != 'HOMA_IR':
        print(f"  {feature}: {corr:.3f}")

# ============================================================================
# Step 4: Pair Plot (Quick Visual Check)
# ============================================================================
print("\n" + "-" * 70)
print("Step 4: Generating Pair Plot")
print("-" * 70)
print("Note: This may take a moment for large datasets...")

sns.pairplot(
    df_eda, 
    plot_kws={'alpha': 0.5, 's': 20}, 
    diag_kws={'kde': True},
    corner=False
)
plt.suptitle("Pair Plot of Metabolic Features", y=1.02, fontsize=16)
plt.tight_layout()
plt.savefig('pair_plot.png', dpi=300, bbox_inches='tight')
print("✓ Pair plot saved to 'pair_plot.png'")
plt.show()

# ============================================================================
# Summary Statistics
# ============================================================================
print("\n" + "=" * 70)
print("Summary Statistics")
print("=" * 70)
print(df_eda.describe().round(3))

print("\n" + "=" * 70)
print("✅ Exploratory Data Analysis (EDA) Complete")
print("=" * 70)
print("\nKey Insights:")
print("  • Review the Correlation Heatmap, paying close attention to HOMA-IR's")
print("    relationship with FBS and FI. This confirms the quality of your features.")
print("  • Distribution plots show the shape and spread of each metabolic feature.")
print("  • Pair plots reveal pairwise relationships and potential clusters.")
print("\nGenerated files:")
print("  • feature_distributions.png")
print("  • correlation_heatmap.png")
print("  • pair_plot.png")

