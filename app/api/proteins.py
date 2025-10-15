from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.protein import Protein, ProteinCreate, ProteinUpdate, ProteinSearch
from app.services.protein_service import ProteinService
from app.utils.dependencies import get_current_active_user, require_role
from app.models.user import User, UserRole

router = APIRouter(prefix="/proteins", tags=["proteins"])

@router.post("/", response_model=Protein)
def create_protein(
    protein: ProteinCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.RESEARCHER))
):
    existing = ProteinService.get_protein_by_uniprot_id(db, protein.uniprot_id)
    if existing:
        raise HTTPException(status_code=400, detail="Protein with this UniProt ID already exists")

    return ProteinService.create_protein(db=db, protein=protein, user=current_user)

@router.get("/", response_model=List[Protein])
def list_proteins(
    skip: int = 0,
    limit: int = 100,
    query: Optional[str] = None,
    organism: Optional[str] = None,
    protein_family: Optional[str] = None,
    gene_name: Optional[str] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    has_pdb: Optional[bool] = None,
    is_validated: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    search = ProteinSearch(
        query=query,
        organism=organism,
        protein_family=protein_family,
        gene_name=gene_name,
        min_length=min_length,
        max_length=max_length,
        has_pdb=has_pdb,
        is_validated=is_validated
    )
    return ProteinService.get_proteins(db=db, skip=skip, limit=limit, search=search)

@router.get("/{protein_id}", response_model=Protein)
def get_protein(
    protein_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    protein = ProteinService.get_protein(db, protein_id=protein_id)
    if not protein:
        raise HTTPException(status_code=404, detail="Protein not found")
    return protein

@router.put("/{protein_id}", response_model=Protein)
def update_protein(
    protein_id: int,
    protein_update: ProteinUpdate,
    change_description: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.RESEARCHER))
):
    protein = ProteinService.update_protein(
        db=db,
        protein_id=protein_id,
        protein_update=protein_update,
        user=current_user,
        change_description=change_description
    )
    if not protein:
        raise HTTPException(status_code=404, detail="Protein not found")
    return protein

@router.delete("/{protein_id}")
def delete_protein(
    protein_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    success = ProteinService.delete_protein(db=db, protein_id=protein_id, user=current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Protein not found")
    return {"message": "Protein deleted successfully"}

@router.get("/{protein_id}/versions")
def get_protein_versions(
    protein_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    versions = ProteinService.get_protein_versions(db=db, protein_id=protein_id)
    return versions
