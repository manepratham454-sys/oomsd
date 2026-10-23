from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.models import Vehicle
from app.repositories.base import BaseRepository

class VehicleRepository(BaseRepository[Vehicle]):
    def __init__(self, db: Session):
        super().__init__(Vehicle, db)

    def get_by_user_id(self, user_id: int) -> List[Vehicle]:
        return self.db.query(Vehicle).filter(Vehicle.user_id == user_id).all()

    def get_by_reg_no(self, reg_no: str) -> Optional[Vehicle]:
        return self.db.query(Vehicle).filter(Vehicle.reg_no.ilike(reg_no)).first()
