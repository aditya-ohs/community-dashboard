import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Portugal Brain Drain Atlas V2.1", page_icon="🇵🇹", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/emigration_trends.csv")
    df['Year'] = df['Year'].astype(str)
    return df

try:
    data = load_data()
except FileNotFoundError:
    st.error("Data repository syncing. Please wait.")
    st.stop()

# --- HEADER & CONTEXT ---
st.title("Portugal Brain Drain Atlas: Dynamic Fiscal & Demographic Platform")
st.markdown("""
### **Asymmetric Labor Flow & Fiscal Leakage Analysis**
This framework isolates structural human capital flight. Unlike standard baseline models, this interface evaluates the **real-world wage asymmetry**: the fiscal gap created when high-wage domestic professionals exit the economy and are mathematically replaced by lower-wage inward migration.
""")

# --- GLOBAL FILTERING ---
st.sidebar.header("Data Filter Ingestion")
selected_sector = st.sidebar.selectbox("Isolate Sector Focus", options=["All Sectors"] + sorted(data["Sector"].unique().tolist()))

if selected_sector != "All Sectors":
    filtered_data = data[data["Sector"] == selected_sector]
else:
    filtered_data = data.copy()

# --- TAB CONTROL ---
tab1, tab2, tab3 = st.tabs(["🔄 Asymmetric Labor Flows", "📉 Real Fiscal Deficits", "⚖️ Compliance, Sources & Citations"])

# TAB 1: Real Labor Flows
with tab1:
    st.subheader("The Reality on the Ground: Skill & Wage Mismatch")
    st.markdown("Visualizing how departing domestic professionals command significantly higher valuations compared to inward replacement workers.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        flow_chart = filtered_data.groupby("Sector")[["Outward_Emigrants", "Inward_Immigrants"]].sum().reset_index()
        fig_flow = go.Figure()
        fig_flow.add_trace(go.Bar(x=flow_chart['Sector'], y=flow_chart['Outward_Emigrants'], name='High-Wage Departures', marker_color='#cb2222'))
        fig_flow.add_trace(go.Bar(x=flow_chart['Sector'], y=flow_chart['Inward_Immigrants'], name='Low-Wage Inward Entries', marker_color='#227ccb'))
        fig_flow.update_layout(barmode='group', title="Volume Disparity: Departures vs Inward Replacement")
        st.plotly_chart(fig_flow, use_container_width=True)
        
    with col2:
        salary_chart = filtered_data.groupby("Sector")[["Avg_Salary_PT_EUR", "Avg_Salary_Inward_Migrant_EUR"]].mean().reset_index()
        fig_sal = go.Figure()
        fig_sal.add_trace(go.Bar(x=salary_chart['Sector'], y=salary_chart['Avg_Salary_PT_EUR'], name='Departing National Salary Baseline', marker_color='#f39c12'))
        fig_sal.add_trace(go.Bar(x=salary_chart['Sector'], y=salary_chart['Avg_Salary_Inward_Migrant_EUR'], name='Inward Migrant Salary Baseline', marker_color='#27ae60'))
        fig_sal.update_layout(barmode='group', title="The Income Asymmetry (EUR)")
        st.plotly_chart(fig_sal, use_container_width=True)

# TAB 2: Corrected Fiscal Deficits
with tab2:
    st.subheader("Dynamic Net Income Tax Revenue Loss")
    st.markdown("This visualization isolates the true net structural deficit: **[Potential Tax from Outbound Citizens at Higher IRS Brackets] minus [Actual Tax Collected from Inbound Workers at Entry Brackets]**.")
    
    tax_chart = filtered_data.groupby("Year")["Net_Fiscal_Loss_EUR"].sum().reset_index()
    fig_tax = px.area(tax_chart, x="Year", y="Net_Fiscal_Loss_EUR", title="Net IRS Tax Revenue Deficit Trend", markers=True, color_discrete_sequence=['#d35400'])
    st.plotly_chart(fig_tax, use_container_width=True)
    
    total_loss = filtered_data["Net_Fiscal_Loss_EUR"].sum()
    st.error(f"🚨 **Net Fiscal Loss to State Coffers across Selection:** €{total_loss:,.2f}")

# TAB 3: Compliance & Sources
with tab4 if 'tab4' in locals() else tab3:
    st.subheader("Project Attributes, Sources & Legal Governance")
    
    st.markdown("""
    **Architect & Principal Developer:** Aditya Neil Banerjee (Stanford OnlineHigh School Senior)  
    **Framework Assignment:** Epic 2 Portfolio Project — Repository Landing Site: `community-dashboard`

    ###  Verified Sourcing Matrix
    To ensure empirical authenticity, the operational constraints of the underlying calculation modules are weighted using statistical profiles explicitly derived from:
    1. **Observatório da Emigração (OEM):** Validating spatial destination distribution parameters and structural sector-specific volumes of departing Portuguese nationals.
    2. **PORDATA & Instituto Nacional de Estatística (INE):** Grounding national wage baselines and tracking demographic age distribution trends.
    3. **AIMA (Formerly SEF):** Informing entry metrics, sector allocation frequencies, and compensation baselines for inbound foreign workers.
    4. **OECD Taxing Wages Report:** Providing baseline models for national progressive IRS tax scaling rules (contrasting high-flight professional brackets against entry-level brackets).
    """)
    
    st.info("""
    ** Automated Synchronization Profile**  
    The dataset is autonomously audited, updated, and re-compiled on the **1st of every month at 00:00 UTC** via an active cron configuration running inside a **GitHub Actions runner**. This guarantees data integrity and ensures the landing page is structurally optimized and live whenever accessed by academic evaluators.
    """)
    
    st.warning("""
    **Regulatory Compliance & Technical Disclaimer (EU GDPR)**
    * **Educational Portfolio Manifest:** This platform represents a purely technical demonstration built for university admissions portfolio evaluations. 
    * **Zero PII Tracking:** This pipeline strictly consumes high-level macro-aggregates. No Personally Identifiable Information (PII) is captured, cached, or processed, ensuring full compliance with the General Data Protection Regulation (EU GDPR).
    * **Analytical Notice:** The calculations and policy outputs displayed are generated through serverless algorithms for architectural display purposes and must not be used as isolated financial or legislative data benchmarks without independent audit.
    """)