import streamlit as st

st.set_page_config(
    page_title="Protein Lab",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧬 Protein Lab")
st.markdown("### Comprehensive Protein Database Management Platform")

st.markdown("""
Welcome to **Protein Lab** - your all-in-one platform for protein database management,
analysis, and visualization.

#### Features
- 🔐 **Secure Authentication** - Role-based access control
- 📊 **Database Management** - Full CRUD operations with audit trails
- 🔍 **Advanced Search** - Filter and find proteins efficiently
- 🤖 **AI Assistant** - Natural language to SQL query generation
- 📈 **Analytics Dashboard** - Insights and visualizations
- 🧬 **Sequence Analysis** - BLAST, alignment, and motif detection
- 🎨 **3D Visualization** - Interactive protein structure viewer
- 📦 **Batch Operations** - Upload multiple proteins via CSV/Excel
- 🔄 **External Integration** - UniProt and PDB database connectivity
- 📥 **Export Options** - FASTA, GenBank, CSV, JSON formats

#### Getting Started
1. Login or register using the sidebar
2. Navigate through different sections using the menu
3. Explore, analyze, and manage protein data

#### Navigation
Use the sidebar to access different modules:
- **Home** - Overview and quick stats
- **Proteins** - View and manage protein database
- **Add Protein** - Create new protein entries
- **Search** - Advanced search and filtering
- **AI Assistant** - Chat with AI for SQL queries
- **Analytics** - Dashboard and insights
- **Sequence Analysis** - Analysis tools
- **3D Viewer** - Structure visualization
- **Batch Upload** - Import multiple proteins
- **Export** - Download data in various formats
""")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.token = None

with st.sidebar:
    st.header("Authentication")

    if not st.session_state.authenticated:
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")

                if submit:
                    st.info("Login functionality will be connected to API")

        with tab2:
            with st.form("register_form"):
                email = st.text_input("Email")
                username = st.text_input("Username")
                full_name = st.text_input("Full Name")
                password = st.text_input("Password", type="password")
                role = st.selectbox("Role", ["viewer", "researcher", "admin"])
                submit = st.form_submit_button("Register")

                if submit:
                    st.info("Registration functionality will be connected to API")
    else:
        st.success(f"Welcome, {st.session_state.user}!")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.token = None
            st.rerun()
