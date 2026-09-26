

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, silhouette_samples
import warnings
import os
from datetime import datetime

warnings.filterwarnings('ignore')

# ==================== CONFIGURATION ====================
RANDOM_STATE = 42
PLOTS_DIR = 'plots'
DATA_DIR = 'data'
np.random.seed(RANDOM_STATE)

# Create plots directory if it doesn't exist
os.makedirs(PLOTS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Configure matplotlib style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


# ==================== DATA LOADING & PREPROCESSING ====================

def load_data(filepath):
    """
    Load customer data from CSV file.
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded dataframe
    """
    print("=" * 70)
    print("STEP 1: LOADING DATA")
    print("=" * 70)
    
    df = pd.read_csv(filepath)
    print(f"✓ Data loaded successfully!")
    print(f"  - Shape: {df.shape[0]} customers, {df.shape[1]} features")
    print(f"  - Columns: {', '.join(df.columns[:10])}...")
    print()
    
    return df


def preprocess_data(df):
    """
    Preprocess the data: handle missing values and create derived features.
    
    Args:
        df (pd.DataFrame): Raw dataframe
        
    Returns:
        pd.DataFrame: Preprocessed dataframe with derived features
    """
    print("=" * 70)
    print("STEP 2: DATA PREPROCESSING")
    print("=" * 70)
    
    # Create a copy to avoid modifying original
    df_processed = df.copy()
    
    # Handle missing values in Income
    missing_income = df_processed['Income'].isna().sum()
    if missing_income > 0:
        income_median = df_processed['Income'].median()
        df_processed['Income'].fillna(income_median, inplace=True)
        print(f"✓ Filled {missing_income} missing Income values with median: ${income_median:,.2f}")
    
    # Create Age from Year_Birth
    current_year = datetime.now().year
    df_processed['Age'] = current_year - df_processed['Year_Birth']
    print(f"✓ Created 'Age' feature from Year_Birth")
    
    # Create Children: total kids and teens at home
    df_processed['Children'] = df_processed['Kidhome'] + df_processed['Teenhome']
    print(f"✓ Created 'Children' feature (Kidhome + Teenhome)")
    
    # Create TotalSpend: sum of all product category spending
    spending_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 
                     'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
    df_processed['TotalSpend'] = df_processed[spending_cols].sum(axis=1)
    print(f"✓ Created 'TotalSpend' feature (sum of product categories)")
    
    # Create Total Purchases across channels
    purchase_cols = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']
    df_processed['TotalPurchases'] = df_processed[purchase_cols].sum(axis=1)
    print(f"✓ Created 'TotalPurchases' feature (across all channels)")
    
    # Print summary statistics
    print(f"\n  Data Summary (after preprocessing):")
    print(f"  - Missing values: {df_processed.isnull().sum().sum()}")
    print(f"  - Age range: {df_processed['Age'].min()} - {df_processed['Age'].max()} years")
    print(f"  - Income range: ${df_processed['Income'].min():,.0f} - ${df_processed['Income'].max():,.0f}")
    print(f"  - TotalSpend range: ${df_processed['TotalSpend'].min():,.0f} - ${df_processed['TotalSpend'].max():,.0f}")
    print()
    
    return df_processed


def normalize_features(df):
    """
    Normalize numerical features using StandardScaler.
    
    Args:
        df (pd.DataFrame): Preprocessed dataframe
        
    Returns:
        tuple: (scaled_data, scaler, feature_names)
    """
    print("=" * 70)
    print("STEP 3: FEATURE NORMALIZATION")
    print("=" * 70)
    
    # Select numerical features for clustering
    numerical_features = ['Age', 'Income', 'Children', 'TotalSpend', 
                         'TotalPurchases', 'Recency', 'NumWebVisitsMonth']
    
    # Extract numerical features
    X = df[numerical_features].copy()
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print(f"✓ Normalized {len(numerical_features)} numerical features")
    print(f"  Features: {', '.join(numerical_features)}")
    print(f"  Scaled data shape: {X_scaled.shape}")
    print()
    
    return X_scaled, scaler, numerical_features


# ==================== EXPLORATORY DATA ANALYSIS ====================

def perform_eda(df):
    """
    Perform exploratory data analysis and generate visualizations.
    
    Args:
        df (pd.DataFrame): Preprocessed dataframe
    """
    print("=" * 70)
    print("STEP 4: EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 70)
    
    # Create figure with subplots for distributions
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle('Customer Characteristics - Distribution Analysis', fontsize=16, fontweight='bold')
    
    # Age distribution
    axes[0, 0].hist(df['Age'], bins=30, color='steelblue', edgecolor='black', alpha=0.7)
    axes[0, 0].set_title('Age Distribution', fontweight='bold')
    axes[0, 0].set_xlabel('Age (years)')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].axvline(df['Age'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["Age"].mean():.1f}')
    axes[0, 0].legend()
    
    # Income distribution
    axes[0, 1].hist(df['Income'], bins=30, color='seagreen', edgecolor='black', alpha=0.7)
    axes[0, 1].set_title('Income Distribution', fontweight='bold')
    axes[0, 1].set_xlabel('Annual Income ($)')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].axvline(df['Income'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: ${df["Income"].mean():,.0f}')
    axes[0, 1].legend()
    
    # TotalSpend distribution
    axes[0, 2].hist(df['TotalSpend'], bins=30, color='coral', edgecolor='black', alpha=0.7)
    axes[0, 2].set_title('Total Spend Distribution', fontweight='bold')
    axes[0, 2].set_xlabel('Total Spend ($)')
    axes[0, 2].set_ylabel('Frequency')
    axes[0, 2].axvline(df['TotalSpend'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: ${df["TotalSpend"].mean():,.0f}')
    axes[0, 2].legend()
    
    # Children distribution
    children_counts = df['Children'].value_counts().sort_index()
    axes[1, 0].bar(children_counts.index, children_counts.values, color='purple', alpha=0.7, edgecolor='black')
    axes[1, 0].set_title('Number of Children Distribution', fontweight='bold')
    axes[1, 0].set_xlabel('Number of Children')
    axes[1, 0].set_ylabel('Count')
    
    # Recency distribution
    axes[1, 1].hist(df['Recency'], bins=30, color='orange', edgecolor='black', alpha=0.7)
    axes[1, 1].set_title('Recency Distribution (Days Since Last Purchase)', fontweight='bold')
    axes[1, 1].set_xlabel('Days')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].axvline(df['Recency'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["Recency"].mean():.1f}')
    axes[1, 1].legend()
    
    # Web visits distribution
    axes[1, 2].hist(df['NumWebVisitsMonth'], bins=20, color='teal', edgecolor='black', alpha=0.7)
    axes[1, 2].set_title('Monthly Web Visits Distribution', fontweight='bold')
    axes[1, 2].set_xlabel('Visits per Month')
    axes[1, 2].set_ylabel('Frequency')
    axes[1, 2].axvline(df['NumWebVisitsMonth'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["NumWebVisitsMonth"].mean():.1f}')
    axes[1, 2].legend()
    
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/01_distributions.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: 01_distributions.png")
    plt.close()
    
    # Correlation Heatmap
    numerical_cols = ['Age', 'Income', 'Children', 'TotalSpend', 'TotalPurchases', 
                      'Recency', 'NumWebVisitsMonth', 'MntWines', 'MntFruits', 
                      'MntMeatProducts', 'MntFishProducts']
    
    fig, ax = plt.subplots(figsize=(12, 10))
    correlation_matrix = df[numerical_cols].corr()
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=0.5, cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title('Correlation Heatmap of Numerical Features', fontweight='bold', fontsize=14)
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/02_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: 02_correlation_heatmap.png")
    plt.close()
    
    # Boxplots for spending categories
    spending_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 
                     'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle('Spending by Product Category - Box Plots', fontsize=16, fontweight='bold')
    
    for idx, col in enumerate(spending_cols):
        ax = axes[idx // 3, idx % 3]
        ax.boxplot(df[col], vert=True)
        ax.set_title(col, fontweight='bold')
        ax.set_ylabel('Spending ($)')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/03_spending_boxplots.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: 03_spending_boxplots.png")
    plt.close()
    
    print(f"\n  EDA Summary:")
    print(f"  - Total customers analyzed: {len(df)}")
    print(f"  - Average age: {df['Age'].mean():.1f} years")
    print(f"  - Average income: ${df['Income'].mean():,.2f}")
    print(f"  - Average total spend: ${df['TotalSpend'].mean():,.2f}")
    print()


# ==================== CLUSTERING ====================

def find_optimal_clusters(X_scaled, max_k=10):
    """
    Determine optimal number of clusters using elbow method and silhouette score.
    
    Args:
        X_scaled (np.ndarray): Normalized feature matrix
        max_k (int): Maximum number of clusters to test
        
    Returns:
        tuple: (inertias, silhouette_scores, optimal_k)
    """
    print("=" * 70)
    print("STEP 5: DETERMINING OPTIMAL NUMBER OF CLUSTERS")
    print("=" * 70)
    
    inertias = []
    silhouette_scores = []
    K_range = range(2, max_k + 1)
    
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
        print(f"  k={k}: Inertia={kmeans.inertia_:.2f}, Silhouette Score={silhouette_scores[-1]:.3f}")
    
    # Find optimal k by silhouette score
    optimal_k = list(K_range)[np.argmax(silhouette_scores)]
    print(f"\n✓ Optimal number of clusters: {optimal_k} (based on silhouette score)")
    
    # Plot elbow curve and silhouette scores
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Elbow plot
    axes[0].plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
    axes[0].axvline(optimal_k, color='red', linestyle='--', linewidth=2, label=f'Optimal k={optimal_k}')
    axes[0].set_xlabel('Number of Clusters (k)', fontweight='bold')
    axes[0].set_ylabel('Inertia (Within-cluster sum of squares)', fontweight='bold')
    axes[0].set_title('Elbow Method', fontweight='bold', fontsize=12)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    
    # Silhouette score plot
    axes[1].plot(K_range, silhouette_scores, 'go-', linewidth=2, markersize=8)
    axes[1].axvline(optimal_k, color='red', linestyle='--', linewidth=2, label=f'Optimal k={optimal_k}')
    axes[1].set_xlabel('Number of Clusters (k)', fontweight='bold')
    axes[1].set_ylabel('Silhouette Score', fontweight='bold')
    axes[1].set_title('Silhouette Analysis', fontweight='bold', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/04_optimal_clusters.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 04_optimal_clusters.png\n")
    plt.close()
    
    return inertias, silhouette_scores, optimal_k


def perform_clustering(X_scaled, optimal_k):
    """
    Perform K-Means clustering with optimal number of clusters.
    
    Args:
        X_scaled (np.ndarray): Normalized feature matrix
        optimal_k (int): Optimal number of clusters
        
    Returns:
        KMeans: Fitted KMeans model
    """
    print("=" * 70)
    print("STEP 6: PERFORMING K-MEANS CLUSTERING")
    print("=" * 70)
    
    kmeans = KMeans(n_clusters=optimal_k, random_state=RANDOM_STATE, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    
    print(f"✓ K-Means clustering completed with {optimal_k} clusters")
    print(f"  - Final inertia: {kmeans.inertia_:.2f}")
    print(f"  - Silhouette score: {silhouette_score(X_scaled, cluster_labels):.3f}")
    
    # Print cluster sizes
    unique, counts = np.unique(cluster_labels, return_counts=True)
    print(f"\n  Cluster Distribution:")
    for cluster_id, count in zip(unique, counts):
        percentage = (count / len(cluster_labels)) * 100
        print(f"    Cluster {cluster_id}: {count} customers ({percentage:.1f}%)")
    print()
    
    return kmeans


# ==================== VISUALIZATION ====================

def visualize_clusters(X_scaled, kmeans, df_processed):
    """
    Create PCA-based visualization of clusters.
    
    Args:
        X_scaled (np.ndarray): Normalized feature matrix
        kmeans (KMeans): Fitted KMeans model
        df_processed (pd.DataFrame): Processed dataframe
    """
    print("=" * 70)
    print("STEP 7: CLUSTER VISUALIZATION")
    print("=" * 70)
    
    # Apply PCA for 2D visualization
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    X_pca = pca.fit_transform(X_scaled)
    
    print(f"✓ Applied PCA for dimensionality reduction")
    print(f"  - Explained variance: {pca.explained_variance_ratio_.sum():.1%}")
    print(f"  - PC1 variance: {pca.explained_variance_ratio_[0]:.1%}")
    print(f"  - PC2 variance: {pca.explained_variance_ratio_[1]:.1%}")
    
    # 2D scatter plot of clusters
    fig, ax = plt.subplots(figsize=(12, 8))
    
    cluster_labels = kmeans.labels_
    n_clusters = len(np.unique(cluster_labels))
    
    colors = plt.cm.Set3(np.linspace(0, 1, n_clusters))
    
    for i in range(n_clusters):
        mask = cluster_labels == i
        ax.scatter(X_pca[mask, 0], X_pca[mask, 1], 
                   label=f'Cluster {i} (n={mask.sum()})',
                   alpha=0.6, s=100, color=colors[i], edgecolors='black', linewidth=0.5)
    
    # Plot cluster centers (transformed to PCA space)
    centers_pca = pca.transform(kmeans.cluster_centers_)
    ax.scatter(centers_pca[:, 0], centers_pca[:, 1], 
               marker='*', s=800, c='red', edgecolors='black', linewidth=2,
               label='Cluster Centers', zorder=5)
    
    ax.set_xlabel(f'First Principal Component ({pca.explained_variance_ratio_[0]:.1%})', fontweight='bold')
    ax.set_ylabel(f'Second Principal Component ({pca.explained_variance_ratio_[1]:.1%})', fontweight='bold')
    ax.set_title('Customer Clusters (PCA Visualization)', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/05_cluster_visualization_pca.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 05_cluster_visualization_pca.png")
    plt.close()
    
    # Add cluster labels to dataframe
    df_processed['Cluster'] = cluster_labels
    
    # Create spending profile chart
    spending_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 
                     'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
    
    avg_spending = df_processed.groupby('Cluster')[spending_cols].mean()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    avg_spending.plot(kind='bar', ax=ax, width=0.8, color=colors[:n_clusters])
    ax.set_title('Average Spending by Product Category per Cluster', fontsize=14, fontweight='bold')
    ax.set_xlabel('Cluster', fontweight='bold')
    ax.set_ylabel('Average Spending ($)', fontweight='bold')
    ax.legend(title='Product Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=0)
    
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/06_spending_by_cluster.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 06_spending_by_cluster.png")
    plt.close()
    
    print()
    return df_processed


# ==================== SEGMENT PROFILING ====================

def profile_segments(df_processed):
    """
    Generate detailed profile of each customer segment.
    
    Args:
        df_processed (pd.DataFrame): DataFrame with cluster assignments
    """
    print("=" * 70)
    print("STEP 8: SEGMENT PROFILING & INSIGHTS")
    print("=" * 70)
    print()
    
    clusters = sorted(df_processed['Cluster'].unique())
    
    for cluster_id in clusters:
        cluster_data = df_processed[df_processed['Cluster'] == cluster_id]
        n_customers = len(cluster_data)
        percentage = (n_customers / len(df_processed)) * 100
        
        print("─" * 70)
        print(f"CLUSTER {cluster_id}: {n_customers} customers ({percentage:.1f}% of total)")
        print("─" * 70)
        
        # Demographics
        print("\n📊 DEMOGRAPHICS:")
        print(f"  Age           | Mean: {cluster_data['Age'].mean():.1f} years | Range: {cluster_data['Age'].min()}-{cluster_data['Age'].max()}")
        print(f"  Income        | Mean: ${cluster_data['Income'].mean():,.2f} | Median: ${cluster_data['Income'].median():,.2f}")
        print(f"  Children      | Mean: {cluster_data['Children'].mean():.2f} | Mode: {cluster_data['Children'].mode()[0]:.0f}")
        
        # Spending behavior
        print("\n💰 SPENDING BEHAVIOR:")
        print(f"  Total Spend   | Mean: ${cluster_data['TotalSpend'].mean():,.2f} | Median: ${cluster_data['TotalSpend'].median():,.2f}")
        print(f"  Wines         | Mean: ${cluster_data['MntWines'].mean():,.2f}")
        print(f"  Meats         | Mean: ${cluster_data['MntMeatProducts'].mean():,.2f}")
        print(f"  Fruits        | Mean: ${cluster_data['MntFruits'].mean():,.2f}")
        print(f"  Fish          | Mean: ${cluster_data['MntFishProducts'].mean():,.2f}")
        print(f"  Sweets        | Mean: ${cluster_data['MntSweetProducts'].mean():,.2f}")
        print(f"  Gold          | Mean: ${cluster_data['MntGoldProds'].mean():,.2f}")
        
        # Purchase channels
        print("\n🛒 PURCHASE CHANNELS:")
        web_purchases = cluster_data['NumWebPurchases'].mean()
        catalog_purchases = cluster_data['NumCatalogPurchases'].mean()
        store_purchases = cluster_data['NumStorePurchases'].mean()
        total_purchases = web_purchases + catalog_purchases + store_purchases
        
        print(f"  Web           | Mean: {web_purchases:.2f} purchases ({web_purchases/total_purchases*100:.1f}%)")
        print(f"  Catalog       | Mean: {catalog_purchases:.2f} purchases ({catalog_purchases/total_purchases*100:.1f}%)")
        print(f"  Store         | Mean: {store_purchases:.2f} purchases ({store_purchases/total_purchases*100:.1f}%)")
        print(f"  Total         | Mean: {total_purchases:.2f} purchases")
        
        # Engagement metrics
        print("\n📱 ENGAGEMENT METRICS:")
        print(f"  Recency       | Mean: {cluster_data['Recency'].mean():.1f} days since last purchase")
        print(f"  Web Visits    | Mean: {cluster_data['NumWebVisitsMonth'].mean():.2f} visits/month")
        print(f"  Complaints    | Total: {cluster_data['Complain'].sum()} complaints")
        
        # Marital status
        print("\n👥 MARITAL STATUS DISTRIBUTION:")
        marital_dist = cluster_data['Marital_Status'].value_counts()
        for status, count in marital_dist.items():
            pct = (count / len(cluster_data)) * 100
            print(f"  {status}: {count} ({pct:.1f}%)")
        
        # Education level
        print("\n🎓 EDUCATION LEVEL DISTRIBUTION:")
        education_dist = cluster_data['Education'].value_counts()
        for education, count in education_dist.items():
            pct = (count / len(cluster_data)) * 100
            print(f"  {education}: {count} ({pct:.1f}%)")
        
        print()
    
    # Generate cluster naming/recommendations
    print("=" * 70)
    print("SEGMENT INSIGHTS & RECOMMENDATIONS")
    print("=" * 70)
    print()
    
    for cluster_id in clusters:
        cluster_data = df_processed[df_processed['Cluster'] == cluster_id]
        avg_spend = cluster_data['TotalSpend'].mean()
        avg_age = cluster_data['Age'].mean()
        avg_income = cluster_data['Income'].mean()
        avg_recency = cluster_data['Recency'].mean()
        
        print(f"\n📌 CLUSTER {cluster_id}:")
        
        # Classify segment
        if avg_spend > df_processed['TotalSpend'].median() and avg_income > df_processed['Income'].median():
            segment_name = "Premium High-Value Segment"
            print(f"   Segment Name: {segment_name}")
            print(f"   Strategy: Focus on exclusive offerings, VIP benefits, and personalized service")
        elif avg_spend < df_processed['TotalSpend'].quantile(0.33):
            segment_name = "Budget-Conscious Segment"
            print(f"   Segment Name: {segment_name}")
            print(f"   Strategy: Offer value packages, promotions, and discounts")
        elif avg_recency > df_processed['Recency'].quantile(0.75):
            segment_name = "At-Risk (Inactive) Segment"
            print(f"   Segment Name: {segment_name}")
            print(f"   Strategy: Re-engagement campaigns, win-back offers, targeted emails")
        else:
            segment_name = "Core Mid-Tier Segment"
            print(f"   Segment Name: {segment_name}")
            print(f"   Strategy: Regular engagement, loyalty programs, cross-selling")
        
        print(f"   Key Characteristics: Avg Age={avg_age:.0f} yrs, Avg Income=${avg_income:,.0f}, Avg Spend=${avg_spend:,.0f}")
    
    print("\n" + "=" * 70)
    print()


# ==================== MAIN WORKFLOW ====================

def main(filepath='data/customer_segmentation.csv'):
    """
    Execute the complete customer segmentation workflow.
    
    Args:
        filepath (str): Path to the customer segmentation CSV file
    """
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  CUSTOMER SEGMENTATION ANALYSIS - COMPLETE PIPELINE  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    # Step 1: Load data
    df = load_data(filepath)
    
    # Step 2: Preprocess
    df_processed = preprocess_data(df)
    
    # Step 3: Normalize features
    X_scaled, scaler, feature_names = normalize_features(df_processed)
    
    # Step 4: EDA
    perform_eda(df_processed)
    
    # Step 5: Find optimal clusters
    inertias, silhouette_scores, optimal_k = find_optimal_clusters(X_scaled, max_k=10)
    
    # Step 6: Perform clustering
    kmeans = perform_clustering(X_scaled, optimal_k)
    
    # Step 7: Visualize clusters
    df_processed = visualize_clusters(X_scaled, kmeans, df_processed)
    
    # Step 8: Profile segments
    profile_segments(df_processed)
    
    # Save clustered data
    df_processed.to_csv(f'{DATA_DIR}/customer_segmentation_with_clusters.csv', index=False)
    print("✓ Saved clustered data: customer_segmentation_with_clusters.csv")
    
    # Print completion message
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  ✓ ANALYSIS COMPLETE!  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("║" + f"  All visualizations saved to: {PLOTS_DIR}/".ljust(68) + "║")
    print("║" + f"  Clustered data saved to: {DATA_DIR}/".ljust(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    return df_processed, kmeans, X_scaled


if __name__ == "__main__":
    # Run the complete pipeline
    df_results, model, X_scaled = main()
