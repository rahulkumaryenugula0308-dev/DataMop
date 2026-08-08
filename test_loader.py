from datamop.loader import load_file


# =========================================================
# GIVE FILE PATH HERE
# =========================================================

file_path = r"C:\Users\Ajay\Downloads\Messy_Sales_Data_for_Analysis.xlsx"


# =========================================================
# AUTOMATICALLY LOAD FILE
# =========================================================

df = load_file(file_path)


# =========================================================
# DISPLAY RESULT
# =========================================================

print("\nLoaded Dataset:")
print("Shape:", df.shape)

print("\nFirst 5 Rows:")
print(df.head())