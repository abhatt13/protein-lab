import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Proteins", page_icon="🧬", layout="wide")

st.title("🧬 Protein Database")

if not st.session_state.get('authenticated', False):
    st.warning("Please login to access this page")
    st.stop()

API_URL = "http://localhost:8000"
headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.markdown("### Browse and Manage Proteins")

try:
    response = requests.get(f"{API_URL}/api/proteins/", headers=headers)
    if response.status_code == 200:
        proteins = response.json()
        total = len(proteins)
        validated = len([p for p in proteins if p.get('is_validated')])
        with_pdb = len([p for p in proteins if p.get('pdb_id')])

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Proteins", total)
        with col2:
            st.metric("Validated", validated)
        with col3:
            st.metric("With PDB", with_pdb)
        with col4:
            st.metric("This Month", 0)
    else:
        st.error("Failed to fetch proteins")
        proteins = []
except Exception as e:
    st.error(f"Error: {str(e)}")
    proteins = []

st.markdown("---")

search_col, filter_col = st.columns([2, 1])

with search_col:
    search_query = st.text_input("🔍 Search proteins", placeholder="Search by name, UniProt ID, or gene name")

with filter_col:
    filter_validated = st.selectbox("Filter", ["All", "Validated Only", "Unvalidated"])

if proteins:
    df_data = {
        "ID": [p['id'] for p in proteins],
        "UniProt ID": [p.get('uniprot_id', 'N/A') for p in proteins],
        "Name": [p['name'] for p in proteins],
        "Organism": [p.get('organism', 'N/A') for p in proteins],
        "Length": [p.get('length', 0) for p in proteins],
        "Family": [p.get('protein_family', 'N/A') for p in proteins],
        "Validated": ["✓" if p.get('is_validated') else "✗" for p in proteins]
    }

    df = pd.DataFrame(df_data)

    if search_query:
        mask = df.apply(lambda row: search_query.lower() in ' '.join(row.astype(str)).lower(), axis=1)
        df = df[mask]

    if filter_validated == "Validated Only":
        df = df[df["Validated"] == "✓"]
    elif filter_validated == "Unvalidated":
        df = df[df["Validated"] == "✗"]

    st.dataframe(df, use_container_width=True, hide_index=True)

    selected_protein = st.selectbox("Select a protein to view details", df["Name"].tolist() if len(df) > 0 else [])
else:
    st.info("No proteins in database")
    selected_protein = None

if selected_protein and proteins:
    protein = next((p for p in proteins if p['name'] == selected_protein), None)

    if protein:
        st.markdown("### Protein Details")

        tab1, tab2, tab3, tab4 = st.tabs(["Info", "Sequence", "History", "Actions"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**UniProt ID:** {protein.get('uniprot_id', 'N/A')}")
                st.markdown(f"**Name:** {protein.get('name', 'N/A')}")
                st.markdown(f"**Gene:** {protein.get('gene_name', 'N/A')}")
                st.markdown(f"**Organism:** {protein.get('organism', 'N/A')}")
            with col2:
                st.markdown(f"**Length:** {protein.get('length', 'N/A')} aa")
                st.markdown(f"**MW:** {protein.get('molecular_weight', 'N/A')} Da")
                st.markdown(f"**Family:** {protein.get('protein_family', 'N/A')}")
                st.markdown(f"**PDB ID:** {protein.get('pdb_id', 'N/A')}")

            if protein.get('function'):
                st.markdown("**Function:**")
                st.markdown(protein['function'])

        with tab2:
            if protein.get('sequence'):
                st.code(protein['sequence'], language="text")
            else:
                st.info("No sequence available")

        with tab3:
            try:
                version_response = requests.get(f"{API_URL}/api/proteins/{protein['id']}/versions", headers=headers)
                if version_response.status_code == 200:
                    versions = version_response.json()
                    st.markdown("**Version History**")
                    for v in versions:
                        st.markdown(f"- v{v['version_number']}: {v.get('change_description', 'No description')} ({v.get('changed_at', 'N/A')[:10]})")
                else:
                    st.info("No version history available")
            except:
                st.info("Could not load version history")

        with tab4:
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Edit"):
                    st.info("Edit functionality coming soon")
            with col2:
                if st.button("Export"):
                    st.info("Export functionality coming soon")
            with col3:
                if st.button("Delete", type="primary"):
                    st.warning("Delete requires admin privileges")
