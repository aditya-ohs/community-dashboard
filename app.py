import pandas as pd
import plotly.express as px
import streamlit as st

# Set the page configuration for a clean presentation.
st.set_page_config(
    page_title="Portugal Brain Drain Atlas",
    page_icon="🇵🇹",
    layout="wide",
)

# Title and introduction section.
st.title("Portugal Brain Drain Atlas (2018-2025)")
st.markdown(
    """
    This dashboard tracks the emigration of highly skilled professionals from Portugal. 
    By visualizing destination countries, affected sectors, and salary disparities, we can better understand the economic pressures driving youth emigration and structural asymmetries.
    """
)

# Load the local CSV data file.
DATA_PATH = "data/emigration_trends.csv"

@st.cache_data
def load_data(path):
    """Load the CSV into a pandas DataFrame and parse any date-like columns."""
    df = pd.read_csv(path)
    # Convert 'Year' back to string/object so it doesn't parse as a full datetime with months/days
    df['Year'] = df['Year'].astype(str)
    return df

# Read the data once and reuse the cached result.
data = load_data(DATA_PATH)

# Show a warning if the data file cannot be read or contains no rows.
if data.empty:
    st.warning("The data file is empty or could not be loaded. Please check your data folder.")
    st.stop()

# Sidebar controls for filtering the dataset.
st.sidebar.header("Filter the data")

# Year Filter
available_years = ["All"] + sorted(data["Year"].unique().tolist())
selected_year = st.sidebar.selectbox("Select a Year", options=available_years)

if selected_year != "All":
    filtered_data = data[data["Year"] == selected_year]
else:
    filtered_data = data.copy()

# Sector Filter
available_sectors = ["All"] + sorted(filtered_data["Sector"].unique().tolist())
selected_sector = st.sidebar.selectbox("Select a Sector", options=available_sectors)

if selected_sector != "All":
    filtered_data = filtered_data[filtered_data["Sector"] == selected_sector]

# Main page layout: two charts side by side.
col1, col2 = st.columns(2)

# First chart: line or scatter trend over time.
with col1:
    st.subheader("Emigration Trends Over Time")
    
    # We want to group by Year and Sector to see the lines clearly
    trend_data = filtered_data.groupby(["Year", "Sector"])["Emigrants"].sum().reset_index()
    
    # Sort by year so the line chart connects properly
    trend_data = trend_data.sort_values(by="Year")
    
    fig_line = px.line(
        trend_data,
        x="Year",
        y="Emigrants",
        color="Sector",
        title="Number of Emigrants by Sector",
        markers=True,
    )
    st.plotly_chart(fig_line, use_container_width=True)

# Second chart: bar chart comparing categories.
with col2:
    st.subheader("Economic Pull Factors")
    
    # We want to show the Salary Multiplier by Destination Country
    bar_data = filtered_data.groupby("Primary_Destination")["Avg_Salary_Multiplier"].mean().reset_index()
    
    fig_bar = px.bar(
        bar_data,
        x="Primary_Destination",
        y="Avg_Salary_Multiplier",
        title="Average Salary Multiplier by Destination",
        labels={"Primary_Destination": "Destination Country", "Avg_Salary_Multiplier": "Salary Multiplier (x higher)"},
        color="Primary_Destination"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Display the filtered data preview at the bottom.
st.markdown("---")
st.subheader("Raw Data Preview")
st.write(
    "Below is the filtered dataset preview. Use the sidebar controls to narrow the data before exporting or inspecting it."
)
st.dataframe(filtered_data.reset_index(drop=True))