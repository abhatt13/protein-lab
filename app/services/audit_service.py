from sqlalchemy.orm import Session
from typing import Optional, Dict
from app.models.audit_log import AuditLog, AuditAction
from app.models.user import User

class AuditService:
    @staticmethod
    def log_action(
        db: Session,
        user: User,
        action: AuditAction,
        entity_type: str,
        entity_id: Optional[int] = None,
        details: Optional[Dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        audit_log = AuditLog(
            user_id=user.id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        return audit_log

    @staticmethod
    def get_entity_history(
        db: Session,
        entity_type: str,
        entity_id: int,
        limit: int = 50
    ):
        return db.query(AuditLog).filter(
            AuditLog.entity_type == entity_type,
            AuditLog.entity_id == entity_id
        ).order_by(AuditLog.timestamp.desc()).limit(limit).all()
