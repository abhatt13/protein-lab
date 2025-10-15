import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.core.database import engine, Base
from app.models import User, Protein, ProteinVersion, AuditLog
from app.core.security import get_password_hash
from app.models.user import UserRole
from sqlalchemy.orm import Session

def init_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

    print("Creating default admin user...")
    db = Session(bind=engine)

    try:
        admin_user = User(
            email="admin@proteinlab.com",
            username="admin",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"[:72]),
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin_user)

        researcher_user = User(
            email="researcher@proteinlab.com",
            username="researcher",
            full_name="Researcher User",
            hashed_password=get_password_hash("researcher"[:72]),
            role=UserRole.RESEARCHER,
            is_active=True
        )
        db.add(researcher_user)

        viewer_user = User(
            email="viewer@proteinlab.com",
            username="viewer",
            full_name="Viewer User",
            hashed_password=get_password_hash("viewer123"[:72]),
            role=UserRole.VIEWER,
            is_active=True
        )
        db.add(viewer_user)

        db.commit()
        print("Default users created successfully!")
        print("\nDefault credentials:")
        print("Admin: admin / admin123")
        print("Researcher: researcher / researcher123")
        print("Viewer: viewer / viewer123")

    except Exception as e:
        print(f"Error creating users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
