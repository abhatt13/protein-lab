import streamlit as st
import pandas as pd

st.set_page_config(page_title="Advanced Search", page_icon="🔍", layout="wide")

st.title("🔍 Advanced Search")

if not st.session_state.get('authenticated', False):
    st.warning("Please login to access this page")
    st.stop()

st.markdown("### Search and Filter Proteins")

with st.form("search_form"):
    text_search = st.text_input("Text Search", placeholder="Search by name, UniProt ID, gene name, or keywords")

    col1, col2, col3 = st.columns(3)

    with col1:
        organism = st.text_input("Organism")
        protein_family = st.text_input("Protein Family")

    with col2:
        gene_name = st.text_input("Gene Name")
        min_length = st.number_input("Min Length", min_value=0, value=0)

    with col3:
        ec_number = st.text_input("EC Number")
        max_length = st.number_input("Max Length", min_value=0, value=10000)

    col1, col2, col3 = st.columns(3)

    with col1:
        has_pdb = st.checkbox("Has PDB Structure")

    with col2:
        is_validated = st.checkbox("Validated Only")

    with col3:
        has_ptm = st.checkbox("Has PTMs")

    submit = st.form_submit_button("Search", type="primary", use_container_width=True)

    if submit:
        st.info("Search functionality will be connected to API")

st.markdown("---")

st.markdown("### Search Results")

results_data = pd.DataFrame({
    "UniProt ID": ["P12345", "Q67890"],
    "Name": ["Insulin", "Hemoglobin"],
    "Organism": ["Homo sapiens", "Homo sapiens"],
    "Length": [110, 141],
    "Family": ["Hormone", "Oxygen transport"],
    "PDB": ["1A7F", "1A3N"],
    "Validated": ["✓", "✓"]
})

st.dataframe(results_data, use_container_width=True, hide_index=True)

st.markdown(f"**Found {len(results_data)} proteins**")
