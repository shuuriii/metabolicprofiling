"""
Task 8: Model Validation (Random Forest Classifier)
Trains a Random Forest classifier to predict metabolic subtypes and validates
the clustering results by assessing how well the model can distinguish between subtypes.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')

# ============================================================================
# Setup: Load Data and Define X and y
# ============================================================================
CLUSTER_FEATURES = ['HOMA_IR', 'FI', 'HbA1c', 'FBS', 'TGL', 'Creatinine']

SUBTYPE_NAMES = {
    0: 'Resilient',
    1: 'CIR',
    2: 'HTD',
    3: 'SNMF'
}

K_CLUSTERS = len(SUBTYPE_NAMES)

print("=" * 70)
print("TASK 8: Model Validation (Random Forest Classifier)")
print("=" * 70)
print("\nThis task validates the clustering results by training a classifier")
print("to predict metabolic subtypes. High accuracy indicates well-separated clusters.\n")

try:
    # 1. Load the final labeled dataset from Task 5
    df_labeled = pd.read_csv('nhanes_metabolic_labeled_task5.csv')
    
    # Verify required columns exist
    if 'Subtype' not in df_labeled.columns:
        raise ValueError("'Subtype' column not found in labeled dataset")
    
    # Use the scaled features array from the .npy files for X
    X = np.concatenate([np.load('X_train_scaled.npy'), np.load('X_test_scaled.npy')], axis=0)
    
    # Use the assigned Subtype label for y
    y = df_labeled['Subtype'].values
    
    # Verify sizes match
    if len(X) != len(y):
        print(f"WARNING: Size mismatch! Features: {len(X)}, Labels: {len(y)}")
        min_size = min(len(X), len(y))
        X = X[:min_size]
        y = y[:min_size]
        print(f"Adjusted to use first {min_size} samples")
    
    print(f"[OK] Data loaded: {len(X)} samples, {X.shape[1]} features")
    print(f"[OK] Subtype distribution:")
    unique, counts = np.unique(y, return_counts=True)
    for subtype_id, count in zip(unique, counts):
        percentage = (count / len(y)) * 100
        print(f"     {SUBTYPE_NAMES[subtype_id]:15s}: {count:4d} ({percentage:5.2f}%)")

except FileNotFoundError as e:
    print(f"\nERROR: Missing required file: {e}")
    print("\nPlease ensure the following files exist:")
    print("  - nhanes_metabolic_labeled_task5.csv (from Task 5)")
    print("  - X_train_scaled.npy (from Task 3)")
    print("  - X_test_scaled.npy (from Task 3)")
    print("\nRun Tasks 1-5 first to generate these files.")
    exit(1)
except Exception as e:
    print(f"\nERROR: {e}")
    exit(1)

# ============================================================================
# Step 8.1: Split Data (matching Task 3's split)
# ============================================================================
print("\n" + "-" * 70)
print("Splitting data into Training and Test sets...")
print("-" * 70)

# Split data back into Training and Test sets (using the same split ratio/seed as Task 3)
# stratify=y ensures balanced class distribution in train/test splits
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.3, 
    random_state=42, 
    stratify=y
)

print(f"[OK] Dataset split:")
print(f"     Training set: {len(X_train)} samples ({len(X_train)/len(X)*100:.1f}%)")
print(f"     Test set: {len(X_test)} samples ({len(X_test)/len(X)*100:.1f}%)")

# Display class distribution in train/test
print(f"\n     Training set class distribution:")
train_unique, train_counts = np.unique(y_train, return_counts=True)
for subtype_id, count in zip(train_unique, train_counts):
    percentage = (count / len(y_train)) * 100
    print(f"       {SUBTYPE_NAMES[subtype_id]:15s}: {count:4d} ({percentage:5.2f}%)")

print(f"\n     Test set class distribution:")
test_unique, test_counts = np.unique(y_test, return_counts=True)
for subtype_id, count in zip(test_unique, test_counts):
    percentage = (count / len(y_test)) * 100
    print(f"       {SUBTYPE_NAMES[subtype_id]:15s}: {count:4d} ({percentage:5.2f}%)")

# ============================================================================
# Step 8.2: Train the Random Forest Classifier
# ============================================================================
print("\n" + "-" * 70)
print("Training Random Forest Classifier...")
print("-" * 70)

# Random Forest parameters:
# - n_estimators=100: Number of trees in the forest
# - random_state=42: For reproducibility
# - class_weight='balanced': Handles imbalanced classes automatically
rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight='balanced',
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1
)

print("Fitting Random Forest model...")
rf_model.fit(X_train, y_train)
print("[OK] Model training complete")

# Get feature importance
feature_importance = pd.DataFrame({
    'Feature': CLUSTER_FEATURES,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nFeature Importance (Top features for subtype prediction):")
for idx, row in feature_importance.iterrows():
    print(f"  {row['Feature']:12s}: {row['Importance']:.4f}")

# ============================================================================
# Step 8.3: Evaluate Model Performance
# ============================================================================
print("\n" + "-" * 70)
print("Evaluating Model Performance on Test Set...")
print("-" * 70)

# Make predictions
y_pred = rf_model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy (Test Set): {accuracy:.4f} ({accuracy*100:.2f}%)")

# Classification report
print("\n" + "=" * 70)
print("Classification Report")
print("=" * 70)
print(classification_report(
    y_test, 
    y_pred, 
    target_names=list(SUBTYPE_NAMES.values()),
    digits=4
))

# ============================================================================
# Step 8.4: Visualize Confusion Matrix
# ============================================================================
print("\n" + "-" * 70)
print("Generating Confusion Matrix...")
print("-" * 70)

cm = confusion_matrix(y_test, y_pred)

# Create confusion matrix visualization
plt.figure(figsize=(8, 7))
sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    cbar=True,
    cbar_kws={'label': 'Count'},
    xticklabels=list(SUBTYPE_NAMES.values()),
    yticklabels=list(SUBTYPE_NAMES.values()),
    linewidths=0.5,
    linecolor='gray'
)

plt.xlabel('Predicted Subtype', fontsize=12, fontweight='bold')
plt.ylabel('True Subtype', fontsize=12, fontweight='bold')
plt.title('Confusion Matrix - Metabolic Subtype Classification', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()

# Save the plot
os.makedirs('visualizations', exist_ok=True)
output_file = 'visualizations/8_confusion_matrix.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"[OK] Confusion matrix saved to: {output_file}")

plt.show()

# ============================================================================
# Additional Analysis: Per-Class Performance
# ============================================================================
print("\n" + "-" * 70)
print("Per-Class Performance Analysis")
print("-" * 70)

# Calculate per-class metrics
from sklearn.metrics import precision_score, recall_score, f1_score

precision = precision_score(y_test, y_pred, average=None)
recall = recall_score(y_test, y_pred, average=None)
f1 = f1_score(y_test, y_pred, average=None)

performance_df = pd.DataFrame({
    'Subtype': [SUBTYPE_NAMES[i] for i in range(K_CLUSTERS)],
    'Precision': precision,
    'Recall': recall,
    'F1-Score': f1
})

print("\nPer-Subtype Metrics:")
print(performance_df.to_string(index=False))

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 70)
print("[SUCCESS] TASK 8 COMPLETE")
print("=" * 70)
print("\nSummary:")
print(f"  • Random Forest classifier trained with {rf_model.n_estimators} trees")
print(f"  • Test set accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"  • Confusion matrix saved to: visualizations/8_confusion_matrix.png")
print("\nInterpretation:")
print("  • High accuracy indicates well-separated, distinct metabolic subtypes")
print("  • Low accuracy may suggest overlapping subtypes or need for refinement")
print("  • Feature importance shows which metabolic markers are most discriminative")
print("\n✅ Task 8 Complete. Model validation metrics are displayed.")

