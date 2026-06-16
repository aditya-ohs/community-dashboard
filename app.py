import pandas as pd
import plotly.express as px
import streamlit as st

# Set the page configuration for a clean presentation.
st.set_page_config(
    page_title="Community Data Dashboard",
    page_icon="📊",
    layout="wide",
)

# Title and introduction section.
st.title("Community Dashboard: Local Data Insights")
st.markdown(
    """
    This dashboard helps local residents explore the key trends and patterns in our community dataset.
    Understanding this information supports better planning, stronger local services, and more informed decisions.
    """
)

# Load the local CSV data file.
# The file is expected to be in the same folder as app.py or at a relative path that matches.
DATA_PATH = "data.csv"

@st.cache_data
def load_data(path):
    """Load the CSV into a pandas DataFrame and parse any date-like columns."""
    df = pd.read_csv(path)

    # Attempt to parse any column with a name containing date or year.
    for col in df.columns:
        if "date" in col.lower() or "year" in col.lower():
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
            except Exception:
                pass

    return df

# Read the data once and reuse the cached result.
data = load_data(DATA_PATH)

# Show a warning if the data file cannot be read or contains no rows.
if data.empty:
    st.warning("The data file is empty or could not be loaded. Please check `data.csv`.")
    st.stop()

# Sidebar controls for filtering the dataset.
st.sidebar.header("Filter the data")

# Detect potential year or date columns for filtering.
date_columns = [col for col in data.columns if "date" in col.lower() or "year" in col.lower()]
selected_date_column = date_columns[0] if date_columns else None

if selected_date_column:
    # If there is a date/year column, use it to populate a year selector.
    data["_year"] = data[selected_date_column].dt.year
    available_years = sorted(data["_year"].dropna().unique())
    selected_year = st.sidebar.selectbox("Select a Year", options=available_years)
    filtered_data = data[data["_year"] == selected_year]
else:
    # If no date/year column exists, use the full dataset.
    filtered_data = data.copy()
    selected_year = None

# Detect numeric columns to build a slider filter.
numeric_columns = filtered_data.select_dtypes(include=["number"]).columns.tolist()
selected_numeric_column = numeric_columns[0] if numeric_columns else None

if selected_numeric_column:
    min_value = float(filtered_data[selected_numeric_column].min())
    max_value = float(filtered_data[selected_numeric_column].max())
    default_value = float(filtered_data[selected_numeric_column].median())

    numeric_threshold = st.sidebar.slider(
        f"Filter by {selected_numeric_column}",
        min_value=min_value,
        max_value=max_value,
        value=(min_value, max_value),
    )

    filtered_data = filtered_data[
        (filtered_data[selected_numeric_column] >= numeric_threshold[0])
        & (filtered_data[selected_numeric_column] <= numeric_threshold[1])
    ]
else:
    st.sidebar.info("No numeric columns found for metric filtering.")

# If the dataset includes a categorical column, select the first one for comparison.
category_columns = [
    col
    for col in filtered_data.columns
    if filtered_data[col].dtype == object or filtered_data[col].dtype.name == "category"
]
selected_category_column = category_columns[0] if category_columns else None

# Main page layout: two charts side by side.
col1, col2 = st.columns(2)

# First chart: line or scatter trend over time.
with col1:
    st.subheader("Trend Over Time")

    if selected_date_column and selected_numeric_column:
        # Build a line chart using the selected year/date column and the numeric metric.
        trend_data = filtered_data.dropna(subset=[selected_date_column, selected_numeric_column])
        if not trend_data.empty:
            fig_line = px.line(
                trend_data,
                x=selected_date_column,
                y=selected_numeric_column,
                title=f"{selected_numeric_column} Trend by {selected_date_column}",
                markers=True,
            )
            fig_line.update_layout(hovermode="x unified")
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("No trend data is available for the selected filters.")
    elif selected_numeric_column:
        # Fallback line chart by index if no date/year column exists.
        fig_line = px.line(
            filtered_data,
            y=selected_numeric_column,
            title=f"{selected_numeric_column} Trend (Index-based)",
            markers=True,
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Add numeric and date columns to generate a trend chart.")

# Second chart: bar chart comparing categories.
with col2:
    st.subheader("Category Comparison")
    if selected_category_column and selected_numeric_column:
        bar_data = (
            filtered_data.groupby(selected_category_column)[selected_numeric_column]
            .mean()
            .reset_index()
            .sort_values(by=selected_numeric_column, ascending=False)
        )
        fig_bar = px.bar(
            bar_data,
            x=selected_category_column,
            y=selected_numeric_column,
            title=f"Average {selected_numeric_column} by {selected_category_column}",
            labels={selected_category_column: selected_category_column, selected_numeric_column: f"Average {selected_numeric_column}"},
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    elif selected_category_column:
        st.info("Numeric columns are needed to create a category comparison chart.")
    else:
        st.info("No categorical columns found for a bar chart.")

# Display the filtered data preview at the bottom.
st.markdown("---")
st.subheader("Raw Data Preview")
st.write(
    "Below is the filtered dataset preview. Use the sidebar controls to narrow the data before exporting or inspecting it."
)
st.dataframe(filtered_data.reset_index(drop=True))
