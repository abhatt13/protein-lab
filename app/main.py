import streamlit as st
import requests

API_URL = "http://localhost:8000"

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
                    try:
                        response = requests.post(
                            f"{API_URL}/api/auth/login",
                            data={"username": username, "password": password}
                        )
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.authenticated = True
                            st.session_state.user = username
                            st.session_state.token = data["access_token"]
                            st.success("Login successful!")
                            st.experimental_rerun()
                        else:
                            st.error("Invalid credentials")
                    except Exception as e:
                        st.error(f"Login failed: {str(e)}")

        with tab2:
            with st.form("register_form"):
                email = st.text_input("Email")
                username = st.text_input("Username")
                full_name = st.text_input("Full Name")
                password = st.text_input("Password", type="password")
                role = st.selectbox("Role", ["viewer", "researcher", "admin"])
                submit = st.form_submit_button("Register")

                if submit:
                    try:
                        response = requests.post(
                            f"{API_URL}/api/auth/register",
                            json={
                                "email": email,
                                "username": username,
                                "full_name": full_name,
                                "password": password,
                                "role": role
                            }
                        )
                        if response.status_code == 200:
                            st.success("Registration successful! Please login.")
                        else:
                            st.error(f"Registration failed: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Registration failed: {str(e)}")
    else:
        st.success(f"Welcome, {st.session_state.user}!")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.token = None
            st.experimental_rerun()
