from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from app.db.models import Station, Charger
from app.repositories.base import BaseRepository

class StationRepository(BaseRepository[Station]):
    def __init__(self, db: Session):
        super().__init__(Station, db)

    def get_with_chargers(self, station_id: int) -> Optional[Station]:
        return self.db.query(Station).options(joinedload(Station.chargers)).filter(Station.id == station_id).first()

    def list_all_with_chargers(self) -> List[Station]:
        return self.db.query(Station).options(joinedload(Station.chargers)).all()

    def filter_stations(self, city: Optional[str] = None) -> List[Station]:
        query = self.db.query(Station).options(joinedload(Station.chargers))
        if city:
            query = query.filter(Station.city.ilike(f"%{city.strip()}%"))
        return query.all()


class ChargerRepository(BaseRepository[Charger]):
    def __init__(self, db: Session):
        super().__init__(Charger, db)

    def get_by_station(self, station_id: int) -> List[Charger]:
        return self.db.query(Charger).filter(Charger.station_id == station_id).all()

    def update_status(self, charger_id: int, status: str) -> Optional[Charger]:
        charger = self.get_by_id(charger_id)
        if charger:
            charger.status = status
            self.db.commit()
            self.db.refresh(charger)
        return charger

    def update_pricing(self, charger_id: int, price_per_unit: float) -> Optional[Charger]:
        charger = self.get_by_id(charger_id)
        if charger:
            charger.price_per_unit = price_per_unit
            self.db.commit()
            self.db.refresh(charger)
        return charger
