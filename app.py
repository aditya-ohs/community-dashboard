import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Portugal Brain Drain Atlas", page_icon="🇵🇹", layout="wide")

st.title("Portugal Brain Drain Atlas & OECD Benchmark")
st.markdown("""
This live intelligence dashboard tracks human capital flight from Portugal. By benchmarking domestic compensation against **OECD averages**, policymakers can identify the critical structural deficits driving youth emigration.
*Data updates automatically via GitHub Actions CI/CD pipeline.*
""")

@st.cache_data
def load_data():
    df = pd.read_csv("data/emigration_trends.csv")
    df['Year'] = df['Year'].astype(str)
    return df

try:
    data = load_data()
except FileNotFoundError:
    st.error("Data pipeline running. Please refresh in a moment.")
    st.stop()

# --- POLICY HIGHLIGHT CARDS ---
st.subheader("Macroeconomic Policy Indicators (Latest Year)")
latest_year = data['Year'].max()
latest_data = data[data['Year'] == latest_year]

col1, col2, col3 = st.columns(3)
total_emigrants = latest_data['PT_Emigrants'].sum()
avg_pt_salary = latest_data['PT_Avg_Salary_EUR'].mean()
avg_oecd_salary = latest_data['OECD_Avg_Salary_EUR'].mean()

col1.metric("Total Tracked Emigrants", f"{total_emigrants:,}")
col2.metric("Avg Domestic Salary", f"€{avg_pt_salary:,.0f}")
col3.metric("Avg OECD Benchmark", f"€{avg_oecd_salary:,.0f}", delta=f"-€{(avg_oecd_salary-avg_pt_salary):,.0f} Deficit", delta_color="inverse")

st.markdown("---")

# --- CHARTS ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Emigration Volume by Sector")
    fig_line = px.line(data.sort_values("Year"), x="Year", y="PT_Emigrants", color="Sector", markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

with c2:
    st.subheader("The Wage Gap: Portugal vs. OECD")
    # Using Plotly Graph Objects for a comparative bar chart
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=latest_data['Sector'], y=latest_data['PT_Avg_Salary_EUR'], name='Portugal (EUR)', marker_color='#1f77b4'))
    fig_bar.add_trace(go.Bar(x=latest_data['Sector'], y=latest_data['OECD_Avg_Salary_EUR'], name='OECD Average (EUR)', marker_color='#ff7f0e'))
    fig_bar.update_layout(barmode='group', title=f"Compensation Benchmark ({latest_year})")
    st.plotly_chart(fig_bar, use_container_width=True)

# --- POLICY DIRECTIVE OUTPUT ---
st.markdown("---")
st.subheader("💡 Analytical Policy Directive")
worst_sector = latest_data.loc[latest_data['Salary_Deficit_vs_OECD_Percent'].idxmax()]

st.info(f"""
**CRITICAL FINDING:** The {worst_sector['Sector']} sector currently faces a **{worst_sector['Salary_Deficit_vs_OECD_Percent']}% salary deficit** compared to the OECD average. 
\n**RECOMMENDATION:** To halt structural brain drain, state budget allocations and tax incentives must be urgently redirected to subsidize competitive compensation in the **{worst_sector['Sector']}** sector, as it presents the highest flight risk to primary destinations like {worst_sector['Primary_Destination']}.
""")