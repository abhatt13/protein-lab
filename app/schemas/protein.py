from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime

class ProteinBase(BaseModel):
    uniprot_id: Optional[str] = None
    name: str
    sequence: str
    organism: Optional[str] = None
    gene_name: Optional[str] = None
    protein_family: Optional[str] = None
    function: Optional[str] = None
    molecular_weight: Optional[float] = None
    length: Optional[int] = None
    pdb_id: Optional[str] = None
    subcellular_location: Optional[str] = None
    post_translational_modifications: Optional[Dict] = None
    keywords: Optional[List[str]] = None
    ec_number: Optional[str] = None

class ProteinCreate(ProteinBase):
    pass

class ProteinUpdate(BaseModel):
    name: Optional[str] = None
    sequence: Optional[str] = None
    organism: Optional[str] = None
    gene_name: Optional[str] = None
    protein_family: Optional[str] = None
    function: Optional[str] = None
    molecular_weight: Optional[float] = None
    pdb_id: Optional[str] = None
    subcellular_location: Optional[str] = None
    post_translational_modifications: Optional[Dict] = None
    keywords: Optional[List[str]] = None
    ec_number: Optional[str] = None

class Protein(ProteinBase):
    id: int
    is_validated: bool
    quality_score: Optional[float] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    version: int

    class Config:
        from_attributes = True

class ProteinSearch(BaseModel):
    query: Optional[str] = None
    organism: Optional[str] = None
    protein_family: Optional[str] = None
    gene_name: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    has_pdb: Optional[bool] = None
    is_validated: Optional[bool] = None
