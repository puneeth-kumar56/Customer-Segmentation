#!/usr/bin/env python
"""
Runner script for Customer Segmentation Analysis

This script executes the complete customer segmentation pipeline.
Run this file from the terminal or VS Code to start the analysis.

Usage:
    python run.py
"""

from segmentation import main

if __name__ == "__main__":
    # Run the segmentation pipeline with the provided CSV file
    df_results, kmeans_model, scaled_features = main(filepath='data/customer_segmentation.csv')
    
    # Print summary
    print("\n" + "=" * 70)
    print("ANALYSIS SUMMARY")
    print("=" * 70)
    print(f"\nDataset: {len(df_results)} customers analyzed")
    print(f"Number of segments created: {len(df_results['Cluster'].unique())}")
    print(f"\nOutput files:")
    print(f"  ✓ Plots: See 'plots/' directory")
    print(f"  ✓ Data: 'data/customer_segmentation_with_clusters.csv'")
    print(f"\nTo explore the results further:")
    print(f"  - View the generated plots in the 'plots/' folder")
    print(f"  - Analyze the clustered data in 'data/customer_segmentation_with_clusters.csv'")
    print(f"  - Modify parameters in segmentation.py and rerun for different results")
    print("\n" + "=" * 70 + "\n")
