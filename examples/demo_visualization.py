from datamop.loader import DataLoader
from datamop.visualization import DataVisualizer


# ==================================================
# Load Dataset
# ==================================================

loader = DataLoader()

df = loader.load(
    "datasets/Titanic-Dataset_Cleaned.csv"
)


# ==================================================
# Create Visualizer
# ==================================================

visualizer = DataVisualizer(
    df,
    output_dir="visualizations/titanic"
)


# ==================================================
# Generate All Charts
# ==================================================

files = visualizer.generate_all()


# ==================================================
# Display Generated Files
# ==================================================

print("\n========== GENERATED FILES ==========")

for file in files:
    print(file)