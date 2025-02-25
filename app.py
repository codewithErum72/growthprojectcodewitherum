import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper",layout="wide")

#custom css
st.markdown(
    """
    <style>
    .stApp{
        background-color: black;
        color: white;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Data Sweeper")
st.write("Transform your files between CSV and Excel formats. Upload your file and download the transformed file.")

#file uploader

uploaded_file = st.file_uploader("Choose a file accepts CSV or Excel", type=["csv","xlsx"], accept_multiple_files=(True))

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Invalid file format. Please upload a CSV or Excel file: {file_ext}")
            continue

        #file details
        st.write("preview the haed of the Dataframe")
        st.write(df.head())

        #data cleaning options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"remove duplicates from the file {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅Duplicates removed")

            with col2:
                if st.button(f"fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values filled")

        st.subheader("select columns to keep")
        columns = st.multiselect(f"choice columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        #data visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"show visualizations for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

            #conversion options
            st.subheader("Conversion Options")
            conversion_type = st.radio(f"convert {file.name} to", ["CSV", "Excel"])
            if st.button(f"convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"Click here to download {file_name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
st.success("all files processed successfully💥🎉")
                                


                
                







