import re
from typing import List, Dict, Tuple
from Bio.Seq import Seq
from Bio.SeqUtils.ProtParam import ProteinAnalysis

class ProteinValidator:
    VALID_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")

    @staticmethod
    def validate_sequence(sequence: str) -> Tuple[bool, List[str]]:
        errors = []

        if not sequence:
            errors.append("Sequence cannot be empty")
            return False, errors

        sequence = sequence.upper().replace(" ", "").replace("\n", "")

        invalid_chars = set(sequence) - ProteinValidator.VALID_AMINO_ACIDS
        if invalid_chars:
            errors.append(f"Invalid amino acids found: {', '.join(invalid_chars)}")

        if len(sequence) < 10:
            errors.append("Sequence too short (minimum 10 amino acids)")

        if len(sequence) > 50000:
            errors.append("Sequence too long (maximum 50,000 amino acids)")

        return len(errors) == 0, errors

    @staticmethod
    def validate_uniprot_id(uniprot_id: str) -> Tuple[bool, List[str]]:
        errors = []

        if not uniprot_id:
            errors.append("UniProt ID cannot be empty")
            return False, errors

        pattern = r'^[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}$'
        if not re.match(pattern, uniprot_id):
            errors.append("Invalid UniProt ID format")

        return len(errors) == 0, errors

    @staticmethod
    def calculate_quality_score(protein_data: Dict) -> float:
        score = 0.0
        max_score = 100.0

        if protein_data.get('uniprot_id'):
            score += 15

        if protein_data.get('name'):
            score += 10

        if protein_data.get('sequence'):
            score += 20
            is_valid, _ = ProteinValidator.validate_sequence(protein_data['sequence'])
            if is_valid:
                score += 10

        if protein_data.get('organism'):
            score += 10

        if protein_data.get('function'):
            score += 10

        if protein_data.get('gene_name'):
            score += 5

        if protein_data.get('protein_family'):
            score += 5

        if protein_data.get('pdb_id'):
            score += 10

        if protein_data.get('ec_number'):
            score += 5

        return (score / max_score) * 10

    @staticmethod
    def calculate_sequence_properties(sequence: str) -> Dict:
        try:
            clean_seq = sequence.upper().replace(" ", "").replace("\n", "")
            analyzer = ProteinAnalysis(clean_seq)

            return {
                "length": len(clean_seq),
                "molecular_weight": round(analyzer.molecular_weight(), 2),
                "aromaticity": round(analyzer.aromaticity(), 4),
                "instability_index": round(analyzer.instability_index(), 2),
                "isoelectric_point": round(analyzer.isoelectric_point(), 2),
                "gravy": round(analyzer.gravy(), 4)
            }
        except:
            return {}

    @staticmethod
    def detect_duplicates(db, sequence: str, threshold: float = 0.95) -> List[Dict]:
        return []

    @staticmethod
    def check_completeness(protein_data: Dict) -> Dict[str, bool]:
        return {
            "has_uniprot_id": bool(protein_data.get('uniprot_id')),
            "has_name": bool(protein_data.get('name')),
            "has_sequence": bool(protein_data.get('sequence')),
            "has_organism": bool(protein_data.get('organism')),
            "has_function": bool(protein_data.get('function')),
            "has_gene_name": bool(protein_data.get('gene_name')),
            "has_structure": bool(protein_data.get('pdb_id'))
        }
