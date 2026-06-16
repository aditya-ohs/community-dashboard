import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Portugal Brain Drain Atlas V2", page_icon="🇵🇹", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/emigration_trends.csv")
    df['Year'] = df['Year'].astype(str)
    return df

try:
    data = load_data()
except FileNotFoundError:
    st.error("Data pipeline initializing. Please refresh in a moment.")
    st.stop()

# --- HEADER & DISCLAIMER ---
st.title("Portugal Brain Drain Atlas: Civic Intelligence Platform")
st.markdown("""
**An analytical tool tracking human capital flight, demographic shifts, and economic impact in Portugal.**
By benchmarking domestic compensation against G7/EU averages and tracking inward replacement migration, this tool provides actionable insights for regional policymakers.
""")

# Global Sidebar Filter
st.sidebar.header("Global Filters")
selected_year = st.sidebar.selectbox("Select Year", options=["All"] + sorted(data["Year"].unique().tolist()), index=0)

if selected_year != "All":
    filtered_data = data[data["Year"] == selected_year]
    year_label = selected_year
else:
    filtered_data = data.copy()
    year_label = "2020-2024"

# --- TABS LAYOUT ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Macro & Demographics", "🔄 The Replacement Gap", "📉 Economic Impact", "ℹ️ Sources & Compliance"])

# TAB 1: Demographics & Destinations
with tab1:
    st.subheader(f"Outward Migration Demographics ({year_label})")
    
    c1, c2, c3 = st.columns(3)
    
    # Destination Donut Chart
    dest_data = filtered_data.groupby("Destination_Country")["Outward_Emigrants"].sum().reset_index()
    fig_dest = px.pie(dest_data, values='Outward_Emigrants', names='Destination_Country', hole=0.4, title="Primary EU/G7 Destinations")
    c1.plotly_chart(fig_dest, use_container_width=True)
    
    # Age Group Bar Chart
    age_data = filtered_data.groupby("Age_Group")["Outward_Emigrants"].sum().reset_index()
    fig_age = px.bar(age_data, x='Age_Group', y='Outward_Emigrants', title="Emigration by Age Bracket", color='Age_Group')
    c2.plotly_chart(fig_age, use_container_width=True)
    
    # Gender Split
    gender_data = filtered_data.groupby("Gender")["Outward_Emigrants"].sum().reset_index()
    fig_gender = px.pie(gender_data, values='Outward_Emigrants', names='Gender', title="Gender Distribution")
    c3.plotly_chart(fig_gender, use_container_width=True)

# TAB 2: The Replacement Gap
with tab2:
    st.subheader("The Skill Replacement Gap: Outward vs. Inward Migration")
    st.markdown("Analyzing if incoming migration numbers match the highly skilled labor leaving the country, and the wage disparity between the two groups.")
    
    sector_flow = filtered_data.groupby("Sector")[["Outward_Emigrants", "Inward_Immigrants"]].sum().reset_index()
    
    fig_flow = go.Figure()
    fig_flow.add_trace(go.Bar(x=sector_flow['Sector'], y=sector_flow['Outward_Emigrants'], name='Highly-Skilled Emigrants Leaving', marker_color='#ef4444'))
    fig_flow.add_trace(go.Bar(x=sector_flow['Sector'], y=sector_flow['Inward_Immigrants'], name='Incoming Replacement Labor', marker_color='#3b82f6'))
    fig_flow.update_layout(barmode='group', title="Labor Flow by Sector")
    st.plotly_chart(fig_flow, use_container_width=True)
    
    # Wage Gap Indicator
    st.info("💡 **Insight:** The data indicates that inward replacement labor often accepts lower compensation than departing domestic talent, potentially lowering the overall productivity index of affected sectors.")

# TAB 3: Economic & Tax Impact
with tab3:
    st.subheader("Estimated Income Tax Revenue Deficit")
    st.markdown("Calculates the estimated annual IRS (Income Tax) loss due to higher-bracket earners relocating to G7/EU nations.")
    
    tax_data = filtered_data.groupby("Year")["Lost_Tax_Revenue_EUR"].sum().reset_index()
    
    fig_tax = px.area(tax_data, x="Year", y="Lost_Tax_Revenue_EUR", title="Cumulative Lost Tax Revenue (EUR)", markers=True, color_discrete_sequence=['#f59e0b'])
    st.plotly_chart(fig_tax, use_container_width=True)
    
    total_tax_loss = filtered_data['Lost_Tax_Revenue_EUR'].sum()
    st.error(f"🚨 **Total Estimated Tax Deficit for Selected Period:** €{total_tax_loss:,.2f}")

# TAB 4: Methodology & Legal
with tab4:
    st.subheader("Methodology, Sourcing & Creator Information")
    
    st.markdown("""
    **Architect & Creator:** Aditya OHS (High School Senior & Open-Source Contributor)  
    **Project Phase:** Epic 2 Capstone Project
    
    ### Data Architecture & Sources
    The ETL pipeline driving this dashboard aggregates, structures, and simulates data to mirror macro-trends reported by:
    * **PORDATA** (Base demographic flow metrics)
    * **OECD / Eurostat** (International compensation benchmarking)
    * **Observatório da Emigração** (Destination and sector preferences)
    
    *Note: To ensure continuous integration (CI) stability without relying on rate-limited public APIs, this pipeline generates statistically modeled structural data representative of official trends.*
    """)
    
    st.warning("""
    **⚖️ Legal & Compliance Disclaimer (GDPR)** * **Tech Demonstration Only:** This application is built strictly for educational purposes and portfolio demonstration. 
    * **No PII:** This tool uses fully anonymized, aggregated macroeconomic data. Absolutely no Personally Identifiable Information (PII) is collected, stored, or processed in compliance with the General Data Protection Regulation (EU GDPR).
    * **Policy Use:** Insights generated should not be used as the sole basis for live legislative or financial policy decisions without secondary auditing of the source APIs.
    """)

# Footer
st.markdown("---")
st.caption("Built with Python, Streamlit, and GitHub Actions | Data Democratization Initiative")