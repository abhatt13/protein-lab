import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Advanced Search", page_icon="🔍", layout="wide")

st.title("🔍 Advanced Search")

if not st.session_state.get('authenticated', False):
    st.warning("Please login to access this page")
    st.stop()

API_URL = "http://localhost:8000"
headers = {"Authorization": f"Bearer {st.session_state.token}"}

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

st.markdown("---")

st.markdown("### Search Results")

if submit or 'search_results' not in st.session_state:
    try:
        params = {}
        if text_search:
            params['query'] = text_search
        if organism:
            params['organism'] = organism
        if protein_family:
            params['protein_family'] = protein_family
        if gene_name:
            params['gene_name'] = gene_name
        if min_length > 0:
            params['min_length'] = min_length
        if max_length < 10000:
            params['max_length'] = max_length
        if has_pdb:
            params['has_pdb'] = True
        if is_validated:
            params['is_validated'] = True

        response = requests.get(f"{API_URL}/api/proteins/", headers=headers, params=params)

        if response.status_code == 200:
            results = response.json()
            st.session_state.search_results = results
        else:
            st.error("Search failed")
            results = []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        results = []
else:
    results = st.session_state.get('search_results', [])

if results:
    results_data = pd.DataFrame({
        "UniProt ID": [p.get('uniprot_id', 'N/A') for p in results],
        "Name": [p['name'] for p in results],
        "Organism": [p.get('organism', 'N/A') for p in results],
        "Length": [p.get('length', 0) for p in results],
        "Family": [p.get('protein_family', 'N/A') for p in results],
        "PDB": [p.get('pdb_id', 'N/A') for p in results],
        "Validated": ["✓" if p.get('is_validated') else "✗" for p in results]
    })

    st.dataframe(results_data, use_container_width=True, hide_index=True)
    st.markdown(f"**Found {len(results)} proteins**")
else:
    st.info("No results. Use the search form above to find proteins.")
