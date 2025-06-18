import pytest
from datetime import date

DOG_DATA = {
    "name": "Buddy",
    "race": "Labrador",
    "date_of_birth": date.today().isoformat()
}

@pytest.mark.asyncio
async def test_create_dog(async_client):
    response = await async_client.post("/dogs", json=DOG_DATA)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == DOG_DATA["name"]

@pytest.mark.asyncio
async def test_get_dogs(async_client):
    # Ensure at least one dog exists
    await async_client.post("/dogs", json=DOG_DATA)
    response = await async_client.get("/dogs")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(dog["name"] == DOG_DATA["name"] for dog in data)

@pytest.mark.asyncio
async def test_get_dog_by_id(async_client):
    # Create a dog and get its id
    create_resp = await async_client.post("/dogs", json=DOG_DATA)
    dog_id = create_resp.json()["id"]
    response = await async_client.get(f"/dogs/{dog_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == dog_id
    assert data["name"] == DOG_DATA["name"]

@pytest.mark.asyncio
async def test_update_dog(async_client):
    # Create a dog
    create_resp = await async_client.post("/dogs", json=DOG_DATA)
    dog_id = create_resp.json()["id"]
    updated_data = DOG_DATA.copy()
    updated_data["name"] = "Max"
    response = await async_client.put(f"/dogs/{dog_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Max"

@pytest.mark.asyncio
async def test_delete_dog(async_client):
    # Create a dog
    create_resp = await async_client.post("/dogs", json=DOG_DATA)
    dog_id = create_resp.json()["id"]
    response = await async_client.delete(f"/dogs/{dog_id}")
    assert response.status_code == 204
    # Confirm deletion
    get_resp = await async_client.get(f"/dogs/{dog_id}")
    assert get_resp.status_code == 404
