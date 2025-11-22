"""
Create Final Capstone Project Archive
Includes all data files, visualizations, output, source code, and documentation
"""

import zipfile
import os

# --- 1. Define all necessary files and folders created across the project ---
FILES_TO_INCLUDE = [
    # Data Files (CSV and NPY)
    'nhanes_metabolic_imputed_task1.csv',
    'X_train_scaled.npy',
    'X_test_scaled.npy',
    
    # Final Deliverables (Saved to output/ but included here for completeness)
    'output/nhanes_metabolic_labeled_task5.csv',
    'output/metabolic_subtype_centers_task5.csv',
    
    # Root level CSV files (for compatibility)
    'nhanes_metabolic_labeled_task5.csv',
    'metabolic_subtype_centers_task5.csv',
    
    # Source Code and Documentation
    '123.py',
    'task4_cluster_determination.py',
    'task5_clustering.py',
    'task7_umap_visualization.py',
    'task8_model_validation.py',
    'task8_final_validation_plot.py',
    'eda.py',
    'visualize.py',
    'create_zip.py',
    'README.md',
    'PROJECT_DOCUMENTATION.md',
    'QUICK_START.md',
    'SCRIPT_SUMMARY.md',
    'IMPLEMENTATION_SUMMARY.md',
    'DOCUMENTATION_INDEX.md',
    'OUTPUT_TABLE.txt',
    'requirements.txt',
    
    # Folders
    'visualizations/',
    'output/'
]

ZIP_FILENAME = 'final_capstone_project_complete.zip'

# --- 2. Create the ZIP archive ---
print("=" * 70)
print(f"Creating final archive: {ZIP_FILENAME}")
print("=" * 70)
print()

added_count = 0
skipped_count = 0

with zipfile.ZipFile(ZIP_FILENAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file_path in FILES_TO_INCLUDE:
        # Check if the file/folder exists before adding
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                # Add folder contents recursively
                folder_files = 0
                for root, _, files in os.walk(file_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        zipf.write(full_path, full_path)
                        folder_files += 1
                print(f"[OK] Added folder: {file_path} ({folder_files} files)")
                added_count += 1
            else:
                # Add individual file
                zipf.write(file_path)
                file_size = os.path.getsize(file_path)
                print(f"[OK] Added file: {file_path} ({file_size:,} bytes)")
                added_count += 1
        else:
            print(f"[SKIP] Not found: {file_path}")
            skipped_count += 1

# Get archive info
archive_size = os.path.getsize(ZIP_FILENAME)
archive_size_mb = archive_size / (1024 * 1024)

print()
print("=" * 70)
print("[SUCCESS] Final project archive created successfully!")
print("=" * 70)
print(f"\nArchive Details:")
print(f"  File: {ZIP_FILENAME}")
print(f"  Size: {archive_size_mb:.2f} MB ({archive_size:,} bytes)")
print(f"  Files/Folders Added: {added_count}")
print(f"  Files/Folders Skipped: {skipped_count}")
print(f"\nLocation: {os.path.abspath(ZIP_FILENAME)}")

