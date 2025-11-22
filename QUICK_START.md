# Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- Internet connection (for NHANES data download)

## Installation (One-Time Setup)

```bash
# Install all required packages
pip install -r requirements.txt
```

## Running the Complete Pipeline

### Option 1: Run All Steps Sequentially

```bash
# Step 1: Data preparation (Tasks 1-3)
python 123.py

# Step 2: Optional - Visualize data
python visualize.py

# Step 3: Find optimal clusters (Task 4)
python task4_cluster_determination.py

# Step 4: Apply clustering (Task 5)
python task5_clustering.py
```

### Option 2: Run Only Essential Steps

```bash
# Essential: Data preparation
python 123.py

# Essential: Cluster determination
python task4_cluster_determination.py

# Essential: Apply clustering
python task5_clustering.py
```

## Expected Runtime

- **Task 1-3** (`123.py`): 5-15 minutes (depends on NHANES download speed)
- **Task 4** (`task4_cluster_determination.py`): 2-5 minutes
- **Task 5** (`task5_clustering.py`): < 1 minute
- **Task 7** (`task7_umap_visualization.py`): 1-2 minutes
- **Task 8** (`task8_model_validation.py`): < 1 minute

## Output Files to Check

After running all tasks, you should have:

1. **Data Files**:
   - `nhanes_metabolic_imputed_task1.csv` - Your processed dataset
   - `X_train_scaled.npy` - Training data
   - `X_test_scaled.npy` - Test data
   - `output/metabolic_subtype_centers_task5.csv` - **Final cluster centers**

2. **Visualizations** (in `visualizations/` folder):
   - `4_optimal_clusters.png` - Shows optimal k value
   - `7_umap_visualization.png` - UMAP plot showing subtype separation
   - `8_confusion_matrix.png` - Model validation confusion matrix
   - Other EDA plots if you ran `visualize.py`

## Understanding Your Results

### Cluster Centers Table

The final output (`metabolic_subtype_centers_task5.csv`) shows:

| Subtype | HOMA_IR | FI | HbA1c | FBS | TGL | Creatinine |
|---------|---------|----|----|----|----|-----------|
| 0 | ... | ... | ... | ... | ... | ... |
| 1 | ... | ... | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... | ... |

Each row represents one metabolic subtype with characteristic values.

### Next Steps

1. **Review cluster centers** - Understand each subtype's profile
2. **Name the subtypes** - Assign clinical names (e.g., "Healthy", "Insulin Resistant")
3. **Validate results** - Check if subtypes make clinical sense
4. **Use for analysis** - Apply subtypes to your research questions

## Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "FileNotFoundError: X_train_scaled.npy"
Run `python 123.py` first to generate required files.

### NHANES download fails
- Check internet connection
- The library may need manual file download (see error message)
- Try running again (network issues are usually temporary)

### Scripts run but no output
- Check console for error messages
- Ensure you're in the correct directory
- Verify Python version: `python --version` (should be 3.8+)

## Getting Help

1. Check `README.md` for detailed documentation
2. Review `PROJECT_DOCUMENTATION.md` for technical details
3. Check code comments in each script
4. Review error messages - they usually indicate what's missing

## Example Workflow

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Prepare data (this takes longest)
python 123.py
# Wait for completion... should see "TASKS 1, 2, and 3 COMPLETE"

# 3. Optional: Visualize
python visualize.py

# 4. Find optimal clusters
python task4_cluster_determination.py
# Review the plot to confirm k=4 is optimal

# 5. Apply clustering
python task5_clustering.py
# Check output/metabolic_subtype_centers_task5.csv for results

# Done! Review your cluster centers.
```

## Success Indicators

You've successfully completed the pipeline when:

✅ `nhanes_metabolic_imputed_task1.csv` exists  
✅ `X_train_scaled.npy` and `X_test_scaled.npy` exist  
✅ `output/metabolic_subtype_centers_task5.csv` exists  
✅ Cluster centers table shows 4 subtypes with meaningful values  
✅ `visualizations/7_umap_visualization.png` exists (if Task 7 run)  
✅ `visualizations/8_confusion_matrix.png` exists (if Task 8 run)  
✅ No error messages in console  

## Common Questions

**Q: How long does this take?**  
A: 10-20 minutes total, mostly for data download.

**Q: Do I need to run all scripts?**  
A: Yes, in order: 123.py → task4 → task5. Visualize is optional.

**Q: Can I change k=4 to a different value?**  
A: Yes, edit `K_CLUSTERS` in `task5_clustering.py` (but check Task 4 results first).

**Q: What if I get different results?**  
A: That's normal! Results depend on your specific NHANES data subset.

**Q: What is UMAP and why do I need it?**  
A: UMAP reduces 6D metabolic features to 2D for visualization. It helps validate that your subtypes are well-separated.

