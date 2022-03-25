"""Main module."""

# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, EmailStr, Field

# FastAPI
from fastapi import Body, Cookie, FastAPI, Form, Header, Query, Path, status

# Models
class Location(BaseModel):
    """Location model."""

    city: str = Field(..., min_length=1, max_length=50, example='Tigre')
    state: str = Field(..., min_length=1, max_length=50, example='Buenos Aires')
    country: str = Field(..., min_length=1, max_length=50, example='Argentina')


class HairColor(Enum):
    """Enum hair color."""

    white = 'white'
    black = 'black'
    brown = 'brown'
    blonde = 'blonde'


class Person(BaseModel):
    """Person model."""

    first_name : str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., gt=0, le=115)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    email: EmailStr = Field(...);
    password: str = Field(..., min_length=8)

    class Config:
        """Testing data."""

        schema_extra = {
            'example': {
                'first_name': 'Marisol',
                'last_name': 'Cardozo',
                'age': 34,
                'hair_color': 'blonde',
                'is_married': False,
                'email': 'cardozomarisolp@gmail.com',
                'password': 'password'
            }
        }


class LoginOut(BaseModel):
    """Login Model."""
    username: str = Field(..., max_length=20, example='mcardozo')


app = FastAPI()

@app.get(path='/', status_code=status.HTTP_200_OK)
def home():
    """Home page."""
    return {'hello': 'world'}


@app.post(
    path='/person/new',
    response_model=Person,
    response_model_exclude={'password'},
    status_code=status.HTTP_201_CREATED
)
def create_person(person: Person = Body(...)):
    """Create a person."""
    return person


@app.get(path='/person/detail', status_code=status.HTTP_200_OK)
def show_person(
        name: Optional[str] = Query(
            None,
            min_length=1,
            max_length=50,
            title='Persona name',
            description='This is the persona name. It is between 1 and 50 characters.',
            example='Suri'
        ),
        age: str = Query(
            ...,
            title='Person age',
            description='This is the persona age. It is required.',
            example=18
        )
):
    """Validate query parameters."""
    return {name: age}


# Validate: Path Parameters
@app.get(path='/person/detail/{person_id}', status_code=status.HTTP_200_OK)
def show_person_detail(
        person_id: int = Path(
            ...,
            gt=0,
            title='Person',
            description='Showing person with id',
            example=23,
        ),
):
    """Return a person detail."""
    return {person_id: "It exist!"}


# Validate: Request body
@app.put(path='/person/{person_id}', status_code=status.HTTP_202_ACCEPTED)
def update_person(
        person_id: int = Path(
            ...,
            title='Person ID',
            description='This is the person ID',
            gt=0,
            example=23
        ),
        person: Person = Body(...),
):
    """Update a person."""
    return person


@app.put(path='/person-location/{person_id}', status_code=status.HTTP_202_ACCEPTED)
def update_person_location(
        person_id: int = Path(
            ...,
            title='Person and location',
            description='Update a person and location',
            gt=0
        ),
        person: Person = Body(...),
        location: Location = Body(...)
):
    """Update a person."""
    results = person.dict()
    results.update(location.dict())
    return results


@app.put(path='/location/{location_id}', status_code=status.HTTP_200_OK)
def update_location(
        location_id: int = Path(
            ...,
            title='Location ID',
            description='Update location',
            gt=0
        ),
        location: Location = Body(...)
):
    """Update a person."""
    return location


# Forms
@app.post(path='/login', response_model=LoginOut, status_code=status.HTTP_200_OK)
def login(username: str = Form(...), password: str = Form(...)):
    """User login."""
    return LoginOut(username=username)


# Cookies and header parameters
@app.post(path='/contact', status_code=status.HTTP_200_OK)
def contact(
        first_name: str = Form(..., max_length=20, min_length=1),
        last_name: str = Form(..., max_length=20, min_length=1),
        email: EmailStr = Form(...),
        message: str = Form(..., min_length=20),
        user_agent: Optional[str] = Header(default=None),
        ads: Optional[str] = Cookie(default=None)
):
    """Contact form."""
    return user_agent
