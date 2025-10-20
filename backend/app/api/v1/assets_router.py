from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from app.database.models import Asset, AccessToken
from app.database.unit_of_work import AbstractUnitOfWork
from .schemas import AssetCreate, AssetUpdate
from .dependencies import get_unit_of_work, resolve_access_token
from . import error_descriptions

# Dependency Injection local to this router


def get_asset(asset_id: int, uow: AbstractUnitOfWork = Depends(get_unit_of_work)
) -> Asset:
    with uow:
        asset = uow.assets.get(asset_id)

        if asset is None:
            raise HTTPException(status_code=404, detail="Asset not found")

        if asset.deleted:
            raise HTTPException(status_code=410, detail="Asset is gone")

        return asset


# Error responses

RESPONSE_STATES = error_descriptions("Asset", _404=True, _410=True, _403=True)

# Router

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("", responses=error_descriptions("Asset", _403=True))
def get_assets(
    include_deleted: bool = False,
    uow: AbstractUnitOfWork = Depends(get_unit_of_work),
    token: AccessToken = Depends(resolve_access_token),
) -> list[Asset]:
    with uow:
        result = uow.assets.get_all(include_deleted)

        result.sort(key=lambda x: x.name)
        return result


@router.get("/{asset_id}", responses=RESPONSE_STATES)
def get_asset(
    asset: Asset = Depends(get_asset),
    token: AccessToken = Depends(resolve_access_token),
) -> Asset:
    return asset


@router.get("/by_name/{asset_name}", responses=RESPONSE_STATES)
def get_asset_by_name(
    asset_name: str,
    uow: AbstractUnitOfWork = Depends(get_unit_of_work),
    token: AccessToken = Depends(resolve_access_token),
) -> Asset:
    with uow:
        asset = uow.assets.get_by_name(asset_name)

        if asset is None:
            raise HTTPException(status_code=404, detail="Asset not found")

        if asset.deleted:
            raise HTTPException(status_code=410, detail="Asset is gone")

        return asset
    
    return asset


@router.put("/{asset_id}", responses=RESPONSE_STATES)
def update_asset(
    update: AssetUpdate,
    asset: Asset = Depends(get_asset),
    uow: AbstractUnitOfWork = Depends(get_unit_of_work),
    token: AccessToken = Depends(resolve_access_token),
) -> Asset:
    with uow:
        return uow.assets.update(asset, update.model_dump())


@router.post("", responses=error_descriptions("Asset", _403=True))
def create_asset(
    asset: AssetCreate,
    uow: AbstractUnitOfWork = Depends(get_unit_of_work),
    token: AccessToken = Depends(resolve_access_token),
) -> Asset:
    try:
        with uow:
            data = asset.model_dump()
            data["deleted"] = False

            return uow.assets.create(data)
    except ValueError:
        raise HTTPException(status_code=422, detail="JSON data is invalid")
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Asset name already exists")


@router.delete(
    "/{asset_id}",
    status_code=204,
    responses={
        204: {
            "description": "Item deleted",
            "content": {
                "application/json": {"example": {"detail": "Process has been deleted"}}
            },
        }
    }
    | RESPONSE_STATES,
)
def delete_asset(
    asset: Asset = Depends(get_asset),
    uow: AbstractUnitOfWork = Depends(get_unit_of_work),
    token: AccessToken = Depends(resolve_access_token),
) -> None:
    with uow:
        uow.assets.delete(asset)

    return
