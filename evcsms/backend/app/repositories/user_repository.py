from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.models import User, Vehicle, Admin
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email.ilike(email)).first()

    def create_admin_profile(self, user_id: int, name: str, email: str) -> Admin:
        admin = Admin(user_id=user_id, name=name, email=email)
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return admin


class VehicleRepository(BaseRepository[Vehicle]):
    def __init__(self, db: Session):
        super().__init__(Vehicle, db)

    def get_by_user_id(self, user_id: int) -> List[Vehicle]:
        return self.db.query(Vehicle).filter(Vehicle.user_id == user_id).all()

    def get_by_reg_no(self, reg_no: str) -> Optional[Vehicle]:
        return self.db.query(Vehicle).filter(Vehicle.reg_no.ilike(reg_no)).first()
