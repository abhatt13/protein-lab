import streamlit as st

st.set_page_config(page_title="Add Protein", page_icon="➕", layout="wide")

st.title("➕ Add New Protein")

if not st.session_state.get('authenticated', False):
    st.warning("Please login to access this page")
    st.stop()

st.markdown("### Enter Protein Information")

with st.form("add_protein_form"):
    col1, col2 = st.columns(2)

    with col1:
        uniprot_id = st.text_input("UniProt ID *")
        name = st.text_input("Protein Name *")
        gene_name = st.text_input("Gene Name")
        organism = st.text_input("Organism *")
        protein_family = st.text_input("Protein Family")

    with col2:
        pdb_id = st.text_input("PDB ID")
        ec_number = st.text_input("EC Number")
        molecular_weight = st.number_input("Molecular Weight (Da)", min_value=0.0)
        subcellular_location = st.text_input("Subcellular Location")

    sequence = st.text_area(
        "Amino Acid Sequence *",
        height=150,
        placeholder="Enter protein sequence in single-letter code"
    )

    function = st.text_area(
        "Function Description",
        height=100,
        placeholder="Describe the protein's biological function"
    )

    keywords = st.text_input(
        "Keywords",
        placeholder="Enter comma-separated keywords"
    )

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        submit = st.form_submit_button("Add Protein", type="primary", use_container_width=True)
    with col2:
        clear = st.form_submit_button("Clear Form", use_container_width=True)

    if submit:
        if not uniprot_id or not name or not sequence or not organism:
            st.error("Please fill in all required fields (*)")
        else:
            st.success(f"Protein '{name}' added successfully!")
            st.info("This will be connected to the API")

    if clear:
        st.rerun()

st.markdown("---")
st.markdown("### Quick Import Options")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### From UniProt")
    uniprot_fetch = st.text_input("Enter UniProt ID to fetch data")
    if st.button("Fetch from UniProt"):
        st.info("UniProt integration coming soon")

with col2:
    st.markdown("#### From PDB")
    pdb_fetch = st.text_input("Enter PDB ID to fetch data")
    if st.button("Fetch from PDB"):
        st.info("PDB integration coming soon")
