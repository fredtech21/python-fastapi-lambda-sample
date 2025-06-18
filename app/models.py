from beanie import Document, PydanticObjectId
from datetime import date
from pydantic import Field, ConfigDict

class Dog(Document):
    id: PydanticObjectId | None = Field(default=None, alias="_id", serialization_alias="id")
    name: str
    race: str
    date_of_birth: date      #= Field(alias="dateOfBirth")   if we want to use camelCase in DB and API

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)