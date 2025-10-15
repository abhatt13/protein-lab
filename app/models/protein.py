from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Protein(Base):
    __tablename__ = "proteins"

    id = Column(Integer, primary_key=True, index=True)
    uniprot_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False, index=True)
    sequence = Column(Text, nullable=False)
    organism = Column(String, index=True)
    gene_name = Column(String, index=True)
    protein_family = Column(String, index=True)
    function = Column(Text)
    molecular_weight = Column(Float)
    length = Column(Integer)
    pdb_id = Column(String)
    subcellular_location = Column(String)
    post_translational_modifications = Column(JSON)
    keywords = Column(JSON)
    ec_number = Column(String)
    is_validated = Column(Boolean, default=False)
    quality_score = Column(Float)
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    version = Column(Integer, default=1)

    versions = relationship("ProteinVersion", back_populates="protein", cascade="all, delete-orphan")

class ProteinVersion(Base):
    __tablename__ = "protein_versions"

    id = Column(Integer, primary_key=True, index=True)
    protein_id = Column(Integer, ForeignKey("proteins.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    uniprot_id = Column(String)
    name = Column(String)
    sequence = Column(Text)
    organism = Column(String)
    gene_name = Column(String)
    protein_family = Column(String)
    function = Column(Text)
    molecular_weight = Column(Float)
    length = Column(Integer)
    pdb_id = Column(String)
    subcellular_location = Column(String)
    post_translational_modifications = Column(JSON)
    keywords = Column(JSON)
    ec_number = Column(String)
    changed_by = Column(Integer, ForeignKey("users.id"))
    change_description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    protein = relationship("Protein", back_populates="versions")
