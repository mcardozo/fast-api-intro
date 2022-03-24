"""Main module."""

# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import Body, FastAPI

# Models
class Person(BaseModel):
    """Person model."""

    first_name : str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


app = FastAPI()

@app.get('/')
def home():
    """Home page."""
    return {'hello': 'world'}

@app.post('/person/new')
def create_person(person: Person = Body(...)):
    """Create a person."""
    return person
