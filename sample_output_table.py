"""
Sample Output Table - Metabolic Subtype Centers
This shows what the output table from Task 5 will look like.
"""

import pandas as pd

# Sample cluster centers table (what Task 5 will produce)
CLUSTER_FEATURES = ['HOMA_IR', 'FI', 'HbA1c', 'FBS', 'TGL', 'Creatinine']

# Example cluster centers (these are illustrative values)
# In reality, these will be calculated from your actual NHANES data
sample_centers = {
    'Subtype 0': {
        'HOMA_IR': 2.15,
        'FI': 8.5,
        'HbA1c': 5.2,
        'FBS': 95.0,
        'TGL': 85.0,
        'Creatinine': 0.85
    },
    'Subtype 1': {
        'HOMA_IR': 4.80,
        'FI': 18.2,
        'HbA1c': 5.8,
        'FBS': 108.0,
        'TGL': 145.0,
        'Creatinine': 0.92
    },
    'Subtype 2': {
        'HOMA_IR': 8.50,
        'FI': 32.5,
        'HbA1c': 6.5,
        'FBS': 118.0,
        'TGL': 220.0,
        'Creatinine': 0.98
    },
    'Subtype 3': {
        'HOMA_IR': 1.80,
        'FI': 6.8,
        'HbA1c': 4.9,
        'FBS': 88.0,
        'TGL': 65.0,
        'Creatinine': 0.78
    }
}

# Create DataFrame
df_centers = pd.DataFrame(sample_centers).T
df_centers.index.name = 'Subtype ID'

print("=" * 80)
print("SAMPLE OUTPUT TABLE: Unscaled Metabolic Subtype Profiles")
print("=" * 80)
print("\nThis is what the output from Task 5 will look like.")
print("These are the characteristic metabolic profiles for each subtype.")
print("(Values are in original units: FI in uU/mL, FBS in mg/dL, HbA1c in %, etc.)\n")
print("-" * 80)
print(df_centers.to_string())
print("-" * 80)

print("\n\n" + "=" * 80)
print("FORMATTED TABLE (Markdown style)")
print("=" * 80)
print("\n" + df_centers.to_markdown())

print("\n\n" + "=" * 80)
print("INTERPRETATION GUIDE")
print("=" * 80)
print("""
Each row represents one metabolic subtype identified by K-Means clustering.

Feature Units:
  - HOMA_IR:  Unitless (calculated from FI × FBS / 405)
  - FI:       Fasting Insulin in uU/mL (micro-units per milliliter)
  - HbA1c:    Hemoglobin A1c in percentage (%)
  - FBS:      Fasting Blood Sugar in mg/dL (milligrams per deciliter)
  - TGL:      Triglycerides in mg/dL
  - Creatinine: Serum Creatinine in mg/dL

Typical Clinical Ranges:
  - HOMA_IR:  < 1.0 (normal), 1.0-2.5 (borderline), > 2.5 (insulin resistant)
  - FI:       2-25 uU/mL (normal fasting range)
  - HbA1c:    < 5.7% (normal), 5.7-6.4% (prediabetes), ≥ 6.5% (diabetes)
  - FBS:      70-100 mg/dL (normal), 100-125 (prediabetes), ≥ 126 (diabetes)
  - TGL:      < 150 mg/dL (normal), 150-199 (borderline), ≥ 200 (high)
  - Creatinine: 0.6-1.2 mg/dL (normal range, varies by gender/age)

Use these centers to:
  1. Understand the metabolic characteristics of each subtype
  2. Name the subtypes based on their profiles (Task 6)
  3. Identify which subtype represents which metabolic phenotype
""")

# Save as CSV for reference
df_centers.to_csv('sample_metabolic_subtype_centers.csv', index=True)
print("\n[OK] Sample table saved to: sample_metabolic_subtype_centers.csv")

