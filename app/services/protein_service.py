from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from app.models.protein import Protein, ProteinVersion
from app.models.user import User
from app.models.audit_log import AuditAction
from app.schemas.protein import ProteinCreate, ProteinUpdate, ProteinSearch
from app.services.audit_service import AuditService

class ProteinService:
    @staticmethod
    def create_protein(db: Session, protein: ProteinCreate, user: User) -> Protein:
        protein_data = protein.model_dump()
        protein_data['length'] = len(protein.sequence) if protein.sequence else None
        protein_data['created_by'] = user.id
        protein_data['updated_by'] = user.id

        db_protein = Protein(**protein_data)
        db.add(db_protein)
        db.flush()

        version = ProteinVersion(
            protein_id=db_protein.id,
            version_number=1,
            **protein.model_dump(),
            changed_by=user.id,
            change_description="Initial creation"
        )
        db.add(version)

        AuditService.log_action(
            db=db,
            user=user,
            action=AuditAction.CREATE,
            entity_type="protein",
            entity_id=db_protein.id,
            details={"name": protein.name, "uniprot_id": protein.uniprot_id}
        )

        db.commit()
        db.refresh(db_protein)
        return db_protein

    @staticmethod
    def get_protein(db: Session, protein_id: int) -> Optional[Protein]:
        return db.query(Protein).filter(Protein.id == protein_id).first()

    @staticmethod
    def get_protein_by_uniprot_id(db: Session, uniprot_id: str) -> Optional[Protein]:
        return db.query(Protein).filter(Protein.uniprot_id == uniprot_id).first()

    @staticmethod
    def get_proteins(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[ProteinSearch] = None
    ) -> List[Protein]:
        query = db.query(Protein)

        if search:
            if search.query:
                query = query.filter(
                    or_(
                        Protein.name.ilike(f"%{search.query}%"),
                        Protein.uniprot_id.ilike(f"%{search.query}%"),
                        Protein.gene_name.ilike(f"%{search.query}%")
                    )
                )
            if search.organism:
                query = query.filter(Protein.organism.ilike(f"%{search.organism}%"))
            if search.protein_family:
                query = query.filter(Protein.protein_family.ilike(f"%{search.protein_family}%"))
            if search.gene_name:
                query = query.filter(Protein.gene_name.ilike(f"%{search.gene_name}%"))
            if search.min_length:
                query = query.filter(Protein.length >= search.min_length)
            if search.max_length:
                query = query.filter(Protein.length <= search.max_length)
            if search.has_pdb is not None:
                if search.has_pdb:
                    query = query.filter(Protein.pdb_id.isnot(None))
                else:
                    query = query.filter(Protein.pdb_id.is_(None))
            if search.is_validated is not None:
                query = query.filter(Protein.is_validated == search.is_validated)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_protein(
        db: Session,
        protein_id: int,
        protein_update: ProteinUpdate,
        user: User,
        change_description: Optional[str] = None
    ) -> Optional[Protein]:
        db_protein = ProteinService.get_protein(db, protein_id)
        if not db_protein:
            return None

        update_data = protein_update.model_dump(exclude_unset=True)

        if "sequence" in update_data:
            update_data["length"] = len(update_data["sequence"])

        version = ProteinVersion(
            protein_id=db_protein.id,
            version_number=db_protein.version + 1,
            uniprot_id=db_protein.uniprot_id,
            name=db_protein.name,
            sequence=db_protein.sequence,
            organism=db_protein.organism,
            gene_name=db_protein.gene_name,
            protein_family=db_protein.protein_family,
            function=db_protein.function,
            molecular_weight=db_protein.molecular_weight,
            length=db_protein.length,
            pdb_id=db_protein.pdb_id,
            subcellular_location=db_protein.subcellular_location,
            post_translational_modifications=db_protein.post_translational_modifications,
            keywords=db_protein.keywords,
            ec_number=db_protein.ec_number,
            changed_by=user.id,
            change_description=change_description or "Updated protein data"
        )
        db.add(version)

        for field, value in update_data.items():
            setattr(db_protein, field, value)

        db_protein.updated_by = user.id
        db_protein.version += 1

        AuditService.log_action(
            db=db,
            user=user,
            action=AuditAction.UPDATE,
            entity_type="protein",
            entity_id=db_protein.id,
            details={"updated_fields": list(update_data.keys())}
        )

        db.commit()
        db.refresh(db_protein)
        return db_protein

    @staticmethod
    def delete_protein(db: Session, protein_id: int, user: User) -> bool:
        db_protein = ProteinService.get_protein(db, protein_id)
        if not db_protein:
            return False

        AuditService.log_action(
            db=db,
            user=user,
            action=AuditAction.DELETE,
            entity_type="protein",
            entity_id=protein_id,
            details={"name": db_protein.name, "uniprot_id": db_protein.uniprot_id}
        )

        db.delete(db_protein)
        db.commit()
        return True

    @staticmethod
    def get_protein_versions(db: Session, protein_id: int) -> List[ProteinVersion]:
        return db.query(ProteinVersion).filter(
            ProteinVersion.protein_id == protein_id
        ).order_by(ProteinVersion.version_number.desc()).all()
