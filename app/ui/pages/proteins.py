import streamlit as st
import pandas as pd

st.set_page_config(page_title="Proteins", page_icon="🧬", layout="wide")

st.title("🧬 Protein Database")

if not st.session_state.get('authenticated', False):
    st.warning("Please login to access this page")
    st.stop()

st.markdown("### Browse and Manage Proteins")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Proteins", "0")
with col2:
    st.metric("Validated", "0")
with col3:
    st.metric("With PDB", "0")
with col4:
    st.metric("This Month", "0")

st.markdown("---")

search_col, filter_col = st.columns([2, 1])

with search_col:
    search_query = st.text_input("🔍 Search proteins", placeholder="Search by name, UniProt ID, or gene name")

with filter_col:
    filter_validated = st.selectbox("Filter", ["All", "Validated Only", "Unvalidated"])

sample_data = pd.DataFrame({
    "ID": [1, 2, 3],
    "UniProt ID": ["P12345", "Q67890", "R11223"],
    "Name": ["Insulin", "Hemoglobin", "Actin"],
    "Organism": ["Homo sapiens", "Homo sapiens", "Mus musculus"],
    "Length": [110, 141, 375],
    "Family": ["Hormone", "Oxygen transport", "Structural"],
    "Validated": ["✓", "✓", "✗"]
})

st.dataframe(
    sample_data,
    use_container_width=True,
    hide_index=True
)

selected_protein = st.selectbox("Select a protein to view details", sample_data["Name"].tolist())

if selected_protein:
    st.markdown("### Protein Details")

    tab1, tab2, tab3, tab4 = st.tabs(["Info", "Sequence", "History", "Actions"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**UniProt ID:** P12345")
            st.markdown("**Name:** Insulin")
            st.markdown("**Gene:** INS")
            st.markdown("**Organism:** Homo sapiens")
        with col2:
            st.markdown("**Length:** 110 aa")
            st.markdown("**MW:** 5808 Da")
            st.markdown("**Family:** Hormone")
            st.markdown("**PDB ID:** 1A7F")

    with tab2:
        st.code("""
MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN
        """, language="text")

    with tab3:
        st.markdown("**Version History**")
        st.markdown("- v1: Initial creation (2024-01-15)")

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
