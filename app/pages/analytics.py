import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

st.title("📊 Analytics Dashboard")

if not st.session_state.get('authenticated', False):
    st.warning("Please login to access this page")
    st.stop()

st.markdown("### Database Insights and Statistics")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Proteins", "1,234", "+15%")
with col2:
    st.metric("Validated", "987", "+8%")
with col3:
    st.metric("With PDB", "456", "+12%")
with col4:
    st.metric("Organisms", "45", "+3")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Proteins by Organism")
    organism_data = pd.DataFrame({
        "Organism": ["Homo sapiens", "Mus musculus", "E. coli", "S. cerevisiae", "Others"],
        "Count": [450, 320, 180, 140, 144]
    })
    fig = px.pie(organism_data, values="Count", names="Organism", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### Protein Family Distribution")
    family_data = pd.DataFrame({
        "Family": ["Kinase", "Transferase", "Hydrolase", "Oxidoreductase", "Ligase"],
        "Count": [280, 250, 220, 190, 150]
    })
    fig = px.bar(family_data, x="Family", y="Count", color="Count")
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Sequence Length Distribution")
    length_data = pd.DataFrame({
        "Length Range": ["0-100", "100-300", "300-500", "500-1000", "1000+"],
        "Count": [120, 450, 380, 220, 64]
    })
    fig = px.bar(length_data, x="Length Range", y="Count", color="Count")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### Monthly Additions")
    monthly_data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Additions": [45, 52, 48, 67, 71, 58]
    })
    fig = px.line(monthly_data, x="Month", y="Additions", markers=True)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.markdown("### Data Quality Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Complete Records", "892", "72%")
with col2:
    st.metric("Missing Sequences", "12", "1%")
with col3:
    st.metric("Missing Functions", "156", "13%")
with col4:
    st.metric("Duplicates", "3", "0.2%")
with col5:
    st.metric("Quality Score", "8.7/10", "+0.3")
