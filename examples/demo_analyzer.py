from datamop.loader import DataLoader
from datamop.analyzer import DataAnalyzer


# Load dataset
loader = DataLoader()

df = loader.load(
    "datasets/Titanic-Dataset-selected-columns.csv"
)


# Analyze dataset
analyzer = DataAnalyzer(df)

analyzer.display_report()