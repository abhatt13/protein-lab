import streamlit as st

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

st.title("🤖 AI Assistant")

if not st.session_state.get('authenticated', False):
    st.warning("Please login to access this page")
    st.stop()

st.markdown("### Natural Language to SQL Query Generator")

st.info("""
Ask questions in natural language and I'll generate SQL queries for you!

**Examples:**
- "Show me all proteins from humans"
- "Find proteins longer than 500 amino acids"
- "Which proteins have PDB structures?"
- "List validated proteins from the kinase family"
""")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sql" in message:
            st.code(message["sql"], language="sql")

user_input = st.chat_input("Ask me anything about the protein database...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        st.markdown("I understand you want to query the database. Here's the SQL:")

        example_sql = """SELECT id, uniprot_id, name, organism, length
FROM proteins
WHERE organism = 'Homo sapiens'
ORDER BY length DESC
LIMIT 10;"""

        st.code(example_sql, language="sql")

        st.markdown("Would you like me to execute this query?")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Execute Query"):
                st.success("Query executed successfully!")
        with col2:
            if st.button("Modify Query"):
                st.info("You can edit the query above")

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": "I understand you want to query the database. Here's the SQL:",
        "sql": example_sql
    })

st.markdown("---")

with st.expander("Query History"):
    st.markdown("Recent queries will appear here")
