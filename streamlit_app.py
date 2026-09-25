import os
from pathlib import Path

import pandas as pd
import streamlit as st

from datamop import clean, visualize


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="DataMop - Data Cleaning Engine",
    page_icon="🧹",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🧹 DataMop")

st.caption(
    "Automated Data Cleaning, Analysis, Visualization and Reporting"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Cleaning Settings")

remove_duplicates = st.sidebar.checkbox(
    "Remove duplicates",
    value=True
)

handle_missing = st.sidebar.checkbox(
    "Handle missing values",
    value=True
)

convert_datatypes = st.sidebar.checkbox(
    "Convert data types",
    value=True
)

remove_outliers = st.sidebar.checkbox(
    "Remove outliers",
    value=False
)

outlier_method = st.sidebar.selectbox(
    "Outlier method",
    ["iqr", "zscore"]
)


# ============================================================
# MISSING VALUE SETTINGS
# ============================================================

st.sidebar.subheader("Missing Value Settings")

missing_threshold = st.sidebar.slider(
    "Missing-value threshold (%)",
    min_value=0,
    max_value=100,
    value=40,
    step=5
)


# ============================================================
# TEXT STANDARDIZATION
# ============================================================

st.sidebar.subheader("Text Standardization")

standardize_text = st.sidebar.checkbox(
    "Standardize text values",
    value=True
)

text_case = st.sidebar.selectbox(
    "Text case",
    ["lower", "upper", "title"],
    disabled=not standardize_text
)

normalize_categories = st.sidebar.checkbox(
    "Normalize category labels",
    value=True,
    disabled=not standardize_text
)


# ============================================================
# FILE UPLOAD
# ============================================================

st.header("📂 Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_file(file):
    """Load CSV or Excel file."""

    if file.name.lower().endswith(".csv"):
        return pd.read_csv(file)

    if file.name.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(file)

    raise ValueError("Unsupported file format.")


def show_metrics(df, title):

    st.subheader(title)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Rows",
            df.shape[0]
        )

    with col2:
        st.metric(
            "Columns",
            df.shape[1]
        )

    with col3:
        st.metric(
            "Missing Values",
            int(df.isna().sum().sum())
        )

    with col4:
        st.metric(
            "Duplicate Rows",
            int(df.duplicated().sum())
        )


def show_cleaning_log(log):

    st.subheader("📋 Cleaning Log")

    if not log:
        st.info(
            "No cleaning operations were recorded."
        )
        return

    if isinstance(log, pd.DataFrame):

        st.dataframe(
            log,
            use_container_width=True,
            hide_index=True
        )

        return

    if isinstance(log, list):

        try:

            log_df = pd.DataFrame(log)

            if not log_df.empty:

                st.dataframe(
                    log_df,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "No cleaning operations were recorded."
                )

        except Exception:

            for item in log:
                st.write(item)

        return

    st.write(log)


def show_visualizations():

    """
    Find and display visualization files generated
    by DataMop.
    """

    st.header("📊 DataMop Visualizations")

    possible_directories = [
        Path("datamop_output"),
        Path("visualizations"),
        Path("test_visual_output"),
        Path("data_tools_project/visualizations")
    ]

    image_files = []

    for directory in possible_directories:

        if not directory.exists():
            continue

        for pattern in [
            "*.png",
            "*.jpg",
            "*.jpeg",
            "*.webp"
        ]:

            image_files.extend(
                directory.glob(pattern)
            )

    # Remove duplicate paths
    image_files = list(
        dict.fromkeys(image_files)
    )

    if not image_files:

        st.warning(
            "No visualization images were generated."
        )

        st.info(
            "The DataMop visualization engine did not "
            "return any image files for this dataset."
        )

        return

    # Sort for stable display
    image_files.sort(
        key=lambda path: path.name.lower()
    )

    st.success(
        f"Found {len(image_files)} visualization(s)."
    )

    # Display two visualizations per row
    for index in range(
        0,
        len(image_files),
        2
    ):

        columns = st.columns(2)

        for column_index in range(2):

            file_index = index + column_index

            if file_index >= len(image_files):
                break

            image_path = image_files[file_index]

            with columns[column_index]:

                st.subheader(
                    image_path.stem.replace(
                        "_",
                        " "
                    ).title()
                )

                st.image(
                    str(image_path),
                    use_container_width=True
                )


def show_before_after(
    original,
    cleaned
):

    st.header("🔄 Before vs After")

    comparison = pd.DataFrame(
        {
            "Metric": [
                "Rows",
                "Columns",
                "Missing Values",
                "Duplicate Rows"
            ],
            "Before": [
                original.shape[0],
                original.shape[1],
                int(
                    original.isna()
                    .sum()
                    .sum()
                ),
                int(
                    original.duplicated()
                    .sum()
                )
            ],
            "After": [
                cleaned.shape[0],
                cleaned.shape[1],
                int(
                    cleaned.isna()
                    .sum()
                    .sum()
                ),
                int(
                    cleaned.duplicated()
                    .sum()
                )
            ]
        }
    )

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# NO FILE
# ============================================================

if uploaded_file is None:

    st.info(
        "👆 Upload a CSV or Excel file to start."
    )

    st.markdown(
        """
        ### What DataMop can do

        🔍 Detect missing values

        🧹 Handle missing values

        ♻️ Remove duplicate rows

        🔢 Convert data types

        📝 Standardize text

        🏷️ Normalize categories

        📊 Detect/remove outliers

        📈 Generate visualizations

        📋 Create cleaning logs

        📥 Download cleaned data
        """
    )

    st.stop()


# ============================================================
# LOAD DATA
# ============================================================

try:

    dataframe = load_file(
        uploaded_file
    )

except Exception as error:

    st.error(
        f"❌ Unable to load file: {error}"
    )

    st.stop()


# ============================================================
# ORIGINAL DATA
# ============================================================

st.header("📊 Original Dataset")

show_metrics(
    dataframe,
    "Dataset Overview"
)

with st.expander(
    "👀 Preview Original Data",
    expanded=True
):

    st.dataframe(
        dataframe.head(100),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# COLUMN INFORMATION
# ============================================================

with st.expander(
    "🔎 Column Information"
):

    column_info = pd.DataFrame(
        {
            "Column": dataframe.columns,
            "Data Type": [
                str(dtype)
                for dtype in dataframe.dtypes
            ],
            "Missing Count": [
                int(
                    dataframe[column]
                    .isna()
                    .sum()
                )
                for column in dataframe.columns
            ],
            "Missing %": [
                round(
                    dataframe[column]
                    .isna()
                    .mean()
                    * 100,
                    2
                )
                for column in dataframe.columns
            ],
            "Unique Values": [
                int(
                    dataframe[column]
                    .nunique(
                        dropna=True
                    )
                )
                for column in dataframe.columns
            ]
        }
    )

    st.dataframe(
        column_info,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# SETTINGS SUMMARY
# ============================================================

st.header("⚙️ Current Settings")

setting_col1, setting_col2 = st.columns(2)

with setting_col1:

    st.write(
        f"**Missing threshold:** "
        f"{missing_threshold}%"
    )

    st.write(
        f"**Remove duplicates:** "
        f"{remove_duplicates}"
    )

    st.write(
        f"**Handle missing values:** "
        f"{handle_missing}"
    )

    st.write(
        f"**Convert data types:** "
        f"{convert_datatypes}"
    )

with setting_col2:

    st.write(
        f"**Remove outliers:** "
        f"{remove_outliers}"
    )

    st.write(
        f"**Outlier method:** "
        f"{outlier_method}"
    )

    st.write(
        f"**Text standardization:** "
        f"{standardize_text}"
    )

    st.write(
        f"**Text case:** "
        f"{text_case}"
    )


# ============================================================
# CLEAN BUTTON
# ============================================================

st.header("🧹 Run DataMop")

if st.button(
    "🚀 Clean Dataset",
    type="primary",
    use_container_width=True
):

    # --------------------------------------------------------
    # Clear previous output
    # --------------------------------------------------------

    output_directory = Path(
        "datamop_output"
    )

    output_directory.mkdir(
        exist_ok=True
    )

    # --------------------------------------------------------
    # CLEAN
    # --------------------------------------------------------

    with st.spinner(
        "DataMop is cleaning your dataset..."
    ):

        try:

            result = clean(
                data=dataframe,
                remove_duplicates=remove_duplicates,
                handle_missing=handle_missing,
                remove_outliers=remove_outliers,
                convert_datatypes=convert_datatypes,
                outlier_method=outlier_method,
                missing_threshold=missing_threshold,
                standardize_text=standardize_text,
                text_case=text_case,
                normalize_categories=normalize_categories,
                output_dir="datamop_output"
            )

        except Exception as error:

            st.error(
                f"❌ Data cleaning failed: {error}"
            )

            st.exception(error)

            st.stop()


    # --------------------------------------------------------
    # GET CLEANED DATA
    # --------------------------------------------------------

    cleaned_dataframe = result.get(
        "cleaned_dataframe"
    )

    if cleaned_dataframe is None:

        cleaned_dataframe = result.get(
            "dataframe"
        )

    if cleaned_dataframe is None:

        st.error(
            "❌ DataMop did not return a cleaned DataFrame."
        )

        st.stop()


    # --------------------------------------------------------
    # SAVE SESSION STATE
    # --------------------------------------------------------

    st.session_state[
        "original_dataframe"
    ] = dataframe.copy()

    st.session_state[
        "cleaned_dataframe"
    ] = cleaned_dataframe.copy()

    st.session_state[
        "clean_result"
    ] = result

    st.session_state[
        "cleaning_log"
    ] = result.get(
        "cleaning_log",
        []
    )


    # --------------------------------------------------------
    # VISUALIZATIONS
    # --------------------------------------------------------

    with st.spinner(
        "Generating DataMop visualizations..."
    ):

        try:

            visualization_result = visualize(
                cleaned_dataframe,
                output_dir="datamop_output"
            )

            st.session_state[
                "visualization_result"
            ] = visualization_result

        except Exception as error:

            st.session_state[
                "visualization_result"
            ] = None

            st.warning(
                f"Visualizations could not be generated: "
                f"{error}"
            )


    st.success(
        "✅ DataMop processing completed successfully!"
    )


# ============================================================
# RESULTS
# ============================================================

if (
    "cleaned_dataframe"
    in st.session_state
):

    original_dataframe = (
        st.session_state[
            "original_dataframe"
        ]
    )

    cleaned_dataframe = (
        st.session_state[
            "cleaned_dataframe"
        ]
    )

    cleaning_log = (
        st.session_state.get(
            "cleaning_log",
            []
        )
    )


    # ========================================================
    # CLEANED DATA
    # ========================================================

    st.header("✨ Cleaned Dataset")

    show_metrics(
        cleaned_dataframe,
        "Cleaned Dataset Overview"
    )


    # ========================================================
    # BEFORE AFTER
    # ========================================================

    show_before_after(
        original_dataframe,
        cleaned_dataframe
    )


    # ========================================================
    # CLEANED PREVIEW
    # ========================================================

    with st.expander(
        "👀 Preview Cleaned Data",
        expanded=True
    ):

        st.dataframe(
            cleaned_dataframe.head(100),
            use_container_width=True,
            hide_index=True
        )


    # ========================================================
    # CLEANING LOG
    # ========================================================

    show_cleaning_log(
        cleaning_log
    )


    # ========================================================
    # VISUALIZATIONS
    # ========================================================

    show_visualizations()


    # ========================================================
    # DOWNLOAD
    # ========================================================

    st.header("📥 Download")

    csv_data = (
        cleaned_dataframe
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        label="⬇️ Download Cleaned CSV",
        data=csv_data,
        file_name="datamop_cleaned_data.csv",
        mime="text/csv",
        use_container_width=True
    )


    # ========================================================
    # OUTPUT FILES
    # ========================================================

    output_directory = Path(
        "datamop_output"
    )

    if output_directory.exists():

        with st.expander(
            "📁 DataMop Output Files"
        ):

            output_files = list(
                output_directory.iterdir()
            )

            if output_files:

                for file in output_files:

                    st.write(
                        f"📄 {file.name}"
                    )

            else:

                st.info(
                    "No output files found."
                )


    # ========================================================
    # FINAL MESSAGE
    # ========================================================

    st.success(
        "🎉 DataMop cleaning, analysis and visualization "
        "process completed."
    )