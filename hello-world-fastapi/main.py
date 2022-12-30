#Python
from typing import Optional
from enum import Enum
#Pydantic
from pydantic import BaseModel, Field
#FasAPI
from fastapi import FastAPI, Body, Query, Path


app = FastAPI()


# Models
class HairColor(Enum):
    whith = "whith"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Person(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=40)  # ... mandatory
    last_name: str = Field(..., min_length=1, max_length=40)
    age: int
    hair_color: Optional[HairColor] = Field(default=None)  # validar usando la clase HairColor
    is_married: Optional[bool] = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                'first_name':"Daniel",
                "last_name":"Portugal",
                "age": 33,
                "hair_color": "black",
                "is_married": False
            }

        }

class Location(BaseModel):
    city:  str = Field(default=None, min_length=1, max_length=30, example="Arequipa")
    state:  str = Field(default=None, min_length=1, max_length=30, example="Arequipa")
    country:  str = Field(default=None, min_length=1, max_length=30, example="Peru")


@app.get("/")
def home():
    return {"hello": "World!"}


# Request and Response Body
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person


# Validations: Query Parameters
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None, min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters."
        ),
    age: int = Query(...,
        title="Person Age",
        description="This parameter is required"
    ) 
):
    return {'name': name, 'age':age}


# Path parameter
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(..., gt=0)
):
    return {person_id: "It exist"}


# Request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(...,description="Person ID", gt=0),
    person: Person = Body(...),  
    location: Location = Body(...)
):
    result = person.dict()
    result.update(location.dict())  # anidar 2 request body
    return result
    # return person