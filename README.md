# DataMop

## Automatic Data Science Engine for Python

DataMop is an automated Python library designed to simplify common
data preparation, analysis, cleaning, profiling, visualization,
correlation analysis, and reporting tasks.

Instead of manually performing multiple data-processing operations,
users can provide a dataset to DataMop and allow the library to
automatically execute a complete data-processing pipeline.

---

# 📌 About DataMop

DataMop provides a simple interface for automating common data science
preprocessing and exploratory data analysis tasks.

The library is designed around the idea:

```text
Input Dataset
      ↓
Automatic Analysis
      ↓
Data Profiling
      ↓
Data Cleaning
      ↓
Missing Value Handling
      ↓
Duplicate Detection
      ↓
Outlier Detection
      ↓
Datatype Handling
      ↓
Smart Visualization
      ↓
Correlation Analysis
      ↓
HTML Report
      ↓
Cleaned Dataset + Logs + Charts

⚙️ How DataMop Works

                    DATAMOP
                       │
                       ▼
                 LOAD DATASET
                       │
                       ▼
                 DATA ANALYSIS
                       │
                       ▼
                 COLUMN PROFILING
                       │
                       ▼
                 DATA CLEANING
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Missing       Duplicate      Outlier
       Values        Handling      Detection
          │            │            │
          └────────────┼────────────┘
                       ▼
                 DATATYPE HANDLING
                       │
                       ▼
              SMART VISUALIZATION
                       │
              ┌────────┴────────┐
              ▼                 ▼
       Column Charts       Correlation
              │                 │
              └────────┬────────┘
                       ▼
                  HTML REPORT
                       │
                       ▼
                  FINAL OUTPUT





📦 Installation
Install from a Built Wheel

DataMop can be installed from the generated wheel package:

pip install datamop-0.2.0-py3-none-any.whl

Development Installation
Clone the repository:

git clone <repository-url>

Move into the project:

cd datamop


Install the project in editable mode:

pip install -e .


⚡ Quick Start

The simplest way to use DataMop is through its automatic cleaning
pipeline.

import datamop


result = datamop.auto_clean(
    "dataset.csv"
)

DataMop automatically performs the processing pipeline and generates
the corresponding output files.

🧪 Quick Start with an Output Directory

You can specify where DataMop should store the generated results.

import datamop


result = datamop.auto_clean(
    "dataset.csv",
    output_dir="datamop_output"
)
The output directory contains the cleaned dataset, visualizations,
report, and cleaning log.



📂 Input Data

DataMop is designed to process tabular datasets.

Example CSV input:

import datamop


result = datamop.auto_clean(
    "Titanic-Dataset.csv"
)

The dataset is loaded and converted into a pandas DataFrame before
being processed by the DataMop pipeline.


🔄 Automatic Processing Pipeline

When auto_clean() is executed, DataMop performs the following
major stages.

1. Dataset Loading

The loader reads the input dataset and creates a pandas DataFrame.

The loading stage provides information such as:

File name
Number of rows
Number of columns
Dataset structure


2. Dataset Analysis

The analyzer examines the dataset and provides information about:

Dataset shape
Numerical columns
Categorical columns
Missing values
Duplicate records
Numerical statistics
Categorical statistics
Data quality information
3. Column Profiling

DataMop profiles individual columns and classifies them according to
their characteristics.

Supported classifications include:

ID
numeric_continuous
numeric_discrete
binary
categorical
high_cardinality
datetime

For example:

PassengerId → ID
Age         → numeric_continuous
Pclass      → numeric_discrete
Sex         → binary
Embarked    → categorical
Name        → high_cardinality

This classification is used by the Smart Visualization Engine.

🧹 Data Cleaning

DataMop provides an automatic cleaning pipeline that performs several
common data preparation operations.

The cleaning pipeline includes:

Datatype Conversion
        ↓
Missing Value Handling
        ↓
Duplicate Removal
        ↓
Outlier Processing

Cleaning operations are recorded in the cleaning log.

❓ Missing Value Handling

DataMop can detect missing values in datasets.

The missing-value module provides functionality for:

Detecting missing values
Calculating missing-value counts
Calculating missing-value percentages
Identifying columns containing missing values
Filling numerical values
Filling categorical values
Dropping rows
Dropping columns
Automatic missing-value handling
🔁 Duplicate Detection

DataMop can identify duplicate records in a dataset.

The duplicate handling module provides functionality for:

Detecting duplicates
Counting duplicate records
Calculating duplicate percentage
Retrieving duplicate records
Removing duplicate records
Removing duplicates based on selected columns
📈 Outlier Detection

DataMop supports two major statistical approaches for outlier
detection.

IQR Method

The Interquartile Range method calculates:

Q1
Q3
IQR
Lower Bound
Upper Bound

The standard IQR rule is used to identify observations outside the
acceptable range.

Z-Score Method

The Z-score method calculates the standardized distance of a value
from the mean.

DataMop provides both IQR-based and Z-score-based outlier detection.

Example concept:

IQR Outlier Detection
        OR
Z-Score Outlier Detection
🔄 Datatype Handling

DataMop includes automatic datatype analysis and conversion.

The datatype module can identify and handle:

Numerical columns
Categorical columns
Boolean columns
Datetime columns
Numeric candidates
Datetime candidates

It also provides automatic datatype conversion functionality.

📊 Smart Visualization Engine

One of the major features of DataMop is its Smart Visualization
Engine.

Instead of generating the same chart for every column, DataMop
examines the detected column type and selects an appropriate
visualization.

Visualization Strategy
Column Type	Visualization
Continuous Numerical	Histogram + Boxplot
Discrete Numerical	Bar Chart
Binary	Bar Chart
Categorical	Bar Chart
High Cardinality	Skipped
ID Column	Skipped

Example:

CONTINUOUS NUMERICAL


Age  → Histogram + Boxplot
Fare → Histogram + Boxplot




DISCRETE NUMERICAL


Survived → Bar Chart
Pclass   → Bar Chart
SibSp    → Bar Chart
Parch    → Bar Chart




BINARY


Sex → Bar Chart




CATEGORICAL


Cabin    → Bar Chart
Embarked → Bar Chart




HIGH CARDINALITY


Name   → Skipped
Ticket → Skipped




ID COLUMNS


PassengerId → Skipped

This approach helps prevent meaningless visualizations for columns
such as identifiers and high-cardinality text fields.

🔗 Correlation Analysis

DataMop automatically generates correlation analysis for suitable
numerical columns.

A correlation matrix is generated and visualized as a heatmap.

The correlation functionality also avoids treating identified ID
columns as meaningful analytical variables.

Example output:

correlation_heatmap.png
📄 HTML Reports

DataMop automatically generates an HTML report after processing.

Example:

Titanic-Dataset_report.html

The report provides a human-readable summary of the processed dataset
and the analysis/cleaning results.

📝 Cleaning Log

DataMop maintains a cleaning log during the cleaning process.

Example:

cleaning_log.csv

The log provides a record of cleaning-related operations performed
during the pipeline.

This makes the cleaning process more transparent and easier to review.

💾 Output Structure

After running DataMop, the output directory is organized into
different sections.

Example:

datamop_output/
│
├── cleaned_data/
│   └── Titanic-Dataset_cleaned.csv
│
├── visualizations/
│   └── Titanic-Dataset/
│       ├── histogram_Age.png
│       ├── boxplot_Age.png
│       ├── histogram_Fare.png
│       ├── boxplot_Fare.png
│       ├── bar_Survived.png
│       ├── bar_Pclass.png
│       ├── bar_Sex.png
│       └── correlation_heatmap.png
│
├── reports/
│   └── Titanic-Dataset_report.html
│
└── cleaning_log.csv

The exact number of generated charts depends on the dataset and the
column classifications.

🔌 Public API

DataMop provides a public API for interacting with its main
functionality.

The main automated entry point is:

import datamop


result = datamop.auto_clean(
    "dataset.csv"
)

The public API is designed to hide the internal complexity of the
individual modules while allowing users to perform common operations
through a simple interface.

🧩 Main Modules

DataMop is organized into independent modules.

Loader

Responsible for loading datasets.

datamop/loader.py
Analyzer

Responsible for dataset-level analysis.

datamop/analyzer.py
Cleaner

Coordinates data-cleaning operations.

datamop/cleaner.py
Missing Values

Handles missing-value detection and processing.

datamop/missing_values.py
Duplicates

Handles duplicate detection and removal.

datamop/duplicates.py
Outliers

Provides statistical outlier detection.

datamop/outliers.py
Datatype

Handles datatype detection and conversion.

datamop/datatype.py
Profiler

Profiles individual columns and classifies their types.

datamop/profiler.py
Visualization

Generates automatic and smart visualizations.

datamop/visualization.py
Correlation

Generates correlation matrices and heatmaps.

datamop/correlation.py
Pipeline

Coordinates the complete DataMop processing workflow.

datamop/pipeline.py
Report

Generates the HTML processing report.

datamop/report.py
Validation

Validates DataMop inputs and configuration.

datamop/validation.py
Exceptions

Contains DataMop-specific exception handling.

datamop/exceptions.py
Logger

Handles cleaning and processing logs.

datamop/logger.py
📁 Project Structure

The current project structure is:

datamop/
│
├── datamop/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── cleaner.py
│   ├── correlation.py
│   ├── dashboard.py
│   ├── datatype.py
│   ├── duplicates.py
│   ├── exceptions.py
│   ├── loader.py
│   ├── logger.py
│   ├── missing_values.py
│   ├── outliers.py
│   ├── pipeline.py
│   ├── profiler.py
│   ├── report.py
│   ├── validation.py
│   └── visualization.py
│
├── tests/
│   ├── test_analyzer.py
│   ├── test_cleaner.py
│   ├── test_correlation.py
│   ├── test_datatype.py
│   ├── test_duplicates.py
│   ├── test_loader.py
│   ├── test_missing_values.py
│   ├── test_outliers.py
│   ├── test_pipeline.py
│   ├── test_profiler.py
│   ├── test_public_api.py
│   ├── test_validation.py
│   └── test_visualization.py
│
├── examples/
│
├── datasets/
│
├── docs/
│
├── dist/
│
├── README.md
├── requirements.txt
├── pyproject.toml
├── setup.py
├── LICENSE
└── .gitignore
🧪 Testing

DataMop uses pytest for automated testing.

To run the complete test suite:

pytest -v

The current development test suite contains 26 tests.

Current status:

26 passed

The tests cover major components including:

Analyzer
Cleaner
Correlation
Datatype handling
Duplicate handling
Loader
Missing values
Outlier detection
Pipeline
Profiler
Public API
Validation
Visualization
📦 Package Information

Current DataMop version:

0.2.0

DataMop is packaged using modern Python packaging configuration
through:

pyproject.toml

The project can generate:

datamop-0.2.0-py3-none-any.whl
datamop-0.2.0.tar.gz

Build the package with:

python -m build
📚 Dependencies

DataMop currently uses the following main Python packages:

pandas
numpy
matplotlib
seaborn
openpyxl

Development and testing:

pytest
build
🧪 Example: Titanic Dataset

A complete example using the Titanic dataset:

import datamop


result = datamop.auto_clean(
    r"E:\datasets\Titanic-Dataset.csv",
    output_dir="datamop_output"
)


print("Cleaned file:")
print(result["cleaned_file"])


print("Report:")
print(result["report"])


print("Cleaning log:")
print(result["cleaning_log"])


print("Charts generated:")
print(len(result["visualizations"]))

A typical DataMop execution follows:

============================================================
                    DATAMOP
          AUTOMATIC DATA SCIENCE ENGINE
============================================================


[1/5] Loading dataset...


[2/5] Analyzing dataset...


[3/5] Cleaning dataset...


[4/5] Generating visualizations...


[5/5] Generating report...


============================================================
             DATAMOP PROCESSING COMPLETED
============================================================
📊 Example Smart Visualization Plan

For a Titanic-style dataset, DataMop can automatically determine a
visualization plan such as:

CONTINUOUS NUMERICAL
--------------------
Age  → Histogram + Boxplot
Fare → Histogram + Boxplot




DISCRETE NUMERICAL
------------------
Survived → Bar Chart
Pclass   → Bar Chart
SibSp    → Bar Chart
Parch    → Bar Chart




BINARY
------
Sex → Bar Chart




CATEGORICAL
-----------
Cabin    → Bar Chart
Embarked → Bar Chart




HIGH CARDINALITY
----------------
Name   → Skipped
Ticket → Skipped




ID COLUMNS
----------
PassengerId → Skipped

This allows DataMop to generate useful visualizations automatically
without requiring the user to manually select charts for every column.

⚠️ Current Limitations

DataMop is currently focused on automated processing of tabular data.

Some datasets may require domain-specific cleaning rules that cannot
be safely inferred automatically.

Automatic cleaning and visualization decisions should therefore be
reviewed when working with important or domain-specific datasets.

The Smart Visualization Engine selects visualizations based on
automatically detected column characteristics.

🔮 Future Enhancements

Planned improvements for future versions include:

Additional input file formats
Interactive dashboard support
Advanced statistical analysis
More visualization types
Custom visualization configuration
User-defined cleaning rules
Advanced outlier handling
Machine learning-assisted data analysis
Automated feature engineering
Command-line interface
Configuration files for custom pipelines
More comprehensive documentation
Additional test coverage
PyPI publication
Documentation website
Improved HTML reports
Interactive reports
Dataset comparison functionality
🛠️ Development

To contribute to DataMop:

Clone the repository.
git clone <repository-url>
Enter the project directory.
cd datamop
Install the project in editable mode.
pip install -e .
Install development dependencies.
pip install pytest
Run the test suite.
pytest -v
Create your feature branch.
git checkout -b feature/your-feature
Implement and test your changes.
Commit your changes.
git add .
git commit -m "Add your feature"
Push your branch.
git push origin feature/your-feature
🤝 Contributing

Contributions are welcome.

Before submitting changes:

Ensure existing functionality is not broken.
Add tests for new functionality.
Run the complete pytest suite.
Keep modules focused on their individual responsibilities.
Follow clear Python coding practices.
Update documentation when adding user-facing functionality.
👥 Contributors
DataMop Development Team
Srivigneshwar — Project Lead
Rahul — Team Member
Shurthy — Team Member
Sanjana — Team Member
Akshithaa — Team Member

Update the names and responsibilities above if your final team
structure differs.

📄 License

DataMop is distributed under the license specified in the project's
LICENSE file.

See:

LICENSE

for the complete license terms.

⭐ Project Vision

DataMop aims to make common data science preprocessing and exploratory
analysis tasks easier by providing an automated, reusable, and
extensible Python library.

The long-term goal is to allow users to move from:

Raw Dataset

to:

Clean Dataset
+
Analysis
+
Visualizations
+
Correlation
+
Cleaning Log
+
HTML Report

with minimal manual effort.

🚀 DataMop at a Glance
                     ┌─────────────────┐
                     │   RAW DATASET   │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │     LOADER      │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │    ANALYZER     │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │    PROFILER     │
                     └────────┬────────┘
                              │
                              ▼
              ┌──────────────────────────────┐
              │       CLEANING ENGINE        │
              │                              │
              │ Missing Values               │
              │ Duplicates                   │
              │ Outliers                     │
              │ Datatypes                    │
              └──────────────┬───────────────┘
                             │
                             ▼
                  ┌────────────────────┐
                  │ SMART VISUALIZATION│
                  └──────────┬─────────┘
                             │
                             ▼
                  ┌────────────────────┐
                  │    CORRELATION     │
                  └──────────┬─────────┘
                             │
                             ▼
                  ┌────────────────────┐
                  │   REPORT ENGINE    │
                  └──────────┬─────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │              FINAL OUTPUT              │
        │                                        │
        │  Cleaned Dataset                       │
        │  Visualizations                        │
        │  Correlation Heatmap                   │
        │  HTML Report                           │
        │  Cleaning Log                          │
        └────────────────────────────────────────┘
DataMop

Automatic Data Science Engine for Python

Version: 0.2.0

Built to automate repetitive data preparation, analysis, cleaning,
visualization, and reporting workflows.