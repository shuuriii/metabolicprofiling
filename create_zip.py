"""
Create zip archive of all project outputs
"""
import zipfile
import os
from pathlib import Path

# Create zip file
zip_filename = 'capstone_metabolic_subtyping.zip'

print("Creating zip archive...")
print(f"Archive name: {zip_filename}\n")

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Add CSV files
    csv_files = list(Path('.').glob('*.csv'))
    if csv_files:
        print(f"Adding {len(csv_files)} CSV file(s)...")
        for csv_file in csv_files:
            zipf.write(csv_file)
            print(f"  - {csv_file}")
    
    # Add NumPy files
    npy_files = list(Path('.').glob('*.npy'))
    if npy_files:
        print(f"\nAdding {len(npy_files)} NumPy file(s)...")
        for npy_file in npy_files:
            zipf.write(npy_file)
            print(f"  - {npy_file}")
    
    # Add visualizations directory
    if os.path.exists('visualizations'):
        print(f"\nAdding visualizations/ directory...")
        for root, dirs, files in os.walk('visualizations'):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path)
                print(f"  - {file_path}")
    
    # Add output directory
    if os.path.exists('output'):
        print(f"\nAdding output/ directory...")
        for root, dirs, files in os.walk('output'):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path)
                print(f"  - {file_path}")

# Get file size
file_size = os.path.getsize(zip_filename)
file_size_mb = file_size / (1024 * 1024)

print(f"\n{'='*60}")
print(f"[SUCCESS] Zip archive created successfully!")
print(f"{'='*60}")
print(f"File: {zip_filename}")
print(f"Size: {file_size_mb:.2f} MB ({file_size:,} bytes)")

