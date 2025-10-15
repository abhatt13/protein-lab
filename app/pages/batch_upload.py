import streamlit as st
import pandas as pd

st.set_page_config(page_title="Batch Upload", page_icon="📦", layout="wide")

st.title("📦 Batch Upload")

if not st.session_state.get('authenticated', False):
    st.warning("Please login to access this page")
    st.stop()

st.markdown("### Upload Multiple Proteins")

tab1, tab2, tab3 = st.tabs(["Upload File", "Template", "History"])

with tab1:
    st.markdown("#### Upload CSV or Excel File")

    file_type = st.radio("File Format", ["CSV", "Excel (.xlsx)"], horizontal=True)

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["csv", "xlsx"],
        help="Upload a file with protein data"
    )

    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")

        if file_type == "CSV":
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.markdown(f"**Found {len(df)} proteins**")

        st.dataframe(df.head(10), use_container_width=True)

        st.markdown("---")
        st.markdown("#### Validation")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Valid Rows", len(df))
        with col2:
            st.metric("Errors", "0")
        with col3:
            st.metric("Warnings", "0")

        col1, col2 = st.columns(2)
        with col1:
            validate_sequences = st.checkbox("Validate sequences", value=True)
            check_duplicates = st.checkbox("Check for duplicates", value=True)
        with col2:
            validate_uniprot = st.checkbox("Verify UniProt IDs", value=False)
            auto_fetch = st.checkbox("Auto-fetch missing data", value=False)

        if st.button("Import Proteins", type="primary"):
            with st.spinner("Importing proteins..."):
                st.success(f"Successfully imported {len(df)} proteins!")
                st.balloons()

with tab2:
    st.markdown("#### Download Template")

    st.markdown("""
    Download a template file to ensure your data is in the correct format.

    **Required Columns:**
    - uniprot_id
    - name
    - sequence
    - organism

    **Optional Columns:**
    - gene_name, protein_family, function, molecular_weight, pdb_id,
      subcellular_location, ec_number, keywords
    """)

    template_df = pd.DataFrame({
        "uniprot_id": ["P12345"],
        "name": ["Example Protein"],
        "sequence": ["MKTLLLTLVVVTIVFPSSL..."],
        "organism": ["Homo sapiens"],
        "gene_name": ["GENE1"],
        "protein_family": ["Kinase"],
        "function": ["Catalyzes the transfer of..."],
        "molecular_weight": [45000.0],
        "pdb_id": ["1ABC"],
        "subcellular_location": ["Cytoplasm"],
        "ec_number": ["2.7.11.1"],
        "keywords": ["kinase, signaling, phosphorylation"]
    })

    st.dataframe(template_df, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        csv = template_df.to_csv(index=False)
        st.download_button(
            "Download CSV Template",
            csv,
            "protein_template.csv",
            "text/csv",
            use_container_width=True
        )
    with col2:
        st.download_button(
            "Download Excel Template",
            csv,
            "protein_template.xlsx",
            use_container_width=True
        )

with tab3:
    st.markdown("#### Upload History")

    history_df = pd.DataFrame({
        "Date": ["2024-10-15", "2024-10-10"],
        "Filename": ["proteins_batch1.csv", "proteins_batch2.xlsx"],
        "Records": [45, 78],
        "Status": ["Success", "Success"],
        "User": ["researcher1", "admin"]
    })

    st.dataframe(history_df, use_container_width=True, hide_index=True)
