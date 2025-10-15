import streamlit as st
import streamlit.components.v1 as components
import requests
import py3Dmol

st.set_page_config(page_title="3D Structure Viewer", page_icon="🎨", layout="wide")

st.title("🎨 3D Protein Structure Viewer")

if not st.session_state.get('authenticated', False):
    st.warning("Please login to access this page")
    st.stop()

st.markdown("### Visualize Protein Structures")

col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("#### Settings")

    pdb_source = st.radio("Structure Source", ["From Database", "Upload PDB", "Fetch from RCSB"])

    if pdb_source == "From Database":
        protein_select = st.selectbox("Select Protein", ["Insulin (1A7F)", "Hemoglobin (1A3N)", "Lysozyme (1LYZ)"])
    elif pdb_source == "Upload PDB":
        uploaded_file = st.file_uploader("Upload PDB file", type=["pdb"])
    else:
        pdb_id = st.text_input("Enter PDB ID", placeholder="1A7F")
        if st.button("Fetch Structure"):
            st.info("Fetching from RCSB PDB...")

    st.markdown("---")
    st.markdown("#### Display Options")

    style = st.selectbox("Style", ["Cartoon", "Stick", "Sphere", "Surface", "Line"])
    color_scheme = st.selectbox("Color", ["Spectrum", "Chain", "Secondary Structure", "Atom Type"])
    bg_color = st.color_picker("Background", "#FFFFFF")

    show_labels = st.checkbox("Show Labels", value=False)
    show_surface = st.checkbox("Show Surface", value=False)

with col2:
    st.markdown("#### Structure Visualization")

    pdb_code = "1A7F"
    if pdb_source == "From Database":
        pdb_code = protein_select.split("(")[1].strip(")")
    elif pdb_source == "Fetch from RCSB" and 'pdb_id' in locals() and pdb_id:
        pdb_code = pdb_id.upper()

    try:
        pdb_url = f"https://files.rcsb.org/download/{pdb_code}.pdb"
        response = requests.get(pdb_url)

        if response.status_code == 200:
            pdb_data = response.text

            xyzview = py3Dmol.view(width=800, height=600)
            xyzview.addModel(pdb_data, 'pdb')

            style_mapping = {
                "Cartoon": "cartoon",
                "Stick": "stick",
                "Sphere": "sphere",
                "Surface": "surface",
                "Line": "line"
            }

            color_mapping = {
                "Spectrum": "spectrum",
                "Chain": "chain",
                "Secondary Structure": "ss",
                "Atom Type": "element"
            }

            xyzview.setStyle({style_mapping[style]: {'color': color_mapping[color_scheme]}})

            if show_surface:
                xyzview.addSurface(py3Dmol.VDW, {'opacity': 0.7})

            xyzview.setBackgroundColor(bg_color)
            xyzview.zoomTo()

            html = xyzview._make_html()
            components.html(html, height=600, scrolling=False)

            st.info("Left click + drag: Rotate | Scroll: Zoom | Right click + drag: Pan")
        else:
            st.error(f"Failed to fetch PDB structure for {pdb_code}")
    except Exception as e:
        st.error(f"Error loading structure: {str(e)}")

st.markdown("---")

st.markdown("### Structure Information")

try:
    info_url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_code}"
    info_response = requests.get(info_url)

    if info_response.status_code == 200:
        info = info_response.json()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"**PDB ID:** {pdb_code}")
            resolution = info.get('rcsb_entry_info', {}).get('resolution_combined', ['N/A'])[0] if isinstance(info.get('rcsb_entry_info', {}).get('resolution_combined'), list) else info.get('rcsb_entry_info', {}).get('resolution_combined', 'N/A')
            st.markdown(f"**Resolution:** {resolution} Å" if resolution != 'N/A' else "**Resolution:** N/A")
            method = info.get('exptl', [{}])[0].get('method', 'N/A') if info.get('exptl') else 'N/A'
            st.markdown(f"**Method:** {method}")

        with col2:
            polymer_count = info.get('rcsb_entry_info', {}).get('polymer_entity_count', 'N/A')
            st.markdown(f"**Chains:** {polymer_count}")
            st.markdown(f"**Molecular Weight:** {info.get('rcsb_entry_info', {}).get('molecular_weight', 'N/A')}")

        with col3:
            release_date = info.get('rcsb_accession_info', {}).get('initial_release_date', 'N/A')
            st.markdown(f"**Released:** {release_date[:10] if release_date != 'N/A' else 'N/A'}")
            deposit_date = info.get('rcsb_accession_info', {}).get('deposit_date', 'N/A')
            st.markdown(f"**Deposited:** {deposit_date[:10] if deposit_date != 'N/A' else 'N/A'}")
    else:
        st.warning("Structure information not available")
except Exception as e:
    st.warning(f"Could not fetch structure information")
