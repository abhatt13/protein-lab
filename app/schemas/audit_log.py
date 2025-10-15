from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from app.models.audit_log import AuditAction

class AuditLogBase(BaseModel):
    user_id: int
    action: AuditAction
    entity_type: str
    entity_id: Optional[int] = None
    details: Optional[Dict] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class AuditLog(AuditLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
