import requests
from typing import Optional, Dict
from app.core.config import get_settings

settings = get_settings()

class ExternalDBService:
    @staticmethod
    def fetch_from_uniprot(uniprot_id: str) -> Optional[Dict]:
        try:
            url = f"{settings.uniprot_api_url}/uniprotkb/{uniprot_id}.json"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()

                protein_data = {
                    "uniprot_id": uniprot_id,
                    "name": data.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value"),
                    "organism": data.get("organism", {}).get("scientificName"),
                    "sequence": data.get("sequence", {}).get("value"),
                    "length": data.get("sequence", {}).get("length"),
                    "molecular_weight": data.get("sequence", {}).get("molWeight"),
                    "gene_name": data.get("genes", [{}])[0].get("geneName", {}).get("value") if data.get("genes") else None,
                    "function": ExternalDBService._extract_function(data),
                    "keywords": [kw.get("name") for kw in data.get("keywords", [])],
                    "subcellular_location": ExternalDBService._extract_subcellular_location(data),
                }

                return protein_data
            return None
        except Exception as e:
            return None

    @staticmethod
    def _extract_function(data: Dict) -> Optional[str]:
        comments = data.get("comments", [])
        for comment in comments:
            if comment.get("commentType") == "FUNCTION":
                return comment.get("texts", [{}])[0].get("value")
        return None

    @staticmethod
    def _extract_subcellular_location(data: Dict) -> Optional[str]:
        comments = data.get("comments", [])
        for comment in comments:
            if comment.get("commentType") == "SUBCELLULAR LOCATION":
                locations = comment.get("subcellularLocations", [])
                if locations:
                    return locations[0].get("location", {}).get("value")
        return None

    @staticmethod
    def fetch_from_pdb(pdb_id: str) -> Optional[Dict]:
        try:
            url = f"{settings.pdb_api_url}/core/entry/{pdb_id}"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()

                return {
                    "pdb_id": pdb_id,
                    "title": data.get("struct", {}).get("title"),
                    "resolution": data.get("rcsb_entry_info", {}).get("resolution_combined"),
                    "method": data.get("exptl", [{}])[0].get("method"),
                    "release_date": data.get("rcsb_accession_info", {}).get("initial_release_date"),
                }
            return None
        except Exception as e:
            return None

    @staticmethod
    def search_uniprot(query: str, limit: int = 10) -> list:
        try:
            url = f"{settings.uniprot_api_url}/uniprotkb/search"
            params = {
                "query": query,
                "size": limit,
                "format": "json"
            }
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return data.get("results", [])
            return []
        except Exception as e:
            return []
