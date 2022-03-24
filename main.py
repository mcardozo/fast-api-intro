"""Main module."""

# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import Body, FastAPI, Query, Path

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


@app.get('/person/detail')
def show_person(
        name: Optional[str] = Query(
            None,
            min_length=1,
            max_length=50,
            title='Persona name',
            description='This is the persona name. It is between 1 and 50 characters.'
        ),
        age: int = Query(...)
):
    """Validate query parameters."""
    return {name: age}


@app.get('/person/detail/{person_id}')
def show_person_detail(
        person_id: int = Path(
            ...,
            gt=0,
            title='Person',
            description='Showing person with id',
        ),
):
    """Return a person detail."""
    return {person_id: "It exist!"}
