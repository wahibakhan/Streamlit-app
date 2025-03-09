import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# App Title
st.title("📊 Simple Data Dashboard")

# Upload CSV File
uploaded_file = st.file_uploader("📂 Upload a CSV file", type="csv")

if uploaded_file:
    # Read CSV File
    df = pd.read_csv(uploaded_file)

    # Show Data Preview
    st.subheader("🔍 Data Preview")
    st.write(df.head())

    # Show Data Summary
    st.subheader("📊 Data Summary")
    st.write(df.describe())

    # Filter Data
    st.subheader("🎯 Filter Data")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select column to filter", columns)
    unique_values = df[selected_column].dropna().unique()
    selected_value = st.selectbox("Select value", unique_values)

    filtered_df = df[df[selected_column] == selected_value]
    st.write(filtered_df)

    # Plot Data
    st.subheader("📈 Data Visualization")
    chart_type = st.radio("Select Chart Type", ["Line Chart", "Bar Chart", "Histogram"])

    x_column = st.selectbox("Select X-axis column", columns)
    y_column = st.selectbox("Select Y-axis column", columns)

    if st.button("Generate Chart"):
        if chart_type == "Line Chart":
            st.line_chart(filtered_df.set_index(x_column)[y_column])
        elif chart_type == "Bar Chart":
            st.bar_chart(filtered_df.set_index(x_column)[y_column])
        elif chart_type == "Histogram":
            fig, ax = plt.subplots()
            ax.hist(df[y_column].dropna(), bins=20)
            st.pyplot(fig)

    # Word Cloud Generator
    st.subheader("☁️ Word Cloud (for text data)")
    text_columns = [col for col in df.columns if df[col].dtype == "object"]
    if text_columns:
        text_column = st.selectbox("Select text column", text_columns)
        if st.button("Generate Word Cloud"):
            text = " ".join(df[text_column].dropna().astype(str))
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)
    else:
        st.warning("No text column found in the dataset.")

else:
    st.write("📌 Please upload a CSV file to get started.")

