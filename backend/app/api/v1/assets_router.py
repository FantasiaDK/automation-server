from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from app.database.models import Asset, AccessToken
from app.database.unit_of_work import AbstractUnitOfWork
from .schemas import AssetCreate, AssetUpdate
from .dependencies import get_unit_of_work, resolve_access_token
from . import error_descriptions

# Dependency Injection local to this router


def get_Asset(
    Asset_id: int, uow: AbstractUnitOfWork = Depends(get_unit_of_work)
) -> Asset:
    with uow:
        Asset = uow.Assets.get(Asset_id)

        if Asset is None:
            raise HTTPException(status_code=404, detail="Asset not found")

        if Asset.deleted:
            raise HTTPException(status_code=410, detail="Asset is gone")

        return Asset


# Error responses

RESPONSE_STATES = error_descriptions("Asset", _404=True, _410=True, _403=True)

# Router

router = APIRouter(prefix="/Assets", tags=["Assets"])


@router.get("", responses=error_descriptions("Asset", _403=True))
def get_Assets(
    include_deleted: bool = False,
    uow: AbstractUnitOfWork = Depends(get_unit_of_work),
    token: AccessToken = Depends(resolve_access_token),
) -> list[Asset]:
    with uow:
        result = uow.Assets.get_all(include_deleted)

        result.sort(key=lambda x: x.name)
        return result


@router.get("/{Asset_id}", responses=RESPONSE_STATES)
def get_Asset(
    Asset: Asset = Depends(get_Asset),
    token: AccessToken = Depends(resolve_access_token),
) -> Asset:
    return Asset


@router.get("/by_name/{Asset_name}", responses=RESPONSE_STATES)
def get_Asset_by_name(
    Asset_name: str,
    uow: AbstractUnitOfWork = Depends(get_unit_of_work),
    token: AccessToken = Depends(resolve_access_token),
) -> Asset:
    with uow:
        Asset = uow.Assets.get_by_name(Asset_name)

        if Asset is None:
            raise HTTPException(status_code=404, detail="Asset not found")

        if Asset.deleted:
            raise HTTPException(status_code=410, detail="Asset is gone")

        return Asset
    
    return Asset


@router.put("/{Asset_id}", responses=RESPONSE_STATES)
def update_Asset(
    update: AssetUpdate,
    Asset: Asset = Depends(get_Asset),
    uow: AbstractUnitOfWork = Depends(get_unit_of_work),
    token: AccessToken = Depends(resolve_access_token),
) -> Asset:
    with uow:
        return uow.Assets.update(Asset, update.model_dump())


@router.post("", responses=error_descriptions("Asset", _403=True))
def create_Asset(
    Asset: AssetCreate,
    uow: AbstractUnitOfWork = Depends(get_unit_of_work),
    token: AccessToken = Depends(resolve_access_token),
) -> Asset:
    try:
        with uow:
            data = Asset.model_dump()
            data["deleted"] = False

            return uow.Assets.create(data)
    except ValueError:
        raise HTTPException(status_code=422, detail="JSON data is invalid")
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Asset name already exists")


@router.delete(
    "/{Asset_id}",
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
def delete_Asset(
    Asset: Asset = Depends(get_Asset),
    uow: AbstractUnitOfWork = Depends(get_unit_of_work),
    token: AccessToken = Depends(resolve_access_token),
) -> None:
    with uow:
        uow.Assets.delete(Asset)

    return
