from fastapi.testclient import TestClient
from sqlmodel import Session

import app.database.models as models

from . import generate_basic_data  # noqa: F401


def test_get_assets(session: Session, client: TestClient):
    generate_basic_data(session)

    response = client.get("/assets/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["name"] == "Test asset"
    assert data[0]["deleted"] is False

    response = client.get("/assets/?include_deleted=true")
    data = response.json()
    assert len(data) == 2

    assert data[1]["name"] == "Test deleted asset"
    assert data[1]["deleted"] is True


def test_get_asset(session: Session, client: TestClient):
    generate_basic_data(session)

    response = client.get("/assets/1")

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Test asset"
    assert data["deleted"] is False

    response = client.get("/assets/2")

    assert response.status_code == 410


def test_update_asset(session: Session, client: TestClient):
    generate_basic_data(session)

    response = client.put(
        "/assets/1",
        json={
            "name": "Test asset updated",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Test asset"

    response = client.put(
        "/assets/2",
        json={
            "name": "Test deleted asset",
            "description": "New description",
        },
    )

    assert response.status_code == 410

def test_create_asset(session: Session, client: TestClient):
    generate_basic_data(session)   

    response = client.post(
        "/assets/",
        json={
            "name": "New asset",
        },
    )

    assert response.status_code == 200
    
def test_delete_asset(session: Session, client: TestClient):
    generate_basic_data(session)

    response = client.delete("/assets/1")

    assert response.status_code == 204

    # Verify against the database
    
    asset = session.get(models.asset, 1)
    assert asset.deleted is True


    response = client.delete("/assets/2")

    assert response.status_code == 410

def test_retrieve_existing_asset_by_name(session: Session, client: TestClient):
    generate_basic_data(session)

    response = client.get("/assets/by_name/Test asset")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Test asset"
    assert data["deleted"] is False

def test_asset_not_found(session: Session, client: TestClient):
    generate_basic_data(session)

    response = client.get("/assets/by_name/nonexistent_asset")

    assert response.status_code == 404
    assert response.json() == {"detail": "asset not found"}

def test_asset_deleted(session: Session, client: TestClient):
    generate_basic_data(session)

    response = client.get("/assets/by_name/Test deleted asset")

    assert response.status_code == 410
    assert response.json() == {"detail": "asset is gone"}

def test_case_sensitivity(session: Session, client: TestClient):
    generate_basic_data(session)

    response = client.get("/asset/by_name/tEsT asset")
    assert response.status_code == 404  # Assuming case-sensitive

def test_empty_asset_name(session: Session, client: TestClient):
    response = client.get("/asset/by_name/")
    assert response.status_code == 404  # Assuming FastAPI route validation catches this

def test_insert_non_unique_named_asset(session: Session, client: TestClient):
    generate_basic_data(session)

    response = client.post(
        "/assets/",
        json={
            "name": "Test asset",
        },
    )

    assert response.status_code == 422

def test_create_asset_with_invalid_json_data(session: Session, client: TestClient):
    response = client.post(
        "/assets/",
        json={
            "name": "New asset",
            "data": "invalid json",
        },
    )

    assert response.status_code == 422    

def test_create_asset_with_empty_json_data(session: Session, client: TestClient):
    response = client.post(
        "/assets/",
        json={
            "name": "New asset",
            "data": {},
        },
    )

    assert response.status_code == 200