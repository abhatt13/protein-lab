import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.core.database import SessionLocal
from app.models import Protein, User
from app.services.protein_service import ProteinService
from app.schemas.protein import ProteinCreate

def seed_proteins():
    db = SessionLocal()

    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            print("Admin user not found. Run init_db.py first.")
            return

        sample_proteins = [
            {
                "uniprot_id": "P01308",
                "name": "Insulin",
                "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN",
                "organism": "Homo sapiens",
                "gene_name": "INS",
                "protein_family": "Insulin family",
                "function": "Insulin decreases blood glucose concentration. It increases cell permeability to monosaccharides, amino acids and fatty acids.",
                "molecular_weight": 5808.0,
                "pdb_id": "1A7F",
                "subcellular_location": "Secreted",
                "keywords": ["Diabetes mellitus", "Disease variant", "Hormone", "Secreted"]
            },
            {
                "uniprot_id": "P69905",
                "name": "Hemoglobin subunit alpha",
                "sequence": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR",
                "organism": "Homo sapiens",
                "gene_name": "HBA1",
                "protein_family": "Globin family",
                "function": "Involved in oxygen transport from the lung to the various peripheral tissues.",
                "molecular_weight": 15258.0,
                "pdb_id": "1A3N",
                "subcellular_location": "Cytoplasm",
                "keywords": ["Oxygen transport", "Heme", "Iron", "Metal-binding"]
            }
        ]

        print("Seeding sample proteins...")

        for protein_data in sample_proteins:
            existing = db.query(Protein).filter(
                Protein.uniprot_id == protein_data["uniprot_id"]
            ).first()

            if not existing:
                protein_create = ProteinCreate(**protein_data)
                ProteinService.create_protein(db, protein_create, admin_user)
                print(f"Added protein: {protein_data['name']}")
            else:
                print(f"Protein {protein_data['name']} already exists, skipping...")

        print("Seeding completed successfully!")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_proteins()
