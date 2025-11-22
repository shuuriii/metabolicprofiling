"""
Comprehensive Visualization Script for Metabolic Profiling Data
Generates multiple visualizations including distributions, correlations, and pair plots.
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import os

warnings.filterwarnings('ignore')

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300

# Define the 6 features
CLUSTER_FEATURES = ['HOMA_IR', 'FI', 'HbA1c', 'FBS', 'TGL', 'Creatinine']

def load_data():
    """Load data from CSV file or create sample data for demonstration."""
    # Try to load the actual data file
    data_files = [
        'nhanes_metabolic_imputed_task1.csv',
        'X_train_scaled.csv',
        'X_test_scaled.csv'
    ]
    
    for file in data_files:
        if os.path.exists(file):
            print(f"[OK] Loading data from: {file}")
            df = pd.read_csv(file)
            
            # If it's scaled data, we might need to handle it differently
            if 'X_train_scaled' in file or 'X_test_scaled' in file:
                # Check if columns match
                if all(col in df.columns for col in CLUSTER_FEATURES):
                    return df, file
            else:
                # Regular imputed data
                if 'HOMA_IR' not in df.columns and 'FI' in df.columns and 'FBS' in df.columns:
                    df['HOMA_IR'] = (df['FI'] * df['FBS']) / 405
                return df, file
    
    # If no data file found, create sample data for demonstration
    print("WARNING: No data file found. Generating sample data for visualization demonstration...")
    np.random.seed(42)
    n_samples = 500
    
    # Generate realistic sample data based on typical metabolic values
    sample_data = {
        'FI': np.random.lognormal(mean=2.5, sigma=0.8, size=n_samples),  # Fasting Insulin
        'FBS': np.random.normal(loc=100, scale=15, size=n_samples),      # Fasting Blood Sugar
        'HbA1c': np.random.normal(loc=5.5, scale=0.8, size=n_samples),   # HbA1c
        'TGL': np.random.lognormal(mean=4.5, sigma=0.7, size=n_samples), # Triglycerides
        'Creatinine': np.random.normal(loc=0.9, scale=0.2, size=n_samples) # Creatinine
    }
    
    # Ensure positive values
    sample_data['FI'] = np.abs(sample_data['FI'])
    sample_data['FBS'] = np.abs(sample_data['FBS'])
    sample_data['TGL'] = np.abs(sample_data['TGL'])
    sample_data['Creatinine'] = np.abs(sample_data['Creatinine'])
    
    df = pd.DataFrame(sample_data)
    df['HOMA_IR'] = (df['FI'] * df['FBS']) / 405
    
    # Reorder columns
    df = df[CLUSTER_FEATURES]
    
    return df, "sample_data"

def plot_distributions(df, save_path='visualizations'):
    """Create distribution plots (KDE) for all features."""
    print("\n[1/5] Creating Distribution Plots...")
    
    # Melt data for easier plotting
    df_plot = df[CLUSTER_FEATURES].melt()
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    for idx, feature in enumerate(CLUSTER_FEATURES):
        ax = axes[idx]
        data = df[feature].dropna()
        
        # KDE plot
        sns.kdeplot(data=data, ax=ax, fill=True, color='darkblue', alpha=0.7)
        
        # Add histogram overlay
        ax.hist(data, bins=30, density=True, alpha=0.3, color='steelblue', edgecolor='black')
        
        # Add mean line
        mean_val = data.mean()
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
        
        ax.set_title(f'{feature} Distribution', fontsize=14, fontweight='bold')
        ax.set_xlabel(f'{feature} Value', fontsize=12)
        ax.set_ylabel('Density', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.suptitle('Feature Distributions - Metabolic Profiling Data', 
                 fontsize=18, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(f'{save_path}/1_distributions.png', bbox_inches='tight', facecolor='white')
    print(f"  [OK] Saved: {save_path}/1_distributions.png")
    plt.show()

def plot_correlation_heatmap(df, save_path='visualizations'):
    """Create correlation heatmap."""
    print("\n[2/5] Creating Correlation Heatmap...")
    
    corr_matrix = df[CLUSTER_FEATURES].corr()
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create heatmap
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt='.3f',
        cmap='coolwarm',
        center=0,
        square=True,
        linewidths=1.5,
        linecolor='black',
        cbar_kws={"shrink": 0.8, "label": "Correlation Coefficient"},
        ax=ax,
        vmin=-1,
        vmax=1
    )
    
    ax.set_title('Correlation Matrix of Metabolic Features', 
                fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(f'{save_path}/2_correlation_heatmap.png', bbox_inches='tight', facecolor='white')
    print(f"  [OK] Saved: {save_path}/2_correlation_heatmap.png")
    
    # Print correlation values
    print("\n  Correlation Summary:")
    print("  " + "-" * 50)
    homa_corr = corr_matrix['HOMA_IR'].sort_values(ascending=False)
    for feature, corr_val in homa_corr.items():
        if feature != 'HOMA_IR':
            print(f"  HOMA_IR <-> {feature:12s}: {corr_val:6.3f}")
    
    plt.show()

def plot_pairplot(df, save_path='visualizations'):
    """Create pair plot showing relationships between all features."""
    print("\n[3/5] Creating Pair Plot (this may take a moment)...")
    
    # Create pair plot
    g = sns.pairplot(
        df[CLUSTER_FEATURES],
        plot_kws={'alpha': 0.6, 's': 15, 'edgecolor': 'black', 'linewidth': 0.5},
        diag_kws={'kde': True, 'fill': True, 'alpha': 0.7},
        corner=False,
        height=2.5
    )
    
    g.fig.suptitle('Pair Plot of Metabolic Features', 
                   fontsize=16, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(f'{save_path}/3_pairplot.png', bbox_inches='tight', facecolor='white')
    print(f"  [OK] Saved: {save_path}/3_pairplot.png")
    plt.show()

def plot_boxplots(df, save_path='visualizations'):
    """Create box plots for all features."""
    print("\n[4/5] Creating Box Plots...")
    
    # Melt data for box plot
    df_plot = df[CLUSTER_FEATURES].melt()
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    sns.boxplot(data=df_plot, x='variable', y='value', ax=ax, palette='Set2')
    sns.stripplot(data=df_plot, x='variable', y='value', ax=ax, 
                  color='black', alpha=0.3, size=2)
    
    ax.set_title('Box Plots of Metabolic Features', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Feature', fontsize=12)
    ax.set_ylabel('Value', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(f'{save_path}/4_boxplots.png', bbox_inches='tight', facecolor='white')
    print(f"  [OK] Saved: {save_path}/4_boxplots.png")
    plt.show()

def plot_homa_relationships(df, save_path='visualizations'):
    """Create specific plots showing HOMA-IR relationships."""
    print("\n[5/5] Creating HOMA-IR Relationship Plots...")
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # HOMA-IR vs FBS
    axes[0].scatter(df['FBS'], df['HOMA_IR'], alpha=0.6, s=30, edgecolors='black', linewidth=0.5)
    z = np.polyfit(df['FBS'], df['HOMA_IR'], 1)
    p = np.poly1d(z)
    axes[0].plot(df['FBS'], p(df['FBS']), "r--", linewidth=2, label=f'Trend line')
    axes[0].set_xlabel('Fasting Blood Sugar (FBS)', fontsize=12)
    axes[0].set_ylabel('HOMA-IR', fontsize=12)
    axes[0].set_title('HOMA-IR vs Fasting Blood Sugar', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # HOMA-IR vs FI
    axes[1].scatter(df['FI'], df['HOMA_IR'], alpha=0.6, s=30, edgecolors='black', linewidth=0.5, color='green')
    z = np.polyfit(df['FI'], df['HOMA_IR'], 1)
    p = np.poly1d(z)
    axes[1].plot(df['FI'], p(df['FI']), "r--", linewidth=2, label=f'Trend line')
    axes[1].set_xlabel('Fasting Insulin (FI)', fontsize=12)
    axes[1].set_ylabel('HOMA-IR', fontsize=12)
    axes[1].set_title('HOMA-IR vs Fasting Insulin', fontsize=14, fontweight='bold')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.suptitle('HOMA-IR Key Relationships', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(f'{save_path}/5_homa_relationships.png', bbox_inches='tight', facecolor='white')
    print(f"  [OK] Saved: {save_path}/5_homa_relationships.png")
    plt.show()

def print_summary_statistics(df):
    """Print summary statistics."""
    print("\n" + "=" * 70)
    print("SUMMARY STATISTICS")
    print("=" * 70)
    print(df[CLUSTER_FEATURES].describe().round(3))
    print("\n" + "=" * 70)

def main():
    """Main function to run all visualizations."""
    print("=" * 70)
    print("METABOLIC PROFILING - DATA VISUALIZATION")
    print("=" * 70)
    
    # Load data
    df, data_source = load_data()
    print(f"\n[OK] Data loaded: {len(df)} samples, {df.shape[1]} features")
    print(f"  Source: {data_source}")
    
    if data_source == "sample_data":
        print("  WARNING: Using sample data for demonstration purposes")
        print("  Run 'python 123.py' first to generate real NHANES data")
    
    # Print summary statistics
    print_summary_statistics(df)
    
    # Create all visualizations
    save_path = 'visualizations'
    
    plot_distributions(df, save_path)
    plot_correlation_heatmap(df, save_path)
    plot_boxplots(df, save_path)
    plot_homa_relationships(df, save_path)
    plot_pairplot(df, save_path)  # Last because it takes longest
    
    print("\n" + "=" * 70)
    print("[SUCCESS] ALL VISUALIZATIONS COMPLETE")
    print("=" * 70)
    print(f"\nAll plots saved to '{save_path}/' directory:")
    print("  • 1_distributions.png - Feature distribution plots")
    print("  • 2_correlation_heatmap.png - Correlation matrix")
    print("  • 3_pairplot.png - Pairwise feature relationships")
    print("  • 4_boxplots.png - Box plots for all features")
    print("  • 5_homa_relationships.png - HOMA-IR key relationships")
    print("\nTIP: Review the correlation heatmap to understand feature relationships,")
    print("     especially HOMA-IR's relationship with FBS and FI.")

if __name__ == "__main__":
    main()

