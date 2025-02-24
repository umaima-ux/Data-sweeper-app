# Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set Up Our App
st.set_page_config(page_title="Data Sweeper", layout='wide')
st.title("Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning & visualization!")

# Upload File
uploaded_files = st.file_uploader("Upload your file (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported File Type: {file_ext}")
            continue  # Skip to the next file

    # ✅ Save last processed file reference
    last_file = file  

    # Display File Information
    st.write(f"**File Name:** {last_file.name}")
    st.write(f"**File Size:** {last_file.size / 1024:.2f} KB")

    # Show Data Preview
    st.write("Preview of the Dataframe:")
    st.dataframe(df.head())

    # Data Cleaning Options
    st.subheader("Data Cleaning Options")

    if st.checkbox(f"Clean Data For {last_file.name}"):
        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"Remove Duplicates from {last_file.name}"):
                df.drop_duplicates(inplace=True)
                st.write("✅ Duplicates Removed!")

        with col2:
            if st.button(f"Fill Missing Values For {last_file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("✅ Missing Values Filled!")

    # ✅ Column Selection
    st.subheader("Select Columns To Keep")
    columns = st.multiselect(f"Choose Columns for {last_file.name}", df.columns.tolist(), default=df.columns.tolist())
    
    if columns:
        df = df[columns]

    # ✅ Data Visualization
    st.subheader("📊 Data Visualizations")
    if st.checkbox(f"Show Visualizations for {last_file.name}"):
        st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

    # ✅ File Conversion Section
    st.subheader("Conversion Options")
    conversion_type = st.radio(f"Convert {last_file.name} to:", ["CSV", "Excel"], key=last_file.name)

    if st.button(f"Convert {last_file.name}"):
        buffer = BytesIO()

        if conversion_type == "CSV":
            df.to_csv(buffer, index=False)
            file_name = last_file.name.replace(file_ext, ".csv")
            mime_type = "text/csv"

        elif conversion_type == "Excel":
            df.to_excel(buffer, index=False)
            file_name = last_file.name.replace(file_ext, ".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        buffer.seek(0)

        # ✅ Download Button
        st.download_button(
            label=f"🚀 Download {last_file.name} as {conversion_type}",
            data=buffer,
            filename=file_name,
            mime=mime_type
        )

    st.success("🎉 All files processed successfully!")
