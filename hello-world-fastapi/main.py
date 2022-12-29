#Python
from typing import Optional
#Pydantic
from pydantic import BaseModel
#FasAPI
from fastapi import FastAPI, Body, Query, Path


app = FastAPI()


# Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


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
    person_id: int = Path(..., gt=0),
    person: Person = Body(...)
):
    return person