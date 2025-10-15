import pytest
from app.utils.sequence_tools import SequenceTools

class TestSequenceTools:
    def test_to_fasta(self):
        proteins = [
            {
                "uniprot_id": "P12345",
                "name": "Insulin",
                "organism": "Homo sapiens",
                "sequence": "MKTLLLTLVVVTIVFPSSL"
            }
        ]
        fasta = SequenceTools.to_fasta(proteins)
        assert ">P12345" in fasta
        assert "Insulin" in fasta
        assert "MKTLLLTLVVVTIVFPSSL" in fasta

    def test_from_fasta(self):
        fasta_content = """>Test|Protein
MKTLLLTLVVVTIVFPSSL"""
        proteins = SequenceTools.from_fasta(fasta_content)
        assert len(proteins) == 1
        assert proteins[0]["name"] == "Test"
        assert proteins[0]["sequence"] == "MKTLLLTLVVVTIVFPSSL"

    def test_calculate_similarity(self):
        seq1 = "MKTLLLTLVVVTIVFPSSL"
        seq2 = "MKTLLLTLVVVTIVFPSSL"
        similarity = SequenceTools.calculate_similarity(seq1, seq2)
        assert similarity == 1.0

    def test_find_motif(self):
        sequence = "MKTLLLTLVVVTIVFPSSLTLL"
        motif = "TLL"
        positions = SequenceTools.find_motif(sequence, motif)
        assert len(positions) > 0
        assert 2 in positions
