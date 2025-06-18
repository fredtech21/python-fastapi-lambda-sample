from fastapi import APIRouter, HTTPException
from app.models import Dog

router = APIRouter(prefix="/dogs", tags=["dogs"])

@router.post("", response_model=Dog, status_code=201, response_model_by_alias=True)
async def create_dog(dog: Dog):
    await dog.insert()
    return dog

@router.get("", response_model=list[Dog], status_code=200, response_model_by_alias=True)
async def get_dogs():
    return await Dog.find_all().to_list()

@router.get("/{dog_id}", response_model=Dog, status_code=200, response_model_by_alias=True)
async def get_dog(dog_id: str):
    dog = await Dog.get(dog_id)
    if dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dog

@router.put("/{dog_id}", response_model=Dog)
async def update_dog(dog_id: str, updated_dog: Dog):
    dog = await Dog.get(dog_id)
    if dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    dog.name = updated_dog.name
    dog.race = updated_dog.race
    dog.date_of_birth = updated_dog.date_of_birth
    await dog.save()
    return dog

@router.delete("/{dog_id}", status_code=204)
async def delete_dog(dog_id: str):
    dog = await Dog.get(dog_id)
    if dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    await dog.delete()
    return {"message": "Dog deleted"}
