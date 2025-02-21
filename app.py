#Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="💹 Data Sweeper", layout="wide")
st.title("💹 Data Sweeper")
st.write("Data Sweeper is a user-friendly web app for transforming CSV and Excel files. With built-in data cleaning and visualization tools, it simplifies tasks like removing duplicates, handling missing values, and formatting data for analysis. 🚀📊")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read File
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # File Information
        file_size = len(file.getvalue()) / 1024  # Convert to KB
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file_size:.2f} KB")

        # Show Preview
        st.write("Preview the Head of the Data Frame")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader(f"☢️ Data Cleaning Options - {file.name}")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Values Filled")

        # Column Selection
        st.subheader(f"📉 Select Columns for {file.name}")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader(f"📊 Data Visualization - {file.name}")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.line_chart(df.select_dtypes(include='number').iloc[:, :2])

        # File Conversion
        st.subheader(f"💿 Conversion Options - {file.name}")
        conversion_type = st.radio(
            f"Convert {file.name} to:",
            ["CSV", "Excel"],
            key=file.name
        )

        # **Move button inside the loop**
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()

            # Ensure file_name is defined before conditions
            new_file_name = file.name
            mime_type = "text/plain"  # Default MIME type to avoid NameError

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False, encoding='utf-8')
                new_file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                new_file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)  # Reset buffer before downloading

            # Download Button
            st.download_button(
                label=f"Download {new_file_name}",
                data=buffer,
                file_name=new_file_name,
                mime=mime_type
            )

            st.success(f"✅ {new_file_name} processed successfully!")
