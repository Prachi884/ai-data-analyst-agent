from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# Page config — dark theme
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for that dashboard feel
st.markdown("""
<style>
    .metric-card { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# AI setup
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-3.6-flash")

# Session state
if "df" not in st.session_state:
    st.session_state.df = None

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.write("AI-powered data analyst. Chat with your CSV files!")
    st.write("---")
    st.write("**Features:**")
    st.write("• CSV upload + sample data")
    st.write("• AI conversational Q&A")
    st.write("• Multi-chart dashboard")
    st.write("• Auto insights report")
    st.write("---")
    st.write("Built with Python, Streamlit, and Google Gemini.")

# Header
st.title("🤖 AI Data Analyst Agent")
st.write("Upload a CSV file **or** try the sample data to explore an AI-powered dashboard.")

st.divider()

# Upload + sample data
uploaded_file = st.file_uploader("📁 Upload your CSV file", type="csv")

if uploaded_file is not None:
    st.session_state.df = pd.read_csv(uploaded_file)

with st.expander("👀 No CSV handy? Try sample sales data"):
    st.write("Click below to load demo data so you can see how the app works.")
    if st.button("📊 Load sample sales data"):
        sample_data = {
            "Month": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
            "Sales": [12000, 15000, 18000, 14000, 22000, 25000, 23000, 28000, 30000, 32000, 38000, 45000],
            "Region": ["North","North","South","East","South","East","North","South","East","North","South","East"],
            "Customers": [120, 150, 180, 140, 220, 250, 230, 280, 300, 320, 380, 450],
            "Satisfaction": [4.2, 4.5, 4.0, 3.8, 4.7, 4.6, 4.4, 4.8, 4.5, 4.6, 4.7, 4.9]
        }
        st.session_state.df = pd.DataFrame(sample_data)
        st.rerun()

# Main app — only when we have data
if st.session_state.df is not None:
    df = st.session_state.df
    
    st.success(f"✅ Data loaded! {len(df)} rows × {len(df.columns)} columns")
    
    # ----- DATA PREVIEW -----
    with st.expander("📋 View raw data preview", expanded=False):
        st.dataframe(df.head(20), use_container_width=True)
    
    # ----- KPI DASHBOARD -----
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    
    if numeric_cols:
        st.subheader("📊 Key Metrics")
        # Show up to 4 KPI cards
        kpi_cols_to_show = numeric_cols[:4]
        kpi_layout = st.columns(len(kpi_cols_to_show))
        for col_name, col_slot in zip(kpi_cols_to_show, kpi_layout):
            total = df[col_name].sum()
            avg = df[col_name].mean()
            col_slot.metric(
                label=col_name,
                value=f"{total:,.0f}" if abs(total) > 100 else f"{total:.2f}",
                delta=f"avg: {avg:.2f}"
            )
    
    st.divider()
    
    # ----- MULTI-CHART DASHBOARD -----
    st.subheader("📈 Dashboard Charts")
    
    if numeric_cols:
        # Row 1: Distribution + Category breakdown
        row1_col1, row1_col2 = st.columns(2)
        
        with row1_col1:
            first_num = numeric_cols[0]
            fig1 = px.histogram(
                df, x=first_num, 
                title=f"Distribution of {first_num}",
                color_discrete_sequence=["#636EFA"],
                template="plotly_dark"
            )
            fig1.update_layout(height=350)
            st.plotly_chart(fig1, use_container_width=True)
        
        with row1_col2:
            if cat_cols and numeric_cols:
                top_data = (
                    df.groupby(cat_cols[0])[numeric_cols[0]]
                    .sum()
                    .nlargest(10)
                    .reset_index()
                )
                fig2 = px.bar(
                    top_data, x=cat_cols[0], y=numeric_cols[0],
                    title=f"{numeric_cols[0]} by {cat_cols[0]}",
                    color=numeric_cols[0],
                    color_continuous_scale="Viridis",
                    template="plotly_dark"
                )
                fig2.update_layout(height=350)
                st.plotly_chart(fig2, use_container_width=True)
            else:
                fig2 = px.box(
                    df, y=numeric_cols[0],
                    title=f"Spread of {numeric_cols[0]}",
                    template="plotly_dark"
                )
                fig2.update_layout(height=350)
                st.plotly_chart(fig2, use_container_width=True)
        
        # Row 2: Trend line (full width)
        if len(df) > 3:
            first_num = numeric_cols[0]
            fig3 = px.line(
                df.reset_index(), y=first_num,
                title=f"📉 {first_num} Trend (across rows)",
                markers=True,
                template="plotly_dark"
            )
            fig3.update_layout(height=300)
            st.plotly_chart(fig3, use_container_width=True)
        
        # Row 3: Correlation heatmap (only if 2+ numeric cols)
        if len(numeric_cols) >= 2:
            corr = df[numeric_cols].corr()
            fig4 = px.imshow(
                corr, text_auto=".2f", aspect="auto",
                color_continuous_scale="RdBu_r",
                title="🔗 Correlation Heatmap — how columns relate",
                template="plotly_dark"
            )
            fig4.update_layout(height=400)
            st.plotly_chart(fig4, use_container_width=True)
    
    st.divider()
    
    # ----- AI Q&A -----
    st.subheader("💬 Ask questions about your data")
    question = st.text_input("Type your question:", placeholder="e.g. What's the highest sales month?")
    
    if question:
        with st.spinner("🤔 AI is analyzing..."):
            try:
                data_context = f"""You are a data analyst. Dataset summary:
Columns: {list(df.columns)}
Sample rows: {df.head(15).to_string()}
Total rows: {len(df)}

User question: {question}

Answer concisely with specific numbers from the data."""
                response = model.generate_content(data_context)
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.divider()
    
    # ----- AI INSIGHTS REPORT -----
    st.subheader("🔮 AI Insights Report")
    st.write("Click below to get a full AI-written executive summary.")
    
    if st.button("✨ Generate full insights report"):
        with st.spinner("📝 AI is writing your report (~15 seconds)..."):
            try:
                stats = df.describe(include="all").to_string()
                prompt = f"""You are a senior data analyst. Write a professional insights report.

Dataset statistics:
{stats}

Total rows: {len(df)}
Columns: {list(df.columns)}

Write 4 sections (use markdown):
1. **Overview** — what kind of data
2. **Key Findings** — 3-5 bullets with specific numbers
3. **Anomalies / Things to watch**
4. **Recommendations** — what to do next

Be concise but insightful."""
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")