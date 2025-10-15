import pytest
from app.utils.validators import ProteinValidator

class TestProteinValidator:
    def test_valid_sequence(self):
        sequence = "MKTLLLTLVVVTIVFPSSLGLDL"
        is_valid, errors = ProteinValidator.validate_sequence(sequence)
        assert is_valid
        assert len(errors) == 0

    def test_invalid_amino_acids(self):
        sequence = "MKTLLLTLVVVTIVFPXXX"
        is_valid, errors = ProteinValidator.validate_sequence(sequence)
        assert not is_valid
        assert len(errors) > 0

    def test_empty_sequence(self):
        sequence = ""
        is_valid, errors = ProteinValidator.validate_sequence(sequence)
        assert not is_valid
        assert "Sequence cannot be empty" in errors[0]

    def test_sequence_too_short(self):
        sequence = "MKTLL"
        is_valid, errors = ProteinValidator.validate_sequence(sequence)
        assert not is_valid
        assert any("too short" in error for error in errors)

    def test_valid_uniprot_id(self):
        uniprot_id = "P12345"
        is_valid, errors = ProteinValidator.validate_uniprot_id(uniprot_id)
        assert is_valid
        assert len(errors) == 0

    def test_invalid_uniprot_id(self):
        uniprot_id = "INVALID"
        is_valid, errors = ProteinValidator.validate_uniprot_id(uniprot_id)
        assert not is_valid
        assert len(errors) > 0

    def test_quality_score_calculation(self):
        protein_data = {
            "uniprot_id": "P12345",
            "name": "Test Protein",
            "sequence": "MKTLLLTLVVVTIVFPSSL",
            "organism": "Homo sapiens",
            "function": "Test function",
            "gene_name": "TEST",
            "protein_family": "Test family",
            "pdb_id": "1ABC",
            "ec_number": "1.1.1.1"
        }
        score = ProteinValidator.calculate_quality_score(protein_data)
        assert score > 0
        assert score <= 10
