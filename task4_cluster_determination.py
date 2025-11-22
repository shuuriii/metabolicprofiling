"""
Task 4: Optimal Cluster Determination
Uses Elbow Method and Silhouette Score to determine the optimal number
of metabolic subtypes (clusters) for K-Means clustering.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import warnings
import os

warnings.filterwarnings('ignore')  # Suppress warnings

# ============================================================================
# Step 4.1: Load Training Data
# ============================================================================
print("=" * 70)
print("TASK 4: Optimal Cluster Determination")
print("=" * 70)

try:
    # Load the scaled training data generated in Task 3
    X_train_scaled = np.load('X_train_scaled.npy')
    print(f"[OK] Scaled Training Data loaded with shape: {X_train_scaled.shape}")
    print(f"     Samples: {X_train_scaled.shape[0]}, Features: {X_train_scaled.shape[1]}")
except FileNotFoundError:
    print("ERROR: 'X_train_scaled.npy' not found.")
    print("Please ensure Task 3 (123.py) ran successfully and the file is in the current directory.")
    exit(1)

# ============================================================================
# Step 4.2: Calculate Metrics for each k
# ============================================================================
# Define the range of clusters (k) to test
# Based on clinical relevance, we expect 4-5 metabolic subtypes
k_range = range(2, 11)
inertia = []
silhouette_scores = []

print(f"\nCalculating Inertia (Elbow Method) and Silhouette Scores for k = {min(k_range)} to {max(k_range)}...")
print("This may take a moment...")

for k in k_range:
    # Initialize and train K-Means model
    # Use n_init='auto' for modern scikit-learn versions (or n_init=10 for older versions)
    try:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto', max_iter=300)
    except TypeError:
        # Fallback for older scikit-learn versions
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10, max_iter=300)
    
    kmeans.fit(X_train_scaled)
    
    # 1. Elbow Method: Record Inertia (Within-Cluster Sum of Squares)
    inertia.append(kmeans.inertia_)
    
    # 2. Silhouette Score: Record Score (only for k > 1)
    if k > 1:
        score = silhouette_score(X_train_scaled, kmeans.labels_)
        silhouette_scores.append(score)
        print(f"  k={k:2d}: Inertia={kmeans.inertia_:.2f}, Silhouette={score:.4f}")
    else:
        print(f"  k={k:2d}: Inertia={kmeans.inertia_:.2f}")

# Find optimal k based on silhouette score
k_list = list(k_range)
optimal_k_silhouette = k_list[1:][np.argmax(silhouette_scores)]  # k_list[1:] because silhouette starts at k=2

# Find elbow point (simplified: find k where decrease in inertia starts to level off)
# Calculate rate of change in inertia
inertia_changes = np.diff(inertia)
inertia_change_rates = np.diff(inertia_changes)
# Find where the rate of change is maximum (the elbow)
if len(inertia_change_rates) > 0:
    optimal_k_elbow_idx = np.argmax(inertia_change_rates) + 2  # +2 because of double diff and k starts at 2
    optimal_k_elbow = k_list[optimal_k_elbow_idx] if optimal_k_elbow_idx < len(k_list) else 4
else:
    optimal_k_elbow = 4  # Default suggestion

print(f"\n[Analysis] Optimal k (Silhouette): {optimal_k_silhouette}")
print(f"[Analysis] Optimal k (Elbow method): {optimal_k_elbow}")

# ============================================================================
# Step 4.3: Visualize Results
# ============================================================================
print("\nGenerating visualization plots...")

plt.style.use("ggplot")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Elbow Method
axes[0].plot(k_range, inertia, marker='o', linewidth=2, markersize=8, color='steelblue')
axes[0].set_xlabel("Number of Clusters (k)", fontsize=12)
axes[0].set_ylabel("Inertia (Within-Cluster Sum of Squares)", fontsize=12)
axes[0].set_title("1. Elbow Method to Determine Optimal k", fontsize=14, fontweight='bold')
axes[0].grid(True, alpha=0.3)

# Highlight potential optimal k values (4-5 based on clinical relevance)
axes[0].axvline(x=4, color='red', linestyle='--', linewidth=2, alpha=0.7, label='k=4 (Clinical suggestion)')
axes[0].axvline(x=5, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='k=5 (Clinical suggestion)')
axes[0].axvline(x=optimal_k_elbow, color='green', linestyle=':', linewidth=2, alpha=0.7, label=f'k={optimal_k_elbow} (Elbow point)')
axes[0].legend(loc='best')
axes[0].set_xticks(k_range)

# Plot 2: Silhouette Score
# Note: Silhouette scores list starts at k=2, so k_range_plot starts at 2
k_range_plot = list(k_range)[1:]  # Start from k=2

axes[1].plot(k_range_plot, silhouette_scores, marker='o', linewidth=2, markersize=8, color='darkgreen')
axes[1].set_xlabel("Number of Clusters (k)", fontsize=12)
axes[1].set_ylabel("Average Silhouette Score", fontsize=12)
axes[1].set_title("2. Silhouette Score to Determine Optimal k", fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3)

# Highlight optimal k based on silhouette score
axes[1].axvline(x=optimal_k_silhouette, color='green', linestyle='-', linewidth=2, alpha=0.7, label=f'k={optimal_k_silhouette} (Max Silhouette)')
axes[1].axvline(x=4, color='red', linestyle='--', linewidth=2, alpha=0.7, label='k=4 (Clinical suggestion)')
axes[1].axvline(x=5, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='k=5 (Clinical suggestion)')
axes[1].legend(loc='best')
axes[1].set_xticks(k_range_plot)

# Add value annotations
for i, (k, score) in enumerate(zip(k_range_plot, silhouette_scores)):
    if k == optimal_k_silhouette:
        axes[1].annotate(f'{score:.3f}', (k, score), textcoords="offset points", 
                        xytext=(0,10), ha='center', fontweight='bold', color='green')

plt.suptitle("Determining Optimal Metabolic Subtypes (k)", fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Save the plot
os.makedirs('visualizations', exist_ok=True)
plt.savefig('visualizations/4_optimal_clusters.png', dpi=300, bbox_inches='tight', facecolor='white')
print(f"[OK] Plot saved to: visualizations/4_optimal_clusters.png")
plt.show()

# ============================================================================
# Summary Table
# ============================================================================
print("\n" + "=" * 70)
print("SUMMARY: Cluster Evaluation Metrics")
print("=" * 70)

summary_df = pd.DataFrame({
    'k': list(k_range),
    'Inertia': inertia,
    'Inertia_Change': [0] + list(np.diff(inertia)),
    'Silhouette_Score': [None] + silhouette_scores
})

print("\nDetailed Metrics:")
print(summary_df.to_string(index=False))

print("\n" + "=" * 70)
print("INTERPRETATION GUIDE")
print("=" * 70)
print("1. ELBOW METHOD (Inertia Plot):")
print("   - Look for the 'elbow' where the rate of decrease in inertia slows down")
print("   - The optimal k is typically at the elbow point")
print(f"   - Suggested k (elbow): {optimal_k_elbow}")
print("\n2. SILHOUETTE SCORE:")
print("   - Higher scores indicate better-defined clusters")
print("   - Score ranges from -1 (poor) to +1 (excellent)")
print(f"   - Optimal k (max silhouette): {optimal_k_silhouette}")
print(f"   - Best silhouette score: {max(silhouette_scores):.4f} at k={optimal_k_silhouette}")
print("\n3. CLINICAL RELEVANCE:")
print("   - Metabolic profiling typically suggests 4-5 distinct subtypes")
print("   - Consider both statistical metrics and clinical interpretability")

print("\n" + "=" * 70)
print("[SUCCESS] TASK 4 COMPLETE")
print("=" * 70)
print("\nNext Steps:")
print("  - Review the plots to visually confirm the optimal number of clusters")
print("  - Consider both statistical metrics and clinical relevance")
print("  - Proceed to Task 5: Apply K-Means clustering with the chosen k value")

