import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Toronto Ferry Tickets", layout="wide")

st.title("🚢 Toronto Island Ferry Ticket Analytics")

try:
    # 1. Load the data
    df = pd.read_csv('ferry_data.csv')

    # 2. Convert Timestamp to real date format
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # 3. Sidebar Filters
    st.sidebar.header("Data Filters")
    date_range = st.sidebar.date_input("Select Date Range", 
                                       [df['Timestamp'].min(), df['Timestamp'].max()])

    # 4. Key Metrics
    col1, col2, col3 = st.columns(3)
    total_sales = df['Sales Count'].sum()
    total_redemptions = df['Redemption Count'].sum()
    efficiency = (total_redemptions / total_sales) * 100 if total_sales > 0 else 0

    col1.metric("Total Tickets Sold", f"{total_sales:,}")
    col2.metric("Total Redemptions", f"{total_redemptions:,}")
    col3.metric("Redemption Rate", f"{efficiency:.1f}%")

    # 5. Interactive Chart
    st.subheader("Sales vs. Redemptions Over Time")
    fig = px.line(df, x='Timestamp', y=['Sales Count', 'Redemption Count'], 
                  labels={'value': 'Count', 'variable': 'Type'},
                  title="Ferry Ticket Activity")
    st.plotly_chart(fig, use_container_width=True)

    # 6. Raw Data Preview
    if st.checkbox("Show Data Table"):
        st.dataframe(df)

except FileNotFoundError:
    st.error("Make sure 'ferry_data.csv' is in your 'saved' folder!")