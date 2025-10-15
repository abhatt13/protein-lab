import streamlit as st
import pandas as pd

st.set_page_config(page_title="Export Data", page_icon="📥", layout="wide")

st.title("📥 Export Data")

if not st.session_state.get('authenticated', False):
    st.warning("Please login to access this page")
    st.stop()

st.markdown("### Export Protein Data")

tab1, tab2 = st.tabs(["Export Proteins", "Export Settings"])

with tab1:
    st.markdown("#### Select Data to Export")

    export_option = st.radio(
        "Export",
        ["All Proteins", "Filtered Selection", "Specific Proteins"],
        horizontal=True
    )

    if export_option == "Filtered Selection":
        col1, col2, col3 = st.columns(3)
        with col1:
            organism_filter = st.multiselect("Organism", ["Homo sapiens", "Mus musculus", "E. coli"])
        with col2:
            family_filter = st.multiselect("Family", ["Kinase", "Transferase", "Hydrolase"])
        with col3:
            validated_filter = st.checkbox("Validated only")

    elif export_option == "Specific Proteins":
        protein_ids = st.text_area(
            "Enter protein IDs (comma-separated)",
            placeholder="P12345, Q67890, R11223"
        )

    st.markdown("---")
    st.markdown("#### Export Format")

    format_option = st.selectbox(
        "Select Format",
        ["FASTA", "CSV", "Excel", "JSON", "GenBank", "XML"]
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Include Fields:**")
        include_sequence = st.checkbox("Sequence", value=True)
        include_function = st.checkbox("Function", value=True)
        include_structure = st.checkbox("Structure Info", value=True)
        include_metadata = st.checkbox("Metadata", value=True)

    with col2:
        st.markdown("**Options:**")
        compress = st.checkbox("Compress as ZIP", value=False)
        include_versions = st.checkbox("Include version history", value=False)
        include_audit = st.checkbox("Include audit logs", value=False)

    st.markdown("---")

    if st.button("Generate Export", type="primary", use_container_width=True):
        with st.spinner("Generating export file..."):
            st.success("Export file generated successfully!")

            if format_option == "FASTA":
                example_content = """>sp|P12345|INSULIN_HUMAN Insulin
MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"""
                st.download_button(
                    "Download FASTA",
                    example_content,
                    "proteins_export.fasta",
                    "text/plain"
                )
            elif format_option == "CSV":
                sample_df = pd.DataFrame({
                    "uniprot_id": ["P12345"],
                    "name": ["Insulin"],
                    "organism": ["Homo sapiens"]
                })
                st.download_button(
                    "Download CSV",
                    sample_df.to_csv(index=False),
                    "proteins_export.csv",
                    "text/csv"
                )

with tab2:
    st.markdown("#### Export Preferences")

    st.markdown("**Default Format:**")
    default_format = st.selectbox("Preferred export format", ["FASTA", "CSV", "JSON"])

    st.markdown("**Default Fields:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.checkbox("UniProt ID", value=True, key="default_uniprot")
        st.checkbox("Name", value=True, key="default_name")
    with col2:
        st.checkbox("Sequence", value=True, key="default_seq")
        st.checkbox("Organism", value=True, key="default_org")
    with col3:
        st.checkbox("Function", value=False, key="default_func")
        st.checkbox("Structure", value=False, key="default_struct")

    if st.button("Save Preferences"):
        st.success("Export preferences saved!")

st.markdown("---")
st.markdown("### Recent Exports")

recent_exports = pd.DataFrame({
    "Date": ["2024-10-15", "2024-10-12"],
    "Format": ["FASTA", "CSV"],
    "Records": [1234, 567],
    "Size": ["2.4 MB", "890 KB"]
})

st.dataframe(recent_exports, use_container_width=True, hide_index=True)
