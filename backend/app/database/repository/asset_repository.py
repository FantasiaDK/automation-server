from sqlmodel import Session, select
from sqlalchemy import or_

from app.database.models import Asset

from .database_repository import DatabaseRepository, AbstractRepository

class AbstractAssetRepository(AbstractRepository[Asset]):
    pass

class AssetRepository(DatabaseRepository[Asset]):
    def __init__(self, session: Session) -> None:
        super().__init__(Asset, session)

    def get_by_name(self, name: str) -> Asset:
        return self.session.exec(select(Asset).filter(Asset.name == name)).first()
    
    # replaced the broken method with this one
    def get_by_name_or_name_with_environment(self, name: str, environment: str) -> Asset:
        env_name = f"{name}_{environment}"
        return self.session.exec(
            select(Asset).where(or_(Asset.name == name, Asset.name == env_name))
        ).first()