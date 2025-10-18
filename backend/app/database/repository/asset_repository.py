from sqlmodel import Session, select

from app.database.models import Asset

from .database_repository import DatabaseRepository, AbstractRepository

class AbstractAssetRepository(AbstractRepository[Asset]):
    pass

class AssetRepository(DatabaseRepository[Asset]):
    def __init__(self, session: Session) -> None:
        super().__init__(Asset, session)

    def get_by_name(self, name: str) -> Asset:
        return self.session.exec(select(Asset).filter(Asset.name == name)).first()