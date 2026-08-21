from datamop.loader import DataLoader
from datamop.correlation import CorrelationAnalyzer


# ==================================================
# Load Dataset
# ==================================================

loader = DataLoader()

df = loader.load(
    "datasets/Titanic-Dataset.csv"
)


# ==================================================
# Create Correlation Analyzer
# ==================================================

analyzer = CorrelationAnalyzer(
    df,
    output_dir="visualizations/correlation"
)


# ==================================================
# Display Report
# ==================================================

analyzer.display_report()


# ==================================================
# Generate Heatmap
# ==================================================

heatmap = analyzer.heatmap()

print("\nHeatmap:")
print(heatmap)


# ==================================================
# Strong Correlations
# ==================================================

print(
    "\nStrong Correlations:"
)

print(
    analyzer.find_strong_correlations()
)