from openai import OpenAI
from typing import Optional
from app.core.config import get_settings

settings = get_settings()

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    def generate_sql_query(self, natural_language_query: str, schema_info: str = "") -> dict:
        system_prompt = f"""You are a SQL expert helping users query a protein database.

Database Schema:
{schema_info or '''
Table: proteins
Columns:
- id (integer, primary key)
- uniprot_id (string)
- name (string)
- sequence (text)
- organism (string)
- gene_name (string)
- protein_family (string)
- function (text)
- molecular_weight (float)
- length (integer)
- pdb_id (string)
- subcellular_location (string)
- keywords (json array)
- ec_number (string)
- is_validated (boolean)
- created_at (timestamp)
- updated_at (timestamp)
'''}

Convert the user's natural language query into a valid PostgreSQL query.
Return ONLY the SQL query without any explanation or markdown formatting."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": natural_language_query}
                ],
                temperature=0.1,
                max_tokens=500
            )

            sql_query = response.choices[0].message.content.strip()
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

            return {
                "success": True,
                "sql": sql_query,
                "explanation": self._explain_query(sql_query)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _explain_query(self, sql_query: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Explain this SQL query in simple terms."},
                    {"role": "user", "content": sql_query}
                ],
                temperature=0.3,
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
        except:
            return "Query explanation unavailable"

    def analyze_protein_function(self, sequence: str) -> dict:
        try:
            prompt = f"""Analyze this protein sequence and predict its likely function and properties:

Sequence: {sequence[:100]}{'...' if len(sequence) > 100 else ''}

Provide a brief analysis including:
1. Likely protein family
2. Potential function
3. Notable characteristics"""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a protein bioinformatics expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=300
            )

            return {
                "success": True,
                "analysis": response.choices[0].message.content.strip()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
