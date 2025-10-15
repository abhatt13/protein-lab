from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from typing import List, Dict
import io

class SequenceTools:
    @staticmethod
    def to_fasta(proteins: List[Dict]) -> str:
        fasta_records = []

        for protein in proteins:
            header = f">{protein.get('uniprot_id', 'UNKNOWN')}|{protein.get('name', 'Unknown')}"
            if protein.get('organism'):
                header += f"|{protein['organism']}"

            sequence = protein.get('sequence', '')
            fasta_records.append(f"{header}\n{sequence}")

        return "\n".join(fasta_records)

    @staticmethod
    def from_fasta(fasta_content: str) -> List[Dict]:
        proteins = []

        fasta_io = io.StringIO(fasta_content)

        for record in SeqIO.parse(fasta_io, "fasta"):
            protein = {
                "name": record.id,
                "sequence": str(record.seq),
                "description": record.description
            }
            proteins.append(protein)

        return proteins

    @staticmethod
    def calculate_similarity(seq1: str, seq2: str) -> float:
        if len(seq1) != len(seq2):
            return 0.0

        matches = sum(a == b for a, b in zip(seq1, seq2))
        return matches / len(seq1)

    @staticmethod
    def find_motif(sequence: str, motif: str) -> List[int]:
        positions = []
        start = 0

        while True:
            pos = sequence.find(motif, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1

        return positions

    @staticmethod
    def translate_dna_to_protein(dna_sequence: str) -> str:
        try:
            seq = Seq(dna_sequence)
            return str(seq.translate())
        except:
            return ""

    @staticmethod
    def reverse_complement(dna_sequence: str) -> str:
        try:
            seq = Seq(dna_sequence)
            return str(seq.reverse_complement())
        except:
            return ""
